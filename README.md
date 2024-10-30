# Rock-Paper-Scissors Hand Gesture Game

## Overview
This project is a Rock-Paper-Scissors game that utilizes computer vision techniques to interpret hand gestures as game moves. Built using OpenCV and a custom hand tracking module, the application can determine the outcome of the game played with hand gestures captured via webcam.

## Features
- **Hand Gesture Recognition**: Uses OpenCV and the MediaPipe library to recognize hand gestures in real-time.
- **Game Logic Implementation**: Determines the winner of Rock-Paper-Scissors based on the recognized gestures.
- **Real-time Interaction**: Players can see the game result instantly on the screen after their gestures are recognized.

## Technologies Used
- **Python**: The core programming language used.
- **OpenCV (cv2)**: For image processing and capturing video input from a webcam.
- **MediaPipe**: Used for robust hand tracking and gesture recognition.

## Installation

To run this application, you will need Python installed along with OpenCV and MediaPipe. Follow these steps to set up:

1. **Install Python**:
   Ensure Python is installed on your system. You can download it from [python.org](https://www.python.org).

2. **Install Required Libraries**:
   Install OpenCV and MediaPipe using pip:
   ```bash
   pip install opencv-python mediapipe
   
3. **Running the Application**
After installing the necessary libraries, you can run the application by executing the main Python script. Make sure your webcam is connected and permitted to be used by Python scripts.
   ```bash
   python game_rock_paper_scissors.py

## Usage

- **Start the Game**: Run the script and position your hands within the webcam's field of view.
- **Make Your Gesture**: Use rock, paper, or scissors gestures. The system will recognize these gestures and display the corresponding move on the screen.
- **Game Results**: After both players have made their moves, the game will determine and display the winner on the screen.

## Contributing

Contributions are welcome, and here are some ways you can help improve the project:

- **Enhance Gesture Recognition**: Improve the accuracy and efficiency of the hand tracking and gesture recognition.
- **Add Features**: Introduce new functionalities like score tracking or support for multiple rounds.
- **Improve Documentation**: Help make the project more accessible to new users by enhancing the existing documentation.

To contribute, fork the repository, make your changes, and submit a pull request.
