'''
This file takes in a folder to a list of point clouds, and outputs a folder of depth images.
'''
import os
import open3d as o3d
import numpy as np
import matplotlib.pyplot as plt
import cv2

def pointcloud_to_depth_image(pointcloud_file, img_width=640, img_height=480, focal_length=350):
    # Load point cloud
    pcd = o3d.io.read_point_cloud(pointcloud_file)
    points = np.asarray(pcd.points)

    # Extract x, y, z coordinates
    x, y, z = points[:, 0], points[:, 1], points[:, 2]
    print(len(x), len(y), len(z))

    # Project 3D points to 2D (simple perspective projection)
    u = (focal_length * x / z).astype(int) + img_width // 2
    v = (focal_length * y / z).astype(int) + img_height // 2

    # Initialize an image array with maximum possible depth
    depth_image = np.full((img_height, img_width), np.inf)

    # Map depth (z) values to the 2D coordinates
    for i in range(len(z)):
        if 0 <= u[i] < img_width and 0 <= v[i] < img_height:
            # Only keep the closest depth at each pixel
            depth_image[v[i], u[i]] = min(depth_image[v[i], u[i]], z[i])

    # Replace 'inf' values (no points) with a large depth (e.g., max depth in image)
    max_depth = np.nanmax(np.where(np.isinf(depth_image), np.nan, depth_image))
    depth_image[depth_image == np.inf] = max_depth

    # Smooth the depth image using a Gaussian filter
    depth_image = cv2.GaussianBlur(depth_image, (5, 5), 0)



    # In the image, find the mean and variance of the depth values that are between 10000 and 60000
    # This is to remove outliers (e.g., background points) and allow us to scale the depth values by "zooming in" to the second deviation

    # print(depth_image)

    mean_depth = np.mean(depth_image[(depth_image > 0.10000) & (depth_image < 0.60000)])
    std_depth = np.std(depth_image[(depth_image > 0.10000) & (depth_image < 0.60000)])

    # Normalize depth values to mean +/- 2*std for better visualization
    print(f"Mean depth: {mean_depth}, Std depth: {std_depth}")
    
    # if point is less than mean_depth - std_depth, set it to mean_depth - std_depth
    depth_image[depth_image < mean_depth - 1.75*std_depth] = mean_depth - 1.75*std_depth

    # if point is greater than mean_depth + std_depth, set it to mean_depth + std_depth
    depth_image[depth_image > mean_depth + 1.75*std_depth] = mean_depth + 1.75*std_depth



    depth_image = np.clip((depth_image - mean_depth) / (2 * std_depth), -1, 1)

    # Normalize depth values to 0-255 for visualization
    depth_image_normalized = (2**16 * (depth_image / max_depth)).astype(np.uint16)

    # rotate 90 degree
    # depth_image_normalized = np.rot90(depth_image_normalized, k=3)

    # Display the depth image
    cv2.imshow('Depth Image', depth_image_normalized)
    cv2.waitKey(20)

    return depth_image_normalized

def main():
    print("Enter the full path to the folder containing the point clouds.")
    folder_path = "rock" #input("Path to folder: ").strip()

    print("Enter the full path to the folder where you want to save the depth images.")
    output_folder = "outrock" #input("Path to output folder: ").strip()

    print(os.listdir(folder_path))

    # Load all point clouds in the folder
    pcd_files = [f for f in os.listdir(folder_path) if f.endswith('.ply')]
    for pcd_file in pcd_files:
        print(f"Processing {pcd_file}...")
        depth_image = pointcloud_to_depth_image(os.path.join(folder_path, pcd_file))

        # Save the depth image
        depth_image_file = os.path.join(output_folder, f"{pcd_file[:-4]}.png")
        cv2.imwrite(depth_image_file, depth_image)

        print(f"Depth image saved to {depth_image_file}")

main()