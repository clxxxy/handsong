import cv2
import pyautogui
import mediapipe as mp

from PIL import Image

# Definição da Paleta de Cores
preto = (0, 0, 0)
cinza_claro = (224, 224, 224)
cinza_escuro = (74, 69, 70)
branco = (255, 255, 255)
laranja = (17, 127, 255)

# Class HandPlayer: responsável por capturar e processar a imagem da webcam
class HandPlayer:

    # Construtor da classe HandPlayer, inicializa a webcam e configura os parâmetros de captura, e os mapeamentos de dedos para teclas
    def __init__(self, width=640, height=480):
        self.width = width
        self.height = height
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7)
        
        self.prev_finger_state = {}
        self.active_notes = set()
        self.active_keys = {}  # Controle de teclas pressionadas

        # Mapeamento de dedos para teclas
        self.finger_map_lower_default = {(20, 'Left'): 'q', (12, 'Left'): 'w', (8, 'Left'): 'e', (4, 'Left'): 'r', (8, 'Right'): 't', (12, 'Right'): 'y', (20, 'Right'): 'u'}
        self.finger_map_lower_polegar = {(20, 'Left'): '2', (12, 'Left'): '3', (8, 'Left'): None, (4, 'Left'): '5', (8, 'Right'): '6', (12, 'Right'): '7', (20, 'Right'): None}
        self.finger_map_upper_default = {(20, 'Left'): 'i', (12, 'Left'): 'o', (8, 'Left'): 'p', (4, 'Left'): 'z', (8, 'Right'): 'x', (12, 'Right'): 'c', (20, 'Right'): 'v'}
        self.finger_map_upper_polegar = {(20, 'Left'): '9', (12, 'Left'): '0', (8, 'Left'): None, (4, 'Left'): 's', (8, 'Right'): 'd', (12, 'Right'): 'f', (20, 'Right'): None}
        self.key_note_labels = {'q': 'C3', 'w': 'D3', 'e': 'E3', 'r': 'F3', 't': 'G3', 'y': 'A3', 'u': 'B3', '2': 'C#3', '3': 'D#3', '5': 'F#3', '6': 'G#3', '7': 'A#3', 'i': 'C4', 'o': 'D4', 'p': 'E4', 'z': 'F4', 'x': 'G4', 'c': 'A4', 'v': 'B4', '9': 'C#4', '0': 'D#4', 's': 'F#4', 'd': 'G#4', 'f': 'A#4'}

    # Verifica se o dedo está levantado, comparando a posição da ponta do dedo com a posição da articulação
    def is_finger_up(self, landmarks, tip_id, hand_label):
        if tip_id == 4:
            if hand_label == 'Left':
                return landmarks.landmark[tip_id].x < landmarks.landmark[tip_id - 2].x
            else:
                return landmarks.landmark[tip_id].x > landmarks.landmark[tip_id - 2].x
        else:
            return landmarks.landmark[tip_id].y < landmarks.landmark[tip_id - 2].y

    # Polegar de controle: alterna entre notas comuns e sustenidas
    def is_thumb_typing_up(self, landmarks, hand_label):
        tip_id = 4
        return landmarks.landmark[tip_id].x < landmarks.landmark[tip_id - 2].x if hand_label == 'Left' else landmarks.landmark[tip_id].x > landmarks.landmark[tip_id - 2].x

    # Processa o frame da webcam, detecta as mãos e os dedos, e envia os comandos de teclado correspondentes
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

        # Desenha a linha de refêrencia para as duas regiões de oitavas
        mid_line_y = h // 2
        cv2.line(frame, (0, mid_line_y), (w, mid_line_y), (255, 255, 255), 2)

        # Armazena as teclas que devem estar pressionadas neste frame, e limpa a lista de notas ativas
        current_keys = set()  
        self.active_notes.clear()

        # Verifica se há mãos detectadas e se o polegar direito está levantado
        if results.multi_hand_landmarks and results.multi_handedness:
            polegar_direito_levantado = False

            # Detecção do polegar direito
            for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                if handedness.classification[0].label == 'Right':
                    polegar_direito_levantado = self.is_finger_up(hand_landmarks, 4, 'Right')
                    break
            
            # Detecta o estado dos dedos e atualiza as teclas pressionadas
            for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                hand_label = handedness.classification[0].label
                center_y = hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y * h
                region = 'upper' if center_y < mid_line_y else 'lower'

                finger_map = (self.finger_map_upper_polegar if polegar_direito_levantado else self.finger_map_upper_default) if region == 'upper' else (self.finger_map_lower_polegar if polegar_direito_levantado else self.finger_map_lower_default)

                for (tip_id, label) in finger_map:
                    if label == hand_label:
                        finger_id = (tip_id, hand_label)
                        key = finger_map[finger_id]
                        if key is None:
                            continue

                        # Lógica de detecção de estado do dedo
                        is_control_thumb = (tip_id == 4 and hand_label == 'Right' and polegar_direito_levantado)
                        is_typing_thumb = (tip_id == 4 and not is_control_thumb)
                        is_up = not self.is_thumb_typing_up(hand_landmarks, hand_label) if is_typing_thumb else self.is_finger_up(hand_landmarks, tip_id, hand_label)

                        if finger_id not in self.prev_finger_state:
                            self.prev_finger_state[finger_id] = True
                        self.prev_finger_state[finger_id] = is_up

                        # Adiciona à lista de teclas atuais se estiver pressionado
                        if not is_up and key in self.key_note_labels:
                            current_keys.add(key)
                            self.active_notes.add(self.key_note_labels[key])

                        # Código de desenho
                        cx = int(hand_landmarks.landmark[tip_id].x * w)
                        cy = int(hand_landmarks.landmark[tip_id].y * h)
                        cor_final = laranja if not is_up else (branco if region == 'upper' else cinza_claro) if not polegar_direito_levantado else preto if region == 'upper' else cinza_escuro
                        cv2.circle(frame, (cx, cy), 10, cor_final, -1)
                        if key in self.key_note_labels:
                            cv2.putText(frame, self.key_note_labels[key], (cx + 10, cy - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

        # Atualiza estados das teclas
        for key in list(self.active_keys.keys()):
            if key not in current_keys:
                pyautogui.keyUp(key)
                del self.active_keys[key]

        for key in current_keys:
            if key not in self.active_keys:
                pyautogui.keyDown(key)
                self.active_keys[key] = True
                pyautogui.sleep(0.02)  # pequeno delay para estabilização

        # Exibição de notas ativas
        if self.active_notes:
            text = ", ".join(sorted(self.active_notes))
            text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
            cv2.putText(frame, text, (w - text_size[0] - 20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        return Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    def stop(self):
        for key in list(self.active_keys.keys()):
            pyautogui.keyUp(key)
        self.active_keys.clear()
        self.cap.release()