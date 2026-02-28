from sqlalchemy import Column, String, Boolean, ForeignKey, DateTime, Text, Integer
from sqlalchemy.orm import relationship
from .database import Base
import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    projects = relationship("Project", back_populates="owner", cascade="all, delete-orphan")

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