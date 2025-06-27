# Use uma imagem base Ubuntu com Python
FROM ubuntu:22.04

# Evita prompts interativos durante a instalação
ENV DEBIAN_FRONTEND=noninteractive

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    cmake \
    build-essential \
    libopencv-dev \
    libdlib-dev \
    libboost-all-dev \
    libx11-dev \
    libgtk-3-dev \
    libgstreamer1.0-dev \
    libgstreamer-plugins-base1.0-dev \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    libv4l-dev \
    libxvidcore-dev \
    libx264-dev \
    libatlas-base-dev \
    gfortran \
    wget \
    pulseaudio \
    alsa-utils \
    && rm -rf /var/lib/apt/lists/*

# Define diretório de trabalho
WORKDIR /app

# Copia arquivos de requisitos e instala dependências Python
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Baixa o modelo de marcos faciais do dlib
RUN wget -O shape_predictor_68_face_landmarks.dat \
    https://huggingface.co/spaces/asdasdasdasd/Face-forgery-detection/resolve/ccfc24642e0210d4d885bc7b3dbc9a68ed948ad6/shape_predictor_68_face_landmarks.dat

# Copia código da aplicação
COPY . .

# Cria usuário não-root para segurança
RUN groupadd -r appuser && useradd -r -g appuser appuser
RUN chown -R appuser:appuser /app
USER appuser

# Expõe variáveis de ambiente para X11
ENV DISPLAY=:0
ENV QT_X11_NO_MITSHM=1

# Comando padrão
CMD ["python3", "main.py"] 