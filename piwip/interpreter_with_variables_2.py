class Interpter:
    def __init__(self):
        self.stack = []
        self.env = {}

    def STORE_NAME(self, name):
        val = self.stack.pop()
        self.env[name] = val

    def LOAD_NAME(self, name):
        val = self.env[name]
        self.stack.append(val)

    def parse_arg(self, instn, arg, what_to_execute):
        numbers = ['LOAD_VALUE']
        names = ['LOAD_NAME', 'STORE_NAME']
        if instn in numbers:
            arg = what_to_execute['numbers'][arg]
        elif instn in names:
            arg = what_to_execute['names'][arg]
        return arg

    def LOAD_VALUE(self, number):
        self.stack.append(number)

    def PRINT_ANSWER(self):
        answer = self.stack.pop()
        print(answer)

    def ADD_TWO_VALUES(self):
        first_num = self.stack.pop()
        second_num = self.stack.pop()
        total = first_num + second_num
        self.stack.append(total)

    def run_code(self, what_to_execute):
        instructions = what_to_execute['instructions']
        for step in instructions:
            instn, arg = step
            arg = self.parse_arg(instn, arg, what_to_execute)
            bytecode_method = getattr(self, instn)
            if arg is None:
                bytecode_method()
            else:
                bytecode_method(arg)


if __name__ == "__main__":
    # a = 7
    # b = 5
    # a + b
    what_to_execute = {
        "instructions": [
            ("LOAD_VALUE", 0),
            ("STORE_NAME", 0),
            ("LOAD_VALUE", 1),
            ("STORE_NAME", 1),
            ("LOAD_NAME", 0),
            ("LOAD_NAME", 1),
            ("ADD_TWO_VALUES", None),
            ("PRINT_ANSWER", None),
        ],
        "numbers": [7, 5],
        "names": ["a", "b"]
    }
    interpter = Interpter()
    interpter.run_code(what_to_execute)
