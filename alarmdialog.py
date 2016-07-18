import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class AlarmDialog(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "Set Alarm", parent, 0,
                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                             Gtk.STOCK_OK, Gtk.ResponseType.OK))

        # set dialog measures and spacing
        self.set_default_size(150, 100)
        box = self.get_content_area()

        box.set_orientation(Gtk.Orientation.VERTICAL)
        box.set_border_width(10)

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

        # creates a : separator between the two SpinButtons
        time_sep_label = Gtk.Label()
        time_sep_label.set_text(' : ')

        # add time fields to the box
        time_hbox.add(self.hours_field)
        time_hbox.add(time_sep_label)
        time_hbox.add(self.minutes_field)

        # add time box to calendar box
        box.add(time_hbox)

        self.show_all()

    #def get_alarm():
    #    return self.alarm_time
