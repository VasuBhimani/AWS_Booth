import base64
from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import threading
import time
import json
import requests
from email.message import EmailMessage
import ssl
import smtplib
import mysql.connector


from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# global user_no
# user_no = None

@app.route('/')
def index():
    return render_template('loading.html')
#-----------------------------------------------------------------------------------------------
# Save the image locally when the POST request is made


@app.route('/save-image', methods=['POST'])
def save_image():
    data = request.json
    print("Received request data")

    # Extract base64 part of the image
    image_data = data['image'].split(",")[1]  # Assumes data:image/jpeg;base64,xxxx
    image_path = os.path.join('static', 'captured_image.jpg')
    
    # Save the image to the local folder
    with open(image_path, 'wb') as f:
        f.write(base64.b64decode(image_data))
    print(f"Image saved to {image_path}")

    # Prepare API call to Segmind
    api_key = "SG_c2323b49cd816bb0"
    url = "https://api.segmind.com/v1/instantid"
    
    # Convert the saved image to base64
    b64_image = to_base64(image_path)  
    print("Image converted to base64")

    # Payload for Segmind API
    payload = {
        "prompt": "photo of a man",
        "face_image": b64_image,
        "negative_prompt": "lowquality, badquality, sketches",
        "style": "Vibrant Color",
        "samples": 1,
        "num_inference_steps": 10,
        "guidance_scale": 5,
        "seed": 354849415,
        "identity_strength": 0.8,
        "adapter_strength": 0.8,
        "enhance_face_region": True,
        "base64": False
    }

    headers = {
        'x-api-key': api_key
    }

    # Send the API request
    response = requests.post(url, json=payload, headers=headers)

    print("Sent API request, waiting for response...")
    
    # Check the response content type
    if response.status_code == 200:
        content_type = response.headers.get('Content-Type')

        if 'application/json' in content_type:
            # Handle JSON response
            try:
                result = response.json()
                print("API call successful, response received")
                return jsonify({"status": "success", "data": result})
            except ValueError:
                print("Error decoding JSON:", response.text)
                return jsonify({"status": "error", "message": "Invalid JSON response"}), 500
        elif 'image' in content_type:
            # Handle binary image response
            with open('static/processed_image.jpg', 'wb') as img_file:
                img_file.write(response.content)
            print("Image saved as processed_image.jpg")
            print(url_for('output'))  # Check the generated URL

# Create a dictionary with a key-value pair
            data = {
                "status": "image is ready"
            }
            # Write the dictionary to the image.json file
            with open('image.json', 'w') as json_file:
                json.dump(data, json_file)
            print("data write inside image file")
            send_email_with_image()


            return "Processing complete. Check the output page for results."
    #     else:
    #         print("Unexpected content type:", content_type)
    #         return jsonify({"status": "error", "message": "Unexpected content type"}), 500
    # else:
    #     print(f"API Error {response.status_code}: {response.text}")
    #     return jsonify({"status": "error", "message": response.text}), response.status_code

# Utility function to convert the saved image to base64
def to_base64(img_path):
    with open(img_path, 'rb') as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

@app.route('/output')
def output():

    with open('image.json', 'w'):
        pass 
    # print(user_no)
    # print(type(user_no))
    # update_flag()
    restart()
    return render_template('output.html')


#------------------------------------------------------------------------------------------------

@app.route('/next_page')
def next_page():
    # with open('request.json', 'w') as json_file:
    #     pass  # This will clear the file without writing anything
    return render_template('loading_animation.html')

#-------------------------------------------------------------------------------------------------

last_received_data = None

@app.route('/webhook', methods=['POST'])
def webhook():
    global last_received_data
    data = request.get_json()
    print(last_received_data)
    print(type(last_received_data))
    if data != last_received_data:
        last_received_data = data
        print(f"Received data: {data}")
        # return jsonify({'status': 'success', 'data': data}), 200
        # return render_template('index.html')
        with open('request.json', 'w') as json_file:
            json.dump(data, json_file)

        with open('request.json', 'r') as file:
            data = json.load(file)
            user_no = data["no"]  # Extract the value of "no"
            print("user no is :---------",user_no)
        return jsonify({'status': 'success', 'data': data}), 200
    else:
        # print("Duplicate data received. Ignoring.")
        return jsonify({'status': 'ignored', 'data': data}), 200


@app.route('/get-request-data', methods=['GET'])
def get_request_data():
    try:
        with open('request.json', 'r') as json_file:
            data = json.load(json_file)
        return jsonify(data)
    except FileNotFoundError:
        return ""
    except json.JSONDecodeError:
        return ""

@app.route('/get-request-data2', methods=['GET'])
def get_request_data2():
    try:
        with open('image.json', 'r') as json_file:
            data = json.load(json_file)
        return jsonify(data)
    except FileNotFoundError:
        return ""
    except json.JSONDecodeError:
        return ""        

@app.route('/get-request-data3', methods=['GET'])
def get_request_data3():
    try:
        with open('request.json', 'r') as json_file:
            data = json.load(json_file)
        return jsonify(data)
    except FileNotFoundError:
        return ""
    except json.JSONDecodeError:
        return ""        

@app.route('/home')
def home():
    print("index page showing")
    with open('request.json','w'):
        pass
    return render_template('index.html')

