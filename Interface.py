import customtkinter as ctk
from PIL import Image
from handplayer import HandPlayer
import webbrowser

# paleta de cores
preto = "#000000"
cinza = "#8C8A93"
branco = "#FFFFFF"
laranja = "#FF7F11"

class HandCamApp:
    def __init__(self):
        self.app = None
        self.handplayer = None
        self.label_video = None
        self.frame_principal = None
        self.frame_webcam = None
        self.piano_url = "https://www.onlinepianist.com/virtual-piano" # piano virtual
    
    def github_link(self):
        webbrowser.open("https://github.com/clxxxy/handsong")

    def cifras_link(self):
        webbrowser.open("https://ciframelodica.com.br") # site de cifras

    def init_ui(self):
        self.app = ctk.CTk()
        self.app.geometry("1280x720")
        self.app.title("Handsong")
        self.show_main_menu()

    def show_main_menu(self):

        # limpa frames anteriores se existirem
        if self.frame_webcam:
            self.frame_webcam.destroy()
            self.frame_webcam = None
        if self.handplayer:
            self.handplayer.stop()
            self.handplayer = None

        # cria o frame principal (menu)
        if not self.frame_principal:
            self.frame_principal = ctk.CTkFrame(self.app, fg_color=preto)
            self.frame_principal.pack(fill="both", expand=True, padx=20, pady=20)
        else:
             # limpa widgets do frame principal se já existir
            for widget in self.frame_principal.winfo_children():
                widget.destroy()
            self.frame_principal.pack(fill="both", expand=True, padx=20, pady=20) # garante que está visível
        
        try:
            logo_image = Image.open("interface\logo.png")
            ctk_logo = ctk.CTkImage(light_image=logo_image, size=(1000, 1000))
            logo_label = ctk.CTkLabel(self.frame_principal, image=ctk_logo, text="")
            logo_label.place(relx=0.5, rely=0.3, anchor=ctk.CENTER)

        except FileNotFoundError:
            print("Erro: Arquivo logo.png não encontrado.")
            logo_label = ctk.CTkLabel(self.frame_principal, text="[Handsong]")
            logo_label.place(relx=0.5, rely=0.3, anchor=ctk.CENTER)

        # botôes
        botao_play = ctk.CTkButton(self.frame_principal,
                                   text="iniciar",
                                   command=self.start_webcam_view,
                                   fg_color=cinza,
                                   hover_color=laranja,
                                   font=ctk.CTkFont(family="Century", size=24, weight="normal"))
        botao_play.place(relx=0.5, rely=0.7, anchor=ctk.CENTER)


        botao_cifras = ctk.CTkButton(self.frame_principal,
                                   text="cifras",
                                   command=self.cifras_link,
                                   fg_color=preto,
                                   hover_color=laranja,
                                   font=ctk.CTkFont(family="Century", size=16, weight="normal"))
        botao_cifras.place(relx=0.5, rely=0.8, anchor=ctk.CENTER)
        

        botao_link = ctk.CTkButton(self.frame_principal,
                                   text="github",
                                   command=self.github_link,
                                   fg_color=preto,
                                   hover_color=laranja,
                                   font=ctk.CTkFont(family="Century", size=16, weight="normal"))
        botao_link.place(relx=0.5, rely=0.85, anchor=ctk.CENTER)

        # label inferior
        label_inferior = ctk.CTkLabel(self.frame_principal,
                                    text="Handsong - v1.0 | desenvolvido por Cleydson Junior e Ismael Alves",
                                    font=ctk.CTkFont(family="Century", size=12, weight="normal"),
                                    text_color="gray")
        label_inferior.pack(side=ctk.BOTTOM, pady=10, padx=10)

    # frame da webcam
    def start_webcam_view(self):
        # esconde o frame principal
        if self.frame_principal:
            self.frame_principal.pack_forget()

        # cria o frame da webcam
        self.frame_webcam = ctk.CTkFrame(self.app, fg_color=preto)
        self.frame_webcam.pack(fill="both", expand=True, padx=20, pady=20)

        # label para o vídeo da webcam
        self.label_video = ctk.CTkLabel(self.frame_webcam, text="")
        self.label_video.pack(pady=0, padx=0, anchor=ctk.CENTER, fill="both", expand=True)

        # botões
        botao_abrir_piano = ctk.CTkButton(self.frame_webcam,
                                          text="Abrir Piano Virtual",
                                          command=self.abrir_piano,
                                          fg_color=preto,
                                          hover_color=laranja,
                                          font=ctk.CTkFont(family="Century", size=16, weight="normal"))
        botao_abrir_piano.pack(pady=50, padx=100, side=ctk.RIGHT)


        botao_voltar = ctk.CTkButton(self.frame_webcam,
                                     text="Voltar ao Menu",
                                     command=self.show_main_menu,
                                     fg_color=preto,
                                     hover_color=laranja,
                                     font=ctk.CTkFont(family="Century", size=16, weight="normal"))
        botao_voltar.pack(pady=50, padx=100, side=ctk.LEFT)

        try:
            logo_path = "interface\logo.png"
            tamanho_logo_pequena = (110, 110)

            pil_logo = Image.open(logo_path)
            ctk_logo_pequena = ctk.CTkImage(light_image=pil_logo, size=tamanho_logo_pequena)

            logo_label_webcam = ctk.CTkLabel(self.frame_webcam, image=ctk_logo_pequena, text="")
            logo_label_webcam.place(relx=0.5, rely=1.0, anchor=ctk.S, y=-10) 

        except FileNotFoundError:
            print(f"Erro: Arquivo da logo '{logo_path}' não encontrado para o frame da webcam.")
        except Exception as e:
            print(f"Erro ao carregar logo para webcam: {e}")

        # inicializa o HandPlayer
        self.handplayer = HandPlayer()
        self._atualizar_frame()

    # abre o piano virtual
    def abrir_piano(self):
        webbrowser.open(self.piano_url)

    def _atualizar_frame(self):
        if not self.frame_webcam or not self.frame_webcam.winfo_exists():
            if self.handplayer:
                self.handplayer.stop()
                self.handplayer = None
            return

        if self.handplayer:
            frame = self.handplayer.get_frame()
            if frame:
                max_width = self.frame_webcam.winfo_width() * 0.7
                max_height = self.frame_webcam.winfo_height() - 100
                
                if max_width > 10 and max_height > 10:
                    frame.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
                    ctk_image = ctk.CTkImage(light_image=frame, size=frame.size)
                    self.label_video.configure(image=ctk_image)
                    self.label_video.image = ctk_image
                else:
                     self.label_video.configure(image=None)
                     self.label_video.image = None
            self.app.after(10, self._atualizar_frame)
        else:
             self.label_video.configure(image=None)
             self.label_video.image = None

    def run(self):
        self.init_ui()
        self.app.mainloop()

        # garante que a câmera seja liberada ao fechar
        if self.handplayer:
            self.handplayer.stop()

if __name__ == "__main__":
    app_instance = HandCamApp()
    app_instance.run()