from typing import Optional, Dict, Any, Set

from functools import lru_cache

import ciphey
from ciphey.iface import T, ParamSpec, Config

import json, csv

# We can use a generic resource loader here, as we can instantiate it later
class Json(ciphey.iface.ResourceLoader):
    def whatResources(self) -> T:
        return self._names

    @lru_cache
    def getResource(self, name: str) -> T:
        return T(json.load(self._paths[int(name) - 1]))

    @staticmethod
    def getName() -> str:
        return "json"

    @staticmethod
    def getParams() -> Optional[Dict[str, ciphey.iface.ParamSpec]]:
        return {
            "path": ParamSpec(req=True, desc="The path to a JSON file", list=True)
        }

    def __init__(self, config: ciphey.iface.Config):
        super().__init__(config)
        self._paths = self._params()["path"]
        self._names = set(range(1, len(self._paths)))


# We can use a generic resource loader here, as we can instantiate it later
class Csv(ciphey.iface.ResourceLoader):
    def whatResources(self) -> T:
        return self._names

    @lru_cache
    def getResource(self, name: str) -> T:
        ret = T()
        for i in csv.reader(open(self._paths[int(name) - 1])):
            ret.append(i)
        return ret

    @staticmethod
    def getName() -> str:
        return "csv"

    @staticmethod
    def getParams() -> Optional[Dict[str, ciphey.iface.ParamSpec]]:
        return {
            "path": ParamSpec(req=True, desc="The path to a CSV file", list=True)
        }

    def __init__(self, config: ciphey.iface.Config):
        super().__init__(config)
        self._paths = self._params()["path"]
        self._names = set(range(1, len(self._paths)))


ciphey.iface.registry.register(Json, ciphey.iface.ResourceLoader)
ciphey.iface.registry.register(Csv, ciphey.iface.ResourceLoader)