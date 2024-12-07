import os
import cv2
import numpy as np
from skimage import feature

# Fungsi untuk menghitung fitur HOG dari gambar
def compute_hog_features(image):
    # Mengonversi gambar ke grayscale
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Resize gambar untuk HOG
    image_resized = cv2.resize(image_gray, (128, 64))
    # Menghitung fitur HOG
    hog_features = feature.hog(image_resized, 
                                orientations=9, 
                                pixels_per_cell=(8, 8), 
                                cells_per_block=(2, 2), 
                                visualize=False)
    return hog_features

# Fungsi untuk menyiapkan data pelatihan dari folder (jika perlu diambil dari folder gambar)
def prepare_training_data(folder_path):
    X, y = [], []
    for filename in os.listdir(folder_path):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            image_path = os.path.join(folder_path, filename)
            image = cv2.imread(image_path)
            if image is not None:
                features = compute_hog_features(image)
                X.append(features)
                # Mengambil label dari nama file (misal person_01.jpg => label person)
                label = filename.split('_')[0]
                y.append(label)
            else:
                print(f"Warning: Gagal memuat gambar {filename}")
    return np.array(X), np.array(y)
