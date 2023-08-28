import os

from botocore.exceptions import ClientError

from whiplash.whiplash import Whiplash

REGION = os.environ.get("AWS_DEFAULT_REGION")
STAGE = os.environ.get("STAGE", "dev")

def initialize():
    whiplash = Whiplash(REGION, STAGE)
    try:
        whiplash.setup()
    except ClientError as e:
        if e.response['Error']['Code'] == "ResourceInUseException":
            print("Table already exists")
        else:
            print(e)
            raise 

    return {"message": "success"}
