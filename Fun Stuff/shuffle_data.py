import os
import shutil
import random
from collections import defaultdict
import csv

def split_dataset_and_create_csv(main_dir, output_dir, classes, ratio, seed=None):
    """
    Split images into training and test directories based on a ratio, and generate corresponding CSV files.

    Args:
        main_dir (str): Path to the directory containing all image files.
        output_dir (str): Path to the directory to create training and test subdirectories.
        classes (list): List of file prefixes representing the classes.
        ratio (float): Ratio of training data (e.g., 0.8 for 80% training, 20% test).
        seed (int, optional): Seed for randomization.
    """
    if seed is not None:
        random.seed(seed)

    # Create output directories
    train_dir = os.path.join(output_dir, "training")
    test_dir = os.path.join(output_dir, "test")
    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(test_dir, exist_ok=True)

    # Map classes to indices and collect files
    class_to_index = {cls: idx + 1 for idx, cls in enumerate(classes)}
    images_by_class = defaultdict(list)

    for filename in os.listdir(main_dir):
        for cls in classes:
            if filename[1:].startswith(cls) or filename[2:].startswith(cls):
                images_by_class[cls].append(os.path.join(main_dir, filename))
                break

    # Split and copy files
    train_data = []
    test_data = []

    for cls, images in images_by_class.items():
        random.shuffle(images)
        split_point = int(len(images) * ratio)
        train_images = images[:split_point]
        test_images = images[split_point:]

        # Copy files and collect data for CSVs
        for img_path in train_images:
            dest_path = os.path.join(train_dir, os.path.basename(img_path))
            shutil.copy(img_path, dest_path)
            train_data.append((os.path.basename(img_path), class_to_index[cls]))

        for img_path in test_images:
            dest_path = os.path.join(test_dir, os.path.basename(img_path))
            shutil.copy(img_path, dest_path)
            test_data.append((os.path.basename(img_path), class_to_index[cls]))

    # Create CSVs
    def create_csv(data, csv_path):
        with open(csv_path, mode="w", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["filename", "class_#"])
            writer.writerows(data)

    create_csv(train_data, os.path.join(output_dir, "training.csv"))
    create_csv(test_data, os.path.join(output_dir, "test.csv"))

    print(f"Data split and CSVs created at {output_dir}")

def redistribute_images(old_dir1, old_dir2, new_dir1, new_dir2, classes, seed=None):
    """
    Create new directories with the same class breakdown as the old directories,
    but randomize the image selection from the combined set of images.

    Args:
        old_dir1 (str): Path to the first source directory.
        old_dir2 (str): Path to the second source directory.
        new_dir1 (str): Path for the new directory for the first source.
        new_dir2 (str): Path for the new directory for the second source.
        classes (list): List of file prefixes representing the classes.
        seed (int, optional): Seed for randomization.
    """
    if seed is not None:
        random.seed(seed)

    # Create new directories
    os.makedirs(new_dir1, exist_ok=True)
    os.makedirs(new_dir2, exist_ok=True)

    # Collect images by class
    def collect_images(directory):
        images_by_class = defaultdict(list)
        for filename in os.listdir(directory):
            for cls in classes:
                if filename[1:].startswith(cls) or filename[2:].startswith(cls):
                    images_by_class[cls].append(os.path.join(directory, filename))
                    break
        return images_by_class

    images_dir1 = collect_images(old_dir1)
    images_dir2 = collect_images(old_dir2)

    # Combine images by class from both directories
    combined_images_by_class = {
        cls: images_dir1[cls] + images_dir2[cls] for cls in classes
    }

    # Get original breakdowns for each directory
    breakdown_dir1 = {cls: len(images_dir1[cls]) for cls in classes}
    breakdown_dir2 = {cls: len(images_dir2[cls]) for cls in classes}

    # Randomly select images for the new directories based on the breakdown
    for cls in classes:
        combined_images = combined_images_by_class[cls]
        random.shuffle(combined_images)

        # Select images for new_dir1 and new_dir2 based on the original counts
        selected_for_dir1 = combined_images[:breakdown_dir1[cls]]
        selected_for_dir2 = combined_images[breakdown_dir1[cls]:breakdown_dir1[cls] + breakdown_dir2[cls]]

        # Copy files to the new directories
        for img_path in selected_for_dir1:
            shutil.copy(img_path, os.path.join(new_dir1, os.path.basename(img_path)))
        for img_path in selected_for_dir2:
            shutil.copy(img_path, os.path.join(new_dir2, os.path.basename(img_path)))

    print(f"New directories created at:\n{new_dir1}\n{new_dir2}")


def create_csv_from_directories(dir_path, csv_path, classes):
    """
    Create a CSV file listing the filenames and their corresponding class numbers.

    Args:
        dir_path (str): Path to the directory containing the image files.
        csv_path (str): Path to save the CSV file.
        classes (list): List of file prefixes representing the classes.
    """
    class_to_index = {cls: idx + 1 for idx, cls in enumerate(classes)}  # Map classes to indices
    data = []

    # Collect file information
    for filename in os.listdir(dir_path):
        for cls in classes:
            if filename[1:].startswith(cls) or filename[2:].startswith(cls):
                data.append((filename, class_to_index[cls]))
                break

    # Write to CSV
    with open(csv_path, mode="w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["filename", "class_#"])
        writer.writerows(data)

    print(f"CSV file created at {csv_path}")



def main():
    old_directory1 = "G:/My Drive/RPI/Classes/Intro to ML/FInal Project/Fun Stuff/#test"
    old_directory2 = "G:/My Drive/RPI/Classes/Intro to ML/FInal Project/Fun Stuff/#train"
    new_directory1 = "G:/My Drive/RPI/Classes/Intro to ML/FInal Project/Fun Stuff/120924_2"
    new_directory2 = "G:/My Drive/RPI/Classes/Intro to ML/FInal Project/Fun Stuff/#randomized_train"
    total_dir = "G:/My Drive/RPI/Classes/Intro to ML/FInal Project/Fun Stuff/#total"
    image_classes = ["hangloose", "middlefinger", "peace", "rock", "spiderman", "thumbsup"]  # Add all class prefixes here

    # redistribute_images(old_directory1, old_directory2, new_directory1, new_directory2, image_classes, seed=42)
    
    split_dataset_and_create_csv(total_dir, new_directory1, image_classes, 0.65, seed=10)

    # csv_path1 = "G:/My Drive/RPI/Classes/Intro to ML/FInal Project/Fun Stuff/#randomized_test/data.csv"
    # csv_path2 = "G:/My Drive/RPI/Classes/Intro to ML/FInal Project/Fun Stuff/#randomized_train/data.csv"

    # create_csv_from_directories(new_directory1, csv_path1, image_classes)
    # create_csv_from_directories(new_directory2, csv_path2, image_classes)
    
if __name__ == "__main__":
    main()