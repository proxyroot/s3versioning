import boto3
import pytest

from moto import mock_s3


@pytest.fixture(scope="function")
def _s3():
    with mock_s3():
        conn = boto3.resource("s3", region_name="us-east-1")
        conn.create_bucket(Bucket="bucket.proxyroot.com")
        versioning = conn.BucketVersioning("bucket.proxyroot.com")
        versioning.enable()
        yield {"client": boto3.client("s3", region_name="us-east-1"), "resource": conn}
