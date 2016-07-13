import datetime


class Task:
    """
    Defines a task with id, description, creation time and alarm
    """
    def __init__(self, task_id, task_desc):
        self.task_id = task_id
        self.task_desc = task_desc
        self.has_alarm = False
        self.date_created = datetime.datetime.now()
        self.alarm_date = None

    def set_task_desc(self, task_desc):
        self.task_desc = task_desc

    def get_task_id(self):
        return self.task_id

    def get_task_desc(self):
        return self.task_desc

    def get_creation_date(self):
        return self.date_created

    def alarm_on(self):
        self.has_alarm = True

    def alarm_off(self):
        self.has_alarm = False

    def set_alarm(self, date):
        assert isinstance(date, datetime.datetime)
        self.alarm_date = date
        self.alarm_on()

    def get_alarm(self):
        return self.alarm_date

    def get_alarm_state(self):
        if self.has_alarm:
            return "Alarm On"
        return "Alarm Off"
