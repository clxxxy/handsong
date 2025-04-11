# HANDSong
Projeto final da cadeira de IA aplicada à Música
- - -
Este projeto permite que você toque piano virtual usando os dedos detectados por uma câmera, com reconhecimento em tempo real através da biblioteca [MediaPipe](https://github.com/google/mediapipe) e controle de teclado via [PyAutoGUI](https://pyautogui.readthedocs.io/). O sistema interage com o site [Online Pianist](https://www.onlinepianist.com/virtual-piano) de forma automatizada, simulando pressionamentos de tecla conforme o movimento dos dedos.

## Como Funciona

- O sistema identifica mãos e dedos em tempo real usando MediaPipe.
- Os dedos levantados são mapeados para notas do piano virtual.
- A tela é dividida em duas regiões (superior e inferior) para simular oitavas diferentes.
- Um polegar direito levantado alterna para notas sustenidas (C#, D#, etc).
- Cada dedo é mapeado para uma tecla do teclado que corresponde a uma nota no piano virtual.
- A tecla correspondente é "pressionada" automaticamente quando um dedo é detectado como abaixado.

## Tecnologias Utilizadas

- Python 3
- OpenCV
- MediaPipe
- PyAutoGUI
- Webbrowser (abre o piano virtual no navegador)

## Pré-requisitos

Instale as dependências necessárias:

```bash
pip install opencv-python mediapipe pyautogui
```

## Como Usar

- Execute o código
- O navegador abrirá automaticamente o site do piano virtual.
- Posicione sua mão na frente da webcam.
- Toque as "teclas" movendo e abaixando os dedos.

## Interface

- A interface desenha os dedos com cores diferentes dependendo da região (superior/inferior).
- Exibe o nome da nota na ponta do dedo quando ativada.
- Mostra a nota ativa no canto superior direito da tela.

- - -

> Este projeto é livre para uso educacional e experimental.
