import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk

from . import share


class SeeTasks(Gtk.Window):
    def __init__(self, application):
        Gtk.Window.__init__(self, application=application, title='See Tasks')
        self.connect('destroy', self.quit_window)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        box.set_margin_top(10)
        box.set_margin_bottom(10)
        box.set_margin_start(10)
        box.set_margin_end(10)

        self.store = Gtk.ListStore(str, str, str, bool)
        for task in share.tasklist.get_task_list():
            self.store.append([str(task.id), task.description, str(task.alarm), False])

        tree = Gtk.TreeView.new_with_model(self.store)
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

        renderer.connect('toggled', self.on_task_check)

        box.append(tree)
        self.set_child(box)

    def on_task_check(self, renderer, path):
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
    def __init__(self, application):
        Gtk.Window.__init__(self, application=application, title='Past Tasks')
        self.connect('destroy', self.quit_window)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        box.set_margin_top(10)
        box.set_margin_bottom(10)
        box.set_margin_start(10)
        box.set_margin_end(10)

        store = Gtk.ListStore(str, str, str)
        for task in share.tasklist.get_due_tasks():
            store.append([str(task.id), task.description, str(task.alarm)])

        tree = Gtk.TreeView.new_with_model(store)
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Id", renderer, text=0)
        tree.append_column(column)
        column = Gtk.TreeViewColumn("Description", renderer, text=1)
        tree.append_column(column)
        column = Gtk.TreeViewColumn("Alarm", renderer, text=2)
        tree.append_column(column)

        box.append(tree)

        button = Gtk.Button(label="Clear and Close")
        button.connect('clicked', self.clear)
        box.append(button)

        self.set_child(box)

    def clear(self, widget):
        share.tasklist.clear_due_tasks()
        self.quit_window(self)

    def quit_window(self, window):
        self.destroy()