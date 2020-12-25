import gi.repository
import subprocess
from settings import ScriptSettings

gi.require_version("Budgie", "1.0")
gi.require_version("Gtk", "3.0")
from gi.repository import Budgie, GObject, Gtk  # noqa: E402


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
        self.button = Gtk.Button.new()
        self.button.set_relief(Gtk.ReliefStyle.NONE)
        self.add(self.button)
        self.show_all()

        self.settings = ScriptSettings(uuid, on_changed=self.schedule)

        # schedule execution
        self.schedule()

    def schedule(self):

        # cancel currrent job
        if self.job_id:
            GObject.source_remove(self.job_id)

        # run once on start
        self.update()

        # schedule to run every <interval> seconds
        interval = self.settings.load()["interval"]
        self.job_id = GObject.timeout_add_seconds(interval, self.update)

    def update(self):

        # load command for this script from settings
        command = self.settings.load()["command"]
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
        return self.settings.create_ui()
