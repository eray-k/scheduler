from datetime import datetime

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


class TagActivityLink(SQLModel, table=True):
    tag_id: int | None = Field(default=None, foreign_key="tag.id", primary_key=True)
    activity_id: int | None = Field(default=None, foreign_key="activity.id", primary_key=True)


class TagBase(SQLModel):
    name: str = Field(index=True)


class Tag(TagBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    activities: list["Activity"] = Relationship(back_populates="tags", link_model=TagActivityLink,
                                                sa_relationship_kwargs={"lazy": "noload"})


class TagCreate(TagBase):
    pass


class TagPublic(TagBase):
    id: int


class TagUpdate(SQLModel):
    title: str | None = None


class ActivityBase(SQLModel):
    content: str = Field(default="", max_length=200)
    beginning_datetime: datetime
    ending_datetime: datetime | None = Field(default=None)
    is_done: bool = Field(default=False)


class Activity(ActivityBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    owner_id: int = Field(index=True, foreign_key="user.id")
    owner: User = Relationship(back_populates="activities")

    tags: list[Tag] = Relationship(back_populates="activities", link_model=TagActivityLink)


class ActivityCreate(ActivityBase):
    pass


class ActivityUpdate(SQLModel):
    content: str | None = None
    beginning_datetime: datetime | None = None
    ending_datetime: datetime | None = None
    is_done: bool | None = None


class ActivityPublic(ActivityBase):
    id: int


class ActivityPublicWithOwner(ActivityPublic):
    owner: User


User.update_forward_refs(Activity=Activity)
UserPublicWithActivities.update_forward_refs(Activity=Activity)

Tag.update_forward_refs(Activity=Activity)
