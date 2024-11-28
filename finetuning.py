import os
import torch
import argparse

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_dir', default= '/DATA/temp/auto_avsr/sample_1')
    parser.add_argument('--ckpt', default='last.ckpt')
    parser.add_argument('--pth_path', default='/DATA/temp/auto_avsr/avsr_trlrwlrs2lrs3vox2avsp_base.pth')
    parser.add_argument('--saving', default='new.ckpt')
    args=parser.parse_args()


    model_dir = args.model_dir #모델이 저장된 폴더
    ckpt = os.path.join(model_dir, args.ckpt) #파인튜닝시킬 모델 ckpt 파일, 보통 last.ckpt 사용
    pth_path = args.pth_path # 파인튜닝할 모델 ckpt파일. https://github.com/mpc001/auto_avsr 의 model zoo에서 다운 가능
    model = torch.load(ckpt)
    new_ckpt = args.saving # 파인튜닝 완료할 모델 ckpt파일명
    check = model['state_dict']
    state_dict = torch.load(pth_path)

    for key in list(state_dict.keys()):
        if ('decoder' not in key) and ('ctc' not in key) and (key in check.keys()):
            model['state_dict']['model.'+key]  = state_dict[key]
    torch.save(model, os.path.join(model_dir, new_ckpt))
    print('\nfinetuning complete\n')