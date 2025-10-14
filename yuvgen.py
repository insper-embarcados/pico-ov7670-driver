import serial
import re
import time
from PIL import Image
import numpy as np

# --- Configurações da Câmera e da Serial ---
# As dimensões da imagem devem ser as mesmas do microcontrolador
WIDTH = 80
HEIGHT = 60
# A porta serial do seu microcontrolador (pode ser diferente no seu sistema)
PORTA_SERIAL = '/dev/ttyACM0'
# A taxa de comunicação serial (baud rate) deve ser a mesma configurada no seu microcontrolador
BAUD_RATE = 115200

def gerar_jpeg_luminancia(dados_brutos, largura, altura, nome_arquivo):
    """
    Gera um arquivo JPEG em escala de cinza a partir de uma string de valores de luminância (Y).
    """
    try:
        # Extrai todos os números da string
        valores_y = [int(n) for n in re.findall(r'\b\d+\b', dados_brutos)]
    except ValueError:
        print("❌ Erro ao converter dados. Verifique a formatação da saída da sua câmera.")
        return False

    if len(valores_y) != largura * altura:
        print(f"❌ Erro: O número de valores Y ({len(valores_y)}) não corresponde às dimensões esperadas ({largura * altura}).")
        return False

    # Converte a lista de valores em uma matriz NumPy
    array_pixels = np.array(valores_y, dtype=np.uint8).reshape((altura, largura))
    
    # Cria um objeto de imagem Pillow a partir do array de pixels
    # O modo 'L' é para imagens de 8-bit em escala de cinza (Luminância)
    try:
        imagem = Image.fromarray(array_pixels, 'L')
    except ValueError as e:
        print(f"❌ Erro ao criar a imagem Pillow: {e}")
        return False
        
    # Salva a imagem como JPEG
    try:
        imagem.save(nome_arquivo, 'JPEG')
        print(f"✅ Arquivo JPEG de luminância '{nome_arquivo}' gerado com sucesso!")
        return True
    except Exception as e:
        print(f"❌ Erro ao salvar o arquivo JPEG: {e}")
        return False

# --- Loop de leitura da serial ---
try:
    with serial.Serial(PORTA_SERIAL, BAUD_RATE, timeout=1) as ser:
        print(f"Conectado a {ser.portstr}. Aguardando dados de luminância (Y)...")
        
        while True:
            line = ser.readline().decode('utf-8', 'ignore').strip()
            
            if "frame start:[" in line:
                print("Início de frame Y detectado. Lendo dados...")
                dados_frame_y = line
                
                # Lê o resto do frame até encontrar o marcador de fim
                while "]frame finish" not in dados_frame_y:
                    dados_frame_y += ser.readline().decode('utf-8', 'ignore').strip()

                timestamp = int(time.time())
                nome_arquivo = f"luminancia_Y_{timestamp}.jpg"
                
                gerar_jpeg_luminancia(dados_frame_y, WIDTH, HEIGHT, nome_arquivo)

except serial.SerialException as e:
    print(f"❌ Erro ao abrir a porta serial: {e}")
    print("Verifique se o microcontrolador está conectado, se a porta está correta e se o usuário tem permissão para acessá-la.")
    print("Dica: Em sistemas Linux, pode ser necessário adicionar seu usuário ao grupo 'dialout' ou rodar com 'sudo'.")

except KeyboardInterrupt:
    print("\nPrograma encerrado pelo usuário.")