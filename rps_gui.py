import cv2
import numpy as np
import hand_tracking_module as htm
import time
import tkinter as tk
from PIL import Image, ImageTk
import threading


class RPSGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Rock Paper Scissors \u2014 Hand Tracking")
        self.root.configure(bg="#08090e")
        self.root.resizable(False, False)

        self.BG = "#08090e"
        self.PANEL = "#10121a"
        self.CARD = "#181c28"
        self.BORDER = "#252a3a"
        self.TEXT = "#e0e4f0"
        self.DIM = "#5a6078"
        self.CYAN = "#22d3ee"
        self.ORANGE = "#f59e0b"
        self.RED = "#ef4444"
        self.GREEN = "#10b981"
        self.PINK = "#ec4899"

        self.p1_score = 0
        self.p2_score = 0
        self.draws = 0
        self.p1_gesture = "..."
        self.p2_gesture = "..."
        self.result_text = "SHOW YOUR HANDS"
        self.result_color = (180, 180, 200)
        self.round_count = 0
        self.fps_val = 0

        self.cap = None
        self.detector = htm.handDetector(detectionCon=0.75, modelComplexity=0)
        self.running = False
        self.photo = None
        self._last_result = None
        self.frame_skip = 0
        self.cached_lmList = []

        self.build_ui()
        self.start_camera()

    def build_ui(self):
        top = tk.Frame(self.root, bg=self.BG)
        top.pack(fill="x", padx=16, pady=(12, 0))

        tk.Label(top, text="\u270a \u270b \u270c", fg=self.CYAN, bg=self.BG,
                 font=("Consolas", 12)).pack(side="left")
        tk.Label(top, text="ROCK  PAPER  SCISSORS", fg=self.TEXT, bg=self.BG,
                 font=("Consolas", 14, "bold")).pack(side="left", padx=(8, 0))
        tk.Label(top, text="HAND TRACKING", fg=self.DIM, bg=self.BG,
                 font=("Consolas", 9)).pack(side="left", padx=(10, 0))

        self.fps_label = tk.Label(top, text="", fg=self.DIM, bg=self.BG,
                                  font=("Consolas", 9))
        self.fps_label.pack(side="right")

        score_bar = tk.Frame(self.root, bg=self.PANEL, height=70)
        score_bar.pack(fill="x", padx=16, pady=(10, 0))
        score_bar.pack_propagate(False)

        inner = tk.Frame(score_bar, bg=self.PANEL)
        inner.pack(expand=True)

        p1_frame = tk.Frame(inner, bg=self.PANEL)
        p1_frame.pack(side="left", padx=30)
        tk.Label(p1_frame, text="LEFT PLAYER", fg=self.CYAN, bg=self.PANEL,
                 font=("Consolas", 8, "bold")).pack()
        self.p1_score_label = tk.Label(p1_frame, text="0", fg=self.TEXT, bg=self.PANEL,
                                       font=("Consolas", 28, "bold"))
        self.p1_score_label.pack()

        vs_frame = tk.Frame(inner, bg=self.PANEL)
        vs_frame.pack(side="left", padx=30)
        self.result_label = tk.Label(vs_frame, text="SHOW YOUR HANDS", fg=self.DIM, bg=self.PANEL,
                                     font=("Consolas", 11, "bold"))
        self.result_label.pack()
        self.gesture_label = tk.Label(vs_frame, text="... vs ...", fg=self.DIM, bg=self.PANEL,
                                      font=("Consolas", 9))
        self.gesture_label.pack()

        p2_frame = tk.Frame(inner, bg=self.PANEL)
        p2_frame.pack(side="left", padx=30)
        tk.Label(p2_frame, text="RIGHT PLAYER", fg=self.ORANGE, bg=self.PANEL,
                 font=("Consolas", 8, "bold")).pack()
        self.p2_score_label = tk.Label(p2_frame, text="0", fg=self.TEXT, bg=self.PANEL,
                                       font=("Consolas", 28, "bold"))
        self.p2_score_label.pack()

        self.canvas = tk.Canvas(self.root, bg="#000", highlightthickness=0,
                                width=960, height=540, cursor="crosshair")
        self.canvas.pack(padx=16, pady=(10, 0))

        bottom = tk.Frame(self.root, bg=self.BG)
        bottom.pack(fill="x", padx=16, pady=(10, 12))

        self.round_label = tk.Label(bottom, text="Round 0  |  Draws: 0", fg=self.DIM, bg=self.BG,
                                    font=("Consolas", 9))
        self.round_label.pack(side="left")

        self.quit_btn = tk.Button(bottom, text="QUIT", command=self.quit_app,
                                  bg=self.CARD, fg=self.DIM, activebackground=self.CARD,
                                  font=("Consolas", 9, "bold"), relief="flat", bd=0,
                                  padx=16, pady=4, cursor="hand2")
        self.quit_btn.pack(side="right")

        self.reset_btn = tk.Button(bottom, text="RESET SCORE", command=self.reset_scores,
                                   bg=self.CARD, fg=self.DIM, activebackground=self.CARD,
                                   font=("Consolas", 9, "bold"), relief="flat", bd=0,
                                   padx=16, pady=4, cursor="hand2")
        self.reset_btn.pack(side="right", padx=(0, 8))

    def start_camera(self):
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.cap.set(cv2.CAP_PROP_FPS, 60)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        self.running = True
        self.prev_time = time.time()
        self.process_frame()

    def process_frame(self):
        if not self.running:
            return

        ret, img = self.cap.read()
        if not ret:
            self.root.after(30, self.process_frame)
            return

        img = cv2.flip(img, 1)

        now = time.time()
        dt = now - self.prev_time
        self.prev_time = now
        self.fps_val = 1.0 / dt if dt > 0 else 0

        self.frame_skip += 1
        if self.frame_skip % 2 == 0:
            small = cv2.resize(img, (640, 360))
            small = self.detector.findHands(small, draw=False)
            raw_lm = self.detector.findPosition(small)
            sh, sw = small.shape[:2]
            fh, fw = img.shape[:2]
            self.cached_lmList = []
            for pt in raw_lm:
                self.cached_lmList.append([pt[0], int(pt[1] * fw / sw), int(pt[2] * fh / sh)])

        lmList = self.cached_lmList

        if len(lmList) == 42:
            img = self.detector.findHands(img, draw=True)
            p1_gesture = self.detect_gesture(lmList, 0)
            p2_gesture = self.detect_gesture(lmList, 21)

            p1_side, p2_side = self.assign_sides(lmList)

            self.p1_gesture = p1_gesture if p1_side == "left" else p2_gesture
            self.p2_gesture = p2_gesture if p2_side == "right" else p1_gesture

            result = self.winner(self.p1_gesture, self.p2_gesture)

            if result == "left":
                self.result_text = "LEFT PLAYER WINS"
                self.result_color = (238, 211, 34)
                if self._last_result != result:
                    self.p1_score += 1
                    self.round_count += 1
            elif result == "right":
                self.result_text = "RIGHT PLAYER WINS"
                self.result_color = (238, 211, 34)
                if self._last_result != result:
                    self.p2_score += 1
                    self.round_count += 1
            elif result == "draw":
                self.result_text = "DRAW"
                self.result_color = (180, 180, 200)
                if self._last_result != result:
                    self.draws += 1
                    self.round_count += 1
            else:
                self.result_text = "SHOW GESTURES"
                self.result_color = (180, 180, 200)

            self._last_result = result

            h, w = img.shape[:2]
            mid = w // 2
            cv2.line(img, (mid, 0), (mid, h), (34, 211, 238), 1)

            self.draw_player_hud(img, self.p1_gesture, "LEFT", 20, (34, 211, 238))
            self.draw_player_hud(img, self.p2_gesture, "RIGHT", w - 220, (11, 158, 245))
        else:
            self.result_text = "SHOW BOTH HANDS"
            self.result_color = (90, 96, 120)
            self._last_result = None

        self.draw_overlay(img)
        self.root.after(0, lambda: self.update_ui())

        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        rgb = cv2.resize(rgb, (960, 540))
        self.photo = ImageTk.PhotoImage(image=Image.fromarray(rgb))
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor="nw", image=self.photo)

        self.root.after(1, self.process_frame)

    def detect_gesture(self, lmList, offset):
        tips = [4, 8, 12, 16, 20]
        bases = [3, 6, 10, 14, 18]
        fingers_up = 0

        if lmList[tips[0] + offset][2] < lmList[bases[0] + offset][2]:
            fingers_up += 1

        for i in range(1, 5):
            tip = lmList[tips[i] + offset]
            base = lmList[bases[i] + offset]
            ref = lmList[0 + offset]

            if lmList[12 + offset][1] < ref[1]:
                if tip[1] < base[1]:
                    fingers_up += 1
            else:
                if tip[1] > base[1]:
                    fingers_up += 1

        if fingers_up >= 4:
            return "paper"
        elif fingers_up <= 1:
            return "rock"
        else:
            idx_up = False
            mid_up = False
            ring_up = False
            pinky_up = False
            ref = lmList[0 + offset]
            if lmList[12 + offset][1] < ref[1]:
                idx_up = lmList[8 + offset][1] < lmList[6 + offset][1]
                mid_up = lmList[12 + offset][1] < lmList[10 + offset][1]
                ring_up = lmList[16 + offset][1] < lmList[14 + offset][1]
                pinky_up = lmList[20 + offset][1] < lmList[18 + offset][1]
            else:
                idx_up = lmList[8 + offset][1] > lmList[6 + offset][1]
                mid_up = lmList[12 + offset][1] > lmList[10 + offset][1]
                ring_up = lmList[16 + offset][1] > lmList[14 + offset][1]
                pinky_up = lmList[20 + offset][1] > lmList[18 + offset][1]

            if idx_up and mid_up and not ring_up and not pinky_up:
                return "scissors"
            elif fingers_up >= 4:
                return "paper"
            else:
                return "rock"

    def assign_sides(self, lmList):
        h1_x = lmList[0][1]
        h2_x = lmList[21][1]
        if h1_x < h2_x:
            return "left", "right"
        return "right", "left"

    def winner(self, p1, p2):
        if p1 not in ["rock", "paper", "scissors"] or p2 not in ["rock", "paper", "scissors"]:
            return None
        if p1 == p2:
            return "draw"
        wins = {"rock": "scissors", "scissors": "paper", "paper": "rock"}
        return "left" if wins[p1] == p2 else "right"

    def draw_player_hud(self, img, gesture, side, x, color):
        emoji = {"rock": "ROCK", "paper": "PAPER", "scissors": "SCISSORS"}.get(gesture, "?")

        overlay = img.copy()
        cv2.rectangle(overlay, (x, 10), (x + 200, 80), (10, 10, 18), -1)
        cv2.addWeighted(overlay, 0.7, img, 0.3, 0, img)

        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img, side, (x + 10, 32), font, 0.45, color, 1, cv2.LINE_AA)
        cv2.putText(img, emoji, (x + 10, 65), font, 0.9, (255, 255, 255), 2, cv2.LINE_AA)

    def draw_overlay(self, img):
        h, w = img.shape[:2]
        overlay = img.copy()

        cv2.rectangle(overlay, (0, h - 50), (w, h), (8, 9, 14), -1)
        cv2.addWeighted(overlay, 0.85, img, 0.15, 0, img)

        font = cv2.FONT_HERSHEY_SIMPLEX

        result_w = cv2.getTextSize(self.result_text, font, 0.7, 2)[0][0]
        rx = (w - result_w) // 2
        cv2.putText(img, self.result_text, (rx, h - 18), font, 0.7,
                    self.result_color, 2, cv2.LINE_AA)

        score_text = f"{self.p1_score}  -  {self.p2_score}"
        sw = cv2.getTextSize(score_text, font, 0.5, 1)[0][0]
        cv2.putText(img, score_text, ((w - sw) // 2, h - 38), font, 0.5,
                    (200, 200, 220), 1, cv2.LINE_AA)

    def update_ui(self):
        self.p1_score_label.configure(text=str(self.p1_score))
        self.p2_score_label.configure(text=str(self.p2_score))
        self.result_label.configure(
            text=self.result_text,
            fg=self.GREEN if "WINS" in self.result_text else self.DIM
        )
        self.gesture_label.configure(text=f"{self.p1_gesture}  vs  {self.p2_gesture}")
        self.round_label.configure(text=f"Round {self.round_count}  |  Draws: {self.draws}")
        self.fps_label.configure(text=f"FPS: {self.fps_val:.0f}")

    def reset_scores(self):
        self.p1_score = 0
        self.p2_score = 0
        self.draws = 0
        self.round_count = 0
        self.update_ui()

    def quit_app(self):
        self.running = False
        if self.cap:
            self.cap.release()
        self.root.destroy()


def main():
    root = tk.Tk()
    app = RPSGame(root)
    root.protocol("WM_DELETE_WINDOW", app.quit_app)
    root.mainloop()


if __name__ == "__main__":
    main()
