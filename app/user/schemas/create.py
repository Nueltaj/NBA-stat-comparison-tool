from pydantic import BaseModel, EmailStr, Field, field_validator


class UserCreate(BaseModel):
    """
    Create schema for users
    """

    first_name: str = Field(description="The User's First Name", max_length=50)
    last_name: str = Field(description="The User's Last Name", max_length=50)
    email: EmailStr = Field(description="The User's email Address")
    phone: str = Field(description="The User's Phone Number", max_length=14)
    password: str = Field(description="The User's raw password")

    @field_validator("email")
    def validate_email(cls, v: str):
        """
        Field validator for email
        """
        return v.lower()
