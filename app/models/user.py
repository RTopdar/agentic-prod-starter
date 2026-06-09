from typing import TYPE_CHECKING, List
import bcrypt
from sqlmodel import Field, Relationship
from app.models.base import BaseModel

# prevent circular imports for type checking
if TYPE_CHECKING:
    from app.models.session import Session


class User(BaseModel, table=True):
    """
    Represents a user in the system with authentication credentials and related sessions.
    """

    id: int = Field(default=None, primary_key=True)

    # Email must be unique and indexed for fast lookups
    email: str = Field(index=True, unique=True)

    # Store the hashed password, not the plaintext
    hashed_password: str

    # Relationship to sessions - one user can have many sessions
    sessions: List["Session"] = Relationship(back_populates="user")

    def verify_password(self, password: str) -> bool:
        """
        Verify a plaintext password against the stored hashed password.
        """
        return bcrypt.checkpw(
            password.encode("utf-8"), self.hashed_password.encode("utf-8")
        )

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash a plaintext password using bcrypt.
        """
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")
