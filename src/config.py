#  Project: Telegram-IP-CALC
#  Filename: config.py
#  Create Date: 12.09.2022, 14:05
#  SantaSpeen Copyright (c) 2022
import logging
import json
import os

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)-29s - %(levelname)-5s - %(message)s")


class Config:

    # noinspection PyTypeChecker
    def __init__(self, config_file="сonfig.json"):
        self.log = logging.getLogger(__name__)
        self.debug = self.log.debug

        self.config_file = config_file
        self.raw_config: dict = None

        self.token: str = None

        self._read_config()

    def _read_config(self):
        self.debug("_read_config(self)")
        if os.path.isfile(self.config_file):
            self.log.info(f"Config file: %s - found" % self.config_file)
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.raw_config = json.load(f)
        else:
            raise FileNotFoundError("Cannot found config file at %s." % self.config_file)

        self.token = self.raw_config.get("token")
