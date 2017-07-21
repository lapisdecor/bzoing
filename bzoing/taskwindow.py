import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from . import alarmdialog
import datetime
from . import tasks
from . import config
import subprocess
from threading import Lock
from pkg_resources import resource_filename

tLock = Lock()

filepath = resource_filename(__name__, 'images/' + "sinoamarelo.svg")

class TaskWindow(Gtk.Window):
    def __init__(self, parent):
        Gtk.Window.__init__(self)
        self.parent = parent
        self.task_desc = None
        self.alarm_time = None
        self.title='Create Task'
        self.set_border_width(10)
        self.set_icon_from_file(filepath)
        self.connect('destroy', self.quit_window)

        # create box to hold the buttons etc.
        vbox = Gtk.Box.new(Gtk.Orientation.VERTICAL, 0)
        hbox = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 6)

        # create a label
        task_label = Gtk.Label()
        task_label.set_text('Task: ')
        hbox.pack_start(task_label, False, False, 2)

        # create a field to input the task description
        task_field = Gtk.Entry()
        hbox.pack_start(task_field, False, False, 2)

        vbox.pack_start(hbox, False, False, 6)

        # create the Alarm button
        button_alarm = Gtk.Button()
        button_alarm.set_label("Alarm")
        button_alarm.connect("clicked", self.button_alarm_clicked)
        vbox.pack_start(button_alarm, False, False, 2)

        # create the OK button
        button_ok = Gtk.Button()
        button_ok.set_label("OK")
        button_ok.connect("clicked", self.task_ok_clicked, task_field)
        vbox.pack_start(button_ok, 0, 0, 2)

        self.add(vbox)
        self.show_all()

    def get_task_desc(self):
        """Returns description of the task"""
        return self.task_desc

    def get_alarm(self):
        """Returns the alarm time for the current task"""
        return self.alarm_time

    def quit_window(self, window):
        """Quits the TaskWindow"""
        window.destroy()

    def button_alarm_clicked(self, button):
        """
        Creates the Alarm Dialog and stores the date and the time
        in the TaskWindow object
        """
        #TODO must allways input a description ?
        my_alarm = alarmdialog.AlarmDialog(self)
        response = my_alarm.run()
        if response == Gtk.ResponseType.OK:
            d       = my_alarm.cal
            my_date = d.get_date()
            h       = my_alarm.hours_field
            hours   = h.get_text()
            m       = my_alarm.minutes_field
            minutes = m.get_text()
            #print("The time is {0:02d}:{1:02d}".format(int(hours), int(minutes)))

            self.alarm_time = datetime.datetime(my_date.year,
                                               my_date.month + 1,
                                               my_date.day,
                                               int(hours),
                                               int(minutes))

            # if time not valid, forget the time with a notification
            if self.alarm_time < datetime.datetime.now():
                self.alarm_time = None
                self.sendmessage("The alarm is in the past, please set it again.")


        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel was pressed")

        my_alarm.destroy()


    def sendmessage(self, message):
        subprocess.Popen(['notify-send', message])
        return


    def task_ok_clicked(self, widget, task_field):
        """
        Creates a task and the task alarm
        """
        self.task_desc = task_field.get_text()

        # gets task description
        desc = self.task_desc

        # inform that no description is entered
        if desc == "":
            self.sendmessage("No task description, create task again")

        # creates task if task was entered
        elif desc != None and desc != "":
            # creates a new task_id
            self.parent.task_id += 1

            # gets alarm time
            alarm_time = self.get_alarm()

            # creates new task
            new_task = tasks.Task(self.parent.task_id, desc)

            # sets alarm if an alarm was defined
            if alarm_time != None:
                # sets the alarm on the new task
                new_task.set_alarm_date(alarm_time)
                print("Alarm is set to ", alarm_time)
            else:
                print("New task '{}' created with no Alarm!".format(desc))

            # appends task to task list
            config.list_of_tasks.append(new_task)

            # run alarm process
            # append list_of_alarms if alarm is set
            if self.alarm_time != None:
                with tLock:
                    #config.list_of_alarms.append((desc, self.alarm_time))
                    config.list_of_alarms.append(new_task)

        self.destroy()
