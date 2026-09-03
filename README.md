# Rock Paper Scissors (Hand Tracking Edition)

Play rock paper scissors against a friend using nothing but your webcam and your hands. No keyboard, no controller, just gestures.

## What it does

Two people sit in front of one webcam, one on the left side of the frame and one on the right. The app tracks both hands using MediaPipe, figures out which gesture each person is making (rock, paper, or scissors), and decides the winner live on screen.

There are two versions in this repo:

* `game_rock_paper_scissors.py`, the original version. It opens a plain OpenCV window and prints the detected gestures and result directly onto the video feed.
* `rps_gui.py`, a nicer version with an actual interface built in tkinter. It has a scoreboard, round counter, FPS display, and buttons to reset the score or quit.

Both use the same hand tracking logic under the hood, defined in `hand_tracking_module.py`.

## How gesture detection works

MediaPipe gives you 21 landmark points per hand (fingertips, knuckles, etc). The code checks the position of each fingertip relative to its base joint to figure out which fingers are extended. All five fingers up means paper, only the index and middle fingers up means scissors, and everything curled in means rock. The GUI version also mirrors this logic but is a bit more robust about which side of the frame each hand is on.

## Tech used

* Python
* OpenCV for capturing and displaying the webcam feed
* MediaPipe for hand landmark detection
* Tkinter and Pillow for the GUI version's interface

## Installation

You'll need Python installed. Then grab the dependencies:

```bash
pip install opencv-python mediapipe pillow
```

## Running it

For the GUI version with the scoreboard:

```bash
python rps_gui.py
```

For the original, simpler version:

```bash
python game_rock_paper_scissors.py
```

Make sure your webcam is connected and both players can fit in frame, one on each side.

## Images

<p align="center">
  <img src="https://github.com/user-attachments/assets/52a747b6-7cb8-421d-8660-ad7f59963ca9" alt="First Image" width="31%" style="margin-right: 10px;"/>
  <img src="https://github.com/user-attachments/assets/cfa104a1-18fd-4c5b-b0f9-1d177898dedb" alt="Second Image" width="31%" style="margin-right: 10px;"/>
  <img src="https://github.com/user-attachments/assets/5f61bf8c-3c21-46ae-8577-32de301cfdf9" alt="Third Image" width="31%"/>
</p>

## Contributing

If you want to help improve gesture accuracy, add best of three rounds, or clean up the detection logic, pull requests are welcome. Fork the repo, make your changes, and submit a PR.
