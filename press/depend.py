from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base
from pymongo import MongoClient, uri_parser
from sqlalchemy.pool import NullPool
from press.conf import config


class CoronaryDbSession(object):

    def __new__(cls, *args, **kwargs):
        if not hasattr(CoronaryDbSession, "_instance"):
            CoronaryDbSession._instance = object.__new__(cls)
        return CoronaryDbSession._instance

    def __init__(self, url=None):
        # 创建数据库引擎
        self.engine = create_engine(config.CORONARY_URI if not url else url,
                                    echo=False, encoding='utf-8', pool_size=5, pool_recycle=3600)
        # 创建数据模型绑定
        self.base = automap_base()
        self.base.prepare(self.engine, reflect=True)

    def table(self, table_name):
        return getattr(self.base.classes, table_name)

    def make_session(self):
        session_class = sessionmaker(bind=self.engine, autoflush=True)
        session = session_class()
        return session


class CerebralDbSession(object):

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self):
        # 创建数据库引擎
        self.engine = create_engine(config.CEREBRAL_URI, echo=False, encoding='utf-8', pool_size=5, pool_recycle=3600)
        # 创建数据模型绑定
        self.base = automap_base()
        self.base.prepare(self.engine, reflect=True)

    def table(self, table_name):
        return getattr(self.base.classes, table_name)

    def make_session(self):
        session_class = sessionmaker(bind=self.engine)
        session = session_class()
        return session


class CalciumDbSession(object):

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self):
        # 创建数据库引擎
        self.engine = create_engine(config.CALCIUM_URI, echo=False, encoding='utf-8', pool_size=5, pool_recycle=3600)
        # 创建数据模型绑定
        self.base = automap_base()
        self.base.prepare(self.engine, reflect=True)

    def table(self, table_name):
        return getattr(self.base.classes, table_name)

    def make_session(self):
        session_class = sessionmaker(bind=self.engine)
        session = session_class()
        return session


class ThoracicDbSession(object):

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self):
        # 创建数据库引擎
        self.engine = create_engine(config.THORACIC_URI, echo=False, encoding='utf-8', pool_size=5, pool_recycle=3600)
        # 创建数据模型绑定
        self.base = automap_base()
        self.base.prepare(self.engine, reflect=True)

    def table(self, table_name):
        return getattr(self.base.classes, table_name)

    def make_session(self):
        session_class = sessionmaker(bind=self.engine)
        session = session_class()
        return session


class DicomDbSession(object):

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self):
        # 创建数据库引擎
        self.engine = create_engine(config.DICOM_URI, echo=False, encoding='utf-8', pool_size=5, pool_recycle=3600)
        # 创建数据模型绑定
        self.base = automap_base()
        self.base.prepare(self.engine, reflect=True)

    def table(self, table_name):
        return getattr(self.base.classes, table_name)

    def make_session(self):
        session_class = sessionmaker(bind=self.engine)
        session = session_class()
        return session


def singleton(cls):

    _instance = dict()

    def _singleton(*args, **kwargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kwargs)
        return _instance[cls]
    return _singleton


@singleton
class CoronaryMongo(object):
    def __init__(self, uri):
        self.cx = None
        self.db = None

        if uri is not None:
            args = tuple([uri])
        else:
            raise ValueError(
                "You must specify a URI or set the MONGO_URI Flask config variable",
            )

        parsed_uri = uri_parser.parse_uri(uri)
        database_name = parsed_uri["database"]

        # Avoid a more confusing error later when we try to get the DB
        if not database_name:
            raise ValueError("Your URI must specify a database name")

        self.cx = MongoClient(*args)
        self.db = self.cx[database_name]


@singleton
class CerebralMongo(object):
    def __init__(self, uri):
        self.cx = None
        self.db = None

        if uri is not None:
            args = tuple([uri])
        else:
            raise ValueError(
                "You must specify a URI or set the MONGO_URI Flask config variable",
            )

        parsed_uri = uri_parser.parse_uri(uri)
        database_name = parsed_uri["database"]

        # Avoid a more confusing error later when we try to get the DB
        if not database_name:
            raise ValueError("Your URI must specify a database name")

        self.cx = MongoClient(*args)
        self.db = self.cx[database_name]


@singleton
class CalciumMongo(object):
    def __init__(self, uri):
        self.cx = None
        self.db = None

        if uri is not None:
            args = tuple([uri])
        else:
            raise ValueError(
                "You must specify a URI or set the MONGO_URI Flask config variable",
            )

        parsed_uri = uri_parser.parse_uri(uri)
        database_name = parsed_uri["database"]

        # Avoid a more confusing error later when we try to get the DB
        if not database_name:
            raise ValueError("Your URI must specify a database name")

        self.cx = MongoClient(*args)
        self.db = self.cx[database_name]


@singleton
class ThoracicMongo(object):
    def __init__(self, uri):
        self.cx = None
        self.db = None

        if uri is not None:
            args = tuple([uri])
        else:
            raise ValueError(
                "You must specify a URI or set the MONGO_URI Flask config variable",
            )

        parsed_uri = uri_parser.parse_uri(uri)
        database_name = parsed_uri["database"]

        # Avoid a more confusing error later when we try to get the DB
        if not database_name:
            raise ValueError("Your URI must specify a database name")

        self.cx = MongoClient(*args)
        self.db = self.cx[database_name]
