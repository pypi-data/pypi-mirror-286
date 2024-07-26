#!/usr/bin/env python3
import argparse
import logging
import os
import re
import shutil
import sys
import uuid

import sentry_sdk

from .commands import Commands
from .version import VERSION

DUBHUB_ENV_VAR_NAME = "DUBHUB_ENV"
DEFAULT_ENVIRONMENT = "production"
DUBHUB_DSN_VAR_NAME = "DUBHUB_SENTRY_DSN"
DEFAULT_DSN = (
    "https://a74ab2ee702347d3b4461e63a7049dc0@o604958.ingest.sentry.io/6604591"
)


sentry_sdk.init(
    dsn=os.environ.get(DUBHUB_DSN_VAR_NAME, DEFAULT_DSN),
    environment=os.environ.get(DUBHUB_ENV_VAR_NAME, DEFAULT_ENVIRONMENT),
    traces_sample_rate=0.0,
)


class ArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        self.print_help(sys.stderr)
        self.exit(2, "%s: error: %s\n" % (self.prog, message))


def regex_type_uuid(
    arg_value,
    pat=re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"),
):
    if not pat.match(arg_value):
        raise argparse.ArgumentTypeError
    return arg_value


parser = argparse.ArgumentParser()
parser.add_argument("clone", type=str, help="Dubhub CLI clone commands")
parser.add_argument("--version", action="version", version=VERSION)
parser.add_argument(
    "clone_option", type=str, help="Dubhub CLI clone start/stop command"
)
parser.add_argument("--dubUuid", type=regex_type_uuid, help="Uuid of Dub")
parser.add_argument("--orgToken", type=regex_type_uuid, help="Uuid of Org Token")
parser.add_argument("--projectUuid", type=regex_type_uuid, help="Uuid of Project")
parser.add_argument("--cloneUuid", type=regex_type_uuid, help="Uuid of Clone")
parser.add_argument("--accessToken", help="Gitlab/Github Access Token")
parser.add_argument("--output", type=str, help="Output result of start clone")
parser.add_argument(
    "--wait", action="store_true", help="Wait for snapshot to finish creating"
)
parser.add_argument("--config", type=argparse.FileType('r'), help="Path to configuration file in JSON format")
parser.add_argument(
    "--grace",
    type=int,
    help="Number of seconds from startup that inactivity is not checked",
)
parser.add_argument(
    "--timeout",
    type=int,
    help="Number of seconds of inactivity before clone is shut down",
)
if sys.version_info >= (3, 9):
    parser.add_argument(
        "-i",
        "--cli",
        action=argparse.BooleanOptionalAction,
        help="Run a native CLI (eg psql) for the clone on start",
    )
else:
    parser.add_argument(
        "-i",
        "--cli",
        action="store_true",
        help="Run a native CLI (eg psql) for the clone on start",
    )
    parser.add_argument(
        "--no-cli",
        dest="cli",
        action="store_false",
        help="Run a native CLI (eg psql) for the clone on start",
    )
    parser.set_defaults(cli=False)


logger = logging.getLogger(__name__)

DEFAULT_HOST = "https://app.dubhub.io"
DEFAULT_HOST_ENV = "DUBHUB_HOST"

def is_valid_uuid(val):
    try:
        uuid.UUID(str(val))
        return True
    except ValueError:
        return False


def main(cli_args=None, cmd=None):
    cli_args=cli_args or sys.argv[1:]
    host = os.environ.get(DEFAULT_HOST_ENV, DEFAULT_HOST)
    dubhub = cmd or Commands(server=host)
    args = parser.parse_args(cli_args)
    if not args.orgToken:
        logger.error("Please provide --orgToken")
    elif args.clone == "clone" and args.clone_option == "start":
        if args.cli and shutil.which("psql") is None:
            print("psql command not found")
            return 1
        output = None
        if args.output is not None:
            output = args.output
        dub_uuid = args.dubUuid
        if not is_valid_uuid(dub_uuid):
            logger.error("Dub Uuid entered isn't valid a Uuid")
            raise TypeError("Dub Uuid entered isn't valid a Uuid")
        org_token = args.orgToken
        if not is_valid_uuid(org_token):
            logger.error("Org Token entered isn't valid a Uuid")
            raise TypeError("Org Token entered isn't valid a Uuid")
        dubhub.start_clone(
            dub_uuid, org_token, output, args.grace, args.timeout, cli=args.cli
        )
    elif args.clone == "clone" and args.clone_option == "stop":
        org_token = args.orgToken
        cloneUuid = args.cloneUuid
        if not is_valid_uuid(cloneUuid):
            logger.error("Clone Uuid entered isn't valid a Uuid")
            raise TypeError("Clone Uuid entered isn't valid a Uuid")
        dubhub.stop_clone(cloneUuid, org_token)
    elif args.clone == "dub" and args.clone_option == "snapshot":
        org_token = args.orgToken
        dub_uuid = args.dubUuid
        if not is_valid_uuid(dub_uuid):
            logger.error("Dub Uuid entered isn't valid a Uuid")
            raise TypeError("Dub Uuid entered isn't valid a Uuid")
        dubhub.snapshot(org_token, dub_uuid, args.wait)
    elif args.clone == "dub" and args.clone_option == "subset":
        org_token = args.orgToken
        dub_uuid = args.dubUuid
        if not is_valid_uuid(dub_uuid):
            logger.error("Dub Uuid entered isn't valid a Uuid")
            raise TypeError("Dub Uuid entered isn't valid a Uuid")
        dubhub.subset(org_token, dub_uuid, args.config)
    elif args.clone == "clone" and args.clone_option == "analyse":
        try:
            cloneUuid = args.cloneUuid
            if not is_valid_uuid(cloneUuid):
                logger.error("Clone Uuid entered isn't valid a Uuid")
                raise TypeError("Clone Uuid entered isn't valid a Uuid")
            org_token = args.orgToken
            token = args.accessToken
            dubhub.analyse_clone(cloneUuid, org_token, token)
        except FileNotFoundError as e:
            logger.error("Error reading JSON file:" + str(e))
    elif args.clone == "baseguard" and args.clone_option == "create_run":
        org_token = args.orgToken
        project_uuid = args.projectUuid
        if not is_valid_uuid(project_uuid):
            logger.error("Projecy Uuid entered isn't valid a Uuid")
            raise TypeError("Project Uuid entered isn't valid a Uuid")
        dubhub.create_run(org_token, project_uuid)
    elif args.clone == "baseguard" and args.clone_option == "analyse":
        org_token = args.orgToken
        access_token = args.accessToken
        dubhub.baseguard_analyse(org_token, access_token)
    elif args.clone == "baseguard" and args.clone_option == "upload_schema":
        org_token = args.orgToken
        dubhub.upload_schema(org_token)
    else:
        logger.error("No command found")
        logger.error(
            "To start a clone run: dubhub clone start --orgToken <ORGTOKEN> --dubUuid <DUBUUID>"
        )
        logger.error(
            "To stop a clone run: dubhub clone stop --orgToken <ORGTOKEN> --cloneUuid <DUBUUID>"
        )
