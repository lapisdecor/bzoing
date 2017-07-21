import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from . import config

from pkg_resources import resource_filename
filepath = resource_filename(__name__, 'images/' + 'sinoamarelo.svg')

class TaskListWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)
        self.title="List of tasks"
        self.tasks = config.list_of_tasks

        self.connect('destroy', self.quit_tasklist_window)
        self.set_size_request(320, 240)
        self.set_border_width(10)
        self.set_icon_from_file(filepath)

        box = Gtk.Box(spacing=6)
        box.set_orientation(Gtk.Orientation.VERTICAL)
        self.add(box)

        list_of_gtk_labels = []

        # creates one Gtk.Label for each item in the list_of_tasks
        for each_task in self.tasks:
            if each_task.get_alarm() == None:
                list_of_gtk_labels.append(Gtk.HBox(Gtk.Label(each_task.get_task_desc()), Gtk.Button("Del")))
            else:
                list_of_gtk_labels.append(Gtk.Label(each_task.get_task_desc() + " - " + str(each_task.get_alarm())))

        for label in list_of_gtk_labels:
            box.pack_start(label, 0, 0, 2)
            #box.pack_start(label[1], 0, 0, 2)

        self.show_all()

    def quit_tasklist_window(self, window):
        self.destroy()
