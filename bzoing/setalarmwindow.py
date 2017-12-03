import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import datetime
import subprocess
from . import share
#from pkg_resources import resource_filename


#filepath = resource_filename(__name__, 'images/' + 'sinoamarelo.svg')

class SetAlarmWindow(Gtk.Window):
    def __init__(self, parent):
        Gtk.Window.__init__(self, title="Set Alarm")

        # set dialog measures and spacing
        #self.set_default_size(150, 100)

        # set icon
        #self.set_icon_from_file(filepath)

        self.connect('destroy', self.quit_window)
        box = Gtk.Box()

        box.set_orientation(Gtk.Orientation.VERTICAL)
        box.set_border_width(10)
        box.set_spacing(6)

        # create a label
        task_label = Gtk.Label()
        task_label.set_text('Task: ')
        box.add(task_label)

        # create a field to input the task description
        self.task_field = Gtk.Entry()
        box.add(self.task_field)

        # create calendar
        self.cal = Gtk.Calendar()
        box.add(self.cal)

        # create time fields
        time_hbox = Gtk.HBox()
        hour_adjustment = Gtk.Adjustment(00, 00, 23, 1, 10, 0)
        minute_adjustment = Gtk.Adjustment(00, 00, 59, 1, 10, 0)
        self.hours_field = Gtk.SpinButton()
        self.minutes_field = Gtk.SpinButton()
        self.hours_field.set_adjustment(hour_adjustment)
        self.minutes_field.set_adjustment(minute_adjustment)
        self.hours_field.connect('output', self.show_leading_zeros)
        self.minutes_field.connect('output', self.show_leading_zeros)

        # creates a : separator between the two SpinButtons
        time_sep_label = Gtk.Label()
        time_sep_label.set_text(' : ')

        # add time fields to the box
        time_hbox.add(self.hours_field)
        time_hbox.add(time_sep_label)
        time_hbox.add(self.minutes_field)

        # add time box to calendar box
        box.add(time_hbox)

        # add OK button
        button_set_alarm = Gtk.Button("Set")
        button_set_alarm.connect('clicked', self.button_set_alarm_cliked)
        box.add(button_set_alarm)
        self.add(box)
        self.show_all()

    def show_leading_zeros(self, spin_button):
        adjustement = spin_button.get_adjustment()
        spin_button.set_text('{:02d}'.format(int(adjustement.get_value())))
        return True

    def quit_window(self, window):
        self.destroy()

    def button_set_alarm_cliked(self, button):
        task_description = self.task_field.get_text()
        date = self.cal.get_date()
        hours = self.hours_field.get_text()
        minutes = self.minutes_field.get_text()
        self.alarm_time = datetime.datetime(date.year, date.month + 1, date.day, int(hours), int(minutes))

        # if time not valid, forget the time with a notification
        if self.alarm_time < datetime.datetime.now():
            self.sendmessage("The alarm is in the past, please set it again.")
            self.alarm_time = None
        print(task_description, self.alarm_time)

        # create task
        if self.alarm_time != None:
            share.tasklist.create_task(description=task_description, alarm=self.alarm_time)
            # save the tasks here to avoid shutdown saving
            share.tasklist.save_tasks()
            self.destroy()

    def sendmessage(self, message):
        subprocess.Popen(['notify-send', message])
