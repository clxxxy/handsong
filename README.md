<img src="https://github.com/clxxxy/handsong/blob/main/interface/logo.png" largura="300" />

# handsong: gesture-powered music
Projeto final da cadeira de IA aplicada à música
- - -
Este projeto permite que você toque piano virtual usando os dedos detectados por uma câmera, com reconhecimento em tempo real através das bibliotecas [MediaPipe](https://github.com/google/mediapipe) e [OpenCV](https://opencv.org). O sistema interage com o site [Online Pianist](https://www.onlinepianist.com/virtual-piano) de forma automatizada, simulando pressionamentos de tecla com[PyAutoGUI](https://pyautogui.readthedocs.io/) conforme o movimento dos dedos.

## Como Funciona

- O sistema identifica mãos e dedos em tempo real usando MediaPipe.
- Os dedos levantados são mapeados para notas do piano virtual.
- A tela é dividida em duas regiões (superior e inferior) para simular oitavas diferentes.
- Um polegar direito alterna para notas sustenidas (C#, D#, etc).
- Cada dedo é mapeado para uma tecla do teclado que corresponde a uma nota no piano virtual.
- A tecla correspondente é "pressionada" automaticamente quando um dedo é detectado como abaixado.

## Tecnologias Utilizadas

- Python
- OpenCV
- MediaPipe
- PyAutoGUI
- CustomTkinter

## Pré-requisitos

Instale as dependências necessárias:

```bash
pip install opencv-python mediapipe pyautogui customtkinter
```

## Resultados

A aplicação consegue entregar o feedback sonoro e visual de forma rápida e simples, sem a necessidade de hardware externo, alto poder computacional e webcams de altas resoluções.

Em nossos testes, ambientes com o mínimo de luminosidade conseguem entregar o feedback sonoro e visual, porém, com alguns pequenos bugs nos gestos e, portanto, recomenda-se um ambiente com as mãos bem iluminadas para uma melhor experiência.

## Possíveis melhorias

- Integração com software de produção musical (DAW).
- Exploração de aplicações em realidade aumentada.
- Adição de novos instrumentos e gestos.

## Trabalhos futuros

- Usar a base do app e seus conceitos para outras áreas, como acessibilidade e produtividade.
- Fine-tuning de modelos de detecção de gestos para melhor precisão.

- - -

> handsong v1.0 | desenvolvido por Cleydson Junior e Ismael Alves. Este projeto é livre para uso educacional e experimental.
