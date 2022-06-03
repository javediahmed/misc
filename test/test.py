''' test_template.py start template'''

INPUT_FILES = ('input_filename.txt', )
OUTPUT_FILES = ('output_filename.txt', )

class ExerciseSolution():
    '''basic setup to run multiple steps'''
    def __init__(self, input_files, input_function=read_data):
        self.input_files=input_files
        self.data = {name:input_function(input_file) for input_file in input_files}
        print("len(self.data): ", len(self.data)
    def question_1():
        print('Question 1: ')
    def question_2():
        print('Question 2: ')
    
print(type(INPUT_FILES))
# ExerciseSolution(INPUT_FILES)
