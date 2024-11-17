# prepartion

한국어를 문장 단위로 녹음한 영상을 입부분 모양과 음성으로 분할하는 작업입니다. 학습 시 자막 레이블은 주어졌다고 가정합니다. 

---
## setup

필요  dependency-packages를 설치합니다.
~~~
pip install -r requirements.txt
~~~


## Generate wav file

영상에서 음성을 추출하는 작업입니다. 
~~~
python generate_wav.py --test_dir [My_dir]
~~~

1. test_dir : 영상의 위치를 기입합니다.
   * 음성은  test_dir 이하 wav 라는 폴더에 생성됩니다. 

## Generate mouth ROIs video

영상에서 입 모양 부분을 추출하여 비디오로 나타냅니다. 

### 원본 영상 

<img src='https://github.com/alcien/avsr_test/blob/main/asset/lip_K_5_M_04_C955_A_012_9.gif' style='width:200px'>
</img>

### 입 모양 영상

<img src='https://github.com/alcien/avsr_test/blob/main/asset/mouth_lip_K_5_M_04_C955_A_012_9.gif' width:200px height:100px>
</img>

### 얼굴 landmark를 찾기 위한 필요 파일 다운로드
~~~
wget http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2
bzip2 -d /content/data/misc/shape_predictor_68_face_landmarks.dat.bz2

wget --content-disposition https://github.com/mpc001/Lipreading_using_Temporal_Convolutional_Networks/raw/master/preprocessing/20words_mean_face.npy
~~~

### 입 모양 영상 추출
~~~
python generate_mouth.py --test_dir [dir] --face_predictor_path [face predictor file path] --mean_face_path [mean face file path]
~~~

1. test_dir : 원본 영상이 담긴 폴더
    * 입 모양 영상은 test_dir 이하 mouth 폴더에 저장됩니다.     
2. face_predictor_path : shape_predictor_68_face_landmarks.dat의 위치
3. mean_face_path : 20words_mean_face.npy의 위치



# demo용 파일 만들기

위와 같은 프로세스를 가지나, 파일 하나에 대해서 확인해보고 싶을 때 사용합니다. 

## Generate wav file

영상에서 음성을 추출하는 작업입니다. 
~~~
python generate_wav_infer.py --test_dir [My_dir] --test_fn [filename]
~~~

1. test_dir : 영상이 위치한 폴더
   * 음성은  test_dir 이하 wav 라는 폴더에 생성됩니다.
2. test_fn : test_dir에 위치한 wav로 변환시키고 싶은 파일명

## Generate mouth ROIs video

### 입 모양 영상 추출
~~~
python generate_mouth_infer.py --test_dir [dir] --test_fn [filename] --face_predictor_path [face predictor file path] --mean_face_path [mean face file path]
~~~

1. test_dir : 원본 영상이 담긴 폴더
    * 입 모양 영상은 test_dir 이하 mouth 폴더에 저장됩니다.
2. test_fn : test_dir에 위치한 변환시키고 싶은 파일명 
3. face_predictor_path : shape_predictor_68_face_landmarks.dat의 위치
4. mean_face_path : 20words_mean_face.npy의 위치



