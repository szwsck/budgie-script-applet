import gi.repository
import subprocess
from settings_ui import SettingsBox
import settings


gi.require_version("Budgie", "1.0")
gi.require_version("Gtk", "3.0")
from gi.repository import Budgie, GObject, Gtk, GLib  # noqa: E402


def run(command):

    # run given command with shell
    output = subprocess.run(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        text=True
    ).stdout.rstrip("\n")

    return output


def parse_output(output):
    (label, _, props) = output.partition("\n")
    if(props):
        css = parse_css(f"label {{ {props} }}")
    else:
        css = None
    return (label, css)


def parse_css(css_str):
    css_provider = Gtk.CssProvider()
    css_provider.load_from_data(css_str.encode())
    return css_provider


STYLE_DEFAULT = parse_css("label{padding:0px 16px;}")


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
        self.custom_css = None
        # widget UI

        self.label = Gtk.Label(
            label="",                   # content
            name="self.uuid[:8]",       # css ID
        )

        self.label.set_name(f"{self.uuid[:8]}")
        self.label.get_style_context().add_class("budgie-script")

        # set default style with lower priority than custom css
        self.label.get_style_context().add_provider(
            STYLE_DEFAULT, Gtk.STYLE_PROVIDER_PRIORITY_USER - 1)

        self.add(self.label)
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
        # remove custom css if present
        if(self.custom_css):
            self.label.get_style_context().remove_provider(self.custom_css)
        try:
            (label_text, self.custom_css) = parse_output(run(command))
        except GLib.Error as e:
            print(e)
            (label_text, self.custom_css) = parse_output(
                "err: bad CSS\ncolor:red;")
        if(self.custom_css):
            self.label.get_style_context().add_provider(
                self.custom_css,
                Gtk.STYLE_PROVIDER_PRIORITY_USER)
        self.label.set_label(label_text)
        return True

    def do_supports_settings(self):
        return True

    def do_get_settings_ui(self):
        initial_values = settings.load(self.uuid)
        return SettingsBox(self.uuid, initial_values, self.on_settings_changed)

    def on_settings_changed(self, new_settings):
        settings.save(self.uuid, new_settings)
        self.schedule()


if __name__ == "__main__":
    test_command = "python ~/scripts/test.py"
    settings.save("test-uuid", {"command": test_command, "interval": 1})
    applet = BudgieScriptApplet("test-uuid")
    win = Gtk.Window()
    win.connect("destroy", Gtk.main_quit)
    win.add(applet)
    win.show_all()
    Gtk.main()
