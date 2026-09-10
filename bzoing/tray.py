#!/usr/bin/env python3

import os

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AyatanaAppIndicator3', '0.1')
from gi.repository import Gtk, Gio, GLib
from gi.repository import AyatanaAppIndicator3 as appindicator


APPLICATION_ID = 'com.gatochalupa.bzoing'
OBJECT_PATH = '/' + APPLICATION_ID.replace('.', '/')
APPINDICATOR_ID = 'bzoing'


class BzoingTray:
    def __init__(self):
        icon = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            'images', 'sinoamarelo.svg')
        self.indicator = appindicator.Indicator.new(
            APPINDICATOR_ID,
            os.path.abspath(icon),
            appindicator.IndicatorCategory.APPLICATION_STATUS)
        self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.build_menu())
        self._proxy = None

    def build_menu(self):
        menu = Gtk.Menu()
        menu.append(self._menu_item('Pizza (12 min)', 'pizza'))
        menu.append(self._menu_item('New task', 'new-task'))
        menu.append(self._menu_item('See tasks', 'see-tasks'))
        menu.append(self._menu_item('See past tasks', 'see-past-tasks'))
        menu.append(Gtk.SeparatorMenuItem())
        menu.append(self._menu_item('Quit', 'quit'))
        menu.append(self._menu_item('Settings', 'settings'))
        menu.show_all()
        return menu

    def _menu_item(self, label, action_name):
        item = Gtk.MenuItem(label=label)
        item.connect('activate', self._on_activate, action_name)
        return item

    def _on_activate(self, widget, action_name):
        proxy = self._get_proxy()
        if proxy is None:
            return
        try:
            proxy.call_sync(
                'ActivateAction',
                GLib.Variant('(sava{sv})', (action_name, [], {})),
                Gio.DBusCallFlags.NONE, -1, None)
        except GLib.Error as error:
            print('Could not activate "{}": {}'.format(action_name, error))

    def _get_proxy(self):
        if self._proxy is None:
            self._proxy = Gio.DBusProxy.new_for_bus_sync(
                Gio.BusType.SESSION, Gio.DBusProxyFlags.NONE, None,
                APPLICATION_ID, OBJECT_PATH, 'org.freedesktop.Application', None)
        return self._proxy


def main():
    tray = BzoingTray()

    def on_name_vanish(connection, name):
        print('{} gone, quitting tray'.format(APPLICATION_ID))
        Gtk.main_quit()

    Gio.bus_watch_name(Gio.BusType.SESSION, APPLICATION_ID,
                       Gio.BusNameWatcherFlags.NONE,
                       None, on_name_vanish)
    Gtk.main()


if __name__ == '__main__':
    main()