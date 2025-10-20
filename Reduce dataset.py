import os
import random

# Define paths
train_images_dir = r'C:\Users\mahmo\Downloads\AI-Product detect & search\Grocery Dataset.v5-resized640x640_aug3x.yolov12\train\images'
train_labels_dir = r'C:\Users\mahmo\Downloads\AI-Product detect & search\Grocery Dataset.v5-resized640x640_aug3x.yolov12\train\labels'

# Get all image filenames
image_files = [f for f in os.listdir(train_images_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

# Determine number to delete (50%)
num_to_delete = len(image_files) // 2
files_to_delete = random.sample(image_files, num_to_delete)

print(f"Total images: {len(image_files)}")
print(f"Deleting {num_to_delete} images and corresponding labels...")

# Delete selected images and their corresponding labels
for img_file in files_to_delete:
    img_path = os.path.join(train_images_dir, img_file)
    label_name = os.path.splitext(img_file)[0] + '.txt'
    label_path = os.path.join(train_labels_dir, label_name)

    # Remove image
    if os.path.exists(img_path):
        os.remove(img_path)
        print(f"Removed image: {img_path}")

    # Remove corresponding label
    if os.path.exists(label_path):
        os.remove(label_path)
        print(f"Removed label: {label_path}")

print("Deletion completed successfully.")
