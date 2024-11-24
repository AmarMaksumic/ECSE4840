import open3d as o3d
import os

def load_and_visualize_ply(file_path):

    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist.")
        return

    print(f"Loading point cloud from {file_path}...")
    point_cloud = o3d.io.read_point_cloud(file_path)

    if point_cloud.is_empty():
        print(f"Point cloud in {file_path} is empty or invalid.")
        return

    print("Displaying point cloud. Use mouse and keyboard to navigate.")
    o3d.visualization.draw_geometries([point_cloud],
                                      window_name="Point Cloud Viewer",
                                      width=800,
                                      height=600,
                                      left=50,
                                      top=50,
                                      point_show_normal=False)

def main():
    print("Enter the full path to the .ply file you want to view.")
    file_path = input("Path to .ply file: ").strip()

    load_and_visualize_ply(file_path)

if __name__ == "__main__":
    main()
