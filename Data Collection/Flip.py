# file to rename pointclouds by taking the 3 digits and adding 153 to them

import os
import cv2

def flip(folder_path, new_folder_path):
  # Load all point clouds in the folder
  img_Files = [f for f in os.listdir(folder_path) if f.endswith('.png')]
  print(img_Files)
  for img_file in img_Files:
    print(f"Processing {img_file}...")
    img = cv2.imread(os.path.join(folder_path, img_file))
    img = cv2.flip(img, 0)
    cv2.imwrite(os.path.join(new_folder_path, img_file), img)
    print(f"Flipped {img_file}")

def main():
  normal_folder_path = "outthumbsup"
  flipped_folder_path = "outthumbsdown"

  flip(normal_folder_path, flipped_folder_path)

main()