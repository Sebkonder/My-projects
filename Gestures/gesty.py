# %%
# Importy
import numpy as np
import cv2
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Stałe
FRAME_HEIGHT = 400
FRAME_WIDTH = 400
CALIBRATION_TIME = 30
BG_WEIGHT = 0.5
OBJ_THRESHOLD = 18

# Zmienne
background = None
hand = None
frames_elapsed = 0
codeList = []
codeDict = {}

# Region of interest — prawa górna część kadru
region_top = 0
region_bottom = int(2 * FRAME_HEIGHT / 4)
region_left = int(FRAME_WIDTH / 2)
region_right = FRAME_WIDTH

# Klasa HandData
class HandData:
    top = (0, 0)
    bottom = (0, 0)
    left = (0, 0)
    right = (0, 0)
    centerX = 0
    prevCenterX = 0
    isInFrame = False
    isWaving = False
    fingers = None
    gestureList = []

    def __init__(self, top, bottom, left, right, centerX):
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right
        self.centerX = centerX
        self.prevCenterX = 0
        self.isInFrame = False
        self.isWaving = False

    def update(self, top, bottom, left, right):
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right

    def check_for_waving(self, centerX):
        self.prevCenterX = self.centerX
        self.centerX = centerX

        if abs(self.centerX - self.prevCenterX > 3):
            self.isWaving = True
        else:
            self.isWaving = False

# Funkcje pomocnicze
def get_region(frame):
    region = frame[region_top:region_bottom, region_left:region_right]
    region_color = region.copy()

    hsv = cv2.cvtColor(region, cv2.COLOR_BGR2HSV)
    lower_skin = np.array([0, 30, 60], dtype=np.uint8)
    upper_skin = np.array([20, 150, 255], dtype=np.uint8)
    skin_mask = cv2.inRange(hsv, lower_skin, upper_skin)
    skin_mask = cv2.GaussianBlur(skin_mask, (5, 5), 0)

    return region_color, skin_mask


def get_average(region):
    global background
    if background is None:
        background = region.copy().astype("float")
        return
    cv2.accumulateWeighted(region, background, BG_WEIGHT)


def segment(region):
    global hand
    diff = cv2.absdiff(background.astype(np.uint8), region)
    thresholded_region = cv2.threshold(diff, OBJ_THRESHOLD, 255, cv2.THRESH_BINARY)[1]
    contours, _ = cv2.findContours(thresholded_region.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) == 0:
        if hand is not None:
            hand.isInFrame = False
        return None
    else:
        if hand is not None:
            hand.isInFrame = True
        segmented_region = max(contours, key=cv2.contourArea)
        return (thresholded_region, segmented_region)


def get_hand_data(thresholded_image, segmented_image):
    global hand, frames_elapsed
    convexHull = cv2.convexHull(segmented_image)

    top = tuple(convexHull[convexHull[:, :, 1].argmin()][0])
    bottom = tuple(convexHull[convexHull[:, :, 1].argmax()][0])
    left = tuple(convexHull[convexHull[:, :, 0].argmin()][0])
    right = tuple(convexHull[convexHull[:, :, 0].argmax()][0])
    centerX = int((left[0] + right[0]) / 2)

    if hand is None:
        hand = HandData(top, bottom, left, right, centerX)
    else:
        hand.update(top, bottom, left, right)

    if frames_elapsed % 6 == 0:
        hand.check_for_waving(centerX)

    hand.gestureList.append(count_fingers(thresholded_image))
    if frames_elapsed % 12 == 0:
        hand.fingers = most_frequent(hand.gestureList)
        hand.gestureList.clear()


