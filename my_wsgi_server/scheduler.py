import select
from queue import Queue
from collections import defaultdict


class CoroCall:
    def handle(self):
        pass


class ReadWait(CoroCall):
    def __init__(self, f):
        self.f = f

    def handle(self):
        fd = self.f.fileno()
        self.sched.wait_for_read(self.task, fd)


class WriteWait(CoroCall):
    def __init__(self, file):
        self.file = file

    def handle(self):
        fd = self.file.fileno()
        self.sched.wait_for_write(self.task, fd)


class NewTask(CoroCall):
    def __init__(self, target):
        self.target = target

    def handle(self):
        tid = self.sched.new(self.target)
        self.task.sendval = tid
        self.sched.schedule(self.task)


class Task(object):
    task_id = 0

    def __init__(self, target):
        Task.task_id += 1
        self.tid = Task.task_id
        self.target = target
        self.sendval = None

    def run(self):
        return self.target.send(self.sendval)


class Scheduler(object):
    def __init__(self):
        self.ready = Queue()
        self.taskmap = {}
        self.exit_waiting = defaultdict(list)
        self.read_waiting = {}
        self.write_waiting = {}

    def new(self, target):
        newtask = Task(target)
        self.taskmap[newtask.tid] = newtask
        self.schedule(newtask)
        return newtask.tid

    def schedule(self, task):
        self.ready.put(task)

    def mainloop(self):
        self.new(self.iotask())
        while True:
            task = self.ready.get()
            try:
                result = task.run()
                if isinstance(result, CoroCall):
                    result.task = task
                    result.sched = self
                    result.handle()
                    continue
            except StopIteration:
                self.exit(task)
                continue
            self.schedule(task)

    def exit(self, task):
        del self.taskmap[task.tid]
        for task in self.exit_waiting.pop(task.tid, []):
            self.schedule(task)

    def wait_for_exit(self, task, wait_tid):
        if wait_tid in self.taskmap:
            self.exit_waiting[wait_tid].append(task)
            return True
        else:
            return False

    def wait_for_read(self, task, fd):
        self.read_waiting[fd] = task

    def wait_for_write(self, task, fd):
        self.write_waiting[fd] = task

    def iopoll(self, timeout):
        if self.read_waiting or self.write_waiting:
            r, w, e = select.select(self.read_waiting, self.write_waiting, [],
                                    timeout)
            for fd in r:
                self.schedule(self.read_waiting.pop(fd))

            for fd in w:
                self.schedule(self.write_waiting.pop(fd))

    def iotask(self):
        while True:
            if self.ready.empty():
                self.iopoll(None)
            else:
                self.iopoll(0)
            yield
