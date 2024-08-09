from boto3 import client
from datetime import datetime
import os

class DynamoDBWrapper:
  def __init__(self):
    self.dynamo_client = client('dynamodb')
    self.ssm_client = client('ssm')
    self.table_name = self.ssm_client.get_parameter(Name='/wikimedia_bot/table_name')['Parameter']['Value']

  def record_post_to_table(self, file_id: int, title: str) -> None:
    """
    Returns:
        None
    """
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    self.dynamo_client.put_item(
      TableName=self.table_name,
      Item={
        "file_id": { 'S': str(file_id) },
        "title": { 'S': title },
        "posted_at": { 'S': formatted_time }
      }
    )

  def is_already_posted(self, file_id: int) -> bool:
    response = self.dynamo_client.get_item(
      TableName=self.table_name,
      Key={
        'file_id': {
          'S': str(file_id),
        }
      }
    )

    # If there is a matching item, this field is present.
    # If there is no matching item, this field is absent.
    return 'Item' in response;
