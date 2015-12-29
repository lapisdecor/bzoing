# -*- coding: utf-8 -*-

import datetime


class Task:
    def __init__(self, taskId, taskDesc):
        self.taskId = taskId
        self.taskDesc = taskDesc
        self.alarm = False
        self.dateCreated = datetime.datetime.now()
        self.alarmDate = None

    def set_task_desc(self, taskDesc):
        self.taskDesc = taskDesc

    def get_task_id(self):
        return self.taskId

    def get_task_desc(self):
        return self.taskDesc

    def get_creation_date(self):
        return self.dateCreated


class TaskList:
    def __init__(self):
        self.task_list = []

    def add_task(self, task):
        self.task_list.append(task)

    def show_list(self):
        for task in self.task_list:
            print task.get_task_id(), task.get_creation_date(), task.get_task_desc()


tarefa = Task(0, "Comprar Leite")
tarefa.set_task_desc("Lavar a loiça")
tarefa2 = Task(1, "Comprar tabaco")

lista = TaskList()
lista.add_task(tarefa)
lista.add_task(tarefa2)
lista.show_list()