#--------------------------------------------------------------------------------------------------


import smtplib
import ssl
from email.message import EmailMessage
from email.mime.text import MIMEText

def send_email_with_image():
    # Define email sender and receiver
    email_sender = 'bhimanivasu93@gmail.com'
    email_password = "uptqyffyqspaaqgl"  # Use App Password here
    email_receiver = 'vasubhimani93@gmail.com'

    # Set the subject and body of the email
    subject = 'Check your AVATAR'
    body_html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Your AI-Enhanced Image</title>
        <style>
            body { font-family: Arial, sans-serif; background-color: #f4f4f4; }
            .email-container { max-width: 600px; margin: auto; padding: 20px; background-color: #fff; border-radius: 8px; }
            .header { background-color: #232f3e; padding: 20px; text-align: center; }
            .header img { width: 100px; }
            .header h1 { color: #fff; }
            .content { padding: 20px; text-align: center; }
            .button-container a { background-color: #ff9900; color: #fff; padding: 12px 24px; text-decoration: none; border-radius: 4px; }
            .footer { text-align: center; color: #888; font-size: 12px; margin-top: 20px; }
        </style>
    </head>
    <body>
        <div class="email-container">
            <div class="header">
                <img src="https://d1.awsstatic.com/Identity/AWS_logo_RGB.7fa564d3c99b193e7a9e66a1aa248b4fd3c57b8c.png" alt="AWS Logo">
                <h1>Your AI-Enhanced Image is Ready!</h1>
            </div>
            <div class="content">
                <h2>Hello!</h2>
                <p>Your AI-enhanced image is ready for you to view and download.</p>
                <div class="button-container">
                    <a href="YOUR_DOWNLOAD_LINK_HERE" target="_blank">Download Your Image</a>
                </div>
            </div>
            <div class="footer">
                <p>© 2024 AWS AI Booth. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """

    # Create the email message object
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body_html, subtype="html")

    # Attach the image
    with open('static/processed_image.jpg', 'rb') as img_file:
        img_data = img_file.read()
        em.add_attachment(img_data, maintype='image', subtype='jpeg', filename='image.jpg')

    # Add SSL (layer of security) and send the email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())
        print("Email sent successfully!")



#-------------------------------------------------------------------------------------------------------------------------

# @app.route('/restart', methods=['POST'])
def restart():
    # Send a "hi" message to the target application
    target_url = 'http://localhost:5001/restart'  # Replace with your target URL
    data = {'message': 'hi'}
    print("data is senddddddddddddddddddddddddddddd")
    response = requests.post(target_url, json=data)

    return 'Message sent!', 200

#--------------------------------------------------------------------------------------------------------------------


#---------------------------------------------------------------------------------------------------------------

# body_html = """
# <!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <title>Your AI-Enhanced Image</title>
#     <style>
#         body {
#             font-family: Arial, sans-serif;
#             margin: 0;
#             padding: 0;
#             background-color: #f4f4f4;
#         }
#         .email-container {
#             max-width: 600px;
#             margin: 20px auto;
#             background-color: #fff;
#             padding: 20px;
#             border-radius: 8px;
#             box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
#         }
#         .header {
#             text-align: center;
#             background-color: #232f3e;
#             padding: 20px;
#             border-radius: 8px 8px 0 0;
#         }
#         .header img {
#             width: 100px;
#         }
#         .header h1 {
#             color: #fff;
#             font-size: 24px;
#             margin-top: 10px;
#         }
#         .content {
#             padding: 20px;
#             text-align: center;
#         }
#         .content h2 {
#             color: #333;
#             font-size: 22px;
#         }
#         .content p {
#             color: #555;
#             font-size: 16px;
#         }
#         .content img {
#             width: 100%;
#             max-width: 400px;
#             margin: 20px 0;
#         }
#         .button-container {
#             text-align: center;
#             margin-top: 20px;
#         }
#         .button-container a {
#             background-color: #ff9900;
#             color: #fff;
#             padding: 12px 24px;
#             text-decoration: none;
#             border-radius: 4px;
#             font-size: 16px;
#         }
#         .footer {
#             text-align: center;
#             color: #888;
#             font-size: 12px;
#             margin-top: 20px;
#         }
#     </style>
# </head>
# <body>

# <div class="email-container">
#     <div class="header">
#         <img src="https://d1.awsstatic.com/Identity/AWS_logo_RGB.7fa564d3c99b193e7a9e66a1aa248b4fd3c57b8c.png" alt="AWS Logo">
#         <h1>Your AI-Enhanced Image is Ready!</h1>
#     </div>

#     <div class="content">
#         <h2>Hello!</h2>
#         <p>Thank you for visiting our AI AWS booth. We've enhanced your image using the latest AI technology, and it's ready for you to view and download.</p>
        

#         <div class="button-container">
#             <a href="YOUR_DOWNLOAD_LINK_HERE" target="_blank">Download Your Image</a>
#         </div>  
#     </div>

#     <div class="footer">
#         <p>© 2024 AWS AI Booth. All rights reserved.</p>
#     </div>
# </div>

# </body>
# </html>
# """
if __name__ == '__main__':
    app.run(port=5000,debug=True,host="0.0.0.0")
