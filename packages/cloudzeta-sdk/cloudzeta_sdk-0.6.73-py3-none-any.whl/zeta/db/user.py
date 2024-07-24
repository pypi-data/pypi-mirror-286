from __future__ import annotations
from dataclasses import dataclass
from enum import Enum

from zeta.db.base import BaseData, ZetaBase


class ZetaUserTier(Enum):
    ANONYMOUS = -1
    FREE = 0
    PRO = 1
    ENTERPRISE = 2
    ADMIN = 42

class ZetaUserRole(Enum):
    NONE = None
    OWNER = "owner"
    EDITOR = "editor"
    VIEWER = "viewer"


@dataclass
class ZetaUserData(BaseData):
    displayName: str
    email: str
    photoURL: str
    tier: ZetaUserTier


class ZetaUser(ZetaBase):
    @property
    def collection_name(cls) -> str:
        return "users"

    @property
    def data_class(self):
        return ZetaUserData

    def _data_from_dict(self, data: dict) -> ZetaUserData:
        super()._data_from_dict(data)
        if self._data and type(self._data.tier) == int:
            self._data.tier = ZetaUserTier(self._data.tier)

    # Disable creating a new user
    #   Unlike ZetaBase, uid must be provided for ZetaUser (i.e. we cannot create a new user).
    #   In reality, the ZetaUser class must be created after user sign up and the UID comes
    #   from the authentication service.
    def _create(self, data) -> bool:
        raise NotImplementedError