import cv2
import mediapipe as mp
import pyautogui
import webbrowser

# abre o site do piano (melhor velocidade de resposta até então)
webbrowser.open('https://www.onlinepianist.com/virtual-piano', new=1)

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# mapeamento das notas seguindo as notas (teclas) do site
finger_map_lower_default = {
    (20, 'Left'): 'q',  # C3
    (12, 'Left'): 'w',  # D3
    (8, 'Left'): 'e',   # E3
    (4, 'Left'): 'r',   # F3
    (8, 'Right'): 't',  # G3
    (12, 'Right'): 'y', # A3
    (20, 'Right'): 'u', # B3
}
finger_map_lower_polegar = {
    (20, 'Left'): '2',  # C#3
    (12, 'Left'): '3',  # D#3
    (8, 'Left'): None,
    (4, 'Left'): '5',   # F#3
    (8, 'Right'): '6',  # G#3
    (12, 'Right'): '7', # A#3
    (20, 'Right'): None,
}

finger_map_upper_default = {
    (20, 'Left'): 'i',  # C4
    (12, 'Left'): 'o',  # D4
    (8, 'Left'): 'p',   # E4
    (4, 'Left'): 'z',   # F4
    (8, 'Right'): 'x',  # G4
    (12, 'Right'): 'c', # A4
    (20, 'Right'): 'v', # B4
}
finger_map_upper_polegar = {
    (20, 'Left'): '9',  # C#4
    (12, 'Left'): '0',  # D#4
    (8, 'Left'): None,
    (4, 'Left'): 's',   # F#4
    (8, 'Right'): 'd',  # G#4
    (12, 'Right'): 'f', # A#4
    (20, 'Right'): None,
}

# nome das notas para visualização na interface
key_note_labels = {
    'q': 'C3', 'w': 'D3', 'e': 'E3', 'r': 'F3',
    't': 'G3', 'y': 'A3', 'u': 'B3',
    '2': 'C#3', '3': 'D#3', '5': 'F#3', '6': 'G#3', '7': 'A#3',
    'i': 'C4', 'o': 'D4', 'p': 'E4', 'z': 'F4',
    'x': 'G4', 'c': 'A4', 'v': 'B4',
    '9': 'C#4', '0': 'D#4', 's': 'F#4', 'd': 'G#4', 'f': 'A#4',
}

# ajustes dos polegares
def is_finger_up(landmarks, tip_id, hand_label):
    if tip_id == 4:
        if hand_label == 'Left':
            return landmarks.landmark[tip_id].x < landmarks.landmark[tip_id - 2].x
        else:
            return landmarks.landmark[tip_id].x > landmarks.landmark[tip_id - 2].x
    else:
        return landmarks.landmark[tip_id].y < landmarks.landmark[tip_id - 2].y

def is_thumb_typing_up(landmarks, hand_label):
    tip_id = 4
    return landmarks.landmark[tip_id].x < landmarks.landmark[tip_id - 2].x if hand_label == 'Left' else landmarks.landmark[tip_id].x > landmarks.landmark[tip_id - 2].x

# inicialização
cap = cv2.VideoCapture(0)
prev_finger_state = {}
active_note = None

with mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7) as hands:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        mid_line_y = h // 2
        cv2.line(frame, (0, mid_line_y), (w, mid_line_y), (255, 255, 255), 2)

        active_note = None

        if results.multi_hand_landmarks and results.multi_handedness:
            polegar_direito_levantado = False
            hand_infos = zip(results.multi_hand_landmarks, results.multi_handedness)

            # verificação do polegar de controle
            for hand_landmarks, handedness in hand_infos:
                hand_label = handedness.classification[0].label
                if hand_label == 'Right':
                    polegar_direito_levantado = is_finger_up(hand_landmarks, 4, 'Right')
                    break

            for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                hand_label = handedness.classification[0].label
                center_y = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y * h
                region = 'upper' if center_y < mid_line_y else 'lower'

                cor_regiao = (85, 17, 170) if region == 'upper' else (68, 0, 136)

                if region == 'upper':
                    finger_map = finger_map_upper_polegar if polegar_direito_levantado else finger_map_upper_default
                else:
                    finger_map = finger_map_lower_polegar if polegar_direito_levantado else finger_map_lower_default


                for (tip_id, label) in finger_map:
                    if label == hand_label:
                        finger_id = (tip_id, hand_label)
                        key = finger_map[finger_id]

                        if key is None:
                            continue

                        is_control_thumb = (tip_id == 4 and hand_label == 'Right' and polegar_direito_levantado)
                        is_typing_thumb = (tip_id == 4 and not is_control_thumb)

                        is_up = not is_thumb_typing_up(hand_landmarks, hand_label) if is_typing_thumb else is_finger_up(hand_landmarks, tip_id, hand_label)

                        if finger_id not in prev_finger_state:
                            prev_finger_state[finger_id] = True

                        if not is_up and prev_finger_state[finger_id]:
                            print(f"[{region.upper()}] Pressionando: {key}")
                            pyautogui.press(key)

                        prev_finger_state[finger_id] = is_up

                        # nome da nota
                        if not is_up and key in key_note_labels:
                            active_note = key_note_labels[key]

                        # posição e cor dos dedos
                        cx = int(hand_landmarks.landmark[tip_id].x * w)
                        cy = int(hand_landmarks.landmark[tip_id].y * h)

                        cor_final = (232, 254, 236) if not is_up else (
                            (235, 239, 194) if region == 'upper' else (191, 164, 110)
                        ) if not polegar_direito_levantado else cor_regiao

                        cv2.circle(frame, (cx, cy), 10, cor_final, -1)

                        # desenhar o nome da nota na ponta do dedo, se aplicável
                        if key in key_note_labels:
                            nota = key_note_labels[key]
                            cv2.putText(frame, nota, (cx + 10, cy - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

        # nome da nota na interface
        if active_note:
            font = cv2.FONT_HERSHEY_SIMPLEX
            text = f"{active_note}"
            text_size = cv2.getTextSize(text, font, 1, 2)[0]
            text_x = w - text_size[0] - 20
            text_y = 40
            cv2.putText(frame, text, (text_x, text_y), font, 1, (255, 255, 255), 2, cv2.LINE_AA)

        cv2.imshow("FINGER PIANO", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()