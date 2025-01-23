from datetime import datetime
from pytz import timezone
from sqlalchemy import create_engine, Column, Integer, String, Text, TIMESTAMP, ForeignKey, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()
        
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), nullable=False, default=datetime.now(timezone('Asia/Seoul')))
    
    # 관계 설정: 한 유저는 여러 작품을 가질 수 있다.
    works = relationship("Work", back_populates="user")
    # 관계 설정: 한 유저는 여러 댓글을 남길 수 있다.
    comments = relationship("Comment", back_populates="user")
    # 관계 설정: 한 유저는 여러 선호 작품을 가질 수 있다.
    favorites = relationship("Favorite", back_populates="user")
    # 관계 설정: 한 유저는 여러 좋아요를 누를 수 있다.
    likes = relationship("Like", back_populates="user")
    # 관계 설정: 한 유저는 여러 시청 기록을 가질 수 있다.
    watch_history = relationship("WatchHistory", back_populates="user")
    
class Work(Base):
    __tablename__ = 'works'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    title = Column(String(255), nullable=False)
    description = Column(Text)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), nullable=False, default=datetime.now(timezone('Asia/Seoul')))
    
    # 관계 설정: 한 작품은 하나의 유저에 의해 생성된다.
    user = relationship("User", back_populates="works")
    # 관계 설정: 한 작품은 여러 회차를 가질 수 있다.
    episodes = relationship("Episode", back_populates="work")
    # 관계 설정: 한 작품은 여러 공지사항을 가질 수 있다.
    notices = relationship("Notice", back_populates="work")
    # 관계 설정: 한 작품은 여러 시청 기록을 가질 수 있다.
    favorites = relationship("Favorite", back_populates="work")
    watch_history = relationship("WatchHistory", back_populates="work")

class Episode(Base):
    __tablename__ = 'episodes'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    work_id = Column(Integer, ForeignKey('works.id'))
    title = Column(String(255), nullable=False)
    content = Column(Text)
    created_at = Column(TIMESTAMP, default="CURRENT_TIMESTAMP")
    
    # 관계 설정: 한 회차는 하나의 작품에 속한다.
    work = relationship("Work", back_populates="episodes")
    # 관계 설정: 한 회차는 여러 댓글을 가질 수 있다.
    comments = relationship("Comment", back_populates="episode")

class Notice(Base):
    __tablename__ = 'notices'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    work_id = Column(Integer, ForeignKey('works.id'))
    title = Column(String(255), nullable=False)
    content = Column(Text)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), nullable=False, default=datetime.now(timezone('Asia/Seoul')))
    
    # 관계 설정: 한 공지사항은 하나의 작품에 속한다.
    work = relationship("Work", back_populates="notices")
    # 관계 설정: 한 공지사항은 여러 댓글을 가질 수 있다.
    comments = relationship("Comment", back_populates="notice")

class Comment(Base):
    __tablename__ = 'comments'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    episode_id = Column(Integer, ForeignKey('episodes.id'))
    notice_id = Column(Integer, ForeignKey('notices.id'))
    content = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), nullable=False, default=datetime.now(timezone('Asia/Seoul')))
    
    # 관계 설정: 한 댓글은 하나의 유저에 의해 작성된다.
    user = relationship("User", back_populates="comments")
    # 관계 설정: 한 댓글은 하나의 회차에 속한다.
    episode = relationship("Episode", back_populates="comments")
    # 관계 설정: 한 댓글은 하나의 공지사항에 속한다.
    notice = relationship("Notice", back_populates="comments")
    # 관계 설정: 한 댓글은 여러 좋아요를 받을 수 있다.
    likes = relationship("Like", back_populates="comment")

class Favorite(Base):
    __tablename__ = 'favorites'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    work_id = Column(Integer, ForeignKey('works.id'))
    added_at = Column(TIMESTAMP, default="CURRENT_TIMESTAMP")
    
    # 관계 설정: 한 선호 작품은 하나의 유저와 작품에 속한다.
    user = relationship("User", back_populates="favorites")
    work = relationship("Work", back_populates="favorites")

class Like(Base):
    __tablename__ = 'likes'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    comment_id = Column(Integer, ForeignKey('comments.id'))
    
    # 관계 설정: 한 좋아요는 하나의 유저에 의해 눌린다.
    user = relationship("User", back_populates="likes")
    # 관계 설정: 한 좋아요는 하나의 댓글에 속한다.
    comment = relationship("Comment", back_populates="likes")

class WatchHistory(Base):
    __tablename__ = 'watch_history'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    work_id = Column(Integer, ForeignKey('works.id'))
    watched_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), nullable=False, default=datetime.now(timezone('Asia/Seoul')))
    
    # 관계 설정: 한 시청 기록은 하나의 유저에 의해 생성된다.
    user = relationship("User", back_populates="watch_history")
    # 관계 설정: 한 시청 기록은 하나의 작품에 속한다.
    work = relationship("Work", back_populates="watch_history")