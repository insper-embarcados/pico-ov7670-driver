import serial
import re
import time
import os
import glob

# --- Configurações da Câmera e da Serial ---
# As dimensões da imagem devem ser as mesmas do microcontrolador
WIDTH = 80
HEIGHT = 60
# A porta serial do seu microcontrolador (pode ser diferente no seu sistema)
SERIAL_PORT = '/dev/ttyACM0'
# A taxa de comunicação serial (baud rate) deve ser a mesma configurada no seu microcontrolador
BAUD_RATE = 115200

# --- Lógica de Numeração Sequencial ---
def get_next_image_number(base_dir):
    """
    Verifica a última imagem salva em todas as subpastas e retorna o próximo número disponível.
    """
    # Lista todos os arquivos .ppm em todas as subpastas
    files = glob.glob(os.path.join(base_dir, '**', '*.ppm'), recursive=True)
    
    if not files:
        return 0
    
    # Encontra o maior número de arquivo existente
    max_num = -1
    for f in files:
        match = re.search(r'image_(\d+)\.ppm', os.path.basename(f))
        if match:
            num = int(match.group(1))
            if num > max_num:
                max_num = num
    
    return max_num + 1

# --- Geração do Arquivo PPM ---
def generate_p2_ppm(raw_data, width, height, filename):
    """
    Gera um arquivo PPM em escala de cinza (P2) a partir de uma string de valores de pixel.
    """
    try:
        pixel_values = [int(n) for n in re.findall(r'\b\d+\b', raw_data)]
    except ValueError:
        print("❌ Erro ao converter dados. Verifique a formatação da saída da sua câmera.")
        return False

    if len(pixel_values) != width * height:
        print(f"❌ Erro: O número de pixels ({len(pixel_values)}) não corresponde às dimensões esperadas ({width * height}).")
        return False

    with open(filename, 'w') as f:
        # Cabeçalho PPM (P2 para imagens em escala de cinza)
        f.write("P2\n")
        f.write(f"{width} {height}\n")
        f.write("255\n")  # Valor máximo de pixel
        
        # Escreve os dados de pixel
        for i, y_value in enumerate(pixel_values):
            f.write(str(y_value))
            
            # Adiciona uma quebra de linha após cada linha de pixels
            if (i + 1) % width == 0:
                f.write("\n")
            else:
                f.write(" ")
    
    print(f"✅ Arquivo PPM '{filename}' gerado com sucesso!")
    return True

# --- Loop principal de leitura da serial ---
if __name__ == "__main__":
    BASE_DIR = 'train'
    
    # Pergunta pela label (rótulo) das imagens
    label = input("Qual é a label para as imagens que você vai capturar? (Ex: 'triangulo', 'numero_3'): ").strip()
    
    if not label:
        print("Label não fornecida. As imagens serão salvas na pasta principal de treino.")
        save_dir = BASE_DIR
    else:
        # Define o diretório de salvamento com base na label
        save_dir = os.path.join(BASE_DIR, label)

    # Cria a pasta de destino se ela não existir
    os.makedirs(save_dir, exist_ok=True)
    
    # Obtém o próximo número de imagem disponível
    IMAGE_COUNTER = get_next_image_number(BASE_DIR)
    print(f"Iniciando a captura para a label '{label}' com o número {IMAGE_COUNTER}.")

    # Inicia a comunicação serial
    try:
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
            print(f"Conectado a {ser.portstr}. Aguardando dados...")
            
            while True:
                line = ser.readline().decode('utf-8', 'ignore').strip()
                
                if "frame start:[" in line:
                    print("Início de frame detectado. Lendo dados...")
                    frame_data = line
                    
                    while "]frame finish" not in frame_data:
                        frame_data += ser.readline().decode('utf-8', 'ignore').strip()

                    # Gera o nome do arquivo com a numeração e o caminho da pasta
                    filename = os.path.join(save_dir, f"image_{IMAGE_COUNTER}.ppm")
                    
                    if generate_p2_ppm(frame_data, WIDTH, HEIGHT, filename):
                        IMAGE_COUNTER += 1

    except serial.SerialException as e:
        print(f"❌ Erro ao abrir a porta serial: {e}")
        print("Verifique se o microcontrolador está conectado, se a porta serial está correta e se você tem permissão para acessá-la.")
        print("Dica: Em sistemas Linux, pode ser necessário adicionar seu usuário ao grupo 'dialout' ou rodar com 'sudo'.")

    except KeyboardInterrupt:
        print("\nPrograma encerrado pelo usuário.")