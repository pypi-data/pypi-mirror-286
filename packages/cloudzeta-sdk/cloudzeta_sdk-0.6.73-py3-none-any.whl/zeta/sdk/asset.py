from __future__ import annotations
from enum import Enum
import os
import requests


class ZetaUploadResult(object):
    class Status(Enum):
        INVALID = 0
        PENDING = 1
        SUCCESS = 2
        FAILURE = 3

    def __init__(self):
        self.status: ZetaUploadResult.Status = ZetaUploadResult.Status.INVALID
        self.asset_path: str = None
        self.blob_path: str = None
        self.asset_url: str = None
        self.editor_url: str = None
        self.player_url: str = None
        self._error: str = None

    def __str__(self):
        if self.success:
            return "success"
        elif self.error:
            return f"error: {self.error}"
        else:
            return "pending"

    @property
    def success(self) -> bool:
        return self.status == ZetaUploadResult.Status.SUCCESS

    def set_success(self):
        self.status = ZetaUploadResult.Status.SUCCESS
        return self

    @property
    def error(self) -> str:
        return self._error

    def set_error(self, message: str) -> ZetaUploadResult:
        self._error = message
        self.status = ZetaUploadResult.Status.FAILURE
        return self


class AssetUtils(object):
    @staticmethod
    def is_image_asset(asset_path: str) -> bool:
        _, ext = os.path.splitext(asset_path)
        return ext.lower() in [".png", ".jpg", ".jpeg"]

    @staticmethod
    def is_fbx_asset(asset_path: str) -> bool:
        _, ext = os.path.splitext(asset_path)
        return ext.lower() == ".fbx"

    @staticmethod
    def is_gltf_asset(asset_path: str) -> bool:
        _, ext = os.path.splitext(asset_path)
        return ext.lower() in [".glb", ".gltf"]

    @staticmethod
    def is_obj_asset(asset_path: str) -> bool:
        _, ext = os.path.splitext(asset_path)
        return ext.lower() == ".obj"

    @staticmethod
    def is_usd_asset(asset_path: str) -> bool:
        _, ext = os.path.splitext(asset_path)
        return ext.lower() in [".usd", ".usda", ".usdc", ".usdz", ".zeta"]

    @staticmethod
    def is_usdz_asset(asset_path: str) -> bool:
        _, ext = os.path.splitext(asset_path)
        return ext.lower() == ".usdz"

    @staticmethod
    def is_unpacked_usd_asset(asset_path: str) -> bool:
        _, ext = os.path.splitext(asset_path)
        return ext.lower() in [".usd", ".usda", ".usdc"]

    @staticmethod
    def is_editable_asset(asset_path: str) -> bool:
        return (AssetUtils.is_fbx_asset(asset_path) or
                AssetUtils.is_gltf_asset(asset_path) or
                AssetUtils.is_obj_asset(asset_path) or
                AssetUtils.is_usd_asset(asset_path))

    @staticmethod
    def is_external_asset(asset_path: str) -> bool:
        return (AssetUtils.is_fbx_asset(asset_path) or
                AssetUtils.is_gltf_asset(asset_path) or
                AssetUtils.is_obj_asset(asset_path))

    @staticmethod
    def get_all_parent_paths(asset_path: str) -> set[str]:
        current_path = asset_path
        asset_prefix = set()

        while current_path:
            asset_prefix.add(current_path)
            if current_path == "/":
                break
            else:
                current_path = os.path.dirname(current_path)

        return asset_prefix

    @staticmethod
    def is_asset_file_valid(asset_path) -> bool:
        if not asset_path:
            return False
        if not isinstance(asset_path, str):
            return False
        if not os.path.exists(asset_path):
            return False
        if not os.path.isfile(asset_path):
            return False
        if os.path.getsize(asset_path) == 0:
            return False

        return True


class ZetaAsset(object):
    def __init__(self, engine, owner_name: str, project_name: str, asset_path: str):
        """
        @param owner_name: The owner_name of the project. Note that the owner can be different than
            the current user, as long as the current user has the permission to upload.
        @param project_name: The project_name to upload the asset to.
        @param asset_path: The path to the asset to upload, relative to the project root. A leading
            "/" for the path is not required and will be ignored.

        """
        self._engine = engine
        self._owner_name = owner_name
        self._project_name = project_name
        self._asset_path = asset_path if asset_path.startswith("/") else f"/{asset_path}"
        self._result = ZetaUploadResult()

    def upload(self, data) -> ZetaUploadResult:
        """
        Upload the asset to the asset. The server will validate:
        1. The traget project exists
        2. The user has the permission to upload the asset
        3. There is no asset with the same name in the project

        @param data: The data to upload.

        @return: The signed URL to the uploaded asset.

        Zeta URL schema: https://cloudzeta.com/<owner_name>/<project_name>/asset/main/<asset_path>

        Example: https://cloudzeta.com/zeta/public-demo/asset/main/zeta-logo.usd
            owner_name: zeta
            project_name: public-demo
            asset_path: zeta-logo.usd
        """
        response = self._engine.api_post("/api/asset/upload", json={
            "ownerName": self._owner_name,
            "projectName": self._project_name,
            "assetPath": self._asset_path
        })
        if not response.ok:
            return self._result.set_error(response.json().get("error"))

        self._result.asset_path = self._asset_path
        self._result.blob_path = response.json().get("blobPath")
        signed_url = response.json().get("signedUrl")

        try:
            if not signed_url:
                return self._result.set_error("Failed to get signed URL")

            headers = {
                "Content-Disposition": f"attachment; filename={os.path.basename(self._asset_path)}",
            }
            response = requests.put(signed_url, headers=headers, data=data)
            if not response.ok:
                return self._result.set_error(response.json().get("error"))
        except Exception as e:
            return self._result.set_error(f"Unexpected error when uploading asset: {e}")

        self._result.asset_url = self._engine.make_url(self._owner_name,
                                                       self._project_name,
                                                       "asset",
                                                       "main",
                                                       self._asset_path)
        return self._result.set_success()

    def create_session(self):
        if not self._result.success:
            self._result.set_error("No successful upload, cannot create session")
            return self._result

        response = self._engine.api_post("/api/asset/create_session", json={
            "ownerName": self._owner_name,
            "projectName": self._project_name,
            "assetPath": self._asset_path
        })
        if not response.ok:
            return self._result.set_error(response.json().get("error"))

        session_uid = response.json().get("sessionUid")
        if not session_uid:
            return self._result.set_error("Failed to get session UID")

        # Trigger USD conversion if the asset is editable, but not yet unpacked.
        if (AssetUtils.is_editable_asset(self._asset_path) and
            not AssetUtils.is_unpacked_usd_asset(self._asset_path)):
            self._engine.api_get("/api/usd/convert", params={
                "session": session_uid,
            })

        self._result.editor_url = self._engine.make_url(self._owner_name,
                                                        self._project_name,
                                                        "session",
                                                        session_uid,
                                                        self._asset_path)
        self._result.player_url = self._engine.make_url("player", session_uid)
        return self._result.set_success()