import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk
import datetime
import subprocess
from . import share


class SetAlarmWindow(Gtk.Window):
    def __init__(self, application):
        Gtk.Window.__init__(self, application=application, title="Set Alarm")

        self.connect('destroy', self.quit_window)
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        box.set_margin_top(10)
        box.set_margin_bottom(10)
        box.set_margin_start(10)
        box.set_margin_end(10)

        task_label = Gtk.Label(label='Task: ')
        box.append(task_label)

        self.task_field = Gtk.Entry()
        box.append(self.task_field)

        # Calculate the datetime for NOW + 5 minutes
        localtime = datetime.datetime.now()
        localtime_plus_5_min = localtime + datetime.timedelta(minutes=5)

        self.cal = Gtk.Calendar()
        box.append(self.cal)

        # Setting correct calendar date -> month is between 0 and 11
        self.cal.set_day(localtime_plus_5_min.day)
        self.cal.set_month(localtime_plus_5_min.month - 1)
        self.cal.set_year(localtime_plus_5_min.year)

        time_hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        hour_adjustment = Gtk.Adjustment(value=0, lower=0, upper=23,
                                         step_increment=1, page_increment=10,
                                         page_size=0)
        minute_adjustment = Gtk.Adjustment(value=0, lower=0, upper=59,
                                           step_increment=1, page_increment=10,
                                           page_size=0)
        self.hours_field = Gtk.SpinButton()
        self.minutes_field = Gtk.SpinButton()
        self.hours_field.set_adjustment(hour_adjustment)
        self.minutes_field.set_adjustment(minute_adjustment)
        self.hours_field.connect('output', self.show_leading_zeros)
        self.minutes_field.connect('output', self.show_leading_zeros)

        # Setting correct time values
        self.hours_field.set_value(localtime_plus_5_min.hour)
        self.minutes_field.set_value(localtime_plus_5_min.minute)

        time_sep_label = Gtk.Label(label=' : ')

        time_hbox.append(self.hours_field)
        time_hbox.append(time_sep_label)
        time_hbox.append(self.minutes_field)

        box.append(time_hbox)

        button_set_alarm = Gtk.Button(label="Set")
        button_set_alarm.connect('clicked', self.button_set_alarm_cliked)
        box.append(button_set_alarm)

        self.set_child(box)

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
        self.alarm_time = datetime.datetime(date.get_year(), date.get_month(),
                                            date.get_day_of_month(),
                                            int(hours), int(minutes))

        # if time not valid, forget the time with a notification
        if self.alarm_time < datetime.datetime.now():
            self.sendmessage("The alarm is in the past, please set it again.")
            self.alarm_time = None
        print(task_description, self.alarm_time)

        # create task
        if self.alarm_time is not None:
            share.tasklist.create_task(description=task_description, alarm=self.alarm_time)
            # save the tasks here to avoid shutdown saving
            share.tasklist.save_tasks()
            self.destroy()

    def sendmessage(self, message):
        subprocess.Popen(['notify-send', '-a', 'Bzoing', message])