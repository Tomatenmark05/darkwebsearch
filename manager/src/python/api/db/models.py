from sqlalchemy import (
    create_engine, Column, String, Integer, ForeignKey
)
from sqlalchemy.orm import sessionmaker, relationship, Session, declarative_base
from sqlalchemy.ext.associationproxy import association_proxy

Base = declarative_base()


class ContentTag(Base):
    """Association object for Content <-> Tag relationship

    Stores extra attributes for the relationship, e.g. `priority`.
    """
    __tablename__ = "content_tags"

    content_id = Column(Integer, ForeignKey("contents.id", ondelete="CASCADE"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True)
    priority = Column(Integer, nullable=False, default=0)

    # relationships to the parent objects
    content = relationship("Content", back_populates="tag_links")
    tag = relationship("Tag", back_populates="content_links")


class Content(Base):
    __tablename__ = "contents"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(2083), unique=True, index=True, nullable=False)
    title = Column(String(255), nullable=True)
    description = Column(String(1024), nullable=True)

    # association objects linking to Tag (ContentTag instances)
    tag_links = relationship(
        "ContentTag",
        back_populates="content",
        cascade="all, delete-orphan",
    )

    # convenience proxy to get Tag objects directly: content.tags -> [Tag,...]
    tags = association_proxy("tag_links", "tag")


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True, nullable=False)

    content_links = relationship(
        "ContentTag",
        back_populates="tag",
        cascade="all, delete-orphan",
    )

    contents = association_proxy("content_links", "content")
