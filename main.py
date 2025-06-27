"""
FatigueSensor - Sistema de Detecção Automática de Fadiga em Motoristas
Utilizando Visão Computacional

Autor: Aluisio Martins Junior
Data: Junho 2025
Disciplina: Visão Computacional

Descrição:
    Sistema completo para detecção de fadiga através de análise facial em tempo real,
    utilizando algoritmos de visão computacional para monitorar padrões de piscada,
    detecção de bocejos e geração de alertas de segurança.

Funcionamento:
    1. Captura de vídeo em tempo real da webcam
    2. Detecção facial usando Haar Cascades (OpenCV)
    3. Extração de 68 marcos faciais usando dlib
    4. Cálculo de métricas EAR (Eye Aspect Ratio) e MAR (Mouth Aspect Ratio)
    5. Análise temporal e detecção de padrões de fadiga
    6. Geração de alertas visuais e sonoros

Dependências:
    - OpenCV: Processamento de imagem e detecção facial
    - dlib: Detecção de marcos faciais (shape_predictor_68_face_landmarks.dat)
    - NumPy: Operações numéricas
    - SciPy: Cálculo de distâncias euclidianas
    - Pygame: Sistema de áudio para alertas

Arquivos Necessários:
    - shape_predictor_68_face_landmarks.dat: Modelo pré-treinado do dlib
      Download: https://huggingface.co/spaces/asdasdasdasd/Face-forgery-detection/resolve/ccfc24642e0210d4d885bc7b3dbc9a68ed948ad6/shape_predictor_68_face_landmarks.dat

Uso:
    python main.py [--ear-threshold VALOR] [--mar-threshold VALOR]

Controles:
    - 'q': Sair do sistema
    - 'r': Resetar contadores
"""

import cv2
import numpy as np
import dlib
import time
import threading
import pygame
from scipy.spatial import distance as dist
from collections import deque
import argparse
import sys


