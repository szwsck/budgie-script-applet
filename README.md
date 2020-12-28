# budgie-script-applet
A simple, but very versatile Budgie applet that periodically runs a script and displays its output.
It makes it very easy to implement your own indicator-style applets with your favorite language.
Inspired by [Polybar](https://github.com/polybar/polybar)'s script module.

**Note:** for most purposes, this applet's functionality is a subset of [indicator-sysmonitor](https://github.com/fossfreedom/indicator-sysmonitor). It has, however, some advantages:
 - many more theming options using CSS - support for setting styles either globally or dynamically through script's output
 - each script is a separate applet, meaning you can place them in different places in the panel and style them separately
 - custom tooltip text support
 - (planned) support for native system icon(s) inside the applet
 - (planned) support for click/scroll actions

## Installation
```bash
mkdir -p ~/.local/share/budgie-desktop/plugins
cd ~/.local/share/budgie-desktop/plugins
git clone https://github.com/shymmq/budgie-script-applet.git
```
## Usage
After you add the widget to the panel, you should configure it inside Budgie Desktop Settings. Make sure your script is executable(`chmod +x script.sh`).

Only the first line of the output will be displayed. In the following lines, you can pass any CSS properties [supported by GTK](https://developer.gnome.org/gtk3/stable/chap-css-properties.html). You can also set tooltip text with `tooltip: <tooltip>`

For example, this script:
```shell
$ python ~/events.py
No events
color: green
font-style: italic
tooltip: Next event: Meeting tomorrow at 9:00
```
will result in:

![image](https://user-images.githubusercontent.com/8517017/103217110-12e56b80-4918-11eb-827f-bde5590489c7.png)

You can run budgie-panel with `budgie-panel --replace --gtk-debug=interactive &` to preview your CSS props in a live editor.

If you want to set a global theme, you can do so in `~/.config/gtk-3.0/gtk.css`. You can find the CSS selector for the given widget in settings. Note that this doesn't support tooltips. Use `nohup budgie-panel --replace &` to reset the panel after making changes.

For simple monochrome icons, you can use an icon font such as [MaterialDesign-Font](https://github.com/Templarian/MaterialDesign-Font)

**Warning:** This applet naively runs whatever command you set, without any constraints, timeouts or caching. Don't execute any expensive operations; if you make network calls, it's probably a good idea to cache the result inside your script.

## Ideas
 - Display next event from Google Calendar. See [i3-agenda](https://github.com/rosenpin/i3-agenda)

![image](https://user-images.githubusercontent.com/8517017/103033712-609e5480-4563-11eb-8976-92e4ed986880.png)

- Most of [polybar-scripts](https://github.com/polybar/polybar-scripts) should work out of the box
- Display current CPU/Disk/RAM usage
- Check available package updates
- Display unread notifications from Reddit, Facebook etc.
- Display currently playing song title
