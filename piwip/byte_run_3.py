class VirtualMachineError(Exception):
    pass


class VirtualMachine:
    def __init__(self):
        self.frames = []  # 调用栈，每个vm有一个
        self.frame = None  # 当前frame
        self.return_value = None
        self.last_exception = None

    def run_code(self, code, global_names=None, local_names=None):
        frame = self.make_frame(
            code,
            global_names=global_names,
            local_names=local_names,
        )
        self.run_frame(frame)


class Frame:
    """
    属性的集合，没有任何方法
    每个frame有一个`数据栈`和一个`块栈`
    """

    def __init__(self, code_obj, global_names, local_names, prev_frame):
        self.code_obj = code_obj  # 每个frame只有一个code object
        self.global_names = global_names
        self.local_names = local_names
        self.prev_frame = prev_frame
        self.stack = []  # 每个frame有的一个数据栈
        if prev_frame:
            self.builtin_names = prev_frame.builtin_names
        else:
            self.builtin_names = local_names['__builtins__']
            if hasattr(self.builtin_names, '__dict__'):
                self.builtin_names = self.builtin_names.__dict__
        self.block_stack = []  # 每个frame有的一个块栈
        self.last_instruction = 0  # 最后执行的指令
