# -*- coding: utf-8 -*-

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
        self.taskDesc = task_desc

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


class TaskList:
    """
    Defines a list of tasks
    """
    def __init__(self):
        self.task_list = []

    def add_task(self, task):
        self.task_list.append(task)

    def remove_task(self, task_id):
        for task in self.task_list:
            if task.get_task_id() == task_id:
                self.task_list.remove(task)

    def show_list(self):
        for task in self.task_list:
            print task.get_task_id(), task.get_creation_date(), task.get_task_desc(), task.get_alarm()
        print "-----------------"


tarefa = Task(0, "Comprar Leite")
tarefa.set_task_desc("Lavar a loiça")
tarefa2 = Task(1, "Comprar tabaco")

lista = TaskList()
lista.add_task(tarefa)
lista.add_task(tarefa2)
lista.show_list()
lista.remove_task(0)
lista.show_list()
# data = datetime.datetime(2015,12,29, 11,19,00,0)
# while True:
#     if datetime.datetime.now() == data:
#         print "Bzooooooing!"
#         break


