import json
import uuid


class Article:
    def __init__(self, **kwargs) -> None:
        self.title = kwargs["title"]
        self.content = kwargs["content"]
        self.author = kwargs["author"]
        self.tags = kwargs["tags"]
        self.owner_id = kwargs["owner_id"]

        self.uuid = str(uuid.uuid4())

    def to_dict(self):
        return self.__dict__

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Article):
            return NotImplemented

        return self.title == other.title and self.content == other.content and self.owner_id == other.owner_id and self.uuid == other.uuid

# Article
# Post /article   #Create
# Get /article/id #GetByArticleId
# Get /article?owner_id=uuid #GetArticleByOwnerId
# Get /article?tag=xxx #GetArticleByTag 
# Delete /article/id #DeleteByArticleId