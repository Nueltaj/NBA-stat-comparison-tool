from app.core.settings import get_settings
from app.user import models

# Globals
settings = get_settings()


def format_user(user: models.User):
    """
    Format user obj to dict
    """
    return {
        "id": user.id,
        "pfp_url": settings.MEDIA_URL + user.pfp_url,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "phone": user.phone,
        "is_active": user.is_active,
        "updated_at": user.updated_at,
        "created_at": user.created_at,
    }
