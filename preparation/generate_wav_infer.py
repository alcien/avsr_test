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
    parser.add_argument('--test_dir', default= "/home/aiv-gpu-019/test")
    parser.add_argument('--test_fn', default= "lip_K_5_M_04_C955_A_012_9.mp4")
    args=parser.parse_args()
    
    print('Generate wav from mp4 file..\n')
    fd = args.test_dir#'/content/drive/MyDrive/colab/sample_video/sample_split'
    fn = args.test_fn 


    def generate_wav(fd, fn):
        if (os.path.exists(os.path.join(fd,fn)) == False) and ('.mp4' not in fn):
            print('cannot find .mp4 file') 
            return
        
    
        
        subfile =  os.path.join(fd, fn)
        
        if os.path.isdir(os.path.join(fd,'wav')) ==False:
            print(f'Generate wav folder in {fd}, mouth video will be generated in here\n')
            os.mkdir(os.path.join(fd,'wav'))
        
        extract_audio_from_video(subfile,os.path.join(fd,'wav', fn.split('.')[0]+'.wav'))

    generate_wav(fd,fn)

    print('wav file Generated.\n')