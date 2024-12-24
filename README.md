# Violence Detection and Email Notification System

This project implements a real-time violence detection system using deep learning. The system processes video streams to detect violent activities and sends automated email notifications to alert concerned individuals or authorities. The model is built on **MobileNetV2** for efficient and accurate performance.

## Features
- **Real-Time Detection**: Identifies violent activities in live video streams or recorded footage.
- **Automated Email Alerts**: Sends instant notifications upon detecting violence.
- **Efficient and Lightweight**: Uses MobileNetV2 for fast and resource-efficient processing.
- **Scalable**: Easily adaptable to various environments like schools, workplaces, or public spaces.

## How It Works
1. **Video Input**: Processes video frames from a live feed or pre-recorded videos.
2. **Violence Detection**: Uses a pretrained MobileNetV2 model to identify violent actions in frames.
3. **Email Notification**: Triggers an email alert to predefined recipients if violence is detected.

## Installation
1. Clone the repository:
   ```bash
   git clone git@github.com:Kunal1405/Violence-Detection-and-Email-Notification-System.git
   ```
2. Navigate to the project directory:
   ```bash
   cd Violence-Detection-and-Email-Notification-System
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure email settings in `config.py` with your SMTP credentials.

## Usage
1. Run the script to start the detection system:
   ```bash
   python main.py
   ```
2. Monitor the console for detection logs and email notifications.

## Technologies Used
- **Deep Learning Framework**: TensorFlow/Keras
- **Model Architecture**: MobileNetV2
- **Programming Language**: Python
- **Notification Service**: SMTP/Email APIs

## Applications
- Public safety and surveillance
- School and workplace security
- Crowd monitoring and management

## Contributing
Contributions are welcome! Please fork the repository and create a pull request with your changes. For major changes, open an issue first to discuss your ideas.

## License
This project is licensed under the [MIT License](LICENSE).

## Contact
For any inquiries or support, please reach out to [Kunal Sangwan](mailto:your-email@example.com).

