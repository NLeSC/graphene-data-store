from database import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Boolean, ARRAY, JSON, func
from sqlalchemy.orm import backref, relationship


class Department(Base):
    __tablename__ = 'department'
    id = Column(Integer, primary_key=True)
    name = Column(String)


class Role(Base):
    __tablename__ = 'roles'
    role_id = Column(Integer, primary_key=True)
    name = Column(String)


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    # Use default=func.now() to set the default hiring time
    # of an User to be the current time when an
    # User record was created
    hired_on = Column(DateTime, default=func.now())
    department_id = Column(Integer, ForeignKey('department.id'))
    role_id = Column(Integer, ForeignKey('roles.role_id'))
    # Use cascade='delete,all' to propagate the deletion of a Department onto its Users
    department = relationship(
        Department,
        backref=backref('users',
                        uselist=True,
                        cascade='delete,all'))
    role = relationship(
        Role,
        backref=backref('roles',
                        uselist=True,
                        cascade='delete,all'))

class Dataset(Base):
    __tablename__ = 'datasets'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    table_name = Column(String)
    is_active = Column(Boolean)
    # created_at = Column(DateTime)
    raw = Column(JSON)