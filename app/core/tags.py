from functools import lru_cache

from pydantic import BaseModel


class RouteTags(BaseModel):
    """
    Base model for app route tags
    """

    # User module
    USER: str = "User Endpoints"

    # Thrift Endpoints
    THRIFT: str = "Thrift Endpoints"


@lru_cache
def get_tags():
    """
    Get app rotue tags
    """
    return RouteTags()
