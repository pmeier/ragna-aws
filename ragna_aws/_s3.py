import os
import uuid
from typing import Any

import boto3
import botocore.exceptions
from ragna.core import Config, Document, EnvVarRequirement, RagnaException, Requirement

from ._utils import AWS_DEFAULT_REQUIREMENTS


class S3Document(Document):
    @classmethod
    def requirements(cls) -> list[Requirement]:
        return [*AWS_DEFAULT_REQUIREMENTS, EnvVarRequirement("AWS_S3_BUCKET")]

    @classmethod
    async def get_upload_info(
        cls, *, config: Config, user: str, id: uuid.UUID, name: str
    ) -> tuple[str, dict[str, Any], dict[str, Any]]:
        session = boto3.Session()
        s3 = session.client("s3")

        bucket = os.environ["AWS_S3_BUCKET"]
        response = s3.generate_presigned_post(
            Bucket=bucket,
            Key=str(id),
            # ExpiresIn=config.api.upload_token_ttl,
        )

        url = response["url"]
        data = response["fields"]
        metadata = {"bucket": bucket}

        return url, data, metadata

    def is_readable(self) -> bool:
        session = boto3.Session()
        s3 = session.resource("s3")

        try:
            s3.Object(self.metadata["bucket"], str(self.id)).load()
        except botocore.exceptions.ClientError as error:
            if error.response["Error"]["Code"] == "404":
                return False

            raise RagnaException() from error

        return True

    def read(self) -> bytes:
        session = boto3.Session()
        s3 = session.resource("s3")
        return (  # type: ignore[no-any-return]
            s3.Object(self.metadata["bucket"], str(self.id)).get()["Body"].read()
        )
