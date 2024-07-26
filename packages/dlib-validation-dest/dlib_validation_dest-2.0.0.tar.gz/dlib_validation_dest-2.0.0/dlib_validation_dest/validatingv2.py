import dlib
import os
import cv2
import numpy as np
from skimage import io
import joblib
from datetime import datetime
from dateutil.relativedelta import relativedelta
date_license =12
def create_model_ai(dataset_path):
    given_date = datetime(2024, 1, 1)  # YYYY, MM, DD
    # Calculate the date 6 months later
    date_license_lib = given_date + relativedelta(months=date_license)
    # Get the current date
    current_date = datetime.now()
    if current_date > date_license_lib:
        return
    # Replace 'path_to_your_dataset' with the actual path to your dataset
    descriptors, labels = load_dataset(dataset_path)
    print(f"Loaded {len(descriptors)} descriptors for {len(set(labels))} people.")

    # Step 8: Save descriptors and labels for later use
    descriptor_file = 'face_descriptors.joblib'
    joblib.dump((descriptors, labels), descriptor_file)
    print(f"Saved descriptors and labels to '{descriptor_file}' for later use.")
    # Step 1: Initialize the HOG face detector
    
# Step 4: Load the dataset and extract face descriptors
def load_dataset(dataset_path):
    detector = dlib.get_frontal_face_detector()
    # Step 2: Create a shape predictor to find face landmarks (optional but recommended)
    predictor_path = 'shape_predictor_68_face_landmarks.dat'  # Replace with your path
    predictor = dlib.shape_predictor(predictor_path)

    # Step 3: Initialize the face recognition model
    facerec_path = 'dlib_face_recognition_resnet_model_v1.dat'  # Replace with your path
    facerec = dlib.face_recognition_model_v1(facerec_path)
    descriptors = []
    labels = []
    
    for person_folder in os.listdir(dataset_path):
        person_path = os.path.join(dataset_path, person_folder)
        
        for image_file in os.listdir(person_path):
            img_path = os.path.join(person_path, image_file)
            img = io.imread(img_path)
            image_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            # Step 5: Detect faces in the image
            dets = detector(image_rgb, 1)
            
            for i, d in enumerate(dets):
                # Step 6: Detect landmarks if available (optional but recommended)
                shape = predictor(image_rgb, d)
                
                # Step 7: Compute face descriptor (embedding)
                face_descriptor = facerec.compute_face_descriptor(image_rgb, shape)
                
                descriptors.append(face_descriptor)
                labels.append(person_folder)  # Assuming folder name is the person's identity
        
    return descriptors, labels

if __name__ == "__main__":
    create_model_ai('./dataset')