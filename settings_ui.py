import gi.repository

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk  # noqa: E402


class SettingsBox(Gtk.Box):

    def __init__(self, uuid, initial, on_changed):
        super().__init__(spacing=10,
                         orientation=Gtk.Orientation.VERTICAL)

        self._on_changed = on_changed

        # id
        id_label = Gtk.Label(
            label=f"CSS Selector: .budgie-script#{uuid[:8]}",
            hexpand=True, halign=Gtk.Align.START,
            selectable=True)
        id_label.set_use_markup = True
        self.add(id_label)

        # command
        command_line1 = Gtk.Label(label="Command",
                                  hexpand=True,
                                  halign=Gtk.Align.START,
                                  margin_top=10)
        self.add(command_line1)

        self.command_input = Gtk.Entry(text=initial["command"])
        self.add(self.command_input)

        # interval
        interval_line1 = Gtk.Label(label="Interval",
                                   hexpand=True,
                                   halign=Gtk.Align.START,
                                   margin_top=10)
        self.add(interval_line1)

        interval_line2 = Gtk.Box(spacing=6)
        interval_adjustment = Gtk.Adjustment(
            value=initial["interval"], lower=1, upper=3600, step_increment=1)
        self.interval_input = Gtk.SpinButton(
            numeric=True,
            adjustment=interval_adjustment
        )
        interval_seconds = Gtk.Label(label="seconds",
                                     hexpand=True,
                                     halign=Gtk.Align.START)
        interval_line2.add(self.interval_input)
        interval_line2.add(interval_seconds)
        self.add(interval_line2)

        # save button
        save_button = Gtk.Button.new_with_label("Save")
        save_button.set_hexpand = True
        save_button.set_margin_top = 10
        save_button.connect("clicked", self.on_save_clicked)
        self.add(save_button)

        self.show_all()

    def on_save_clicked(self, box):
        new = {
            "command": self.command_input.get_text(),
            "interval": self.interval_input.get_value_as_int(),
        }
        self._on_changed(new)


if __name__ == "__main__":
    settings = SettingsBox(
        "testid",
        {"command": "echo testing", "interval": 60},
        lambda x: print(x))
    win = Gtk.Window()
    win.connect("destroy", Gtk.main_quit)
    win.add(settings)
    win.show_all()
    Gtk.main()
