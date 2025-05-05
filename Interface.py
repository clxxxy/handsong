import customtkinter as ctk
from PIL import Image
from handplayer import HandPlayer
import webbrowser # Adicionado para abrir o site do piano

# Paleta de cores
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
        self.piano_url = "https://www.onlinepianist.com/virtual-piano" # URL do piano virtual
    
    def github_link(self):
        webbrowser.open("https://github.com/clxxxy/handsong")

    def cifras_link(self):
        webbrowser.open("https://ciframelodica.com.br")  

    def init_ui(self):
        self.app = ctk.CTk()
        self.app.geometry("1280x720")
        self.app.title("Handsong")
        self.show_main_menu()

    def show_main_menu(self):
        # Limpa frames anteriores se existirem
        if self.frame_webcam:
            self.frame_webcam.destroy()
            self.frame_webcam = None
        if self.handplayer:
            self.handplayer.stop()
            self.handplayer = None

        # Cria o frame principal (menu)
        if not self.frame_principal:
            self.frame_principal = ctk.CTkFrame(self.app, fg_color=preto)
            self.frame_principal.pack(fill="both", expand=True, padx=20, pady=20)
        else:
             # Limpa widgets do frame principal se já existir
            for widget in self.frame_principal.winfo_children():
                widget.destroy()
            self.frame_principal.pack(fill="both", expand=True, padx=20, pady=20) # Garante que está visível
        
        try:
            logo_image = Image.open("interface\logo.png") # Carrega a imagem
            ctk_logo = ctk.CTkImage(light_image=logo_image, size=(1000, 1000)) # Ajuste tamanho
            logo_label = ctk.CTkLabel(self.frame_principal, image=ctk_logo, text="")
            logo_label.place(relx=0.5, rely=0.3, anchor=ctk.CENTER) # Ajuste a posição (rely)
        except FileNotFoundError:
            print("Erro: Arquivo logo.png não encontrado.")
            # Opcional: adicionar um texto substituto se a logo não for encontrada
            logo_label = ctk.CTkLabel(self.frame_principal, text="[Handsong]")
            logo_label.place(relx=0.5, rely=0.3, anchor=ctk.CENTER)

        # Botão PLAY
        botao_play = ctk.CTkButton(self.frame_principal,
                                   text="Play",
                                   command=self.start_webcam_view,
                                   fg_color=cinza,
                                   hover_color=laranja,
                                   font=ctk.CTkFont(family="Century", size=24, weight="normal"))
        # Centraliza o botão
        botao_play.place(relx=0.5, rely=0.7, anchor=ctk.CENTER)

        botao_cifras = ctk.CTkButton(self.frame_principal,
                                   text="Cifras",
                                   command=self.cifras_link,
                                   fg_color=preto,
                                   hover_color=laranja,
                                   font=ctk.CTkFont(family="Century", size=16, weight="normal"))
        
        # Posicione o botão onde desejar, por exemplo:
        botao_cifras.place(relx=0.5, rely=0.8, anchor=ctk.CENTER) # Ajuste a posição
        
        # Dentro de show_main_menu, adicione o botão:
        botao_link = ctk.CTkButton(self.frame_principal,
                                   text="Github",
                                   command=self.github_link,
                                   fg_color=preto,
                                   hover_color=laranja,
                                   font=ctk.CTkFont(family="Century", size=16, weight="normal"))
        
        # Posicione o botão onde desejar, por exemplo:
        botao_link.place(relx=0.5, rely=0.85, anchor=ctk.CENTER) # Ajuste a posição

        # Cria o label na parte inferior
        label_inferior = ctk.CTkLabel(self.frame_principal,
                                    text="Handsong - v1.0 | desenvolvido por Cleydson Junior e Ismael Alves", # Coloque seu texto
                                    font=ctk.CTkFont(family="Century", size=12, weight="normal"),
                                    text_color="gray") # Cor opcional para menos destaque

        # Posiciona o label na parte inferior do frame principal
        label_inferior.pack(side=ctk.BOTTOM, pady=10, padx=10)


    def start_webcam_view(self):
        # Esconde o frame principal
        if self.frame_principal:
            self.frame_principal.pack_forget()

        # Cria o frame da webcam
        self.frame_webcam = ctk.CTkFrame(self.app, fg_color=preto)
        self.frame_webcam.pack(fill="both", expand=True, padx=20, pady=20)

        # Label para o vídeo da webcam
        self.label_video = ctk.CTkLabel(self.frame_webcam, text="")
        self.label_video.pack(pady=0, padx=0, anchor=ctk.CENTER, fill="both", expand=True)

        # Botão para abrir o site do piano
        botao_abrir_piano = ctk.CTkButton(self.frame_webcam,
                                          text="Abrir Piano Virtual",
                                          command=self.abrir_piano,
                                          fg_color=preto,
                                          hover_color=laranja,
                                          font=ctk.CTkFont(family="Century", size=16, weight="normal"))
        botao_abrir_piano.pack(pady=50, padx=100, side=ctk.RIGHT)

        # Botão Voltar
        botao_voltar = ctk.CTkButton(self.frame_webcam,
                                     text="Voltar ao Menu",
                                     command=self.show_main_menu,
                                     fg_color=preto,
                                     hover_color=laranja,
                                     font=ctk.CTkFont(family="Century", size=16, weight="normal"))
        botao_voltar.pack(pady=50, padx=100, side=ctk.LEFT)

        try:
            logo_path = "interface\logo.png" # <<< Certifique-se que este é o caminho correto
            tamanho_logo_pequena = (110, 110) # <<< Ajuste o tamanho desejado aqui

            pil_logo = Image.open(logo_path)
            ctk_logo_pequena = ctk.CTkImage(light_image=pil_logo, size=tamanho_logo_pequena)

            logo_label_webcam = ctk.CTkLabel(self.frame_webcam, image=ctk_logo_pequena, text="")
            logo_label_webcam.place(relx=0.5, rely=1.0, anchor=ctk.S, y=-10) 

        except FileNotFoundError:
            print(f"Erro: Arquivo da logo '{logo_path}' não encontrado para o frame da webcam.")
        except Exception as e:
            print(f"Erro ao carregar logo para webcam: {e}")
        # --- Fim Adicionar Logo ---

        # Inicializa o HandPlayer
        self.handplayer = HandPlayer()
        self._atualizar_frame()

    def abrir_piano(self):
        # Abre a URL do piano no navegador padrão
        webbrowser.open(self.piano_url)

    def _atualizar_frame(self):
        # Verifica se o frame da webcam ainda existe
        if not self.frame_webcam or not self.frame_webcam.winfo_exists():
            if self.handplayer:
                self.handplayer.stop()
                self.handplayer = None
            return # Para a atualização se o frame foi destruído

        if self.handplayer:
            frame = self.handplayer.get_frame()
            if frame:
                # Redimensiona a imagem para caber melhor, mantendo a proporção
                max_width = self.frame_webcam.winfo_width() * 0.7 # Ajuste conforme necessário
                max_height = self.frame_webcam.winfo_height() - 100 # Ajuste para espaço dos botões
                
                if max_width > 10 and max_height > 10: # Evita divisão por zero ou tamanho inválido
                    frame.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
                    ctk_image = ctk.CTkImage(light_image=frame, size=frame.size)
                    self.label_video.configure(image=ctk_image)
                    self.label_video.image = ctk_image
                else:
                     # Se o tamanho do frame for inválido, mostra um placeholder ou nada
                     self.label_video.configure(image=None)
                     self.label_video.image = None

            # Agenda a próxima atualização
            self.app.after(10, self._atualizar_frame)
        else:
             # Se handplayer não existe mais, limpa a imagem
             self.label_video.configure(image=None)
             self.label_video.image = None

    def run(self):
        self.init_ui()
        self.app.mainloop()
        # Garante que a câmera seja liberada ao fechar
        if self.handplayer:
            self.handplayer.stop()

if __name__ == "__main__":
    app_instance = HandCamApp()
    app_instance.run()