class Interpter:
    def __init__(self):
        self.stack = []

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
        numbers = what_to_execute['numbers']
        for step in instructions:
            instn, arg = step
            if instn == 'LOAD_VALUE':
                number = numbers[arg]
                self.LOAD_VALUE(number)
            elif instn == 'ADD_TWO_VALUES':
                self.ADD_TWO_VALUES()
            elif instn == 'PRINT_ANSWER':
                self.PRINT_ANSWER()


if __name__ == "__main__":
    # 7 + 5
    what_to_execute = {
        'instructions': [
            ('LOAD_VALUE', 0),
            ('LOAD_VALUE', 1),
            ('ADD_TWO_VALUES', None),
            ('PRINT_ANSWER', None),
        ],
        'numbers': [7, 5]
    }
    interpter = Interpter()
    interpter.run_code(what_to_execute)
