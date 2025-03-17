import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship, declarative_base
from eralchemy2 import render_er

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    firstname = Column(String(50), nullable=True)
    lastname = Column(String(50), nullable=True)
    email = Column(String(120), nullable=False)

    posts = relationship("Post", back_populates="user")
    followers = relationship("Follower", foreign_keys='Follower.user_to_id', back_populates="followed")
    following = relationship("Follower", foreign_keys='Follower.user_from_id', back_populates="follower")
    comments = relationship("Comment", back_populates="author")

class Follower(Base):
    __tablename__ = 'follower'
    user_from_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    user_to_id = Column(Integer, ForeignKey('user.id'), primary_key=True)

    follower = relationship("User", foreign_keys=[user_from_id], back_populates="following")
    followed = relationship("User", foreign_keys=[user_to_id], back_populates="followers")

class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))

    user = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")
    media = relationship("Media", back_populates="post")

class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    comment_text = Column(String(300))
    author_id = Column(Integer, ForeignKey('user.id'))
    post_id = Column(Integer, ForeignKey('post.id'))

    author = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")

class Media(Base):
    __tablename__ = 'media'
    id = Column(Integer, primary_key=True)
    type = Column(String(20))  # e.g. 'image', 'video'
    url = Column(String(250))
    post_id = Column(Integer, ForeignKey('post.id'))

    post = relationship("Post", back_populates="media")

# Generate ER Diagram
try:
    result = render_er(Base, 'diagram.png')
    print("✅ Success! Check the updated diagram.png")
except Exception as e:
    print("❌ There was a problem generating the diagram")
    raise e


