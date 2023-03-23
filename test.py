import time
import picamera
from PIL import Image

# Load the logo image
logo = Image.open('MF.png')

# Take a photo with the PiCamera
with picamera.PiCamera() as camera:
    camera.start_preview()
    time.sleep(2)  # Give the camera time to adjust to lighting
    camera.capture('photo.jpg')
    camera.stop_preview()

# Open the photo and resize the logo to fit on top
photo = Image.open('photo.jpg')
logo_resized = logo.resize((300, 300))  # Adjust size as needed

# Paste the logo onto the photo
photo.paste(logo_resized, (600, 600), logo_resized)

# Save the new photo with the logo
photo.save('photo_with_logo.jpg')
