#! /usr/bin/python3
import time
from datetime import date
import picamera
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import configparser
import tkinter as tk
from tkinter import messagebox
import time

from PIL import Image, ImageTk

config = configparser.ConfigParser()
config.read('config.ini')

smtp_server = config.get('smtp2go', 'server')
smtp_port = config.getint('smtp2go', 'port')
smtp_username = config.get('smtp2go', 'username')
smtp_password = config.get('smtp2go', 'password')
sender_email = config.get('smtp2go', 'email')

def capture_images(num_images):
    logo = Image.open('MF.png')
    with picamera.PiCamera() as camera:
        camera.resolution = (1920, 1080)
        #play with low light
    
        camera.start_preview()
        camera.annotate_text_size = 120

        # Add a brief delay to allow the camera to adjust to lighting
        time.sleep(2)
        image_files = []
        for i in range(num_images):
            # Show a countdown before taking the picture
            for countdown in [3, 2, 1]:
                camera.annotate_text = str(countdown)
                time.sleep(1)
            camera.annotate_text = ''
            # Set the file name to "MakerFaire" and append the current date
            today = date.today().strftime("%Y-%m-%d")
            image_file = f'pics/MakerFaire_{today}_{i}.jpg'
            #image_file = f'MakerFaire_{today}_{i}.jpg'
            camera.capture(image_file)
            image_files.append(image_file)
            camera.annotate_text = ''
            # Open the photo and resize the logo to fit on top
            photo = Image.open(image_file)
            logo_resized = logo.resize((495, 388))  # Adjust size as needed

            # Paste the logo onto the photo
            photo.paste(logo_resized, (1330, 660), logo_resized)

            # Save the new photo with the logo
            photo.save(image_file)
            
            
    return image_files

def send_email(recipient_email, image_files):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = 'Maker Faire Booth Pictures'

    body = 'Thanks for stopping by the Maker Faire Miami photo booth! We hope you enjoyed exploring all the amazing projects and ideas on display. As a special thank you, we\’re sending you a few of your favorite photos from the booth. Don\’t forget to share your Maker Faire Miami experience with your friends and followers! Tag us in your posts using @makerfairemiami, #MFM2023 and #MakerFaireMiami, and show the world your love for creativity, innovation, and DIY projects. We look forward to seeing you at the next Maker Faire Miami event!\n'
    msg.attach(MIMEText(body))

    # Attach the captured images to the email with their original file names
    for image_file in image_files:
        with open(image_file, 'rb') as f:
            # Get the file extension from the image file name
            file_ext = image_file.split('.')[-1]
            # Set the image type based on the file extension
            if file_ext.lower() == 'jpg':
                img_type = 'jpeg'
            else:
                img_type = file_ext.lower()

            # Create the MIMEImage object with the correct image type and original file name
            img = MIMEImage(f.read(), _subtype=img_type)
            img.add_header('Content-Disposition', 'attachment', filename=image_file)
            msg.attach(img)

    # Send the email using SMTP2GO
    with smtplib.SMTP(smtp_server, smtp_port) as smtp:
        smtp.login(smtp_username, smtp_password)
        smtp.send_message(msg)

    print(f"Email sent to {recipient_email}!")

def on_send_email():
    recipient_email = entry_email.get()
    if not recipient_email:
        messagebox.showerror('Error', 'Please enter an email address.')
        return
    image_files = capture_images(3)
    try:
        send_email(recipient_email, image_files)
        messagebox.showinfo('Success', f'Email sent to {recipient_email}!')
    except Exception as e:
        messagebox.showerror('Error', f'Failed to send email: {e}')
    entry_email.delete(0, 'end')

# Create the main window and widgets

window = tk.Tk()
window.title('Photo Booth')



# Create a label widget with the text "Welcome to Maker Faire Miami"
label_welcome = tk.Label(window, text='Welcome to Maker Faire Miami Photo Booth', font=('Helvetica',20,'bold'))
label_welcome.pack(pady=10, fill=tk.BOTH, expand=True, anchor=tk.CENTER)

# Create a label widget with the text "Welcome to Maker Faire Miami"
label_welcome = tk.Label(window, text='Made by ', font=('Helvetica',20,'bold'))
label_welcome.pack(pady=10, fill=tk.BOTH, expand=True, anchor=tk.CENTER)

# Load the image and create a PhotoImage object
image = Image.open("mtm.png")
photo = ImageTk.PhotoImage(image)

# Create a label widget to display the image
label_image = tk.Label(window, image=photo)
label_image.pack(pady=10)

# Create a label widget with the text "Recipient Email:"
label_email = tk.Label(window, text='Enter up to 4 Emails seperated by comas click Send Email step back take some Pics:', font=('Helvetica',15,'bold'))
label_email.pack(fill=tk.BOTH, expand=True, anchor=tk.CENTER)
label_email = tk.Label(window, text='example@test.com,Woody@toystory.com', font=('Helvetica',15,'bold'))
label_email.pack(fill=tk.BOTH, expand=True, anchor=tk.CENTER)

# Create an entry widget for the email input 
entry_email = tk.Entry(window)
entry_email.pack(padx=40, pady=20,fill=tk.BOTH, expand=False, anchor=tk.CENTER)

# Create a button widget to send the email
#button_send_email = tk.Button(window, text='Send Email', font=('Helvetica',15,'bold'), command=on_send_email)
#button_send_email.pack(padx=40, pady=20,fill=tk.BOTH, expand=True, anchor=tk.CENTER)

# Create a button widget to send the email
button_send_email = tk.Button(window, text='Send Email', font=('Helvetica', 15, 'bold'), command=on_send_email, bg='blue', fg='white')
button_send_email.pack(padx=40, pady=20, fill=tk.BOTH, expand=True, anchor=tk.CENTER)

# Bind the 'Return' key to the button's click function
#window.bind('<Return>', lambda event: button_send_email.invoke())



# Set the window size and center it on the screen
window.geometry('1024x768')
window.eval('tk::PlaceWindow . center')

#window.attributes('-fullscreen', True)



# Start the main event loop
window.mainloop()


