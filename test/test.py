''' test_template.py start template'''

IN_FILES = ('./in1.txt', './in2.txt')
OUT_FILES = ('output_filename.txt', )

class Exercise():
    '''basic setup to run multiple step exercise'''
    def __init__(self, in_files=None, out_files=None):
        self.in_files = in_files
        self.out_files = out_files
        elif in_files:
            self.data = {in_file:reader(in_file) for in_file in in_files}
    with open(out_file, 'r') as data_file:
        input_data = (input_record.strip('\n') for input_record in input_file)

class Response(Exercise):
    '''container for results'''
    def __init__(self):
       super.__init__()

Response(IN_FILES)



       
           
