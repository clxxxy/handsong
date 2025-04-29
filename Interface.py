import pygame
import customtkinter as ctk
import time
from threading import Thread
from PIL import Image
from handplayer import HandPlayer

class MusicPlayerApp:
    def __init__(self):
        self.musicas = [
            {"nome": "Fur Elise", "arquivo": "songs/Anunciação.mp3"},
            {"nome": "Anunciação", "arquivo": ".mp3"},
            {"nome": "Jingle Bells", "arquivo": ".mp3"},
        ]
        self.musica_selecionada = None
        self.app = None
        self.handplayer = None
        self.label_video = None
        self.countdown_label = None
        self.botao_confirmar = None

    def init_ui(self):
        self.app = ctk.CTk()
        self.app.geometry("1280x720")
        self.app.title("HandSong 🎵🎶")

        self.frame_principal = ctk.CTkFrame(self.app)
        self.frame_principal.pack(fill="both", expand=True)

        self.label_instrucao = ctk.CTkLabel(self.frame_principal, text="Selecione uma música:", font=ctk.CTkFont(size=20))
        self.label_instrucao.pack(pady=10)

        for musica in self.musicas:
            ctk.CTkButton(self.frame_principal, text=musica['nome'], command=lambda m=musica: self.selecionar_musica(m)).pack(pady=5)

        self.botao_confirmar = ctk.CTkButton(self.frame_principal, text="Confirmar Música", command=self.confirmar)
        self.botao_confirmar.pack(pady=20)

    def selecionar_musica(self, musica):
        self.musica_selecionada = musica
        print(f"Selecionado: {musica['nome']}")

    def confirmar(self):
        if not self.musica_selecionada:
            print("Nenhuma música selecionada!")
            return

        for widget in self.frame_principal.winfo_children():
            widget.destroy()

        self.label_video = ctk.CTkLabel(self.frame_principal, text="")
        self.label_video.pack(pady=10)

        self.countdown_label = ctk.CTkLabel(self.frame_principal, font=ctk.CTkFont(size=48, weight="bold"))
        self.countdown_label.pack(pady=10)

        pygame.mixer.init()
        self.handplayer = HandPlayer()

        Thread(target=self._contagem_regressiva_e_tocar, daemon=True).start()
        self._atualizar_frame()

    def _contagem_regressiva_e_tocar(self):
        for i in range(3, 0, -1):
            self.countdown_label.configure(text=str(i))
            time.sleep(1)
        self.countdown_label.configure(text="Tocando!")
        pygame.mixer.music.load(self.musica_selecionada['arquivo'])
        pygame.mixer.music.play()
        time.sleep(1)
        self.countdown_label.pack_forget()

    def _atualizar_frame(self):
        frame = self.handplayer.get_frame()
        if frame:
            ctk_image = ctk.CTkImage(light_image=frame, size=(640, 480))
            self.label_video.configure(image=ctk_image)
            self.label_video.image = ctk_image
        self.app.after(10, self._atualizar_frame)

    def run(self):
        self.init_ui()
        self.app.mainloop()

if __name__ == "__main__":
    MusicPlayerApp().run()
