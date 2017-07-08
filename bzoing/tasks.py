import datetime


class Task:
    """
    Defines a task with id, description and alarm
    """
    def __init__(self, task_id, task_desc):
        self.task_id = task_id
        self.task_desc = task_desc
        self.alarm_on = False
        self.alarm_date = None

    def set_task_desc(self, task_desc):
        self.task_desc = task_desc

    def get_task_id(self):
        return self.task_id

    def get_task_desc(self):
        return self.task_desc

    def set_alarm_on(self):
        self.alarm_on = True

    def set_alarm_off(self):
        self.alarm_on = False

    def set_alarm_date(self, date):
        assert isinstance(date, datetime.datetime)
        self.alarm_date = date
        self.set_alarm_on()

    def get_alarm(self):
        return self.alarm_date

    def is_alarm_on(self):
        return self.alarm_on
