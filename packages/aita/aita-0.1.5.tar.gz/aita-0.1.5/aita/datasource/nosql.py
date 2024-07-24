from typing import List

try:
    import boto3
except ImportError:
    boto3 = None

from aita.datasource.base import DataSource
from aita.datasource.catalog import Catalog


class DynamodbDataSource(DataSource):
    def __init__(self, region_name: str = None):
        self.region_name = region_name
        self.client = boto3.client("dynamodb", region_name=region_name)

    def get_metadata(self, table_name: str) -> List[Catalog]:
        response = self.client.describe_table(TableName=table_name)
        return response["Table"]
