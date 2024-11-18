from huggingface_hub import hf_hub_download
import os
import shutil

fd1 = 't1207_av'
fd2 = 'train1207'

cpath = os.getcwd()


if os.path.isdir(os.path.join(cpath, fd1))==False:
    os.mkdir(fd1)

if os.path.isdir(os.path.join(cpath, fd2))==False:
    os.mkdir(fd2)

file_path = hf_hub_download(repo_id="kaya218/test", filename= "av.ckpt")
print(f"Downloaded file path: {file_path}")

file_path2 = hf_hub_download(repo_id="kaya218/test", filename= "video.ckpt")
print(f"Downloaded file path: {file_path2}")


shutil.copy(file_path, os.path.join(cpath,fd1,'av.ckpt'))
shutil.copy(file_path2, os.path.join(cpath, fd2, 'video.ckpt'))

print(f'moved into {fd1} and {fd2} folders')

