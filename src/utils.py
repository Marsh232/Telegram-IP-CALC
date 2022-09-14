#  Project: Telegram-IP-CALC
#  Filename: utils.py
#  Create Date: 12.09.2022, 14:05
#  SantaSpeen Copyright (c) 2022
import logging
import json
import os

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)-29s - %(levelname)-5s - %(message)s")


class Config:

    def __init__(self, config_file="config.json"):
        self.log = logging.getLogger("Config class")

        self.config_file = config_file
        self.raw_config: dict

        self.token: str

        self._read_config()

    def _read_config(self):
        self.log.debug("_read_config(self)")
        if os.path.isfile(self.config_file):
            self.log.info(f"Config file: %s - found" % self.config_file)
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.raw_config = json.load(f)
        else:
            raise FileNotFoundError("Cannot found config file at %s." % self.config_file)

        self.token = self.raw_config.get("token")


class Cache:

    def __init__(self, cache_file='cache.json', infile=True):
        self.log = logging.getLogger("Cache class")

        self.cache_file = cache_file
        self.raw_cache: dict = {}

        self._read_cache()

    def _read_cache(self):
        self.log.debug("_read_cache(self)")
        if os.path.isfile(self.cache_file):
            self.log.debug(f"Read cache from %s." % self.cache_file)
            with open(self.cache_file, 'r', encoding='utf-8') as f:
                self.raw_config = json.load(f)
        else:
            self.log.debug("Cannot found cache file at %s. Creating file..." % self.cache_file)
            with open(self.cache_file, 'x', encoding='utf-8') as f:
                json.dump(self.raw_cache, f)
