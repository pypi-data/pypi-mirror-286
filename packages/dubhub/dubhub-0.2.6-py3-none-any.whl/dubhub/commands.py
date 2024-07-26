import json
import logging
import os
import re
from time import sleep
import requests
import shutil
import subprocess

import psycopg

from .schema import PGDatabase, PGDatabaseEncoder
from .version import VERSION

logger = logging.getLogger(__name__)


def parse_connection_string(conn_string, regex):
    match = re.search(regex, conn_string)
    return match.group(1) if match else ""


class Commands:
    def __init__(self, server):
        self.SERVER = server

    def start_clone(self, dub_uuid, org_token, output, grace, timeout, cli=None):
        try:
            CI_PIPELINE_ID = os.environ.get("CI_PIPELINE_ID", None)
            if CI_PIPELINE_ID is None:
                CI_PIPELINE_ID = os.environ.get("GITHUB_RUN_ID", None)
            CI_COMMIT_REF_NAME = os.environ.get("CI_COMMIT_REF_NAME", None)
            if CI_COMMIT_REF_NAME is None:
                CI_COMMIT_REF_NAME = os.environ.get("GITHUB_HEAD_REF", None)
            CI_COMMIT_SHA = os.environ.get("CI_COMMIT_SHA", None)
            if CI_COMMIT_SHA is None:
                CI_COMMIT_SHA = os.environ.get("GITHUB_SHA", None)
            CI_MERGE_REQUEST_IID = os.environ.get("CI_MERGE_REQUEST_IID", "github")
            CI_DEFAULT_BRANCH = os.environ.get("CI_DEFAULT_BRANCH", None)
            if CI_DEFAULT_BRANCH is None:
                CI_DEFAULT_BRANCH = os.environ.get("GITHUB_BASE_REF", None)
            CI_USER = os.environ.get("GITHUB_ACTOR", None)
            json_msg = {
                "dubUuid": dub_uuid,
                "orgToken": org_token,
                "CI_PIPELINE_ID": CI_PIPELINE_ID,
                "CI_COMMIT_REF_NAME": CI_COMMIT_REF_NAME,
                "CI_COMMIT_SHA": CI_COMMIT_SHA,
                "CI_MERGE_REQUEST_IID": CI_MERGE_REQUEST_IID,
                "CI_DEFAULT_BRANCH": CI_DEFAULT_BRANCH,
                "VERSION": VERSION,
                "CI_USER": CI_USER
            }
            if grace:
                json_msg["INACTIVITY_GRACE_SECS"] = grace
            if timeout:
                json_msg["INACTIVITY_TIMEOUT_SECS"] = timeout
            response = requests.post(
                f"{self.SERVER}/api/clone/start",
                json=json_msg,
            )
            if response.status_code == 400 or response.status_code == 500:
                logger.error(json.loads(response.content))
                return
        except Exception as e:
            logger.exception("Error with sending post request:" + str(e))
            # load and dump json so its formatted properly; also helps validate
            # that the json returned is proper
        try:
            connection_string = json.loads(response.content)[
                "conn_string"
            ]
            db_type = "postgres"
            if "db_type" in json.loads(response.content):
                db_type = json.loads(response.content)[
                    "db_type"
                ]

            host = ""
            port = ""
            password = ""
            user = "postgres"  # Default user if not provided

            if db_type == "postgres":
                host_regex = r'host=([^\s]+)'
                port_regex = r'port=([^\s]+)'
                password_regex = r'password=([^\s]+)'

                host = parse_connection_string(connection_string, host_regex)
                port = parse_connection_string(connection_string, port_regex)
                password = parse_connection_string(connection_string, password_regex)
            else:
                host_regex = r'\(([^:]+)'
                port_regex = r':(\d+)(?![^@]*@)'
                password_regex = r':(.*?)(?=@)'
                user_regex = r'^([^@:]+)'

                host = parse_connection_string(connection_string, host_regex)
                port = parse_connection_string(connection_string, port_regex)
                password = parse_connection_string(connection_string, password_regex)
                user = parse_connection_string(connection_string, user_regex)

            json_output = {
                "host": host,
                "port": port,
                "username": user,
                "password": password,
                "database": "postgres",
                "clone_uuid": json.loads(json.dumps(json.loads(response.content)))[
                    "cloneUuid"
                ],
                "dub_uuid": dub_uuid,
            }
            if cli:
                cli_env = os.environ.copy()
                cli_env["PGPASSWORD"] = json_output["password"]
                subprocess.run(
                    [
                        shutil.which("psql"),
                        "-h",
                        json_output["host"],
                        "-p",
                        json_output["port"],
                        "-U",
                        "postgres",
                    ],
                    env=cli_env,
                )
            elif output == "json":
                print(json.dumps(json_output))
            elif output == "file":
                with open("start_clone_output.json", "w") as outfile:
                    json.dump(response.content, outfile)
        except Exception as e:
            logger.exception("Error converting response object to JSON file:" + str(e))

    def stop_clone(self, clone_uuid, org_token):
        try:
            response = requests.post(
                f"{self.SERVER}/api/clone/stop",
                json={
                    "cloneUuid": clone_uuid,
                    "orgToken": org_token,
                    "VERSION": VERSION,
                },
            )
            if response.status_code in [400, 500]:
                logger.error("Failed API call with status code: %s", response.status_code)
                logger.error(response.json())
                return
            print(response.json())
        except Exception as e:
            logger.exception("Error with sending post request:" + str(e))

    def analyse_clone(self, cloneUuid, org_token, token):
        try:
            CI_API_V4_URL = os.environ.get("CI_API_V4_URL", None)
            CI_PROJECT_ID = os.environ.get("CI_PROJECT_ID", None)
            CI_MERGE_REQUEST_IID = os.environ.get("CI_MERGE_REQUEST_IID", None)
            CI_DEFAULT_BRANCH = os.environ.get("CI_DEFAULT_BRANCH", None)
            CI_COMMIT_SHA = os.environ.get("CI_COMMIT_SHA", None)
            if CI_DEFAULT_BRANCH is None:
                CI_DEFAULT_BRANCH = os.environ.get("GITHUB_BASE_REF", None)
            CI_COMMIT_REF_NAME = os.environ.get("CI_COMMIT_REF_NAME", None)
            if CI_COMMIT_REF_NAME is None:
                CI_COMMIT_REF_NAME = os.environ.get("GITHUB_HEAD_REF", None)
            GITHUB_REPOSITORY = os.environ.get("GITHUB_REPOSITORY", None)
            GITHUB_SHA = os.environ.get("GITHUB_SHA", None)
            GITHUB_REF = os.environ.get("GITHUB_REF", None)
            GITHUB_PR_REF = os.environ.get("PR_REF", None)
            if CI_PROJECT_ID is None:
                GITHUB_OR_GITLAB = "github"
            else:
                GITHUB_OR_GITLAB = "gitlab"
        except Exception as e:
            logger.exception("Error converting JSON file to JSON object:" + str(e))
        try:
            response = requests.post(
                f"{self.SERVER}/api/clone/analyse",
                json={
                    "cloneUuid": cloneUuid,
                    "orgToken": org_token,
                    "ACCESS_TOKEN": token,
                    "CI_API_V4_URL": CI_API_V4_URL,
                    "CI_PROJECT_ID": CI_PROJECT_ID,
                    "CI_COMMIT_SHA": CI_COMMIT_SHA,
                    "CI_MERGE_REQUEST_IID": CI_MERGE_REQUEST_IID,
                    "CI_DEFAULT_BRANCH": CI_DEFAULT_BRANCH,
                    "GITHUB_OR_GITLAB": GITHUB_OR_GITLAB,
                    "GITHUB_REPOSITORY": GITHUB_REPOSITORY,
                    "GITHUB_SHA": GITHUB_SHA,
                    "GITHUB_REF": GITHUB_REF,
                    "VERSION": VERSION,
                    "GITHUB_PR_REF": GITHUB_PR_REF,
                    "CI_COMMIT_REF_NAME": CI_COMMIT_REF_NAME,
                },
            )
            if response.status_code in [400, 500]:
                logger.error("Failed API call with status code: %s", response.status_code)
                logger.error(response.json())
                return
            # print(f"See your results here: {response}")
        except Exception as e:
            logger.exception("Error with sending post request:" + str(e))

    def create_run(self, org_token, project_uuid):
        try:
            CI_COMMIT_SHA = os.environ.get("CI_COMMIT_SHA", None)
            GITHUB_SHA = os.environ.get("GITHUB_SHA", None)
            GITHUB_REF = os.environ.get("GITHUB_REF", None)
            GITHUB_RUN_ID = os.environ.get("GITHUB_RUN_ID", None)
            GITHUB_REPOSITORY = os.environ.get("GITHUB_REPOSITORY", None)
            GITHUB_HEAD_REF = os.environ.get("GITHUB_HEAD_REF", None)
            response = requests.post(
                f"{self.SERVER}/api/baseguard/create_run",
                json={
                    "GITHUB_REF": GITHUB_REF,
                    "org_token": org_token,
                    "project_uuid": project_uuid,
                    "GITHUB_SHA": GITHUB_SHA,
                    "CI_COMMIT_SHA": CI_COMMIT_SHA,
                    "GITHUB_RUN_ID": GITHUB_RUN_ID,
                    "GITHUB_REPOSITORY": GITHUB_REPOSITORY,
                    "GITHUB_HEAD_REF": GITHUB_HEAD_REF
                },
            )
            if response.status_code in [400, 500]:
                logger.error("Failed API call with status code: %s", response.status_code)
                logger.error(response.json())
                return
        except Exception as e:
            logger.exception("Error with sending post request:" + str(e))
        try:
            print(response.json())
        except Exception as e:
            logger.exception("Error converting response object to JSON file:" + str(e))

    def snapshot(self, org_token, dub_uuid, wait):
        try:
            response = requests.post(
                f"{self.SERVER}/api/dubhub/snapshot",
                json={
                    "orgToken": org_token,
                    "dubUuid": dub_uuid,
                },
            )
            if response.status_code in [400, 500]:
                logger.error("Failed API call with status code: %s", response.status_code)
                logger.error(response.json())
                return
        except Exception as e:
            logger.exception("Error with sending post request:" + str(e))
        try:
            snapshot_uuid = json.loads(json.dumps(json.loads(response.content)))
            print(f"Creating snapshot {snapshot_uuid}", flush=True)
            if wait is True:
                print("Waiting for creation to complete", end="", flush=True)
                snapshot_created = False
                while snapshot_created is False:
                    sleep(1)
                    print(".", end="", flush=True)
                    wait_response = requests.get(
                        f"{self.SERVER}/api/dubhub/snapshot?snapshot_uuid={snapshot_uuid}&orgToken={org_token}",
                    )
                    snapshot_created = json.loads(
                        json.dumps(json.loads(wait_response.content))
                    )
                if snapshot_created is True:
                    print(f"\nSnapshot {snapshot_uuid} created successfully")
                else:
                    print(snapshot_created)
        except Exception as e:
            logger.exception("Error creating snapshot" + str(e))

    def baseguard_analyse(self, org_token, token):
        try:
            CI_API_V4_URL = os.environ.get("CI_API_V4_URL", None)
            CI_PROJECT_ID = os.environ.get("CI_PROJECT_ID", None)
            CI_MERGE_REQUEST_IID = os.environ.get("CI_MERGE_REQUEST_IID", None)
            CI_DEFAULT_BRANCH = os.environ.get("CI_DEFAULT_BRANCH", None)
            CI_COMMIT_SHA = os.environ.get("CI_COMMIT_SHA", None)
            if CI_DEFAULT_BRANCH is None:
                CI_DEFAULT_BRANCH = os.environ.get("GITHUB_BASE_REF", None)
            GITHUB_REPOSITORY = os.environ.get("GITHUB_REPOSITORY", None)
            GITHUB_SHA = os.environ.get("GITHUB_SHA", None)
            GITHUB_REF = os.environ.get("GITHUB_REF", None)
            GITHUB_PR_REF = os.environ.get("PR_REF", None)
            GITHUB_RUN_ID = os.environ.get("GITHUB_RUN_ID", None)
            if CI_PROJECT_ID is None:
                GITHUB_OR_GITLAB = "github"
            else:
                GITHUB_OR_GITLAB = "gitlab"
        except Exception as e:
            logger.exception("Error converting JSON file to JSON object:" + str(e))
        try:
            response = requests.post(
                f"{self.SERVER}/api/baseguard/analyse",
                json={
                    "orgToken": org_token,
                    "ACCESS_TOKEN": token,
                    "CI_API_V4_URL": CI_API_V4_URL,
                    "CI_PROJECT_ID": CI_PROJECT_ID,
                    "CI_COMMIT_SHA": CI_COMMIT_SHA,
                    "CI_MERGE_REQUEST_IID": CI_MERGE_REQUEST_IID,
                    "CI_DEFAULT_BRANCH": CI_DEFAULT_BRANCH,
                    "GITHUB_OR_GITLAB": GITHUB_OR_GITLAB,
                    "GITHUB_REPOSITORY": GITHUB_REPOSITORY,
                    "GITHUB_SHA": GITHUB_SHA,
                    "GITHUB_REF": GITHUB_REF,
                    "VERSION": VERSION,
                    "GITHUB_PR_REF": GITHUB_PR_REF,
                    "GITHUB_RUN_ID": GITHUB_RUN_ID
                },
            )
            if response.status_code in [400, 500]:
                logger.error("Failed API call with status code: %s", response.status_code)
                logger.error(response.json())
                return
            # print(f"See your results here: {response}")
        except Exception as e:
            logger.exception("Error with sending post request:" + str(e))

    def upload_schema(self, org_token):
        try:
            GITHUB_SHA = os.environ.get("GITHUB_SHA", None)
            GITHUB_RUN_ID = os.environ.get("GITHUB_RUN_ID", None)
            # redundant for now because the driver would looks for these anyway
            conn_params = {
                "dbname": os.getenv("PGDATABASE", default="postgres"),
                "user": os.getenv("PGUSER", default="postgres"),
                "password": os.getenv("PGPASSWORD", default=""),
                "host": os.getenv("PGHOST", default="postgres"),
                "port": os.getenv("PGPORT", default="5432"),
            }
            conn = psycopg.connect(**conn_params)
            db = PGDatabase(conn)
            db.load()
            json_str = json.dumps(db, cls=PGDatabaseEncoder)
            response = requests.post(
                f"{self.SERVER}/api/baseguard/upload_schema",
                json={
                    "orgToken": org_token,
                    "pg_schema_dump": json.loads(json_str),
                    "GITHUB_SHA": GITHUB_SHA,
                    "GITHUB_RUN_ID": GITHUB_RUN_ID
                },
            )
            if response.status_code in [400, 500]:
                logger.error("Failed API call with status code: %s", response.status_code)
                logger.error(response.json())
                return
        except Exception as e:
            logger.exception("Error with sending post request:" + str(e))

    def subset(self, org_token, dub_uuid, config_file):
        try:
            config_data = json.load(config_file)
            config_file.close()
            response = requests.post(
                f"{self.SERVER}/api/dubhub/subset",
                json={
                    "dubUuid": dub_uuid,
                    "orgToken": org_token,
                    "config": config_data,
                },
            )
            if response.status_code in [400, 500]:
                logger.error("Failed API call with status code: %s", response.status_code)
                logger.error(response.json()) 
                return
            print(response.json()) 
        except Exception as e:
            logger.exception("Error with sending post request:" + str(e))
