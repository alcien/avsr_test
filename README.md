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

~~~


##
