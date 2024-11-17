import os 
import cv2
import sentencepiece as spm
import torch
from tqdm import tqdm
import os
import argparse


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', default= "/home/aiv-gpu-019/data-small")
    parser.add_argument('--mouth_fd', default="lip2")
    parser.add_argument('--wav_fd', default='wav2')
    parser.add_argument('--fn', default='/home/aiv-gpu-019/small_test.csv')
    args=parser.parse_args()

    here = args.dataset
    mouth_fd = args.mouth_fd
    wav_fd = args.wav_fd

    print('Creating CSV file for demo\n')

    
    mouthlist = os.listdir(os.path.join(here,mouth_fd))
    wavlist = os.listdir(os.path.join(here,wav_fd))

    
    label_filename = args.fn

    
    f = open(label_filename, "w")

    dataset= here
    
    for fn in tqdm(mouthlist):
      vname = fn.split('.')[0]
      if os.path.isdir(os.path.join(here,mouth_fd,fn)):
          continue
      if (vname+'.wav' not in wavlist) :
        continue
        
      filepath = os.path.join(here, mouth_fd,vname+'.mp4')
      video = cv2.VideoCapture(filepath)


      length = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    
      basename = fn
      vframes = length
    

      f.write(f"{dataset},{vname+'.mp4'},{vframes},0\n")

    f.close()

    print('CSV file Generated')
