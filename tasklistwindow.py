import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class TaskListWindow(Gtk.Window):
    def __init__(self, task_list):
        Gtk.Window.__init__(self)
        self.title="List of tasks"
        self.this_list = task_list

        self.connect('destroy', self.quit_tasklist_window)
        self.set_size_request(320, 240)
        self.set_border_width(10)
        self.set_icon_from_file('sinoamarelo.svg')

        box = Gtk.Box(spacing=6)
        box.set_orientation(Gtk.Orientation.VERTICAL)
        self.add(box)

        list_of_gtk_labels = []

        for each_task in self.this_list:
            # creates one Gtk.Label for each item in the list_of_tasks
            list_of_gtk_labels.append(Gtk.Label(each_task.get_task_desc() + " - " + str(each_task.get_alarm())))

        for label in list_of_gtk_labels:
            box.pack_start(label, 0, 0, 2)

        self.show_all()

    def quit_tasklist_window(self, window):
        self.destroy()
