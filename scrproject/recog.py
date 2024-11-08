import cv2
import numpy as np
import os

# Constants
size = 4
haar_file = 'haarcascade_frontalface_default.xml'
datasets = 'datasets'  # Directory where dataset is stored

print('Training...')

# Initialize data structures
(images, labels, names, id) = ([], [], {}, 0)
for (subdirs, dirs, files) in os.walk(datasets):
    for subdir in dirs:
        names[id] = subdir  # Map user IDs to names
        subjectpath = os.path.join(datasets, subdir)
        for filename in os.listdir(subjectpath):
            path = os.path.join(subjectpath, filename)
            label = id
            images.append(cv2.imread(path, 0))  # Read image in grayscale
            labels.append(int(label))  # Append the label (user ID)
        id += 1

# Check if dataset contains images and labels
if len(images) == 0 or len(labels) == 0:
    print("Error: No images or labels found in the dataset.")
    exit()

(width, height) = (130, 100)

# Convert images and labels to NumPy arrays
(images, labels) = [np.array(lis) for lis in [images, labels]]

# Train the model using LBPHFaceRecognizer
model = cv2.face.LBPHFaceRecognizer_create()
model.train(images, labels)

# Load the face detection classifier
face_cascade = cv2.CascadeClassifier(haar_file)

# Start the webcam
webcam = cv2.VideoCapture(0)

# Check if webcam opened successfully
if not webcam.isOpened():
    print("Error: Could not open webcam.")
    exit()

cnt = 0
while True:
    # Capture frame from webcam
    ret, im = webcam.read()
    if not ret:
        print("Error: Failed to capture image from webcam.")
        break

    # Convert the frame to grayscale
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    print(f"Faces detected: {len(faces)}")  # Debugging: print number of faces detected

    for (x, y, w, h) in faces:
        # Draw a rectangle around each detected face
        cv2.rectangle(im, (x, y), (x + w, y + h), (255, 255, 0), 2)

        # Extract and resize the face for recognition
        face = gray[y:y + h, x:x + w]
        face_resize = cv2.resize(face, (width, height))

        # Predict the identity of the face
        prediction = model.predict(face_resize)

        # Define confidence threshold for "Unknown" classification
        confidence_threshold = 80  # Adjust this threshold based on model performance

        # If the prediction confidence is lower than the threshold, recognize the user
        if prediction[1] < confidence_threshold:
            name = names[prediction[0]]
            confidence = prediction[1]
            cv2.putText(im, f'{name} ', (x-10, y-10), cv2.FONT_HERSHEY_COMPLEX, 1, (51, 255, 255))#- {confidence:.0f}
            print(f"Recognized: {name}, Confidence: {confidence}")
            cnt = 0
        else:
            # If confidence is higher than threshold, classify as "Unknown"
            cnt += 1
            cv2.putText(im, 'Unknown', (x-10, y-10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))
            print("Unknown Person Detected")
            # Optionally save the unknown face image
            if cnt > 100:
                cv2.imwrite("unknown.jpg", im)  # Save the image of the unknown person
                cnt = 0

    # Display the frame with the results
    cv2.imshow('Face Recognition', im)

    # Break loop on 'ESC' or 'Q' key
    key = cv2.waitKey(10)
    if key == 27 or key == ord('q'):  # ESC key or 'Q' key to stop
        break

# Release the webcam and close all windows
webcam.release()
cv2.destroyAllWindows()
