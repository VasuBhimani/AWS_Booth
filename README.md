# 🤖 AI Booth - AWS Student Community Day

The **AI Booth** was developed and showcased at the **AWS Student Community Day** held at CHARUSAT 🎓. This interactive project utilized multiple AWS services to provide attendees and speakers with a personalized AI experience. By combining cloud computing, storage, and database capabilities, the booth demonstrated how technology can automate and enhance event-based interactions ✨.

---

<div style="display: flex; justify-content: space-around;">
  <img src="/static/assets/Demo2.jpeg" alt="AI Avatar Example 1" style="width: 30%; height: auto;">
  <img src="/static/assets/Demo1.png" alt="AI Avatar Example 3" style="width: 30%; height: auto;">
  <img src="/static/assets/Demo3.jpeg" alt="AI Avatar Example 2" style="width: 30%; height: auto;">
</div>

---

## 🔄 Project Workflow

1. **Scan Ticket** 🎟️:  
   Attendees scan their **Community Day Ticket** at the booth.
2. **Activate Camera** 📸:  
   The booth's display activates the camera and starts a countdown timer.
3. **Capture Photo** 📱:  
   Once the timer reaches zero, the camera captures the attendee's photo.
4. **Generate AI Avatar** 🧠:  
   A brief processing period (10-15 seconds) generates an **AI avatar** based on the captured image.
5. **Display and Email Avatar** 📧:  
   The avatar is displayed on the screen and sent to the attendee's registered email address (used during ticket booking).

---

## ☁️ AWS Services Used

This project leverages the following AWS services:

- **Amazon EC2** 💻: For computation and running the application.
- **Amazon S3** 🗄️: For storing captured photos and generated avatars.
- **Amazon RDS** 📊: For managing attendee data, including ticket and email information.

---

## 🎬 Demo Video

Watch the AI Booth in action:  

[![AI Booth Demo Video](https://img.youtube.com/vi/vfTLdJuLZXk/0.jpg)](https://youtube.com/shorts/vfTLdJuLZXk?feature=share)

---

## 🛠️ Setup Instructions

1. **Clone this repository** 📂:  
   ```bash
   git clone https://github.com/VasuBhimani/AWS_Booth.git
   cd AWS_Booth
   ```

2. **Set up AWS services** ☁️:  
   - Launch an **EC2 instance** to host the application.  
   - Create an **S3 bucket** for storing images and avatars.  
   - Set up an **RDS database** for attendee data.  

3. **Install dependencies** 📦:  
   Use the provided `requirements.txt` file:  
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application** ▶️:  
   Start the server using the following command:  
   ```bash
   python app.py
   ```

5. **Access the application** 🌐:  
   Open the application URL in your browser (e.g., `http://<your-ec2-instance-ip>:5000`).

---

## 👥 Contributing

Contributions to improve and extend the functionality of this project are welcome! Feel free to submit issues or open a pull request 🚀.
