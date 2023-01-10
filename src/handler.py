from src.domain.article import Article
from src.domain.article_dao import ArticleDao
from src.core.resources_mgr import ResourcesMgr

import logging
import json

logger = logging.getLogger()
print("create dynamodb resources")
resources_mgr = ResourcesMgr()

dao = ArticleDao(
    dynamodb_resource=resources_mgr.dynamodb_resource,
    dynamodb_client=resources_mgr.dynamodb_client,
    table_name=resources_mgr.table_name(),
)

def create_article(event, context):
    body = json.loads(event["body"])

    try:

        resources_mgr.metrics.put_metric(
            namespace="epiblog", operation="create", is_exception=False
        )

        article = Article(author=body["author"], title=body["title"], content=body["content"], tags=body["tags"], owner_id=body["owner_id"])
        dao.create(article)

    except BaseException as e:
        logging.critical(e, exc_info=True)
        resources_mgr.metrics.put_metric(
            namespace="epiblog", operation="create", is_exception=True
        )

    return {
        "statusCode": 201,
        "headers": {"Content-Type": "application/json",
            "Access-Control-Allow-Headers" : "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
            "Access-Control-Allow-Origin": "*",  
            "Access-Control-Allow-Methods": "POST, OPTIONS" 
        },
        "body": article.to_json(),
    }

def delete_article(event, context):
    try:

        resources_mgr.metrics.put_metric(
            namespace="epiblog", operation="delete", is_exception=False
        )

        dao.delete(uuid=event["pathParameters"]["article_id"])

    except BaseException as e:
        logging.critical(e, exc_info=True)
        resources_mgr.metrics.put_metric(
            namespace="epiblog", operation="delete", is_exception=True
        )

    return {
        "statusCode": 204,
        "headers": {"Content-Type": "application/json",
            "Access-Control-Allow-Headers" : "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
            "Access-Control-Allow-Origin": "*",  
            "Access-Control-Allow-Methods": "DELETE, OPTIONS" 
        },
        "body": "",
    }

def find_by_uuid(event, context):
    try:

        resources_mgr.metrics.put_metric(
            namespace="epiblog", operation="find", is_exception=False
        )

        entities = dao.find_by_uuid(event["pathParameters"]["article_id"],
                                                )

    except BaseException as e:
        logging.critical(e, exc_info=True)
        resources_mgr.metrics.put_metric(
            namespace="epiblog", operation="find", is_exception=True
        )

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json",
            "Access-Control-Allow-Headers" : "Content-Type",
            "Access-Control-Allow-Origin": "*", 
            "Access-Control-Allow-Methods": "GET"
        },
        "body": json.dumps(entities, default=lambda entity: entity.to_json()),
    }


def find_by_owner_id(event, context):
    try:

        resources_mgr.metrics.put_metric(
            namespace="epiblog", operation="find", is_exception=False
        )

        entities = dao.find_by_tag(event["queryStringParameters"]["owner_id"],
                                                )

    except BaseException as e:
        logging.critical(e, exc_info=True)
        resources_mgr.metrics.put_metric(
            namespace="epiblog", operation="find", is_exception=True
        )

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json", 
            "Access-Control-Allow-Headers" : "Content-Type",
            "Access-Control-Allow-Origin": "*", 
            "Access-Control-Allow-Methods": "GET"
        },
        "body": json.dumps(entities, default=lambda entity: entity.to_json()),
    }

def find_by_tag(event, context):
    try:

        resources_mgr.metrics.put_metric(
            namespace="epiblog", operation="find", is_exception=False
        )
        tag = None
        if (event["queryStringParameters"] is not None):
            if ("tag" in event["queryStringParameters"]):
                tag = event["queryStringParameters"]["tag"]

        entities = dao.find_by_tag(tag          )

    except BaseException as e:
        logging.critical(e, exc_info=True)
        resources_mgr.metrics.put_metric(
            namespace="epiblog", operation="find", is_exception=True
        )

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json", 
            "Access-Control-Allow-Headers" : "Content-Type",
            "Access-Control-Allow-Origin": "*", 
            "Access-Control-Allow-Methods": "GET"
        },
        "body": json.dumps(entities, default=lambda entity: entity.to_json()),
    }
    
def get_tags(event, context):
    try:

        resources_mgr.metrics.put_metric(
            namespace="epiblog", operation="find", is_exception=False
        )
        
        entities = dao.get_tags()

    except BaseException as e:
        logging.critical(e, exc_info=True)
        resources_mgr.metrics.put_metric(
            namespace="epiblog", operation="find", is_exception=True
        )

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json", 
            "Access-Control-Allow-Headers" : "Content-Type",
            "Access-Control-Allow-Origin": "*", 
            "Access-Control-Allow-Methods": "GET"
        },
        "body": json.dumps(entities, default=lambda entity: entity.to_json()),
    }