from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base
from ToC.configs import config


class DbSession(object):

    def __new__(cls, *args, **kwargs):
        if not hasattr(DbSession, "_instance"):
            DbSession._instance = object.__new__(cls)
        return DbSession._instance

    def __init__(self):
        # 创建数据库引擎
        self.engine = create_engine(config.MYSQL_URL, echo=False, encoding='utf-8', pool_size=10, pool_recycle=3600)
        # 创建数据模型绑定
        self.base = automap_base()
        self.base.prepare(self.engine, reflect=True)

    def table(self, table_name):
        return getattr(self.base.classes, table_name)

    def make_session(self):
        session_class = sessionmaker(bind=self.engine)
        session = session_class()
        return session