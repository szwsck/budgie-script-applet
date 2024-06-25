from platformdirs import *
from pathlib import Path
import json

_directory = Path(user_config_dir("budgie_script"))
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