def count_fingers(thresholded_image):
    line_height = int(hand.top[1] + (0.2 * (hand.bottom[1] - hand.top[1])))
    line = np.zeros(thresholded_image.shape[:2], dtype=np.uint8)
    cv2.line(line, (thresholded_image.shape[1], line_height), (0, line_height), 255, 1)
    line = cv2.bitwise_and(thresholded_image, thresholded_image, mask=line.astype(np.uint8))
    contours, _ = cv2.findContours(line.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    fingers = 0
    if contours is not None:
        for curr in contours:
            width = len(curr)
            if width < 3 * abs(hand.right[0] - hand.left[0]) / 4 and width > 5:
                fingers += 1
    return fingers


def most_frequent(input_list):
    d = {}
    count = 0
    most_freq = 0
    for item in reversed(input_list):
        d[item] = d.get(item, 0) + 1
        if d[item] >= count:
            count, most_freq = d[item], item
    return most_freq

def get_gesture_text():
    if frames_elapsed < CALIBRATION_TIME:
        return "Kalibracja..."
    elif hand is None or hand.isInFrame is False:
        return "Brak dłoni"
    else:
        if hand.isWaving:
            return "Machanie"
        elif hand.fingers == 0:
            if abs(hand.top[1] - hand.bottom[1]) < 1.5 * abs(hand.right[0] - hand.left[0]):
                return "Kamień"
            else:
                return "Papier"
        elif hand.fingers == 1:
            return "Wskazywanie"
        elif hand.fingers == 2:
            return "Nożyce"
    return "Szukam..."


# Aplikacja
class HandGestureApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Rozpoznawanie gestów dłoni")
        self.root.configure(bg="#1e1e1e")
        self.root.resizable(False, False)

        self.right_frame = tk.Frame(root, bg="#1e1e1e")
        self.right_frame.pack(side="right", fill="both", padx=50)
        self.bottom_frame = tk.Frame(root, bg="#1e1e1e")
        self.bottom_frame.pack(side="bottom")
        self.button_frame = tk.Frame(self.bottom_frame, bg="#1e1e1e")
        self.button_frame.pack(side="left", fill="both")
        self.reset_frame = tk.Frame(self.bottom_frame, bg="#1e1e1e")
        self.reset_frame.pack(side="right", fill="both", padx=10)
        self.info_frame = tk.Frame(self.right_frame, bg="#1e1e1e")
        self.info_frame.pack(side="bottom")

        # Ramka na kamerę
        self.camera_label = tk.Label(root, bg="#1e1e1e", bd=0)
        self.camera_label.pack(padx=10, pady=(10, 5))

        # Etykieta z gestem
        self.gesture_label = tk.Label(
            root,
            text="Kalibracja...",
            font=("Segoe UI", 22, "bold"),
            fg="#00ff88",
            bg="#1e1e1e",
        )
        self.gesture_label.pack(pady=(5, 5))

        # Przycisk resetu kalibracji
        self.reset_button = tk.Button(
            self.reset_frame,
            text="⟳ Resetuj kalibrację",
            font=("Segoe UI", 12),
            fg="#1e1e1e",
            bg="#00ff88",
            activebackground="#00cc66",
            activeforeground="#1e1e1e",
            bd=0,
            padx=15,
            pady=5,
            cursor="hand2",
            width=20,
            command=self.reset_calibration,
        )
        self.reset_button.pack(pady = (0,10))

        # Przycisk zczytywania gestu
        self.save_button = tk.Button(
            self.button_frame,
            text="Zapisz gest",
            font=("Segoe UI", 12),
            fg="#1e1e1e",
            bg="#00ff88",
            activebackground="#00cc66",
            activeforeground="#1e1e1e",
            bd=0,
            padx=15,
            pady=5,
            cursor="hand2",
            width=20,
            command=self.save_gesture,
        )
        self.save_button.pack(pady=(0, 10))

        # Pole na zaszyfrowaną wiadomość
        self.text_box = tk.Text(
            self.button_frame,
            height=3,
            width=26,
            bg="light yellow",
            border=2
        )
        self.text_box.pack(pady=(0, 10))

        # Przycisk potwierdzenia szyfru
        self.last_button = tk.Button(
            self.button_frame,
            text="Potwierdź kombinację",
            font=("Segoe UI", 12),
            fg="#1e1e1e",
            bg="#00ff88",
            activebackground="#00cc66",
            activeforeground="#1e1e1e",
            bd=0,
            padx=15,
            pady=5,
            cursor="hand2",
            width=20,
            command=self.confirm_pattern,
        )
        self.last_button.pack(pady=(0, 10))

        # Przycisk resetu szyfrów
        self.reset_dict_button = tk.Button(
            self.reset_frame,
            text="Resetuj szyfry",
            font=("Segoe UI", 12),
            fg="#1e1e1e",
            bg="#00ff88",
            activebackground="#00cc66",
            activeforeground="#1e1e1e",
            bd=0,
            padx=15,
            pady=5,
            cursor="hand2",
            width=20,
            command=self.reset_dict,
        )
        self.reset_dict_button.pack(pady=(0, 10))

        # Etykieta z codeList
        self.list_label = tk.Label(
            self.right_frame,
            text="Lista jest pusta",
            font=("Segoe UI", 22, "bold"),
            fg="#00ff88",
            bg="#1e1e1e",
        )
        self.list_label.pack(pady=(5, 5))

        # Etykieta z info
        self.info_label = tk.Label(
            self.info_frame,
            text="",
            font=("Segoe UI", 22, "bold"),
            fg="#00ff88",
            bg="#1e1e1e",
            width= 30
        )
        self.info_label.pack(pady=(5, 5))

        # Kamera
        self.capture = cv2.VideoCapture(0)

        # Zamknięcie okna
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Start pętli
        self.update_frame()

    def update_frame(self):
        global frames_elapsed

        ret, frame = self.capture.read()
        if not ret:
            self.root.after(10, self.update_frame)
            return

        frame = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))
        frame = cv2.flip(frame, 1)

        # Przetwarzanie w tle
        region_color, region_gray = get_region(frame)

        if frames_elapsed < CALIBRATION_TIME:
            get_average(region_gray)
        else:
            region_pair = segment(region_gray)
            if region_pair is not None:
                (thresholded_region, segmented_region) = region_pair
                roi = frame[region_top:region_bottom, region_left:region_right]
                get_hand_data(thresholded_region, segmented_region)

        # Prostokąt regionu zainteresowania
        cv2.rectangle(frame, (region_left, region_top),
                      (region_right, region_bottom), (0, 255, 100), 2)

        # Aktualizacja tekstu gestu
        gesture_text = get_gesture_text()
        self.gesture_label.config(text=gesture_text)

        # Aktualizacja tekstu szyfru
        if len(codeList)>0:
            self.list_label.config(text='\n'.join(codeList))
        else:
            self.list_label.config(text="Lista jest pusta")
        
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        imgtk = ImageTk.PhotoImage(image=img)
        self.camera_label.imgtk = imgtk
        self.camera_label.config(image=imgtk)

        frames_elapsed += 1
        self.root.after(15, self.update_frame)

    def reset_calibration(self):
        global background, hand, frames_elapsed
        background = None
        hand = None
        frames_elapsed = 0
        self.gesture_label.config(text="Kalibracja...")

    def reset_dict(self):
        global codeDict
        codeDict = {}
        self.info_label.config(text="Pomyślnie wyczyszczono szyfry.")

    def save_gesture(self):
        global codeList
        if not get_gesture_text() == "Kalibracja..." and not get_gesture_text() == "Szukam...":
            codeList.append(get_gesture_text()[0])

    
    def confirm_pattern(self):
        global codeDict, codeList
        input = self.text_box.get("1.0",'end-1c')
        self.text_box.delete("1.0",'end-1c')
        key = ''.join(codeList)
        if key in codeDict.keys():
            output = codeDict[key]
            self.info_label.config(text=f"Szyfr: {key}\nWartość: {output}")
        else:
            codeDict[key] = input
            self.info_label.config(text="Pomyślnie zapisano nowy szyfr.")
        codeList.clear()


    def on_close(self):
        self.capture.release()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = HandGestureApp(root)
    root.mainloop()


