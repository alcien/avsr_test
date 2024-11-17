import os
import argparse
import numpy
numpy.float = numpy.float64
numpy.int = numpy.int_
from tqdm import tqdm
import dlib, cv2, os
import numpy as np
import skvideo
import skvideo.io
from tqdm import tqdm
from align_mouth import landmarks_interpolate, crop_patch, write_video_ffmpeg
def detect_landmark(image, detector, predictor):
  gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
  rects = detector(gray, 1)
  coords = None
  for (_, rect) in enumerate(rects):
      shape = predictor(gray, rect)
      coords = np.zeros((68, 2), dtype=np.int32)
      for i in range(0, 68):
          coords[i] = (shape.part(i).x, shape.part(i).y)
  return coords


# -- RGB to GRAY
def convert_bgr2gray(data):
  return np.stack([cv2.cvtColor(_, cv2.COLOR_BGR2GRAY) for _ in data], axis=0)



def save2npz(filename, data=None):
  assert data is not None, "data is {}".format(data)
  if not os.path.exists(os.path.dirname(filename)):
      os.makedirs(os.path.dirname(filename))
  np.savez_compressed(filename, data=data)


def video_generator(filename, size, fps, img_array):
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(filename, fourcc=fourcc, fps=fps, frameSize=size)

    for img in img_array:
        out.write(img)

    out.release()



def preprocess_video(input_video_path, output_video_path, face_predictor_path, mean_face_path):
  detector = dlib.get_frontal_face_detector()
  predictor = dlib.shape_predictor(face_predictor_path)
  STD_SIZE = (256, 256)
  mean_face_landmarks = np.load(mean_face_path)
  stablePntsIDs = [33, 36, 39, 42, 45]
  videogen = skvideo.io.vread(input_video_path)
  frames = np.array([frame for frame in videogen])
  landmarks = []
  for frame in tqdm(frames):
      landmark = detect_landmark(frame, detector, predictor)
      landmarks.append(landmark)
  preprocessed_landmarks = landmarks_interpolate(landmarks)
  rois = crop_patch(input_video_path, preprocessed_landmarks, mean_face_landmarks, stablePntsIDs, STD_SIZE,
                        window_margin=12, start_idx=48, stop_idx=68, crop_height=96, crop_width=96)

  data = rois[...,::-1]
  #save2npz(output_data_path, data=data)

  size= ( rois.shape[1], rois.shape[2])
  video_generator(output_video_path, size, 25, rois)
  #write_video_ffmpeg(rois, output_video_path, "/usr/bin/ffmpeg")

  return


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--test_dir', default= "/home/aiv-gpu-019/test")
    parser.add_argument('--test_fn', default= "lip_K_5_M_04_C955_A_012_9.mp4")
    parser.add_argument('--face_predictor_path', default= "/home/aiv-gpu-019/shape_predictor_68_face_landmarks.dat")
    parser.add_argument('--mean_face_path', default= "/home/aiv-gpu-019/20words_mean_face.npy")
    args=parser.parse_args()
    
    print('Generate mouth from mp4 file..\n')
    
    face_predictor_path = args.face_predictor_path
    mean_face_path = args.mean_face_path

    print(f'face_predictor_path:{face_predictor_path}\n')
    print(f'mean_face_path:{mean_face_path}\n')

    if (os.path.exists(face_predictor_path) == False) or (os.path.exists(mean_face_path) == False):
        print('cannot find face predictor path or mean face path')
    
    def generate_mouth(fd, path):
        if (os.path.exists(os.path.join(fd,path)) == False) and ('.mp4' not in path):
            print('cannot find .mp4 file') 
            return
    
        subfile =  os.path.join(fd, path)
        print(f'Find {path} in {fd}\n')
        origin_clip_path = subfile
        
        if os.path.isdir(os.path.join(fd,'mouth')) ==False:
            
            print(f'Generate mouth folder in {fd}, mouth video will be generated in here\n')
            os.mkdir(os.path.join(fd,'mouth'))
        
        mouth_roi_path  = os.path.join(fd,'mouth', path)
       
        preprocess_video(origin_clip_path, mouth_roi_path, face_predictor_path, mean_face_path)

    generate_mouth(args.test_dir, args.test_fn)

    print('End of generating mouth video')

