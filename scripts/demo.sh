mp4_folder=/home/aiv-gpu-019/test
mp4_name=lip_K_5_M_04_C955_A_012_9.mp4

face_path=/home/aiv-gpu-019/shape_predictor_68_face_landmarks.dat
mean_face=/home/aiv-gpu-019/20words_mean_face.npy

csv_file=/home/aiv-gpu-019/test/demo_test.csv

python generate_mouth_infer.py --test_dir $mp4_folder --test_fn $mp4_name --face_predictor_path $face_path --mean_face_path $mean_face
python generate_wav_infer.py --test_dir $mp4_folder --test_fn $mp4_name
python generate_infer.py --dataset $mp4_folder --mouth_fd mouth --wav_fd wav --fn $csv_file

model_folder=/DATA/temp/auto_avsr
modality=video
pretrained_path=/DATA/temp/auto_avsr/train1207/cleaned.ckpt

python $model_folder/eval.py data.modality=$modality data.dataset.root_dir=/DATA/temp/auto_avsr data.dataset.test_file=$csv_file label_flag=0 mouth_dir=mouth wav_dir=wav pretrained_model_path=$pretrained_path 

cat $model_folder/result.txt