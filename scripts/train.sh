model_folder=/DATA/temp/auto_avsr
train_folder=train1207
modality=video
csv_file=/home/aiv-gpu-019/train_aavsr_1207.csv
val_file=/home/aiv-gpu-019/avsr_1207_1.csv

mouth=lip2
wav=wav2

prepare_model=/DATA/temp/auto_avsr/train1207/last.ckpt

python $model_folder/train2.py label_flag=1 exp_dir=$model_folder exp_name=$train_folder data.modality=$modality data.dataset.root_dir=/DATA/temp/auto_avsr data.dataset.train_file=$csv_file data.dataset.val_file=$val_file mouth_dir=$mouth wav_dir=$wav trainer.resume_from_checkpoint=$prepare_model
