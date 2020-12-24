import gi.repository

from appdirs import AppDirs
from pathlib import Path
import os
import json

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk  # noqa: E402

_appdirs = AppDirs(appname="budgie_script", appauthor="wsck")

_directory = _appdirs.user_config_dir
_filename = "budgie_scripts.json"
_path = os.path.join(_directory, _filename)

_default = {"command": "date +%H:%M:%S", "interval": 1}


class ScriptSettings:

    def __init__(self, uuid, on_changed):
        self._uuid = uuid
        self._callback = on_changed

    # =====================================
    # Saved settings manipulation

    def _load_all(self):

        if not os.path.exists(_path):
            print("Settings file doesn't exist")
            return {}

        with open(_path, "r") as file:
            all = json.load(file)

        return all

    def load(self):

        all = self._load_all()
        return all.get(self._uuid, _default)

    def save(self, box):

        new = {
            "command": self.cmd_input.get_text(),
            "interval": self.interval_input.get_value_as_int()
        }

        all = self._load_all()
        all[self._uuid] = new

        Path(_directory).mkdir(parents=True, exist_ok=True)

        with open(_path, "w") as file:
            json.dump(all, file)

        self._callback()

    # =====================================
    # UI methods

    def create_ui(self):

        current = self.load()

        # command

        label1 = Gtk.Label(
            label="Command",
            can_focus=False,
            halign=Gtk.Align.START,
            hexpand=True
        )
        self.cmd_input = Gtk.Entry(
            text=current['command'],
            can_focus=True,
            halign=Gtk.Align.END
        )

        option1 = Gtk.Box(spacing=6)
        option1.add(label1)
        option1.add(self.cmd_input)

        # interval
        label2 = Gtk.Label(
            label="Interval",
            can_focus=False,
            halign=Gtk.Align.START,
            hexpand=True
        )
        adjustment = Gtk.Adjustment(
            lower=1,
            upper=3600,
            step_increment=1,
            page_increment=60,
            value=current["interval"],
        )
        self.interval_input = Gtk.SpinButton(
            numeric=True,
            adjustment=adjustment,
            can_focus=True,
            halign=Gtk.Align.END
        )

        label3 = Gtk.Label(
            label="seconds",
            can_focus=False,
            halign=Gtk.Align.END,
            hexpand=True
        )

        option2 = Gtk.Box(spacing=6)
        option2.add(label2)
        option2.add(self.interval_input)
        option2.add(label3)

        # save button
        save_button = Gtk.Button.new_with_label("Save")
        save_button.connect("clicked", self.save)

        settings_ui = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=10
        )
        settings_ui.add(option1)
        settings_ui.add(option2)
        settings_ui.add(save_button)

        option1.show_all()
        option2.show_all()
        settings_ui.show_all()

        return settings_ui
