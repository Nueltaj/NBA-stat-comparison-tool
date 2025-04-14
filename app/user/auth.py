from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.exceptions import Unauthorized
from app.core.settings import get_settings
from app.user.crud import UserRefreshTokenCRUD

# Globals
settings = get_settings()


class UserTokenGenerator:
    """
    This class is used to generate and verify JWT tokens.
    """

    def __init__(
        self,
    ):
        self.secret_key = settings.USER_SECRET_KEY
        self.access_expire_in = settings.ACCESS_TOKEN_EXPIRE_MIN
        self.refresh_expire_in = settings.REFRESH_TOKEN_EXPIRE_HOUR

    async def generate(self, sub: str, ref_id: int):
        """This method generates a JWT token.

        Args:
            sub (str): The subject of the token, typically the user's ID.
            ref_id (int): The ID of the refresh token

        Returns:
            str: The generated token.
        """

        # Check if sub is valid
        if "-" not in sub:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal Server Error: Invalid Token sub",
            )

        iat = datetime.now()
        expire = iat + timedelta(minutes=self.access_expire_in)

        data = {
            "type": "access",
            "sub": sub,
            "ref_id": str(ref_id),
            "iat": iat.timestamp(),
            "exp": expire.timestamp(),
            "iss": "thriftpals.com",
        }
        return jwt.encode(
            data,
            key=self.secret_key,
            algorithm="HS256",
        )

    async def verify(self, token: str, sub_head: str, db: AsyncSession) -> str:
        """
        Verifies the provided JWT token.

        Args:
            token (str): The JWT token to verify.
            sub_head (str): Expected prefix of the 'sub' field in the token payload.
            db (AsyncSession): The database session

        Returns:
            str | None: The sub's ID if verification succeeds, or None if invalid.

        Raises:
            Unauthorized: If the token is invalid or expired.
        """
        # Init crud
        ref_token_crud = UserRefreshTokenCRUD(db=db)

        try:
            # Decode and validate the token
            payload = jwt.decode(
                jwt=token,
                key=self.secret_key,
                algorithms=["HS256"],
            )

            # Extract and validate the 'sub' field
            sub: str | None = payload.get("sub")
            if not sub:
                raise Unauthorized("Invalid Token")

            # Ensure the token is of type 'access'
            if payload.get("type") != "access":
                raise Unauthorized("Token type is invalid")

            # Validate the 'sub' structure
            sub_parts = sub.split("-")
            if sub_parts[0] != sub_head or len(sub_parts) < 2:
                raise Unauthorized("Invalid Token")

            # Check: valid ref id
            ref_token = await ref_token_crud.get(id=int(payload["ref_id"]))
            if not ref_token or not bool(ref_token.is_active):
                raise Unauthorized("Invalid Refresh Token")

            # Check: ref token isnt expired
            ref_expired_at: datetime = ref_token.created_at + timedelta(
                hours=self.refresh_expire_in
            )  # type: ignore
            if datetime.now() > ref_expired_at.replace(tzinfo=None):
                raise Unauthorized("Invalid Token")

            # Return the ID part of 'sub'
            return sub_parts[1]

        except jwt.ExpiredSignatureError:
            raise Unauthorized("Access Token has expired")

        except jwt.PyJWTError:
            raise Unauthorized("Invalid Token")
