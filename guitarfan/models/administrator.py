#!/usr/bin/env python
# -*- coding: utf-8 -*-

from werkzeug.security import generate_password_hash, check_password_hash

from guitarfan.extensions.flasksqlalchemy import db


class Administrator(db.Model):
    __tablename__ = 'administrator'

    id = db.Column(db.String(50), primary_key=True, unique=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    status = db.Column(db.Integer, nullable=False, default=1)

    def __init__(self, id, name, email, password, status):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.status = status

    @classmethod
    def check_password(self, password):
        return check_password_hash(self.password, password)

    @classmethod
    def update_password(self, new_password):
        self.password = generate_password_hash(new_password, salt_length=8)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return self.status

    @property
    def is_anonymous(self):
        return False

    @classmethod
    def get_id(self):
        return self.id

    def __repr__(self):
        return '<AdminUser %r>' % self.name