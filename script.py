import gi.repository
import subprocess
from settings_ui import SettingsBox
import settings

gi.require_version("Budgie", "1.0")
gi.require_version("Gtk", "3.0")
from gi.repository import Budgie, GObject, Gtk, GLib  # noqa: E402


class BudgieScript(GObject.GObject, Budgie.Plugin):

    # set unique id for this plugin
    __gtype_name__ = "BudgieScript"

    def do_get_panel_widget(self, uuid):
        return BudgieScriptApplet(uuid)  # an instance of Budgie.Applet


class BudgieScriptApplet(Budgie.Applet):
    def __init__(self, uuid):
        Budgie.Applet.__init__(self)

        self.uuid = uuid
        self.job_id = None

        # widget UI
        self.button = Gtk.Button.new_with_label("")
        self.button.set_relief(Gtk.ReliefStyle.NONE)
        self.button.get_style_context().add_class("budgie-script")
        self.button.set_name(f"{self.uuid[:8]}")
        self.add(self.button)
        self.show_all()

        # schedule execution
        self.schedule()

    def schedule(self):

        # cancel currrent job
        if self.job_id:
            GObject.source_remove(self.job_id)

        # run once on start
        self.update()

        # schedule to run every <interval> seconds
        interval = settings.load(self.uuid)["interval"]
        self.job_id = GLib.timeout_add_seconds(interval, self.update)

    def update(self):

        # load command for this script from settings
        command = settings.load(self.uuid)["command"]
        stdout = self.run(command)

        self.button.set_label(stdout)
        return True

    def run(self, command):

        # run given command with shell
        result = subprocess.run(command,
                                shell=True,
                                stdout=subprocess.PIPE,
                                text=True)
        return result.stdout.strip()

    def do_supports_settings(self):
        return True

    def do_get_settings_ui(self):
        initial_values = settings.load(self.uuid)
        return SettingsBox(self.uuid, initial_values, self.on_settings_changed)

    def on_settings_changed(self, new_settings):
        settings.save(self.uuid, new_settings)
        self.schedule()


if __name__ == "__main__":
    applet = BudgieScriptApplet("test-uuid")
    win = Gtk.Window()
    win.connect("destroy", Gtk.main_quit)
    win.add(applet)
    win.show_all()
    Gtk.main()
