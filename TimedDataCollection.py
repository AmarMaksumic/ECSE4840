import pyrealsense2 as rs
import numpy as np
import open3d as o3d
import time
import os
from datetime import datetime

def save_point_cloud(depth_frame, intrinsics, output_filename, output_dir, max_distance=0.7):

    # Convert depth frame to numpy array
    depth_image = np.asanyarray(depth_frame.get_data())

    # Generate 3D point cloud from the depth image
    pc = o3d.geometry.PointCloud()
    points = []

    for y in range(depth_image.shape[0]):
        for x in range(depth_image.shape[1]):
            depth = depth_image[y, x] * depth_frame.get_units()  # Convert depth to meters
            
            if depth < max_distance:
                # Convert (x, y, depth) to 3D point
                point = rs.rs2_deproject_pixel_to_point(intrinsics, [x, y], depth)
                points.append(point)

    pc.points = o3d.utility.Vector3dVector(np.array(points))

    # Save point cloud to file in the new directory
    output_filepath = os.path.join(output_dir, output_filename)
    o3d.io.write_point_cloud(output_filepath, pc)

def main():

    # Create new directory based on the current date and time
    current_time = datetime.now().strftime("%b%d_%H%M%S")
    output_dir = os.path.join(os.getcwd(), current_time)
    os.makedirs(output_dir, exist_ok=True)

    # Configure RealSense pipeline
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

    # filters = [rs.disparity_transform(),
    #        rs.spatial_filter(),
    #        rs.temporal_filter(),
    #        rs.disparity_transform(False)]
    
    # decimate = rs.decimation_filter()
    # decimate.set_option(rs.option.filter_magnitude, 1) # Edit 0 to decimate


    # Start streaming
    pipeline.start(config)

    try:
        print("Starting to capture point clouds. Press Ctrl+C to stop.")
        count = 0
        while True:
            # Wait for a frame
            frames = pipeline.wait_for_frames()
            depth_frame = frames.get_depth_frame()

            # depth_frame = decimate.process(depth_frame)
            
            # # Apply filters
            # for filter in filters:
            #     depth_frame = filter.process(depth_frame)

            if not depth_frame:
                continue

            # Get camera intrinsics
            intrinsics = depth_frame.profile.as_video_stream_profile().intrinsics

            # Save point cloud
            output_filename = f"pointcloud_{count:03d}.ply"
            save_point_cloud(depth_frame, intrinsics, output_filename, output_dir)
            print(f"Saved {output_filename}")

            count += 1
            time.sleep(2)  # Change this to adjust sampling frequency. Most likely cannot go shorter than 1 second.

    except KeyboardInterrupt:
        print("Stopping capture.")
    finally:
        pipeline.stop()

if __name__ == "__main__":
    main()
