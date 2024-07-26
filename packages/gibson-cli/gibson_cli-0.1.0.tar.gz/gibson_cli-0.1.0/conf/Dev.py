import os

from conf.dev.Api import Api
from conf.dev.Base import Base
from conf.dev.Model import Model
from conf.dev.Schema import Schema


class Dev:
    def __init__(self):
        self.active = False
        self.api = Api()
        self.base = Base()
        self.model = Model()
        self.schema = Schema()
