# file to rename pointclouds by taking the 3 digits and adding 153 to them

import os

def rename_pointclouds(folder_path):

    # Load all point clouds in the folder
    pcd_files = [f for f in os.listdir(folder_path) if f.endswith('.ply')]
    for pcd_file in pcd_files:
        print(f"Processing {pcd_file}...")
        new_name = pcd_file[:11] + str(int(pcd_file[11:14]) + 157) + pcd_file[14:]
        os.rename(os.path.join(folder_path, pcd_file), os.path.join(folder_path, new_name))
        print(f"Renamed {pcd_file} to {new_name}")

def main():
    print("Enter the full path to the folder containing the point clouds.")
    folder_path = "Dec06_211933" #input("Path to folder: ").strip()

    rename_pointclouds(folder_path)

main()