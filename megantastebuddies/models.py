# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from sqlalchemy import (
    Column,
    Integer,
    Text,
    )

from sqlalchemy.ext.declarative import declarative_base, declared_attr

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    validates,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class TableSetup(Base):
    """Gives all classes a tablename, repr and id.  Also allows us to
    add, edit, delete, find a member of a class by any attribute or
    combinations of attributes and return all members on request.
    """
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    @declared_attr
    def __repr__(cls):
        return "<(%s)>" % cls.__name__

    id = Column(Integer, primary_key=True, autoincrement=True)

    @classmethod
    def add(cls, session=None, **kwargs):
        if session is None:
            session = DBSession
        instance = cls(**kwargs)
        session.add(instance)
        return instance

    @classmethod
    def all(cls, session=None):
        if session is None:
            session = DBSession
        return session.query(cls).all

    @classmethod
    def lookup_by_attribute(cls, session=None, **kwargs):
        """Should be able to filter any class by any attribute
        or multiple attributes, even if that attribute has
        multiple values in a list.  This is how we suggest
        users to groups or groups to users, how we lookup any
        class by id, lookup any user by username etc."""
        if session is None:
            session = DBSession
        results = {}
        for a, v in kwargs:
            attribute = a
            value = v
            if type(value) == list:
                results[attribute] = []
                for i in value:
                    # iterate through values and see whether one of the users
                    # tastes is equal to this taste.  No idea how to do this.
                    pass
            else:
                results[attribute] = (session.query(cls).filter_by(attribute
                                      == value).all())

        return results

    @classmethod
    def edit(cls, session=None, id=None, **kwargs):
        if session is None:
            session = DBSession
        session.query(cls).filter(cls.id == id).update(**kwargs)

    @classmethod
    def delete(cls, session=None, id=None):
        if session is None:
            session = DBSession
        session.query(cls).filter(cls.id == id).delete()


class User(TableSetup):
    username = Column(Text, nullable=False, unique=True)
    password = Column(Text, nullable=False)
    email = Column(Text, nullable=False, unique=True)
    firstname = Column(Text)
    lastname = Column(Text)
    restaurants = Column(Text)
    fav_food = Column(Text)
    age = one age to many users
    location = one location to many users
    cost =  many to many
    taste = many to many
    diet = many to many
    groups = many to many
    admin_groups = one user to many groups
    verification_code = None
    confirmed = False

    @validates('email')
    def validate_email(self, key, email):
        try:
            assert '@' in email
            assert '.' in email
            return email
        except:
            raise TypeError('Please enter a valid email address')

    def __repr__(self):
        return "<User({} {}, username={})>".format(self.firstname,
                                                   self.lastname,
                                                   self.username)


class Taste(TableSetup):
    taste = Column(Text)


class AgeGroup(TableSetup):
    age_group = Column(Text)


class Location(TableSetup):
    location = Column(Text)


class Cost(TableSetup):
    cost = Column(Text)


class Diet(TableSetup):
    diet = Column(Text)


class Group(TableSetup):
    name = Column(Text, primary_key=True)
    description = Column(Text, nullable=False)
    location = one location to many groups
    discussions = many discussions to one Group
    admin = one group admin to one Group
    taste = many to many
    diet = many to many
    cost = one cost to many groups
    age = many ages to many groups
    members = many users to many group


class Discussion(TableSetup):
    title = Column(Text)
    group = many discussions to one Group
    posts = one discussion to many posts


class Post(TableSetup):
    text =  Column(Text)
    discussion = many posts to one Discussion
