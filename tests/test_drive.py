import sys
import pathlib
import types
import os

sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

from src.app.utils import drive


class FakeFiles:
    def __init__(self):
        self._created = []

    def list(self, q=None, spaces=None, fields=None):
        class Exec:
            def execute(self_non):
                return {"files": []}

        return Exec()

    def create(self, body=None, media_body=None, fields=None):
        class Exec:
            def execute(self_non):
                return {"id": "fake-file-id", "webViewLink": "https://drive.fake/view"}

        return Exec()


class FakeService:
    def files(self):
        return FakeFiles()


def test_upload_file_monkeypatched(tmp_path, monkeypatch):
    # create a temp file
    f = tmp_path / "sample.txt"
    f.write_text("hello")

    # patch get_drive_service to avoid real network calls
    monkeypatch.setattr(drive, "get_drive_service", lambda: FakeService())

    # stub googleapiclient.http.MediaFileUpload if not installed
    import sys as _sys

    if "googleapiclient.http" not in _sys.modules:
        mod = types.ModuleType("googleapiclient.http")
        mod.MediaFileUpload = lambda *a, **k: "MEDIA"
        _sys.modules["googleapiclient.http"] = mod

    file_id = drive.upload_file(str(f))
    assert file_id == "fake-file-id"
