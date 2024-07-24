from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
import os

from pxr import Sdf, Usd, Tf

from zeta.db.base import ZetaBase, BaseData
from zeta.db.layer import ZetaLayer
from zeta.db.project import ZetaProject
from zeta.db.user import ZetaUser
from zeta.usd.resolve import ResolverContext
from zeta.utils.downloader import AssetDownloader
from zeta.utils.logging import zetaLogger


class ZetaSessionState(Enum):
    """
    The state of the session
    """
    INIT = "init"
    PROCESSING = "processing"
    READY = "ready"
    ERROR = "error"


@dataclass
class ZetaSessionData(BaseData):
    projectUid: str
    rootAssetPath: str
    externalAssetPath: str
    assetPrefix: list[str]

    # If true, the session will be public and readable to all registered users.
    isPublic: bool

    # If true, the session will be published the the Internet and readable to all users who have
    # a link to the session.
    isPublished: bool

    # Ephemeral sessions do not need a registered user to create.
    #
    # If true, the session will be automatically deleted in a certain period of time after it
    # becomes inactive.
    isEphemeral: bool

    roles: dict[str, str]
    state: ZetaSessionState;

    annotationLayerUid: str;
    editLayerUid: str;

    error: str;
    thumbnailAsset: str;
    usdzAssetPath: str;


class ZetaSession(ZetaBase):
    def __init__(self):
        super().__init__()

        self._stage: Usd.Stage = None

        self._workspace: str = None
        self._owner: ZetaUser = None
        self._project: ZetaProject = None
        self._resolver_context: ResolverContext = None
        self._edit_layer: ZetaLayer = None

    @property
    def collection_name(cls) -> str:
        return "sessions"

    @property
    def data_class(self):
        return ZetaSessionData

    @property
    def stage(self) -> Usd.Stage:
        return self._stage

    @property
    def root_asset_blobname(self) -> str:
        # Note that we can't use os.path.join here because root_asset_path is an absolute path.
        return os.path.normpath(f"{self._project.data.storagePath}/{self._data.rootAssetPath}")

    @property
    def owner_uid(self) -> str:
        owners = [uid for uid, role in self._data.roles.items() if role == "owner"]
        if len(owners) == 0:
            raise ValueError("Owner not found")
        if len(owners) > 1:
            raise ValueError("Multiple owners found")
        return owners[0]

    def _data_from_dict(self, data: dict):
        super()._data_from_dict(data)

        if self._data and type(self._data.state) == str:
            self._data.state = ZetaSessionState(self._data.state)

    def _push_edit_layer_updates(self, *args):
        self._edit_layer.push_updates()

    def load_stage(self, workspace: str) -> Usd.Stage:
        """
        Load the session into an OpenUSD stage.

        @param workspace: The workspace directory where the asssets will be downloaded.
        """
        if self._stage is not None:
            zetaLogger.warning("Session already loaded")
            return self._stage

        self._workspace = workspace
        self._owner = ZetaUser.get_by_uid(self.owner_uid)
        self._project = ZetaProject.get_from_parent_collection(self._owner, self._data.projectUid)

        root_dir: str = os.path.dirname(self.root_asset_blobname)
        self._resolver_context = ResolverContext(root_dir, self._workspace)
        self._edit_layer = ZetaLayer.get_from_parent_collection(self, self._data.editLayerUid)

        if self._edit_layer is None:
            raise ValueError("Edit layer is not found")

        self._edit_layer.load_layer()
        if self._edit_layer.layer is None:
            raise ValueError("Edit layer is not loaded")

        root_asset_filename: str = AssetDownloader.download_asset(self.root_asset_blobname,
                                                                  self._workspace)

        self._stage = Usd.Stage.Open(root_asset_filename, self._resolver_context)
        if self._stage is None:
            raise ValueError("Stage is not loaded")

        session_layer: Sdf.Layer = self._stage.GetSessionLayer()
        if session_layer is None:
            raise ValueError("Session layer is not found")

        session_layer.subLayerPaths.append(self._edit_layer.layer.identifier)
        self._stage.SetEditTarget(self._edit_layer.layer)

        self._listener = Tf.Notice.Register(
            Usd.Notice.StageContentsChanged,
            self._push_edit_layer_updates,
            self._stage)

        return self._stage