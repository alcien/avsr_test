model_folder=.
modality=video
pretrained_path=train1207/video.ckpt
mouthD=lip2
wavD=wav2
csv_file=/home/aiv-gpu-019/avsr_1207_1.csv

python $model_folder/eval.py data.modality=$modality data.dataset.root_dir=. data.dataset.test_file=$csv_file label_flag=1 mouth_dir=$mouthD wav_dir=$wavD pretrained_model_path=$pretrained_path 
