from appdirs import AppDirs
from pathlib import Path
import json

_appdirs = AppDirs(appname="budgie_script", appauthor="wsck")

_directory = Path(_appdirs.user_config_dir)
_filename = "budgie_script.json"
_path = _directory / _filename

_default = {
    "command": "echo script not set",
    "interval": 60,
    "onclick": "xdg-open https://github.com/shymmq/budgie-script-applet"
}

_directory.mkdir(parents=True, exist_ok=True)
if not _path.exists():
    _path.write_text("{}")
    print(f"Created new budgie-script-applet config file at {_path}")


def _load_all():
    return json.loads(_path.read_text())


def load(uuid):
    return _load_all().get(uuid, _default)


def save(uuid, new):
    all = _load_all()
    all[uuid] = new
    _path.write_text(json.dumps(all))
