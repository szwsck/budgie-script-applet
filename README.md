# budgie-script-applet
A simple, but very versatile Budgie applet that periodically runs a script and displays its output.
It makes it very easy to implement your own indicator-style applets with your favorite language.
Inspired by [Polybar](https://github.com/polybar/polybar)'s script module.

**Note:** for most purposes, this applet's functionality is a subset of [indicator-sysmonitor](https://github.com/fossfreedom/indicator-sysmonitor). It has, however, some advantages:
 - each script is a separate applet, meaning you can place them in different places in the panel
 - each applet can be themed independently using CSS
 - (planned) support for native system icon(s) inside the applet
 - (planned) support for click/scroll actions
 - (planned) custom tooltip text

## Installation
```bash
mkdir -p ~/.local/share/budgie-desktop/plugins
cd ~/.local/share/budgie-desktop/plugins
git clone https://github.com/shymmq/budgie-script-applet.git
```
## Usage
After you add the widget to the panel, you should configure it inside Budgie Desktop Settings. Make sure your script is executable(`chmod +x script.sh`) and prints a single line of text.

**Warning:** This applet naively runs whatever command you set, without any constraints, timeouts or caching. Don't execute any expensive operations; if you make network calls, it's probably a good idea to cache the result inside your script.

For simple monochrome icons, you can use an icon font such as [MaterialDesign-Font](https://github.com/Templarian/MaterialDesign-Font). Their size almost matches the system action icon size, so they actually fit very well into other panel icons.

## Theming
You can modify the look of the applet through CSS attributes in `~/.config/gtk-3.0/gtk.css`. All widgets share the class `.budgie-script` and each script has its unique ID that you can find in the settings.

Some examples:
```css
/* change font of single widget's label */
.budgie-script#41012c76 label {
	font-family: Fantasque Sans Mono;
}
/* make all widgets from the right side of panel highlight on mouse hover */
.end-region .budgie-script:hover{
    background-color: rgba(255,255,255,0.3)
}
```
## Ideas
 - Display next event from Google Calendar. See [i3-agenda](https://github.com/rosenpin/i3-agenda)

![image](https://user-images.githubusercontent.com/8517017/103033712-609e5480-4563-11eb-8976-92e4ed986880.png)

- Display current CPU/Disk/RAM usage
- Check available package updates
- Display unread notifications from Reddit, Facebook etc.
- Display currently playing song title