import base64
import os

import boto3
from botocore.exceptions import ClientError


def get_secret(secret_name, secret_version, region):
    session = boto3.session.Session()

    print(session.available_profiles)

    client = session.client(service_name="secretsmanager", region_name=region)
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name, VersionId=secret_version
        )
    except ClientError as e:
        if e.response["Error"]["Code"] == "DecryptionFailureException":
            print(e)
            # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
            raise e
        elif e.response["Error"]["Code"] == "InternalServiceErrorException":
            print(e)
            # An error occurred on the server side.
            raise e
        elif e.response["Error"]["Code"] == "InvalidParameterException":
            print(e)
            # You provided an invalid value for a parameter.
            raise e
        elif e.response["Error"]["Code"] == "InvalidRequestException":
            print(e)
            # You provided a parameter value that is not valid for the current state of the resource.
            raise e
        elif e.response["Error"]["Code"] == "ResourceNotFoundException":
            print(e)
            # We can't find the resource that you asked for.
            raise e
    else:
        if "SecretString" in get_secret_value_response:
            secret = get_secret_value_response["SecretString"]
        else:
            secret = base64.b64decode(get_secret_value_response["SecretBinary"])
        return secret


# TODO: make this a more generic solution for secrets
def config_secret(secret_file):
    if os.environ["ENVIRONMENT"] == "local":
        pwd = os.environ[secret_file]
    elif os.environ["REGION"] == "eu-west-1" and os.environ["ENVIRONMENT"] == "dev":
        pwd = get_secret(
            f"prospect-search-visualise/eu-west-1/dev/production/staging/{secret_file}",
            "b64c3127-4071-4b6e-ad5c-20e6709f5501",
            "eu-west-1",
        )
    elif os.environ["REGION"] == "eu-west-1" and os.environ["ENVIRONMENT"] == "live":
        pwd = get_secret(
            f"prospect-search-visualise/eu-west-1/live/production/production/{secret_file}",
            "c4e1ba4b-78cd-4db6-ab66-2970eb0a1a35",
            "eu-west-1",
        )
    return pwd
