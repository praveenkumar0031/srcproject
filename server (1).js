// Load environment variables from .env file
require('dotenv').config();

const express = require('express');
const bodyParser = require('body-parser');
const twilio = require('twilio');
const path = require('path');

const app = express();

// Twilio account credentials from environment variables
const accountSid = process.env.TWILIO_ACCOUNT_SID; // Make sure these variables are in .env
const authToken = process.env.TWILIO_AUTH_TOKEN;
const twilioPhoneNumber = process.env.TWILIO_PHONE_NUMBER;

const classTeacherNumber = process.env.CLASS_TEACHER_NUMBER;
const medicalStaffNumber = process.env.MEDICAL_STAFF_NUMBER;

const client = twilio(accountSid, authToken);

// Serve static files from the public directory
app.use(express.static(path.join(__dirname, 'public')));
app.use(bodyParser.json());

// Function to extract latitude and longitude from the location string
function extractCoordinates(location) {
    const regex = /Latitude:\s*([\d.-]+),\s*Longitude:\s*([\d.-]+)/;
    const match = location.match(regex);
    if (match) {
        return {
            latitude: match[1],
            longitude: match[2],
        };
    }
    return null;
}

// Handle Fire Alarm alert
app.post('/fire-alarm', (req, res) => {
    const location = req.body.location; // Get location from request body
    const coordinates = extractCoordinates(location);
    if (coordinates) {
        const googleMapsLink = `https://www.google.com/maps?q=${coordinates.latitude},${coordinates.longitude}`;
        const messageBody = `Fire alarm alert! Immediate action required. Location: ${location}. View on map: ${googleMapsLink}`;

        client.messages
            .create({
                body: messageBody,
                from: twilioPhoneNumber,
                to: classTeacherNumber,
            })
            .then((message) => {
                console.log(`Fire alarm SMS sent: ${message.sid}`);
                res.status(200).send('Fire alarm alert sent successfully.');
            })
            .catch((error) => {
                console.error(`Error sending Fire alarm SMS: ${error.message}`);
                res.status(500).send('Failed to send Fire alarm alert.');
            });
    } else {
        res.status(400).send('Invalid location format.');
    }
});

// Start the server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
