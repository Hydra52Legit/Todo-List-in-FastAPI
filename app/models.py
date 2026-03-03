from sqlalchemy import Column, String, Boolean, ForeignKey, DateTime, Text, Integer, Table
from sqlalchemy.orm import relationship
from .database import Base
import datetime

task_tags = Table(
    'task_tags',
    Base.metadata,
    Column('task_id', Integer, ForeignKey('tasks.id', ondelete="CASCADE"), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id', ondelete="CASCADE"), primary_key=True)
)

class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True, nullable=False)
    color = Column(String(7), default="#808080")  # Hex color code
    tasks = relationship("Task", secondary=task_tags, back_populates="tags")
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    user = relationship("User", back_populates="tags")
    tasks = relationship("Task", secondary=task_tags, back_populates="tags")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    projects = relationship("Project", back_populates="owner", cascade="all, delete-orphan")

    tags = relationship("Tag", back_populates="user", cascade="all, delete-orphan")

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True);
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False);
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    owner = relationship("User", back_populates="projects")
    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    completed = Column(Boolean, default=False)
    priority = Column(Integer, default=1)
    start_time = Column(DateTime, nullable=True)
    end_time = Column(DateTime, nullable=True)
    notes = Column(Text, nullable=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    project = relationship("Project", back_populates="tasks")

    tags = relationship("Tag", secondary=task_tags, back_populates="tasks")
