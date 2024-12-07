import open3d as o3d
import os
import sys

def cycle_point_clouds(folder_path):
    ply_files = [f for f in os.listdir(folder_path) if f.endswith('.ply')]
    if not ply_files:
        print(f"No .ply files found in {folder_path}.")
        return

    index = 54
    while True:
        file_path = os.path.join(folder_path, ply_files[index])
        print(f"Loading point cloud from {file_path}...")
        point_cloud = o3d.io.read_point_cloud(file_path)

        if point_cloud.is_empty():
            print(f"Point cloud in {file_path} is empty or invalid.")
        else:
            print("Displaying point cloud. Use mouse and keyboard to navigate.")
            o3d.visualization.draw_geometries([point_cloud],
                                                window_name="Point Cloud Viewer",
                                                width=1200,
                                                height=900,
                                                left=50,
                                                top=50,
                                                point_show_normal=False)
        index+=1




def rename_files_in_folder(folder_path):
    new_number = int(input("Enter the starting number: "))
    new_folder = input("Enter the new folder name: ")
    new_folder_path = os.path.join("G:/My Drive/RPI/Classes/Intro to ML/FInal Project/", new_folder)

    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)

    for file in os.listdir(folder_path):
        if file.endswith(".ply"):
            old_file_path = os.path.join(folder_path, file)
            base_name, ext = os.path.splitext(file)
            if ext == ".ply":
                new_file_name = f"pointcloud_{new_number:03d}.ply"
                new_file_path = os.path.join(new_folder_path, new_file_name)
                os.rename(old_file_path, new_file_path)
                print(f"Renamed {old_file_path} to {new_file_path}")
                new_number += 1

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "rename":
        folder_path = input("Enter the full path to the folder containing .ply files: ").strip()
        rename_files_in_folder(folder_path)
    else:
        folder_path = input("Enter the full path to the folder containing .ply files: ").strip()
        cycle_point_clouds(folder_path)

if __name__ == "__main__":
    main()
