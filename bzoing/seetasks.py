import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from . import share

class SeeTasks(Gtk.Window):
    def __init__(self, parent):
        Gtk.Window.__init__(self, title='See Tasks')

        self.connect('destroy', self.quit_window)
        store = Gtk.ListStore(str, str, str, bool)
        for task in share.tasklist.get_task_list():
            treeiter = store.append([str(task.id), task.description, str(task.alarm), 0])

        tree = Gtk.TreeView(store)
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Id", renderer, text=0)
        tree.append_column(column)
        column = Gtk.TreeViewColumn("Description", renderer, text=1)
        tree.append_column(column)
        column = Gtk.TreeViewColumn("Alarm", renderer, text=2)
        tree.append_column(column)
        renderer = Gtk.CellRendererToggle()
        column = Gtk.TreeViewColumn("Delete", renderer, active=3)
        tree.append_column(column)

        self.add(tree)
        self.show_all()

    def quit_window(self, window):
        self.destroy()
