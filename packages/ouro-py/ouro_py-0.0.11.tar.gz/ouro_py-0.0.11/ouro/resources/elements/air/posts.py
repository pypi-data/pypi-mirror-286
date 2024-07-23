import logging
from typing import List, Optional

from ouro._resource import SyncAPIResource
from ouro.models import Post

from .content import Content

log: logging.Logger = logging.getLogger(__name__)


__all__ = ["Posts"]


class Posts(SyncAPIResource):
    def create(
        self,
        content: Content,
        name: str,
        description: Optional[str] = None,
        visibility: Optional[str] = None,
        monetization: Optional[str] = None,
        price: Optional[float] = None,
        **kwargs,
    ) -> Post:
        """
        Create a new Post
        """

        post = {
            "name": name,
            "description": description,
            "visibility": visibility,
            "monetization": monetization,
            "price": price,
            **kwargs,
        }
        # Filter out None values
        post = {k: v for k, v in post.items() if v is not None}

        request = self.client.post(
            "/elements/air/posts/create",
            json={
                "post": post,
                "content": content.to_dict(),
            },
        )
        request.raise_for_status()
        response = request.json()
        if response["error"]:
            raise Exception(response["error"])

        return Post(**response["data"])

    def retrieve(self, id: str):
        """
        Retrieve a Post by its id
        """
        request = self.client.get(
            f"/elements/air/posts/{id}",
        )
        request.raise_for_status()
        response = request.json()
        if response["error"]:
            raise Exception(response["error"])

        return Post(**response["data"])

    def update(
        self,
        id: str,
        content: Optional[Content] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        visibility: Optional[str] = None,
        monetization: Optional[str] = None,
        price: Optional[float] = None,
        **kwargs,
    ) -> Post:
        """
        Update a Post by its id
        """

        post = {
            "name": name,
            "description": description,
            "visibility": visibility,
            "monetization": monetization,
            "price": price,
            **kwargs,
        }
        # Filter out None values
        post = {k: v for k, v in post.items() if v is not None}

        request = self.client.put(
            f"/elements/air/posts/{id}",
            json={
                "post": post,
                "content": content.to_dict() if content is not None else None,
            },
        )
        request.raise_for_status()
        response = request.json()
        if response["error"]:
            raise Exception(response["error"])
        return Post(**response["data"])
