from huggingface_hub import hf_hub_download
import os
import shutil
import subprocess


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

file_path3 = hf_hub_download(repo_id="kaya218/test", filename= "last_video.ckpt")
print(f"Downloaded file path: {file_path3}")

url = 'https://huggingface.co/kaya218/test/resolve/main/last_av.ckpt?download=true'

output_path = os.path.join(cpath, fd1, 'last.ckpt')



shutil.copy(file_path, os.path.join(cpath,fd1,'av.ckpt'))
shutil.copy(file_path2, os.path.join(cpath, fd2, 'video.ckpt'))

shutil.copy(file_path3, os.path.join(cpath, fd2, 'last.ckpt'))

subprocess.run(['wget', '-O', output_path, url], check=True)

print(f'moved downloaded files into {fd1} and {fd2} folders')

