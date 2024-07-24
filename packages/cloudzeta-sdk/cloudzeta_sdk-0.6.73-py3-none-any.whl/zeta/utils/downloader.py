from google.cloud import storage
import os
import requests

from zeta.usd.resolve import AssetFetcher
from zeta.utils.logging import zetaLogger


class AssetDownloader(object):
    _engine = None
    _fetcher = AssetFetcher.GetInstance()
    _bucket_name = "gozeta-prod.appspot.com"
    _storage_client = None
    _bucket = None

    @classmethod
    def set_engine(cls, engine):
        cls._engine = engine

    @classmethod
    def download_asset(cls, asset_blobname: str, temp_path: str):
        if cls._engine is not None:
            return cls._download_asset_via_zeta_engine(asset_blobname, temp_path)
        else:
            return cls._download_asset_via_google_storage(asset_blobname, temp_path)

    @classmethod
    def _download_asset_via_zeta_engine(cls, asset_blobname: str, temp_path: str):
        response = cls._engine.api_post("/api/asset/download", json={
            "blobName": asset_blobname
        })
        if not response.ok:
            error = response.json().get("error")
            zetaLogger.error(f"failed to download asset '{asset_blobname}': {error}")
            return ""

        signed_url = response.json().get("signedUrl")
        if not signed_url:
            zetaLogger.error(f"failed to get signed url for asset '{asset_blobname}'")
            return ""

        asset_filename: str = os.path.join(temp_path, asset_blobname)
        asset_dirname: str = os.path.dirname(asset_filename)
        if not os.path.exists(asset_dirname):
            os.makedirs(asset_dirname)

        try:
            with requests.get(signed_url, stream=True) as r:
                r.raise_for_status()
                with open(asset_filename, "wb") as f:
                    # Write the response content to the file in 64K chunks
                    for chunk in r.iter_content(chunk_size=65536):
                        f.write(chunk)
        except Exception as e:
            zetaLogger.error(f"failed to download asset '{asset_blobname}': {e}")
            return ""

        return asset_filename

    @classmethod
    def _download_asset_via_google_storage(cls, asset_blobname: str, temp_path: str):
        if cls._storage_client is None or cls._bucket is None:
            cls._storage_client = storage.Client()
            cls._bucket = cls._storage_client.get_bucket(cls._bucket_name)

        asset_blob = cls._bucket.blob(asset_blobname)
        if not asset_blob.exists():
            zetaLogger.warning(f"asset '{asset_blobname}' does not exist")
            return ""

        asset_filename: str = os.path.join(temp_path, asset_blobname)
        asset_dirname: str = os.path.dirname(asset_filename)
        if not os.path.exists(asset_dirname):
            os.makedirs(asset_dirname)
        asset_blob.download_to_filename(asset_filename)

        return asset_filename


# Register the asset downloader callback. Note that we have to let the AssetDownloader class down
# the PyObject (i.e. AssetFetcher), so that destructor can be called in a proper order.
AssetDownloader._fetcher.SetOnFetchCallback(AssetDownloader.download_asset)