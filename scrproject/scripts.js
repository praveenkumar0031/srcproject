const video = document.getElementById('video');
const captureButton = document.getElementById('capture');
const canvas = document.getElementById('canvas');
const photoContainer = document.getElementById('photo-container');

// Check if the browser supports getUserMedia
if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    // Request access to the webcam
    navigator.mediaDevices.getUserMedia({ video: true })
        .then((stream) => {
            // Assign the stream to the video element's srcObject
            video.srcObject = stream;
        })
        .catch((error) => {
            console.error("Error accessing the webcam: ", error);
        });
} else {
    alert("getUserMedia not supported in this browser.");
}

// Capture the photo when the button is clicked
captureButton.addEventListener('click', () => {
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const context = canvas.getContext('2d');
    context.drawImage(video, 0, 0);
    
    // Convert the canvas to an image and display it
    const img = document.createElement('img');
    img.src = canvas.toDataURL('image/png');
    photoContainer.innerHTML = ''; // Clear previous photos
    photoContainer.appendChild(img);
});
