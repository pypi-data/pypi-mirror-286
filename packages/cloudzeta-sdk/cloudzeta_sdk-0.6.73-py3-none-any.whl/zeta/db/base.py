from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, fields
from datetime import datetime, timezone
from typing import Callable, List

from google.api_core.exceptions import PermissionDenied
from google.cloud import firestore
from google.cloud.firestore_v1 import DocumentSnapshot

from zeta.sdk.uid import generate_uid
from zeta.utils.logging import zetaLogger


@dataclass
class BaseData:
    """
    The unique identifier for this object.
    """
    uid: str

    """
    The name of this object. May be an empty string
    """
    name: str

    """
    The time this object was created, in ISO8601 format
    """
    createdAt: str

    """
    The time this object was updated, in ISO8601 format
    """
    updatedAt: str

    """
    The time this object was deleted, in ISO8601 format

    May be None if the object has not been deleted.
    """
    deletedAt: str


# Base class for all database classes
# The Typescript version of this file is located: src/engine/db/base.ts
class ZetaBase(ABC):
    _db: firestore.Client = None

    def __init__(self):
        if not ZetaBase._db:
            ZetaBase._db = firestore.Client()

        self._parent: ZetaBase = None
        self._collection: firestore.CollectionReference = None
        self._uid: str = None
        self._ref: firestore.DocumentReference = None
        self._data = None
        self._on_update: Callable[[BaseData], None] = None

    @classmethod
    def set_client(cls, client: firestore.Client):
        cls._db = client

    @classmethod
    def get_by_uid(cls, uid: str) -> ZetaBase:
        thiz = cls()
        thiz._collection = cls._db.collection(thiz.collection_name)
        thiz._uid = uid
        thiz._ref = thiz._collection.document(thiz._uid)
        thiz._data_from_dict(thiz._ref.get().to_dict())
        return thiz

    @classmethod
    def get_by_name(cls, name: str):
        thiz = cls()
        thiz._collection = thiz._db.collection(thiz.collection_name)

        query = thiz._collection.where(filter=firestore.FieldFilter("name", "==", name))
        query_res = query.get()

        if len(query_res) == 0:
            zetaLogger.error(f"document not found for name: {name}")
        elif len(query_res) > 1:
            zetaLogger.error(f"multiple documents found for name: {name}")
        else:
            thiz._uid = query_res[0].id
            thiz._ref = query_res[0].reference
            thiz._data_from_dict(query_res[0].to_dict())

        return thiz

    @classmethod
    def list_with_pagination(cls, page_size, page_token=None) -> list[ZetaBase]:
        dummy = cls()
        collection = cls._db.collection(dummy.collection_name)
        query = collection.order_by("createdAt", direction=firestore.Query.DESCENDING)

        if page_token:
            doc = collection.document(page_token).get()
            if doc.exists:
                query = query.start_after(doc)
            else:
                zetaLogger.error(f"Invalid page token: {page_token}")
                return []

        query = query.limit(page_size)
        docs = query.stream()

        result = []
        for doc in docs:
            thiz = cls()
            thiz._uid = doc.id
            thiz._ref = doc.reference
            try:
                thiz._data_from_dict(doc.to_dict())
            except Exception as e:
                zetaLogger.error(f"Error creating object: {e}, uid={thiz._uid}")
                continue
            result.append(thiz)
        return result

    @property
    @abstractmethod
    def collection_name(self) -> str:
        pass

    @property
    @abstractmethod
    def data_class(self):
        pass

    def _data_from_dict(self, data: dict):
        if data is not None:
            self._data = self.data_class(**self._filter_data(data))

    def _filter_data(self, data: dict):
        field_names = {field.name for field in fields(self.data_class)}
        return {key: value for key, value in data.items() if key in field_names}

    @property
    def valid(self) -> bool:
        return self._ref is not None and self._ref.get().exists and self._data is not None

    @property
    def uid(self) -> str:
        return self._uid

    @property
    def data(self):
        return self._data

    @staticmethod
    def get_current_time() -> str:
        now = datetime.now(timezone.utc)
        return now.strftime("%Y-%m-%dT%H:%M:%SZ")

    def _create(self, data) -> bool:
        # Create a new document with a random uid
        self._uid = generate_uid()
        self._collection = (self._db.collection(self.collection_name) if self._parent is None else
                            self._parent._ref.collection(self.collection_name))
        self._ref = self._collection.document(self._uid)

        if self._ref.get().exists:
            zetaLogger.error("Document already exists")
            return False

        created_at = ZetaBase.get_current_time()
        base_data = {
            "uid": self._uid,
            "name": "",
            "createdAt": created_at,
            "updatedAt": created_at,
            "deletedAt": None,
        }
        extended_data = {}
        extended_data.update(base_data)
        extended_data.update(data)

        # check if the data is missing any required fields
        if len(extended_data) != len(fields(self.data_class)):
            field_names = {field.name for field in fields(self.data_class)}
            missing_keys = set(field_names) - set(extended_data.keys())
            raise ValueError(f"Missing required fields: {missing_keys}")

        self._ref.set(base_data)
        self.update(extended_data)

    @classmethod
    def create(cls, data):
        thiz = cls()
        thiz._create(data)
        return thiz

    def update(self, data):
        data["updatedAt"] = ZetaBase.get_current_time()
        filtered_data = self._filter_data(data)

        if len(filtered_data) != len(data):
            # find the keys that were in data but not in the filtered data
            missing_keys = set(data.keys()) - set(filtered_data.keys())
            zetaLogger.warning(f"Unexpected key(s): {missing_keys}")

        self._ref.update(filtered_data)
        self._data_from_dict(self._ref.get().to_dict())

    def _handle_snapshot(self, doc_snapshot: List[DocumentSnapshot], _1, _2):
        if len(doc_snapshot) != 1:
            raise ValueError("Unexpected number of documents in snapshot")

        doc = doc_snapshot[0]
        # TODO: handle changes
        self._data_from_dict(doc.to_dict())
        self._on_update(self._data)

    def on_update(self, callback: Callable[[BaseData], None]):
        if not self.valid:
            raise ValueError("on_update() called on invalid object")

        self._on_update = callback
        self._ref.on_snapshot(self._handle_snapshot)


