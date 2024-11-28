import os


import shutil

fd1 = 'data-small'

m = 'lip2'
w = 'wav2'
l = 'label'


fns = os.listdir(os.path.join(fd1, m))

length = len(fns)

cnt = length//10000

for j in range(1, cnt):
    
    start = j * 10000
    end = (j+1) * 10000
    num = j 

    if num == cnt-1:
        end = length-1
    
    dst = 'testfiles'+str(num)
    dst = '/DATA/temp/small'+dst

    if os.path.isdir(dst) == False:
        print(f'generating {dst}...\n')
        os.mkdir(f'{dst}')
        os.mkdir(f'{dst}/{m}')
        os.mkdir(f'{dst}/{w}')
        os.mkdir(f'{dst}/{l}')


    for i in range(start, end):
        
        batch = []
        batch.append(fd1)
        batch.append(fns[i])
        fn = os.path.join(batch[0], m, batch[1])
        wfn = os.path.join(batch[0], w, batch[1].split('.')[0]+'.wav')
        lfn = os.path.join(batch[0], l, batch[1].split('.')[0]+'.label')
    
        shutil.copy(fn, os.path.join(dst, m, batch[1]))
        shutil.copy(wfn,  os.path.join(dst, w, batch[1].split('.')[0]+'.wav'))
        shutil.copy(lfn,  os.path.join(dst, l, batch[1].split('.')[0]+'.label'))