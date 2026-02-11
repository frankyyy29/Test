import os
from typing import Optional


def _load_service_account_credentials():
    try:
        # Import lazily so tests that don't use Drive won't require the package
        from google.oauth2 import service_account
    except Exception as exc:  # pragma: no cover - import guard
        raise RuntimeError("google auth packages are required for Drive integration") from exc

    keyfile = os.environ.get("GOOGLE_SERVICE_ACCOUNT_FILE")
    keyjson = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")

    if keyfile:
        return service_account.Credentials.from_service_account_file(keyfile, scopes=[
            "https://www.googleapis.com/auth/drive.file",
        ])
    if keyjson:
        import json

        info = json.loads(keyjson)
        return service_account.Credentials.from_service_account_info(info, scopes=[
            "https://www.googleapis.com/auth/drive.file",
        ])

    raise RuntimeError(
        "No Google service account credentials found. Set GOOGLE_SERVICE_ACCOUNT_FILE or GOOGLE_SERVICE_ACCOUNT_JSON"
    )


def get_drive_service():
    """Return an authorized Drive v3 service instance.

    Uses a service account specified by `GOOGLE_SERVICE_ACCOUNT_FILE` (path) or
    `GOOGLE_SERVICE_ACCOUNT_JSON` (JSON content).
    """
    creds = _load_service_account_credentials()
    try:
        from googleapiclient.discovery import build
    except Exception as exc:  # pragma: no cover - import guard
        raise RuntimeError("google-api-python-client is required for Drive integration") from exc

    return build("drive", "v3", credentials=creds)


def ensure_folder(service, name: str, parent: Optional[str] = None) -> str:
    """Find or create a Drive folder with the given name. Returns folder id."""
    # search for folder
    q = f"name = '{name.replace('"', "\\\"")}' and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
    if parent:
        q += f" and '{parent}' in parents"

    resp = service.files().list(q=q, spaces="drive", fields="files(id,name)").execute()
    files = resp.get("files", [])
    if files:
        return files[0]["id"]

    metadata = {"name": name, "mimeType": "application/vnd.google-apps.folder"}
    if parent:
        metadata["parents"] = [parent]

    created = service.files().create(body=metadata, fields="id").execute()
    return created.get("id")


def upload_file(file_path: str, parent: Optional[str] = None, mime_type: Optional[str] = None) -> str:
    """Upload a local file to Drive. Returns created file id.

    Environment:
      - GOOGLE_SERVICE_ACCOUNT_FILE or GOOGLE_SERVICE_ACCOUNT_JSON
    Optional parent: Drive folder id where the file will be stored.
    """
    service = get_drive_service()

    file_metadata = {"name": os.path.basename(file_path)}
    if parent:
        file_metadata["parents"] = [parent]

    try:
        from googleapiclient.http import MediaFileUpload
    except Exception as exc:  # pragma: no cover - import guard
        raise RuntimeError("google-api-python-client is required for Drive integration") from exc

    media = MediaFileUpload(file_path, mimetype=mime_type or "application/octet-stream", resumable=True)
    created = service.files().create(body=file_metadata, media_body=media, fields="id,webViewLink").execute()
    return created.get("id")
