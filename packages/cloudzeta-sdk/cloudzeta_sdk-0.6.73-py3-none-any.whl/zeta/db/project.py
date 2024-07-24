from zeta.db.base import BaseData, NestedZetaBase
from dataclasses import dataclass


@dataclass
class ZetaProjectData(BaseData):
    storagePath: str

    isPublic: bool
    isPublished: bool
    roles: dict[str, str]

class ZetaProject(NestedZetaBase):
    @property
    def collection_name(self) -> str:
        return "projects"

    @property
    def data_class(self):
        return ZetaProjectData
