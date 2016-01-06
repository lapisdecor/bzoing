import datetime


class Task:
    """
    Defines a task with id, description, creation time and alarm
    """
    def __init__(self, task_id, task_desc):
        self.task_id = task_id
        self.task_desc = task_desc
        self.alarm = False
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
        self.alarm = True

    def alarm_off(self):
        self.alarm = False

    def set_alarm(self, date):
        assert isinstance(date, datetime)
        self.alarm_date = date
        self.alarm_on()

    def get_alarm(self):
        if self.alarm:
            return "Alarm On"
        return "Alarm Off"


# Testing Area
# def cria_tarefas():
#     """
#     Creates two sample tasks for testing purposes
#     :return: a list with two tasks
#     """
#     tarefa1 = Task(0, "Comprar Leite")
#     tarefa2 = Task(1, "Comprar tabaco")
#     return [tarefa1, tarefa2]
#
#
# tarefas = cria_tarefas()
# for tarefa in tarefas:
#     print(tarefa.get_task_id(), tarefa.date_created, tarefa.get_task_desc())
