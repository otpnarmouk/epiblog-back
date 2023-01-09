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
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
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
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": book.to_json(),
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
        "headers": {"Content-Type": "application/json"},
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
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(entities, default=lambda entity: entity.to_json()),
    }

def find_by_tag(event, context):
    try:

        resources_mgr.metrics.put_metric(
            namespace="epiblog", operation="find", is_exception=False
        )

        entities = dao.find_by_tag(event["queryStringParameters"]["tag"],
                                                )

    except BaseException as e:
        logging.critical(e, exc_info=True)
        resources_mgr.metrics.put_metric(
            namespace="epiblog", operation="find", is_exception=True
        )

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(entities, default=lambda entity: entity.to_json()),
    }

# def authorizer(event, context):
#     print(event)

#     lambda_function_arn = context.invoked_function_arn
#     aws_account_id = lambda_function_arn.split(":")[4]
#     print(aws_account_id)

#     return Authorizer().authenticate(account=aws_account_id, token=event["authorizationToken"])
