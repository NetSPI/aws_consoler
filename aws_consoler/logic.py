# -*- coding: utf-8 -*-
import json
import requests
import boto3
from botocore.exceptions import ClientError
import argparse
import urllib.parse
import logging

"""Main module."""


def run(args: argparse.Namespace) -> str:
    """
    Takes the arguments from the CLI and generates the link
    :param args: the namespace from the CLI
    :type args: argparse.Namespace
    :return: sign-in URL
    """
    # Set up logging
    logger = logging.getLogger(__name__)

    # Set up the base session
    session: boto3.Session
    logger.debug("Establishing Boto3 session.")
    # If we have a profile, use that.
    if args.profile:
        logger.debug("Using CLI-provided profile.")
        session = boto3.Session(profile_name=args.profile)
        logger.info("Profile session using \"%s\" established.", args.profile)
    # Otherwise, use the command line arguments
    elif args.access_key_id:
        logger.debug("Using CLI-provided credentials.")
        session = boto3.Session(aws_access_key_id=args.access_key_id,
                                aws_secret_access_key=args.secret_access_key,
                                aws_session_token=args.session_token,
                                region_name=args.region)
        logger.info("Session using credential variables established.")
    # Otherwise, let boto figure it out.
    else:
        logger.debug("No credentials detected, forwarding to Boto3.")
        session = boto3.Session()
        logger.info("Boto3 session established.")

    # Get to temporary credentials
    # If we have a role ARN supplied, start assuming them
    if args.role_arn:
        logger.debug("Role detected, setting up STS.")
        sts = session.client("sts")
        logger.info("Assuming role \"%s\" via STS.", args.role_arn)
        resp = sts.assume_role(RoleArn=args.role_arn,
                               RoleSessionName="aws_consoler")
        creds = resp["Credentials"]
        logger.debug("Role assumed, setting up session.")
        session = boto3.Session(
            aws_access_key_id=creds["AccessKeyId"],
            aws_secret_access_key=creds["SecretAccessKey"],
            aws_session_token=creds["SessionToken"])
        logger.info("New role session established.")
    # If we are still a permanent IAM credential, use sts:GetFederationToken
    elif session.get_credentials().get_frozen_credentials() \
            .access_key.startswith("AKIA"):
        sts = session.client("sts")
        logger.warning("Creds still permanent, creating federated session.")
        # Effective access is calculated as the union of our permanent creds
        # and the policies supplied here. Use the AdministratorAccess policy
        # for the largest set of possible permissions.
        try:
            resp = sts.get_federation_token(
                Name="aws_consoler",
                PolicyArns=[
                    {"arn": "arn:aws:iam::aws:policy/AdministratorAccess"}
                ])
            logger.debug("Federation session created, setting up session.")
            creds = resp["Credentials"]
            session = boto3.Session(
                aws_access_key_id=creds["AccessKeyId"],
                aws_secret_access_key=creds["SecretAccessKey"],
                aws_session_token=creds["SessionToken"])
            logger.info("New federated session established.")
        except ClientError:
            message = "Error obtaining federation token from STS. Ensure " \
                      "the IAM user has sts:GetFederationToken permissions, " \
                      "or provide a role to assume. "
            raise PermissionError(message)

    # Check that our credentials are valid.
    sts = session.client("sts")
    resp = sts.get_caller_identity()
    logger.info("Session valid, attempting to federate as %s.", resp["Arn"])

    # TODO: Detect things like user session credentials here.

    # Generate our signin link, given our temporary creds
    creds = session.get_credentials().get_frozen_credentials()
    logger.debug("Session credentials frozen.")
    json_creds = json.dumps(
        {"sessionId": creds.access_key,
         "sessionKey": creds.secret_key,
         "sessionToken": creds.token})
    token_params = {
        "Action": "getSigninToken",
        # TODO: Customize duration for federation and sts:AssumeRole
        "SessionDuration": 43200,
        "Session": json_creds
    }
    logger.debug("Creating console federation token.")
    resp = requests.get(url="https://signin.aws.amazon.com/federation",
                        params=token_params)
    # Stacking AssumeRole sessions together will generate a 400 error here.
    try:
        resp.raise_for_status()
    except requests.exceptions.HTTPError as e:
        raise requests.exceptions.HTTPError(
            "Couldn't obtain federation token (trying to stack roles?): "
            + str(e))

    fed_token = json.loads(resp.text)["SigninToken"]
    logger.debug("Federation token obtained, building URL.")
    console_params = {
        "region": args.region
    }
    login_params = {
        "Action": "login",
        "Issuer": "consoler.local",
        "Destination": "https://console.aws.amazon.com/console/home?"
                       + urllib.parse.urlencode(console_params),
        "SigninToken": fed_token
    }
    login_url = "https://signin.aws.amazon.com/federation?" \
                + urllib.parse.urlencode(login_params)

    logger.info("URL generated!")
    return (login_url)
