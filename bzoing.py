import datetime

class Task:
    def __init__(self, taskId, taskDesc):
        self.taskId = taskId
        self.taskDesc = taskDesc
        self.alarm = False
        self.dateCreated = datetime.datetime.now()
        self.alarmDate = None


    def setTaskDesc(self, taskDesc):
        self.taskDesc = taskDesc

    def getTaskID(self):
        return self.taskId

    def getTaskDesc(self):
        return self.taskDesc

    def getCreationDate(self):
        return self.dateCreated





tarefa = Task(0, "Comprar Leite")
print tarefa.getTaskID(), tarefa.getCreationDate(), tarefa.getTaskDesc()