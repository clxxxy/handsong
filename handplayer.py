import cv2
import mediapipe as mp
import pyautogui
import webbrowser
from PIL import Image

class HandPlayer:
    def __init__(self, width=640, height=480):
        self.width = width
        self.height = height
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7)
        self.drawing_utils = mp.solutions.drawing_utils

        self.prev_finger_state = {}
        self.active_note = None

        # Abre o site do piano virtual
        webbrowser.open('https://www.onlinepianist.com/virtual-piano', new=1)

        self.finger_map_lower_default = {
            (20, 'Left'): 'q', (12, 'Left'): 'w', (8, 'Left'): 'e', (4, 'Left'): 'r',
            (8, 'Right'): 't', (12, 'Right'): 'y', (20, 'Right'): 'u',
        }
        self.finger_map_lower_polegar = {
            (20, 'Left'): '2', (12, 'Left'): '3', (8, 'Left'): None, (4, 'Left'): '5',
            (8, 'Right'): '6', (12, 'Right'): '7', (20, 'Right'): None,
        }
        self.finger_map_upper_default = {
            (20, 'Left'): 'i', (12, 'Left'): 'o', (8, 'Left'): 'p', (4, 'Left'): 'z',
            (8, 'Right'): 'x', (12, 'Right'): 'c', (20, 'Right'): 'v',
        }
        self.finger_map_upper_polegar = {
            (20, 'Left'): '9', (12, 'Left'): '0', (8, 'Left'): None, (4, 'Left'): 's',
            (8, 'Right'): 'd', (12, 'Right'): 'f', (20, 'Right'): None,
        }
        self.key_note_labels = {
            'q': 'C3', 'w': 'D3', 'e': 'E3', 'r': 'F3', 't': 'G3', 'y': 'A3', 'u': 'B3',
            '2': 'C#3', '3': 'D#3', '5': 'F#3', '6': 'G#3', '7': 'A#3',
            'i': 'C4', 'o': 'D4', 'p': 'E4', 'z': 'F4', 'x': 'G4', 'c': 'A4', 'v': 'B4',
            '9': 'C#4', '0': 'D#4', 's': 'F#4', 'd': 'G#4', 'f': 'A#4',
        }

    def is_finger_up(self, landmarks, tip_id, hand_label):
        if tip_id == 4:
            if hand_label == 'Left':
                return landmarks.landmark[tip_id].x < landmarks.landmark[tip_id - 2].x
            else:
                return landmarks.landmark[tip_id].x > landmarks.landmark[tip_id - 2].x
        else:
            return landmarks.landmark[tip_id].y < landmarks.landmark[tip_id - 2].y

    def is_thumb_typing_up(self, landmarks, hand_label):
        tip_id = 4
        return landmarks.landmark[tip_id].x < landmarks.landmark[tip_id - 2].x if hand_label == 'Left' else landmarks.landmark[tip_id].x > landmarks.landmark[tip_id - 2].x

    def get_frame(self):
        if not self.cap.isOpened():
            return None

        ret, frame = self.cap.read()
        if not ret:
            return None

        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb)

        mid_line_y = h // 2
        cv2.line(frame, (0, mid_line_y), (w, mid_line_y), (255, 255, 255), 2)

        self.active_note = None

        if results.multi_hand_landmarks and results.multi_handedness:
            polegar_direito_levantado = False
            hand_infos = zip(results.multi_hand_landmarks, results.multi_handedness)
            for hand_landmarks, handedness in hand_infos:
                hand_label = handedness.classification[0].label
                if hand_label == 'Right':
                    polegar_direito_levantado = self.is_finger_up(hand_landmarks, 4, 'Right')
                    break

            for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                hand_label = handedness.classification[0].label
                center_y = hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y * h
                region = 'upper' if center_y < mid_line_y else 'lower'
                cor_regiao = (85, 17, 170) if region == 'upper' else (68, 0, 136)

                finger_map = (
                    self.finger_map_upper_polegar if polegar_direito_levantado else self.finger_map_upper_default
                ) if region == 'upper' else (
                    self.finger_map_lower_polegar if polegar_direito_levantado else self.finger_map_lower_default
                )

                for (tip_id, label) in finger_map:
                    if label == hand_label:
                        finger_id = (tip_id, hand_label)
                        key = finger_map[finger_id]
                        if key is None:
                            continue

                        is_control_thumb = (tip_id == 4 and hand_label == 'Right' and polegar_direito_levantado)
                        is_typing_thumb = (tip_id == 4 and not is_control_thumb)
                        is_up = not self.is_thumb_typing_up(hand_landmarks, hand_label) if is_typing_thumb else self.is_finger_up(hand_landmarks, tip_id, hand_label)

                        if finger_id not in self.prev_finger_state:
                            self.prev_finger_state[finger_id] = True

                        if not is_up and self.prev_finger_state[finger_id]:
                            pyautogui.press(key)

                        self.prev_finger_state[finger_id] = is_up

                        if not is_up and key in self.key_note_labels:
                            self.active_note = self.key_note_labels[key]

                        cx = int(hand_landmarks.landmark[tip_id].x * w)
                        cy = int(hand_landmarks.landmark[tip_id].y * h)

                        cor_final = (232, 254, 236) if not is_up else (
                            (235, 239, 194) if region == 'upper' else (191, 164, 110)
                        ) if not polegar_direito_levantado else cor_regiao

                        cv2.circle(frame, (cx, cy), 10, cor_final, -1)

                        if key in self.key_note_labels:
                            nota = self.key_note_labels[key]
                            cv2.putText(frame, nota, (cx + 10, cy - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

        if self.active_note:
            font = cv2.FONT_HERSHEY_SIMPLEX
            text = f"{self.active_note}"
            text_size = cv2.getTextSize(text, font, 1, 2)[0]
            text_x = w - text_size[0] - 20
            text_y = 40
            cv2.putText(frame, text, (text_x, text_y), font, 1, (255, 255, 255), 2, cv2.LINE_AA)

        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        return img

    def stop(self):
        self.running = False
        self.cap.release()
