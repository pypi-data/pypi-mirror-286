import importlib
import os
import sys
from logging import Logger, getLogger, Formatter, StreamHandler
from typing import Generic, Type, Optional
from mongey.db import DB, DatabaseConfig
from mongey.context import ctx as mongeyctx
from mongey.cache import TCache
from .config import TConfig, BaseConfig


def get_app_config_class() -> Type[TConfig]:
    try:
        module = importlib.import_module("app.config")
        config_class = module.__dict__["Config"]
    except (ModuleNotFoundError, KeyError):
        print("application config module not found, initializing with ashtree.config.BaseConfig")
        config_class = BaseConfig
    return config_class


def get_project_dir() -> str:
    try:
        module = importlib.import_module("app.config")
        file_dir = os.path.dirname(module.__file__)
        project_dir = os.path.abspath(os.path.join(file_dir, ".."))
    except ModuleNotFoundError:
        print("application config module not found, project_dir is set to \".\"")
        project_dir = "."
    return project_dir


class Context(Generic[TConfig]):
    _cfg: Optional[TConfig] = None
    _log: Optional[Logger] = None
    _l1_cache: Optional["TCache"] = None
    _l2_cache: Optional["TCache"] = None
    _project_dir: Optional[str] = None
    _db: Optional["DB"] = None

    @property
    def project_dir(self) -> str:
        if self._project_dir is None:
            self._project_dir = get_project_dir()
        return self._project_dir

    @property
    def cfg(self) -> TConfig:
        if self._cfg is None:
            cfg_cls = get_app_config_class()
            cfg_filename = os.environ.get("ASHTREE_CONFIG", "application.toml")
            if not os.path.isfile(cfg_filename):
                cfg_filename = os.path.join(self.project_dir, cfg_filename)
            if os.path.isfile(cfg_filename):
                self._cfg = cfg_cls.parse(cfg_filename)
            else:
                print("no configuration files found, using ashtree default config")
                self._cfg = cfg_cls()
        return self._cfg

    @property
    def log(self) -> Logger:
        if self._log is None:
            logger = getLogger(__name__)
            logger.propagate = False
            logger.setLevel(self.cfg.logging.level)
            for handler in logger.handlers:
                logger.removeHandler(handler)
            log_format = Formatter("[%(asctime)s] %(levelname)s %(filename)s:%(lineno)d %(message)s")
            handler = StreamHandler(stream=sys.stdout)
            handler.setLevel(self.cfg.logging.level)
            handler.setFormatter(log_format)
            logger.addHandler(handler)
            self._log = logger
        return self._log

    @property
    def l1_cache(self) -> TCache:
        from .cache import CACHE_ENGINE_MAP, NoCache
        if self._l1_cache is None:
            cache = CACHE_ENGINE_MAP.get(self.cfg.cache.level1)
            if cache is None:
                self.log.error(f"cache engine {self.cfg.cache.level1} not found, falling back to NoCache")
                self._l1_cache = NoCache()
            else:
                self._l1_cache = cache()
        return self._l1_cache

    @property
    def l2_cache(self) -> TCache:
        from .cache import CACHE_ENGINE_MAP, NoCache
        if self._l2_cache is None:
            cache = CACHE_ENGINE_MAP.get(self.cfg.cache.level1)
            if cache is None:
                self.log.error(f"cache engine {self.cfg.cache.level1} not found, falling back to NoCache")
                self._l2_cache = NoCache()
            else:
                self._l2_cache = cache()
        return self._l2_cache

    @property
    def db(self) -> "DB":
        if self._db is None:
            self._db = mongeyctx.db
            dbcfg: DatabaseConfig = {
                "meta": {
                    "uri": self.cfg.database.uri,
                    "kwargs": {
                        "serverSelectionTimeout": self.cfg.database.timeout
                    }
                },
                "shards": {}
            }
            self._db.configure(dbcfg, mock=False)
        return self._db

    def from_config(self, cfg: TConfig):
        self._cfg = cfg
        self._log = None
        self._l1_cache = None
        self._l2_cache = None


ctx = Context()
