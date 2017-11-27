import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from . import share
from pkg_resources import resource_filename

filepath = resource_filename(__name__, 'images/' + 'sinoamarelo.svg')

class SeeTasks(Gtk.Window):
    def __init__(self, parent):
        Gtk.Window.__init__(self, title='See Tasks')
        self.set_icon_from_file(filepath)
        self.connect('destroy', self.quit_window)

        box = Gtk.Box()
        box.set_orientation(Gtk.Orientation.VERTICAL)
        box.set_border_width(10)
        box.set_spacing(6)

        self.store = Gtk.ListStore(str, str, str, bool)
        for task in share.tasklist.get_task_list():
            treeiter = self.store.append([str(task.id), task.description, str(task.alarm), 0])

        tree = Gtk.TreeView(self.store)
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

        #path = Gtk.TreePath(0)
        renderer.connect('toggled', self.on_task_check)

        box.add(tree)
        self.add(box)
        self.show_all()

    def on_task_check(self, something, path):
        # mark checkbox
        self.store[path][3] = not self.store[path][3]

        treeiter = self.store.get_iter(path)

        # get id from ListStore (value at first column)
        this_id = int(self.store.get_value(treeiter, 0))

        # remove
        self.store.remove(treeiter)

        # delete task
        print("Task {} removed".format(this_id))
        share.tasklist.remove_task(this_id)
        share.tasklist.save_tasks()

    def quit_window(self, window):
        self.destroy()


class SeePastTasks(Gtk.Window):
    def __init__(self, parent):
        Gtk.Window.__init__(self, title='Past Tasks')
        self.set_icon_from_file(filepath)
        box = Gtk.Box()
        box.set_orientation(Gtk.Orientation.VERTICAL)
        box.set_border_width(10)
        box.set_spacing(6)

        self.connect('destroy', self.quit_window)
        store = Gtk.ListStore(str, str, str)
        for task in share.tasklist.due_task_list:
            treeiter = store.append([str(task.id), task.description, str(task.alarm)])

        tree = Gtk.TreeView(store)
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Id", renderer, text=0)
        tree.append_column(column)
        column = Gtk.TreeViewColumn("Description", renderer, text=1)
        tree.append_column(column)
        column = Gtk.TreeViewColumn("Alarm", renderer, text=2)
        tree.append_column(column)

        box.add(tree)

        button = Gtk.Button("Clear")
        button.connect('clicked', self.clear)
        box.add(button)

        self.add(box)
        self.show_all()

    def clear(self, widget):
        share.tasklist.due_task_list = []
        self.quit_window(self)
        self.__init__(self)

    def quit_window(self, window):
        self.destroy()
