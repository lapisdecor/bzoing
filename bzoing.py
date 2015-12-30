# -*- coding: utf-8 -*-

import datetime
from gi.repository import Gtk

NORMAL_ICON = 'icons/bzoing.png'

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

    def get_list(self):
        return self.task_list

class MyBzoing(Gtk.Window):

    def __init__(self):

        tarefas = cria_tarefas()
        my_list_of_tasks = cria_lista(tarefas)

        Gtk.Window.__init__(self, title="Bzoing")
        self.box = Gtk.Box(spacing=6)
        self.add(self.box)

        for tarefa in my_list_of_tasks.get_list():
            # this is temporarily wrong, a dictionary or a list of objects must be created
            self.label = Gtk.Label()
            self.label.set_label(tarefa.get_task_desc())
            self.label.set_halign(Gtk.Align.END)

        self.my_status_icon = Gtk.StatusIcon()
        self.my_status_icon.set_from_icon_name("owncloud")



        self.box.add(self.label)

def cria_tarefas():
    """
    Creates two sample tasks for testing purposes
    :return: a list with two tasks
    """
    tarefa1 = Task(0, "Comprar Leite")
    tarefa1.set_task_desc("Lavar a loiça")
    tarefa2 = Task(1, "Comprar tabaco")
    return [tarefa1, tarefa2]

def cria_lista(tarefas):
    """
    Creates a list of tasks for testing purposes
    :param tarefas: a list of tasks
    :return: a Tasklist object
    """
    lista = TaskList()

    for tarefa in tarefas:
        lista.add_task(tarefa)

    # Show the list of tasks in the console
    lista.show_list()

    return lista

    # uncomment the following 2 lines to test removing a task
    # lista.remove_task(0)
    # lista.show_list()


def main():
    win = MyBzoing()
    win.connect("destroy", destroy)
    win.show_all()
    Gtk.main()


def destroy(window):
    Gtk.main_quit()

if __name__ == "__main__":
    main()

# some testing here
# data = datetime.datetime(2015,12,29, 15,30,00,0)
    # while True:
    #     if datetime.datetime.now() == data:
    #         print "Bzooooooing!"
    #         break