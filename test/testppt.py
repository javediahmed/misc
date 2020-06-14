import pptx, pdb
from pptx import Presentation

input_path = '/Users/javed/Desktop/'
input_files = ['test.pptx', 'test2.pptx', 'test3.pptx', 'out.pptx']

output_dirs = [input_path + 'test', input_path + 'test2']

file1 = input_path + input_files[0]
file2 = input_path + input_files[1]


ppt_image_dir = '/ppt/media'
ppt_master_dir = '/ppt/slideMasters/'

def deldir(output_dir):
    os.system('rm -r ' + output_dir)

def unzip_ppt(presfile, output_dir):
    os.system('unzip {} -d '.format(presfile) + output_dir)

def zip_ppt(presfile, output_dir, outfile):
    os.system('zip {} {outfile}'.format(presfile + output_dir, outfile))

    
def getitems(presfile, output_dir, presdir):
    items = os.listdir(output_dir + presdir)
    return(items)

#deldir(output_dirs[0])
#unzip_ppt(file1, output_dirs[1])

pdb.set_trace()

# prs = [Presentation(input_path + i) for i in input_files]
# prs[0]
# masters = [i.slide_master for i in prs]
# bgs = [i.background for i in masters]
# prs[0].slide_master.background = prs[1].slide_master.background
# prs[0].save('out.pptx')
# pdb.set_trace()