class NestedZetaBase(ZetaBase):
    def __init__(self):
        super().__init__()

        self._parent: ZetaBase = None

    @classmethod
    def get_by_uid(cls, uid: str) -> ZetaBase:
        thiz = cls()

        thiz._parent = None
        thiz._collection = thiz._db.collection_group(thiz.collection_name)

        query = thiz._collection.where(filter=firestore.FieldFilter("uid", "==", uid))

        try:
            query_res = query.get()
        except PermissionDenied:
            explain: str = "Permission denied while directly querying nested object by uid."
            raise ValueError(f"{thiz.collection_name}/{uid}: {explain}") from None

        if len(query_res) == 0:
            zetaLogger.error(f"document not found for uid: {uid}")
        elif len(query_res) > 1:
            zetaLogger.error(f"multiple documents found for uid: {uid}")
        else:
            thiz._uid = query_res[0].id
            thiz._ref = query_res[0].reference
            thiz._data_from_dict(query_res[0].to_dict())

        return thiz

    @classmethod
    def get_from_parent_collection(cls, parent: ZetaBase, uid: str):
        thiz = cls()
        thiz._parent = parent
        thiz._collection = thiz._parent._ref.collection(thiz.collection_name)
        thiz._uid = uid
        thiz._ref = thiz._collection.document(thiz._uid)
        thiz._data_from_dict(thiz._ref.get().to_dict())

        return thiz

    @classmethod
    def get_by_name_from_parent_collection(cls, parent: ZetaBase, name: str):
        thiz = cls()
        thiz._parent = parent
        thiz._collection = thiz._parent._ref.collection(thiz.collection_name)

        query = thiz._collection.where(filter=firestore.FieldFilter("name", "==", name))
        query_res = query.get()

        if len(query_res) == 0:
            zetaLogger.error(f"document not found for name: {name}")
        elif len(query_res) > 1:
            zetaLogger.error(f"multiple documents found for name: {name}")
        else:
            thiz._uid = query_res[0].id
            thiz._ref = query_res[0].reference
            thiz._data_from_dict(query_res[0].to_dict())

        return thiz

    @classmethod
    def create_in_parent(cls, parent: ZetaBase, data):
        thiz = cls()
        thiz._parent = parent
        thiz._create(data)
        return thiz