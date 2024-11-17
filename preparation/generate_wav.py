from moviepy.editor import VideoFileClip
import os
import argparse

def extract_audio_from_video(video_file_path, audio_file_path):
    # mp4 등 비디오 파일 불러오기
    video = VideoFileClip(video_file_path)
    
    # 오디오를 추출하여 mp3 파일로 저장
    video.audio.write_audiofile(audio_file_path,fps=16000)




if __name__ == '__main__':
  parser = argparse.ArgumentParser()

  parser.add_argument('--test_dir', default= "/home/aiv-gpu-019/data-all")
  args=parser.parse_args()


  fd = args.test_dir#'/content/drive/MyDrive/colab/sample_video/sample_split'


  fd_1 = os.listdir(fd)
  fns = len(os.listdir(fd))



  for idx in range(len(os.listdir(fd))):
    fn = fd_1[idx]


    if os.path.isdir(os.path.join(fd,fn)):
        continue
    else:
      subfile =  os.path.join(fd, fn)

      if os.path.isdir(os.path.join(fd,'wav')) ==False:
        os.mkdir(os.path.join(fd,'wav'))
      
      extract_audio_from_video(subfile,os.path.join(fd,'wav', fn.split('.')[0]+'.wav'))

