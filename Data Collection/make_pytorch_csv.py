# take in a directory of images and create a csv file for pytorch dataloader

import os
import csv

def make_csv(folder_path, csv_file):
  # Load all images in the folder
  img_files = [f for f in os.listdir(folder_path) if f.endswith('.png')]
  with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['image', 'label'])
    for img_file in img_files:
      label = -1
      if "thumbsdown" in img_file:
        label = 0
      elif "hangloose" in img_file:
        label = 1
      elif "middlefinger" in img_file:
        label = 2
      elif "peace" in img_file:
        label = 3
      elif "rock" in img_file:
        label = 4
      elif "spiderman" in img_file:
        label = 5
      elif "thumbsup" in img_file:
        label = 6
      writer.writerow([img_file, label])
  
  print(f"CSV file saved to {csv_file}")

def main():
  folder_path = "Data Collection/#rdi"
  csv_file = "Data Collection/#rdi/data.csv"

  make_csv(folder_path, csv_file)

main()