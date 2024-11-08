import cv2
import os



haar_file = 'haarcascade_frontalface_default.xml'  # Ensure the correct path
datasets = 'datasets'  # Folder name
sub_data = input("Enter your name:")  # Subfolder for a person's name

# Create the directory if it doesn't exist
path = os.path.join(datasets, sub_data)
if not os.path.isdir(path):
    os.makedirs(path)
    print(f"Created directory: {path}")  # Debug info

(width, height) = (130, 100)  # Fixed size for the face image

# Load the Haar Cascade file for face detection
face_cascade = cv2.CascadeClassifier(haar_file)

# Initialize the webcam (try 0 if 1 doesn't work)
webcam = cv2.VideoCapture(0)
if not webcam.isOpened():
    print("Error: Could not open the webcam.")
    exit()

count = 1  # Start counting images
while count <= 100:  # Capture until 100 images are saved
    print(f"Capturing image {count}")
    
    # Capture frame from webcam
    ret, im = webcam.read()
    
    # Check if the frame is successfully captured
    if not ret:
        print("Error: Failed to capture image from webcam.")
        break
    
    # Convert the frame to grayscale
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    
    # Detect faces in the image
    faces = face_cascade.detectMultiScale(gray, 1.3, 4)
    
    # If at least one face is detected
    if len(faces) > 0:
        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (255, 0, 0), 2)  # Draw rectangle around face
            face = gray[y:y + h, x:x + w]  # Extract face region
            face_resize = cv2.resize(face, (width, height))  # Resize to the required size
            
            # Save the captured face
            success = cv2.imwrite(f'{path}/{count}.png', face_resize)
            if success:
                print(f"Image {count}.png saved successfully.")
            else:
                print(f"Error saving image {count}.png.")
            
            count += 1  # Increment count after saving the image
            
            if count > 100:  # Check if the required count is reached
                break  # Exit the inner loop if 30 images have been captured
    
    # Display the image with rectangles
    cv2.imshow('OpenCV', im)
    
    # Exit if 'Esc' key is pressed
    key = cv2.waitKey(10)
    if key == 27:  # ASCII for 'Esc'
        break
# Release the webcam and close windows
webcam.release()
cv2.destroyAllWindows()
