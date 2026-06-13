from typing import TYPE_CHECKING, List
from sqlmodel import Field, Relationship
from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.user import User  # prevent circular imports for type checking


class Session(BaseModel, table=True):
    """
    Represents a user session in the system, linked to a specific user.
    """

    id: str = Field(default=None, primary_key=True)

    # Foreign key to the User table
    user_id: int = Field(foreign_key="user.id")

    # Optional friendly name for the chat (e.g., "Recipe Ideas")
    name: str = Field(default="")

    # Relationship back to the User
    user: "User" = Relationship(back_populates="sessions")
