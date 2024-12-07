# file to move all images to one folder
import os

def rename_pointclouds(folder_path):
  # Load all folders in the folder
  folders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]
  for folder in folders:
    # Load all images in the folder
    img_files = [f for f in os.listdir(os.path.join(folder_path, folder)) if f.endswith('.png')]
    for img_file in img_files:
      print(f"Processing {img_file}...")
      os.rename(os.path.join(folder_path, folder, img_file), os.path.join(folder_path, folder + img_file))
      print(f"Moved {img_file} to {folder_path}")
    

def main():
  folder_path = "Data Collection/#rdi"

  rename_pointclouds(folder_path)

main()