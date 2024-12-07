# file to rename pointclouds by taking the 3 digits and adding 153 to them

import os
import cv2

def resize(folder_path, new_folder_path):
  # Load all point clouds in the folder
  img_Files = [f for f in os.listdir(folder_path) if f.endswith('.png')]
  print(img_Files)
  for img_file in img_Files:
    print(f"Processing {img_file}...")
    img = cv2.imread(os.path.join(folder_path, img_file))
    img = cv2.resize(img, (224, 224))
    cv2.imwrite(os.path.join(new_folder_path, img_file), img)
    print(f"Flipped {img_file}")

def main():
  normal_folder_path = "Data Collection/outthumbsdown"
  resized_folder_path = "Data Collection/rthumbsdown"

  resize(normal_folder_path, resized_folder_path)

  normal_folder_path = "Data Collection/outhangloose"
  resized_folder_path = "Data Collection/rhangloose"

  resize(normal_folder_path, resized_folder_path)

  
  normal_folder_path = "Data Collection/outmiddlefinger"
  resized_folder_path = "Data Collection/rmiddlefinger"

  resize(normal_folder_path, resized_folder_path)

  
  normal_folder_path = "Data Collection/outpeace"
  resized_folder_path = "Data Collection/rpeace"

  resize(normal_folder_path, resized_folder_path)

  
  normal_folder_path = "Data Collection/outrock"
  resized_folder_path = "Data Collection/rrock"

  resize(normal_folder_path, resized_folder_path)

  
  normal_folder_path = "Data Collection/outspiderman"
  resized_folder_path = "Data Collection/rspiderman"

  resize(normal_folder_path, resized_folder_path)

main()