class FatigueDetector:
    """
    Classe principal para detecção de fadiga em tempo real.

    Esta classe implementa um sistema completo de detecção de fadiga utilizando
    análise facial em tempo real. O sistema monitora padrões de piscada e
    detecção de bocejos para determinar o nível de fadiga do usuário.

    Atributos:
        EAR_THRESHOLD (float): Limiar para detecção de olhos fechados (padrão: 0.25)
        EAR_CONSEC_FRAMES (int): Frames consecutivos para confirmar piscada (padrão: 20)
        MAR_THRESHOLD (float): Limiar para detecção de bocejo (padrão: 0.65)
        MAR_CONSEC_FRAMES (int): Frames consecutivos para confirmar bocejo (padrão: 15)

    Métodos Principais:
        run(): Executa o loop principal do sistema
        process_frame(): Processa um frame individual
        analyze_fatigue_indicators(): Analisa indicadores de fadiga

    Exemplo:
        >>> detector = FatigueDetector()
        >>> detector.run()  # Inicia o sistema
    """

    def __init__(self):
        """
        Inicializa o detector de fadiga com todos os parâmetros necessários.

        Configura os limiares de detecção, inicializa contadores, histórico de dados,
        detectores faciais e sistema de áudio para alertas.

        Raises:
            SystemExit: Se não conseguir inicializar os detectores necessários
        """
        # Parâmetros de detecção
        self.EAR_THRESHOLD = 0.25  # Limiar para detecção de olhos fechados
        self.EAR_CONSEC_FRAMES = 20  # Frames consecutivos para confirmar piscada
        self.MAR_THRESHOLD = 0.65  # Limiar para detecção de bocejo
        self.MAR_CONSEC_FRAMES = 15  # Frames consecutivos para confirmar bocejo

        # Contadores
        self.eye_frame_counter = 0
        self.mouth_frame_counter = 0
        self.blink_counter = 0
        self.yawn_counter = 0

        # Estado do sistema
        self.fatigue_detected = False
        self.alert_active = False

        # Histórico para análise temporal
        self.ear_history = deque(maxlen=30)  # Últimos 30 frames
        self.mar_history = deque(maxlen=30)

        # Inicialização dos detectores
        self.init_detectors()

        # Inicialização do sistema de som
        self.init_audio()

        # Métricas de performance
        self.fps_counter = 0
        self.start_time = time.time()

    def init_detectors(self):
        """
        Inicializa os detectores faciais e de marcos
        """
        try:
            # Detector de faces Haar Cascade
            self.face_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
            )

            # Preditor de marcos faciais dlib
            # Nota: É necessário baixar o arquivo shape_predictor_68_face_landmarks.dat
            self.predictor = dlib.shape_predictor(
                "shape_predictor_68_face_landmarks.dat"
            )

            print("✓ Detectores inicializados com sucesso")

        except Exception as e:
            print(f"✗ Erro ao inicializar detectores: {e}")
            print(
                "Certifique-se de ter o arquivo 'shape_predictor_68_face_landmarks.dat'"
            )
            sys.exit(1)

    def init_audio(self):
        """
        Inicializa o sistema de áudio para alertas
        """
        try:
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
            self.alert_sound_loaded = False
            print("✓ Sistema de áudio inicializado")
        except Exception as e:
            print(f"⚠ Aviso: Sistema de áudio não disponível: {e}")
            self.alert_sound_loaded = False

    def calculate_ear(self, eye_landmarks):
        """
        Calcula o Eye Aspect Ratio (EAR) para detecção de piscadas.

        O EAR é uma métrica que mede a abertura dos olhos baseada nas distâncias
        entre marcos faciais específicos. Valores baixos indicam olhos fechados.

        Fórmula: EAR = (|p2-p6| + |p3-p5|) / (2 * |p1-p4|)
        onde p1-p6 são os 6 marcos do olho ordenados da esquerda para direita.

        Args:
            eye_landmarks (numpy.ndarray): Array 6x2 com coordenadas (x,y) dos
                                          marcos do olho na seguinte ordem:
                                          [canto_esq, topo_esq, topo_dir, canto_dir,
                                           baixo_dir, baixo_esq]

        Returns:
            float: Valor EAR calculado. Valores típicos:
                   - > 0.25: Olho aberto
                   - < 0.25: Olho fechado/piscando
                   - < 0.20: Olho muito fechado (possível sonolência)

        Note:
            O EAR é invariante à escala e rotação da face, tornando-o robusto
            para diferentes posições e distâncias da câmera.
        """
        # Distâncias verticais
        A = dist.euclidean(eye_landmarks[1], eye_landmarks[5])
        B = dist.euclidean(eye_landmarks[2], eye_landmarks[4])

        # Distância horizontal
        C = dist.euclidean(eye_landmarks[0], eye_landmarks[3])

        # Cálculo do EAR
        ear = (A + B) / (2.0 * C)
        return ear

    def calculate_mar(self, mouth_landmarks):
        """
        Calcula o Mouth Aspect Ratio (MAR) para detecção de bocejos.

        O MAR é uma métrica que mede a abertura da boca baseada nas distâncias
        entre marcos faciais específicos. Valores altos indicam boca aberta (bocejo).

        Fórmula: MAR = (|p51-p59| + |p53-p57|) / (2 * |p49-p55|)
        onde os índices se referem aos 68 marcos faciais do dlib.

        Args:
            mouth_landmarks (numpy.ndarray): Array 20x2 com coordenadas (x,y) dos
                                           marcos da boca (pontos 48-67 do dlib).
                                           Ordem: contorno externo da boca.

        Returns:
            float: Valor MAR calculado. Valores típicos:
                   - < 0.5: Boca fechada
                   - 0.5-0.65: Boca ligeiramente aberta
                   - > 0.65: Bocejo detectado
                   - > 0.8: Bocejo pronunciado

        Note:
            O MAR é mais sensível a variações individuais que o EAR.
            Pode ser necessário ajustar o limiar para diferentes usuários.
        """
        # Distâncias verticais
        A = dist.euclidean(mouth_landmarks[2], mouth_landmarks[10])  # 51, 59
        B = dist.euclidean(mouth_landmarks[4], mouth_landmarks[8])  # 53, 57

        # Distância horizontal
        C = dist.euclidean(mouth_landmarks[0], mouth_landmarks[6])  # 49, 55

        # Cálculo do MAR
        mar = (A + B) / (2.0 * C)
        return mar

    def extract_face_landmarks(self, frame, face_rect):
        """
        Extrai marcos faciais de uma região facial detectada

        Args:
            frame: Frame de vídeo
            face_rect: Retângulo da face detectada

        Returns:
            numpy.array: Array com coordenadas dos marcos faciais
        """
        # Converte retângulo OpenCV para formato dlib
        dlib_rect = dlib.rectangle(
            int(face_rect[0]),
            int(face_rect[1]),
            int(face_rect[0] + face_rect[2]),
            int(face_rect[1] + face_rect[3]),
        )

        # Predição dos marcos faciais
        landmarks = self.predictor(frame, dlib_rect)

        # Converte para array numpy
        coords = np.zeros((68, 2), dtype=int)
        for i in range(68):
            coords[i] = (landmarks.part(i).x, landmarks.part(i).y)

        return coords

    def analyze_fatigue_indicators(self, ear_left, ear_right, mar):
        """
        Analisa os indicadores de fadiga e determina o estado de alerta.

        Este método é o núcleo do sistema de detecção de fadiga. Ele analisa
        métricas temporais de EAR e MAR para detectar padrões indicativos de
        sonolência, incluindo piscadas prolongadas e bocejos frequentes.

        Processo de Análise:
        1. Calcula EAR médio dos dois olhos
        2. Atualiza histórico temporal das métricas
        3. Detecta piscadas com base em frames consecutivos de EAR baixo
        4. Detecta bocejos com base em frames consecutivos de MAR alto
        5. Calcula taxas de piscadas e bocejos por minuto
        6. Computa score de fadiga usando lógica fuzzy

        Args:
            ear_left (float): EAR do olho esquerdo (0.0-1.0)
            ear_right (float): EAR do olho direito (0.0-1.0)
            mar (float): MAR da boca (0.0-2.0+)

        Returns:
            dict: Dicionário com análise completa contendo:
                - ear (float): EAR médio dos dois olhos
                - mar (float): MAR da boca
                - blink_detected (bool): True se piscada foi detectada neste frame
                - yawn_detected (bool): True se bocejo foi detectado neste frame
                - blink_rate (float): Taxa de piscadas por minuto
                - yawn_frequency (float): Frequência de bocejos por minuto
                - fatigue_score (float): Score de fadiga (0.0-1.0)
                - fatigue_detected (bool): True se fadiga foi detectada (score > 0.6)

        Note:
            O sistema usa análise temporal para evitar falsos positivos.
            Requer frames consecutivos para confirmar piscadas e bocejos.
        """
        # EAR médio
        avg_ear = (ear_left + ear_right) / 2.0

        # Adiciona ao histórico
        self.ear_history.append(avg_ear)
        self.mar_history.append(mar)

        # Análise de piscadas
        blink_detected = False
        if avg_ear < self.EAR_THRESHOLD:
            self.eye_frame_counter += 1
        else:
            if self.eye_frame_counter >= self.EAR_CONSEC_FRAMES:
                self.blink_counter += 1
                blink_detected = True
            self.eye_frame_counter = 0

        # Análise de bocejos
        yawn_detected = False
        if mar > self.MAR_THRESHOLD:
            self.mouth_frame_counter += 1
            if self.mouth_frame_counter >= self.MAR_CONSEC_FRAMES:
                if not yawn_detected:  # Evita contagem múltipla do mesmo bocejo
                    self.yawn_counter += 1
                    yawn_detected = True
        else:
            self.mouth_frame_counter = 0

        # Cálculo de métricas temporais
        blink_rate = self.calculate_blink_rate()
        yawn_frequency = self.calculate_yawn_frequency()

        # Determinação de fadiga
        fatigue_score = self.calculate_fatigue_score(
            avg_ear, mar, blink_rate, yawn_frequency
        )

        return {
            "ear": avg_ear,
            "mar": mar,
            "blink_detected": blink_detected,
            "yawn_detected": yawn_detected,
            "blink_rate": blink_rate,
            "yawn_frequency": yawn_frequency,
            "fatigue_score": fatigue_score,
            "fatigue_detected": fatigue_score > 0.6,
        }

    def calculate_blink_rate(self):
        """
        Calcula a taxa de piscadas por minuto
        """
        elapsed_time = time.time() - self.start_time
        if elapsed_time > 0:
            return (self.blink_counter / elapsed_time) * 60
        return 0

    def calculate_yawn_frequency(self):
        """
        Calcula a frequência de bocejos por minuto
        """
        elapsed_time = time.time() - self.start_time
        if elapsed_time > 0:
            return (self.yawn_counter / elapsed_time) * 60
        return 0

    def calculate_fatigue_score(self, ear, mar, blink_rate, yawn_frequency):
        """
        Calcula um score de fadiga usando lógica fuzzy simplificada.

        Implementa um sistema de pontuação que combina múltiplos indicadores
        de fadiga em um score único. O algoritmo atribui pesos diferentes
        para cada indicador baseado em sua importância para detecção de fadiga.

        Indicadores e Pesos:
        - EAR baixo (< 0.20): +0.4 pontos (olhos muito fechados)
        - EAR médio (< 0.25): +0.2 pontos (olhos parcialmente fechados)
        - Taxa de piscadas baixa (< 10/min): +0.3 pontos (sonolência)
        - Taxa de piscadas muito baixa (< 15/min): +0.1 pontos
        - Frequência de bocejos alta (> 5/min): +0.4 pontos
        - Frequência de bocejos média (> 2/min): +0.2 pontos
        - Bocejo ativo (MAR > limiar): +0.3 pontos

        Args:
            ear (float): Eye Aspect Ratio médio (0.0-1.0)
            mar (float): Mouth Aspect Ratio (0.0-2.0+)
            blink_rate (float): Taxa de piscadas por minuto (0-60+)
            yawn_frequency (float): Frequência de bocejos por minuto (0-20+)

        Returns:
            float: Score de fadiga normalizado entre 0.0 e 1.0:
                   - 0.0-0.3: Estado normal/alerta
                   - 0.3-0.6: Estado de atenção
                   - 0.6-1.0: Fadiga detectada (alerta necessário)

        Note:
            O score é limitado a 1.0 mesmo se a soma dos pesos for maior.
            A lógica fuzzy permite graduação suave entre estados.
        """
        score = 0.0

        # Contribuição do EAR (olhos fechados frequentemente)
        if ear < 0.20:
            score += 0.4
        elif ear < 0.25:
            score += 0.2

        # Contribuição da taxa de piscadas (muito baixa indica sonolência)
        if blink_rate < 10:
            score += 0.3
        elif blink_rate < 15:
            score += 0.1

        # Contribuição da frequência de bocejos
        if yawn_frequency > 5:
            score += 0.4
        elif yawn_frequency > 2:
            score += 0.2

        # Contribuição de bocejos detectados
        if mar > self.MAR_THRESHOLD:
            score += 0.3

        return min(score, 1.0)  # Garante que não exceda 1.0

    def play_alert_sound(self):
        """
        Reproduz som de alerta
        """
        try:
            if not self.alert_sound_loaded:
                # Gera um tom de alerta simples
                duration = 0.5  # segundos
                frequency = 800  # Hz
                sample_rate = 22050

                frames = int(duration * sample_rate)
                arr = np.zeros((frames, 2))

                for i in range(frames):
                    time_point = float(i) / sample_rate
                    arr[i][0] = np.sin(frequency * 2 * np.pi * time_point) * 0.3
                    arr[i][1] = arr[i][0]

                sound = pygame.sndarray.make_sound((arr * 32767).astype(np.int16))
                sound.play()

        except Exception as e:
            print(f"Erro ao reproduzir alerta: {e}")

    def draw_ui_elements(self, frame, face_analysis, fps):
        """
        Desenha elementos da interface no frame

        Args:
            frame: Frame de vídeo
            face_analysis: Dicionário com análise facial
            fps: Frames por segundo atual
        """
        height, width = frame.shape[:2]

        # Painel de informações
        panel_height = 120
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (width, panel_height), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)

        # Texto de informações
        info_text = [
            f"FPS: {fps:.1f}",
            f"EAR: {face_analysis.get('ear', 0):.3f}",
            f"MAR: {face_analysis.get('mar', 0):.3f}",
            f"Piscadas: {self.blink_counter}",
            f"Bocejos: {self.yawn_counter}",
        ]

        for i, text in enumerate(info_text):
            cv2.putText(
                frame,
                text,
                (10, 25 + i * 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                2,
            )

        # Indicador de fadiga
        fatigue_score = face_analysis.get("fatigue_score", 0)
        bar_width = 200
        bar_height = 20
        bar_x = width - bar_width - 20
        bar_y = 20

        # Fundo da barra
        cv2.rectangle(
            frame,
            (bar_x, bar_y),
            (bar_x + bar_width, bar_y + bar_height),
            (50, 50, 50),
            -1,
        )

        # Barra de fadiga
        fill_width = int(bar_width * fatigue_score)
        color = (
            (0, 255, 0)
            if fatigue_score < 0.3
            else (0, 255, 255)
            if fatigue_score < 0.6
            else (0, 0, 255)
        )

        cv2.rectangle(
            frame, (bar_x, bar_y), (bar_x + fill_width, bar_y + bar_height), color, -1
        )

        # Texto da barra
        cv2.putText(
            frame,
            f"Fadiga: {fatigue_score:.2f}",
            (bar_x, bar_y - 5),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2,
        )

        # Alerta visual
        if face_analysis.get("fatigue_detected", False):
            cv2.rectangle(frame, (0, 0), (width, height), (0, 0, 255), 8)
            cv2.putText(
                frame,
                "ALERTA: FADIGA DETECTADA!",
                (width // 2 - 200, height // 2),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.2,
                (0, 0, 255),
                3,
            )

    def draw_facial_landmarks(self, frame, landmarks):
        """
        Desenha marcos faciais no frame

        Args:
            frame: Frame de vídeo
            landmarks: Array com coordenadas dos marcos
        """
        # Olhos (pontos 36-47)
        left_eye = landmarks[36:42]
        right_eye = landmarks[42:48]

        # Boca (pontos 48-67)
        mouth = landmarks[48:68]

        # Desenha contornos
        cv2.polylines(frame, [left_eye], True, (0, 255, 0), 1)
        cv2.polylines(frame, [right_eye], True, (0, 255, 0), 1)
        cv2.polylines(frame, [mouth], True, (0, 0, 255), 1)

        # Desenha pontos dos olhos e boca
        for x, y in left_eye:
            cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)
        for x, y in right_eye:
            cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)
        for x, y in mouth:
            cv2.circle(frame, (x, y), 2, (0, 0, 255), -1)

    def process_frame(self, frame):
        """
        Processa um frame completo para detecção de fadiga

        Args:
            frame: Frame de vídeo

        Returns:
            tuple: (frame_processado, análise_facial)
        """
        # Converte para escala de cinza
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Equalização de histograma
        gray = cv2.equalizeHist(gray)

        # Detecção de faces
        faces = self.face_cascade.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=5, minSize=(100, 100)
        )

        face_analysis = {
            "ear": 0,
            "mar": 0,
            "blink_detected": False,
            "yawn_detected": False,
            "fatigue_detected": False,
            "fatigue_score": 0,
        }

        # Processa cada face detectada
        for x, y, w, h in faces:
            # Desenha retângulo da face
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            try:
                # Extrai marcos faciais
                landmarks = self.extract_face_landmarks(gray, (x, y, w, h))

                # Desenha marcos faciais
                self.draw_facial_landmarks(frame, landmarks)

                # Calcula EAR para ambos os olhos
                left_eye = landmarks[36:42]
                right_eye = landmarks[42:48]
                ear_left = self.calculate_ear(left_eye)
                ear_right = self.calculate_ear(right_eye)

                # Calcula MAR para a boca
                mouth = landmarks[48:68]
                mar = self.calculate_mar(mouth)

                # Analisa indicadores de fadiga
                face_analysis = self.analyze_fatigue_indicators(
                    ear_left, ear_right, mar
                )

                # Ativa alerta se necessário
                if face_analysis["fatigue_detected"] and not self.alert_active:
                    self.alert_active = True
                    threading.Thread(target=self.play_alert_sound).start()
                elif not face_analysis["fatigue_detected"]:
                    self.alert_active = False

            except Exception as e:
                print(f"Erro ao processar marcos faciais: {e}")

        return frame, face_analysis

    def run(self):
        """
        Executa o sistema de detecção de fadiga em tempo real.

        Este é o método principal que implementa o loop de captura e processamento
        de vídeo. Inicializa a câmera, processa frames continuamente, analisa
        indicadores de fadiga e exibe a interface gráfica com alertas.

        Fluxo de Execução:
        1. Inicializa captura de vídeo (webcam)
        2. Configura resolução e FPS da câmera
        3. Loop principal:
           a. Captura frame da câmera
           b. Espelha horizontalmente (melhor UX)
           c. Processa frame para detecção de fadiga
           d. Calcula FPS em tempo real
           e. Desenha interface com métricas
           f. Exibe frame processado
           g. Verifica comandos do teclado
        4. Limpeza de recursos ao finalizar

        Controles de Teclado:
        - 'q': Finaliza o sistema
        - 'r': Reseta contadores de piscadas e bocejos

        Raises:
            Exception: Se não conseguir acessar a câmera
            KeyboardInterrupt: Se usuário interromper com Ctrl+C

        Note:
            O sistema tenta configurar resolução 1280x720 a 30 FPS.
            Se a câmera não suportar, usará configurações padrão.
            O frame é espelhado para melhor experiência do usuário.
        """
        print("Iniciando sistema de detecção de fadiga...")
        print("Pressione 'q' para sair, 'r' para resetar contadores")

        # Inicializa captura de vídeo
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            print("✗ Erro: Não foi possível acessar a câmera")
            return

        # Configura resolução
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        cap.set(cv2.CAP_PROP_FPS, 30)

        print("✓ Sistema iniciado com sucesso!")
        print("✓ Câmera ativada")

        # Loop principal
        frame_count = 0
        fps_start_time = time.time()

        while True:
            ret, frame = cap.read()
            if not ret:
                print("✗ Erro ao capturar frame")
                break

            # Espelha horizontalmente para melhor usabilidade
            frame = cv2.flip(frame, 1)

            # Processa frame
            processed_frame, face_analysis = self.process_frame(frame)

            # Calcula FPS
            frame_count += 1
            if frame_count % 30 == 0:
                fps_end_time = time.time()
                fps = 30 / (fps_end_time - fps_start_time)
                fps_start_time = fps_end_time
            else:
                fps = 30  # Valor padrão

            # Desenha interface
            self.draw_ui_elements(processed_frame, face_analysis, fps)

            # Mostra frame
            cv2.imshow("Sistema de Detecção de Fadiga", processed_frame)

            # Verifica teclas pressionadas
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
            elif key == ord("r"):
                # Reset dos contadores
                self.blink_counter = 0
                self.yawn_counter = 0
                self.start_time = time.time()
                print("✓ Contadores resetados")

        # Limpeza
        cap.release()
        cv2.destroyAllWindows()
        pygame.mixer.quit()
        print("✓ Sistema finalizado")


def main():
    """
    Função principal do programa
    """
    parser = argparse.ArgumentParser(description="Sistema de Detecção de Fadiga")
    parser.add_argument(
        "--ear-threshold",
        type=float,
        default=0.25,
        help="Limiar EAR para detecção de olhos fechados",
    )
    parser.add_argument(
        "--mar-threshold",
        type=float,
        default=0.65,
        help="Limiar MAR para detecção de bocejo",
    )

    args = parser.parse_args()

    # Cria e executa o detector
    detector = FatigueDetector()
    detector.EAR_THRESHOLD = args.ear_threshold
    detector.MAR_THRESHOLD = args.mar_threshold

    try:
        detector.run()
    except KeyboardInterrupt:
        print("\n✓ Sistema interrompido pelo usuário")
    except Exception as e:
        print(f"✗ Erro crítico: {e}")


if __name__ == "__main__":
    main()
