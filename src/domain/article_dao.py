import logging

from src.domain.article import Article
from boto3.dynamodb.conditions import Key, Attr

logger = logging.getLogger()


class ArticleDao:
    def __init__(self, dynamodb_resource, dynamodb_client, table_name):
        self.dynamodb_resource = dynamodb_resource
        self.dynamodb_client = dynamodb_client
        self.table = self.dynamodb_resource.Table(table_name)

    def create(self, entity: Article) -> None:
        logger.info("[Article] create")
        self.table.put_item(Item=entity.to_dict())

    def delete(self, uuid) -> None:
        logger.info("[Article] delete")

        object = self.table.scan(
            FilterExpression=Attr("uuid").eq(uuid)
            )
        self.table.delete_item(Key={"uuid": uuid, "title": object["Items"][0]["title"]}) if (len(object["Items"]) == 1) else None

        return None

    def find_by_uuid(self, uuid) -> Article:
        logger.info("[entity] entity")

        result = self.table.query(
            KeyConditionExpression=Key("uuid").eq(uuid)
        )

        return result["Items"][0] if "Items" in result else None

    def find_by_owner_id(self, owner_id) -> Article:
        logging.info("[article] find_by_owner_id")

        result = self.table.query(IndexName="owner_id", KeyConditionExpression=Key("owner_id").eq(owner_id))

        return result["Items"] if "Items" in result else None

    def find_by_tag(self, tag):
        logging.info("[article] find_by_tag")
        
        if tag is not None:
            result = self.table.scan(
                FilterExpression=Attr("tags").contains(tag),
            )
        else:
            result = self.table.scan()

        return result["Items"] if "Items" in result else None
        
    def get_tags(self):
        logging.info("[article] find_by_tag")
        
        result = self.table.scan()
        tags = result["Items"]
        print(tags)
        
        return tags

