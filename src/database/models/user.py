from sqlmodel import SQLModel, Field, Relationship



class UserBase(SQLModel):
    username: str = Field(index=True)


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    activities: list["Activity"] = Relationship(back_populates="owner")


class UserCreate(UserBase):
    pass


class UserPublic(UserBase):
    id: int


class UserPublicWithActivities(UserPublic):
    activities: list["Activity"] = []


class UserUpdate(SQLModel):
    username: str | None = None