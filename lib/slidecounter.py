import os, pptx
print('Directory: ', os.getcwd())
ppts = [f for f in os.listdir() if f.endswith('.pptx') and not f.startswith('~')]
for f in ppts:
    ppt = pptx.Presentation(f)
    num = len(ppt.slides)
    print(f'{f}: {num}')


