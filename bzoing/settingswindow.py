import os

import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk


AUTOSTART_PATH = os.path.expanduser('~/.config/autostart/bzoing.desktop')

DESKTOP_FILE = '''[Desktop Entry]
Type=Application
Name=Bzoing
Comment=Calendar alarms for your desktop
Exec=bzoing
Terminal=false
X-GNOME-Autostart-enabled=true
'''


def autostart_enabled():
    return os.path.exists(AUTOSTART_PATH)


def set_autostart(enabled):
    if enabled:
        os.makedirs(os.path.dirname(AUTOSTART_PATH), exist_ok=True)
        with open(AUTOSTART_PATH, 'w') as f:
            f.write(DESKTOP_FILE)
    else:
        try:
            os.remove(AUTOSTART_PATH)
        except OSError:
            pass


class SettingsWindow(Gtk.Window):
    def __init__(self, application):
        Gtk.Window.__init__(self, application=application, title='Settings')
        self.connect('destroy', self.quit_window)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        box.set_margin_top(10)
        box.set_margin_bottom(10)
        box.set_margin_start(10)
        box.set_margin_end(10)

        row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        label = Gtk.Label(label='Start Bzoing on login')
        self.autostart_switch = Gtk.Switch(active=autostart_enabled())
        self.autostart_switch.connect('state-set', self.on_autostart_toggled)
        row.append(label)
        row.append(self.autostart_switch)
        box.append(row)

        self.set_child(box)

    def on_autostart_toggled(self, switch, state):
        set_autostart(bool(state))
        return False

    def quit_window(self, window):
        self.destroy()