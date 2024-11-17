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



def preprocess_video(input_video_path, output_video_path, face_predictor_path, mean_face_path, output_data_path = '.'):
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
  parser.add_argument('--test_dir', default= "/home/aiv-gpu-019/data-small")
  parser.add_argument('--face_predictor_path', default= "/home/aiv-gpu-019/shape_predictor_68_face_landmarks.dat")
  parser.add_argument('--mean_face_path', default= "/home/aiv-gpu-019/20words_mean_face.npy")
  args=parser.parse_args()


  face_predictor_path = args.face_predictor_path
  mean_face_path = args.mean_face_path


  fd = args.test_dir

  fd_1 = os.listdir(fd)

  fns = len(os.listdir(fd))


  for idx in tqdm(range(len(os.listdir(fd)))):
    fn = fd_1[idx]

    if os.path.isdir(os.path.join(fd,fn)):
        continue
    elif '.mp4' not in fn:
        continue
    else:
      subfile =  os.path.join(fd, fn)
      origin_clip_path = subfile

      if os.path.isdir(os.path.join(fd,'mouth')) ==False:
        os.mkdir(os.path.join(fd,'mouth'))

      mouth_roi_path  = os.path.join(fd,'mouth', fn)
      output_path = os.path.join(fd, 'mouth', fn[:-4])
      preprocess_video(origin_clip_path, mouth_roi_path, face_predictor_path, mean_face_path,output_path)

