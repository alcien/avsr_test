import os
import torch
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--dir', default= '/DATA/temp/auto_avsr/train1207_2')
    args=parser.parse_args()


    model_dir = args.dir
    
    ckpt = os.path.join(model_dir, 'last.ckpt')
  
    model = torch.load(ckpt)
    check = model['state_dict']
    for key in list(check.keys()):
        if 'model.' in key:
            check[key.replace('model.','')] = check[key]
            del check[key]
    
    torch.save(check, os.path.join(model_dir, 'cleaned.ckpt'))
    print('complete')
