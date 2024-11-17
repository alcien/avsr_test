import os 
import cv2
import sentencepiece as spm
import torch
from tqdm import tqdm
import os
import argparse

dirN = '/DATA/temp/auto_avsr/spm/unigram/bpe_1207'
model_path= os.path.join(dirN, 'unigram5000.model')
dict_path = os.path.join(dirN, 'unigram5000_units.txt')


class TextTransform:
    """Mapping Dictionary Class for SentencePiece tokenization."""

    def __init__(
        self,
        sp_model_path=model_path,
        dict_path=dict_path,
    ):

        # Load SentencePiece model
        self.sp = spm.SentencePieceProcessor(model_file=sp_model_path)

        # Load units and create dictionary
        units = open(dict_path, encoding='utf8').read().splitlines()
        self.hashmap = {unit.split()[0]: unit.split()[-1] for unit in units}
        # 0 will be used for "blank" in CTC
        self.token_list = ["<blank>"] + list(self.hashmap.keys()) + ["<eos>"]
        self.ignore_id = -1

    def tokenize(self, text):
        tokens = self.sp.EncodeAsPieces(text)
        token_ids = [self.hashmap.get(token, self.hashmap["<unk>"]) for token in tokens]
        return torch.tensor(list(map(int, token_ids)))

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', default= "/home/aiv-gpu-019/data-all")
    parser.add_argument('--mouth_fd', default="lip1")
    parser.add_argument('--label_fd', default='label')
    parser.add_argument('--wav_fd', default='wav2')
    parser.add_argument('--fn', default='trainAvsr.csv')
    parser.add_argument('--Lfn', default='trainAvsr.txt')
    parser.add_argument('--spm_path', default=dirN)
    args=parser.parse_args()

    here = args.dataset
    mouth_fd = args.mouth_fd
    wav_fd = args.wav_fd
    label_fd = args.label_fd
    
    mouthlist = os.listdir(os.path.join(here,mouth_fd))
    wavlist = os.listdir(os.path.join(here,wav_fd))
    labellist = os.listdir(os.path.join(here, label_fd))
    
    label_filename =  args.fn
    txt_filename = args.Lfn
    
    f = open(label_filename, "w")
    fout = open(txt_filename,'w')
    if args.spm_path == dirN:
        texttrans = TextTransform()
    else:
        model_path  = os.path.join(args.spm_path, 'unigram5000.model')
        dict_path = os.path.join(args.spm_path, 'unigram5000_units.txt')
        texttrans = TextTransform(model_path, dict_path)
    
    dataset= here
    
    for fn in tqdm(mouthlist):
      vname = fn.split('.')[0]
    
      if (vname+'.label' not in labellist) :
        continue
      elif (vname+'.wav' not in wavlist) :
        continue
      filepath = os.path.join(here, mouth_fd,vname+'.mp4')
      video = cv2.VideoCapture(filepath)
      with open(os.path.join(here,label_fd,vname+'.label')) as fin:
        lab = fin.readline().strip()
    
      length = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    
      basename = fn
      vframes = length
    
      str1=  texttrans.tokenize(lab)
      token_id_str = " ".join(
                map(str, [_.item() for _ in texttrans.tokenize(lab)])
            )
    
    
      f.write(f"{dataset},{vname+'.mp4'},{vframes},{token_id_str}\n")
      fout.write(f'{lab}\n')
    
    f.close()
    fout.close()