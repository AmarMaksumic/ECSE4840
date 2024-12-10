# file to rename pointclouds by taking the 3 digits and adding 153 to them

import os
import cv2

def resize(folder_path, new_folder_path, prefix):
  # Load all point clouds in the folder
  img_Files = [f for f in os.listdir(folder_path) if f.endswith('.png')]
  print(img_Files)
  i = 0
  for img_file in img_Files:
    print(f"Processing {img_file}...")
    img = cv2.imread(os.path.join(folder_path, img_file))
    img = cv2.resize(img, (224, 224))
    cv2.imwrite(os.path.join(new_folder_path, img_file), img)
    print(f"Flipped {img_file}")
    i += 1

def main():
  normal_folder_path = "G:/My Drive/RPI/Classes/Intro to ML/FInal Project/Data Collection/#nndi"
  resized_folder_path = "G:/My Drive/RPI/Classes/Intro to ML/FInal Project/Data Collection/#nnrdi/"
  resized_prefix = ""

  resize(normal_folder_path, resized_folder_path, resized_prefix)

  # normal_folder_path = "Data Collection/#ndi/HL"
  # resized_folder_path = "Data Collection/#nrdi/"
  # resized_prefix = "nrhangloose"

  # resize(normal_folder_path, resized_folder_path, resized_prefix)

  
  # normal_folder_path = "Data Collection/#ndi/MF"
  # resized_folder_path = "Data Collection/#nrdi/"
  # resized_prefix = "nrmiddlefinger"

  # resize(normal_folder_path, resized_folder_path, resized_prefix)

  
  # # normal_folder_path = "Data Collection/outpeace"
  # # resized_folder_path = "Data Collection/rpeace"

  # # resize(normal_folder_path, resized_folder_path)

  
  # normal_folder_path = "Data Collection/#ndi/Rock"
  # resized_folder_path = "Data Collection/#nrdi/"
  # resized_prefix = "nrrock"

  # resize(normal_folder_path, resized_folder_path, resized_prefix)

  
  # normal_folder_path = "Data Collection/outspiderman"
  # resized_folder_path = "Data Collection/rspiderman"

  # resize(normal_folder_path, resized_folder_path)

main()