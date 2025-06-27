# FatigueSensor

![Python](https://img.shields.io/badge/python-v3.7+-blue.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.0+-green.svg)
![Dlib](https://img.shields.io/badge/dlib-19.0+-orange.svg)
![Docker](https://img.shields.io/badge/docker-supported-blue.svg)
![Status](https://img.shields.io/badge/status-ativo-brightgreen.svg)

Sistema completo de detecção de fadiga em tempo real utilizando visão computacional para análise facial, focado na segurança de motoristas através do monitoramento de padrões de piscada e detecção de bocejos.

## 📋 Índice

- [Sobre o Projeto](#-sobre-o-projeto)
- [Características](#-características)
- [Tecnologias Utilizadas](#️-tecnologias-utilizadas)
- [Requisitos](#-requisitos)
- [Instalação](#-instalação)
- [Como Usar](#-como-usar)
- [Parâmetros](#️-parâmetros)
- [Metodologia](#-metodologia)
- [Interface](#️-interface)
- [Resolução de Problemas](#-resolução-de-problemas)
- [Contribuição](#-contribuição)
- [Licença](#-licença)

## 🎯 Sobre o Projeto

Este sistema foi desenvolvido como parte da disciplina de Visão Computacional e tem como objetivo detectar sinais de fadiga em motoristas através da análise em tempo real de expressões faciais. O sistema monitora continuamente os padrões de piscada e detecção de bocejos, fornecendo alertas visuais e sonoros quando sinais de fadiga são identificados.

### Problemas que o Sistema Resolve

- **Acidentes por Sonolência**: Reduz o risco de acidentes causados por fadiga do motorista
- **Monitoramento Contínuo**: Análise em tempo real sem interrupção da condução
- **Alertas Imediatos**: Notificação instantânea quando fadiga é detectada
- **Interface Intuitiva**: Feedback visual claro sobre o estado de alerta do motorista

## ✨ Características

### Funcionalidades Principais

- 🎥 **Detecção Facial em Tempo Real**: Utilizando OpenCV e Haar Cascades
- 👁️ **Análise de Padrões de Piscada**: Cálculo do Eye Aspect Ratio (EAR)
- 😴 **Detecção de Bocejos**: Monitoramento do Mouth Aspect Ratio (MAR)
- 🔊 **Sistema de Alertas**: Alertas visuais e sonoros para fadiga detectada
- 📊 **Métricas em Tempo Real**: FPS, contadores de piscadas e bocejos
- 🎚️ **Parâmetros Configuráveis**: Limiares ajustáveis via linha de comando
- 📈 **Score de Fadiga**: Sistema de pontuação baseado em lógica fuzzy

### Tecnologias Implementadas

- **Marcos Faciais**: 68 pontos de referência facial usando dlib
- **Equalização de Histograma**: Melhora a detecção em diferentes condições de luz
- **Análise Temporal**: Histórico de medições para análise de tendências
- **Threading**: Processamento de áudio em thread separada
- **Interface Gráfica**: Overlay com informações em tempo real

## 🛠️ Tecnologias Utilizadas

### Linguagem e Frameworks

- **Python 3.7+**: Linguagem principal
- **OpenCV**: Visão computacional e processamento de imagem
- **dlib**: Detecção de marcos faciais
- **NumPy**: Computação numérica
- **SciPy**: Cálculos de distância euclidiana
- **Pygame**: Sistema de áudio para alertas

### Algoritmos

- **Haar Cascades**: Detecção facial
- **Shape Predictor**: Detecção de 68 marcos faciais
- **Eye Aspect Ratio (EAR)**: Análise de abertura dos olhos
- **Mouth Aspect Ratio (MAR)**: Análise de abertura da boca

## 📋 Requisitos

### Requisitos de Sistema

- **Sistema Operacional**: Windows, macOS, ou Linux
- **Python**: Versão 3.7 ou superior
- **Câmera**: Webcam USB ou câmera integrada
- **RAM**: Mínimo 4GB (recomendado 8GB)
- **CPU**: Processador dual-core (recomendado quad-core)

### Dependências Python

```txt
opencv-python>=4.5.0
dlib>=19.22.0
numpy>=1.19.0
scipy>=1.5.0
pygame>=2.0.0
```

### Arquivos Adicionais Necessários

- **shape_predictor_68_face_landmarks.dat**: Modelo pré-treinado do dlib para detecção de marcos faciais

## 🚀 Instalação

### 🐳 Opção 1: Docker (Recomendado)

A instalação via Docker é a forma mais rápida e confiável de executar o FatigueSensor, pois elimina problemas de dependências e configuração.

#### Pré-requisitos

- Docker instalado ([Guia de Instalação do Docker](https://docs.docker.com/get-docker/))
- Câmera conectada ao sistema

#### Setup Automático (Recomendado)

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/FatigueSensor.git
cd FatigueSensor

# Execute o script de instalação automática
chmod +x install.sh
./install.sh
```

O script automaticamente:
- ✅ Verifica se Docker e Docker Compose estão instalados
- ✅ Baixa o modelo de marcos faciais necessário
- ✅ Configura permissões do X11 para interface gráfica
- ✅ Verifica dispositivos de câmera e áudio
- ✅ Cria arquivo de configuração (.env)
- ✅ Mostra todos os comandos disponíveis

#### Setup Manual

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/FatigueSensor.git
cd FatigueSensor

# Construir a imagem Docker
docker build -t fatigue-sensor .

# Executar o container (Linux)
docker run --rm -it \
  --device=/dev/video0 \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
  fatigue-sensor

# Executar o container (Windows com WSL2)
docker run --rm -it \
  --device=/dev/video0 \
  -e DISPLAY=host.docker.internal:0.0 \
  fatigue-sensor

# Executar com parâmetros personalizados
docker run --rm -it \
  --device=/dev/video0 \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
  fatigue-sensor \
  python3 main.py --ear-threshold 0.22 --mar-threshold 0.68
```

#### Dockerfile Incluído

O projeto já inclui um `Dockerfile` otimizado que:

- Instala todas as dependências necessárias do sistema
- Baixa automaticamente o modelo de marcos faciais
- Configura o ambiente adequadamente para OpenCV e dlib
- Inclui configurações de segurança e áudio

#### Alternativa: Docker Compose (Ainda Mais Simples)

O projeto já inclui um arquivo `docker-compose.yml` completo com configurações avançadas:

- **Serviço Principal**: Execução padrão do FatigueSensor
- **Serviço de Desenvolvimento**: Para debug e modificações (profile `dev`)
- **Configurações de Áudio**: Suporte completo ao PulseAudio
- **Múltiplas Câmeras**: Suporte para webcam principal e secundária
- **Privilégios Apropriados**: Configurações de segurança otimizadas

```bash
# Executar o serviço principal
docker-compose up --build

# Executar em background
docker-compose up -d

# Executar serviço de desenvolvimento (com shell interativo)
docker-compose --profile dev up fatigue-sensor-dev

# Parar todos os serviços
docker-compose down

# Ver logs em tempo real
docker-compose logs -f
```

### 🔧 Opção 2: Instalação Local

Para desenvolvedores que preferem controle total sobre o ambiente ou precisam modificar o código.

#### 1. Clone o Repositório

```bash
git clone https://github.com/seu-usuario/FatigueSensor.git
cd FatigueSensor
```

#### 2. Crie um Ambiente Virtual (Recomendado)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

#### 3. Instale as Dependências

```bash
pip install -r requirements.txt
```

#### 4. Baixe o Modelo de Marcos Faciais

```bash
# Opção 1: Download direto (Linux/macOS)
wget https://huggingface.co/spaces/asdasdasdasd/Face-forgery-detection/resolve/ccfc24642e0210d4d885bc7b3dbc9a68ed948ad6/shape_predictor_68_face_landmarks.dat

# Opção 2: Download manual
# Baixe o arquivo do link acima e coloque na pasta raiz do projeto
```

#### 5. Verifique a Instalação

```bash
python main.py --help
```

### 🆚 Comparação das Opções

| Aspecto | Docker (com script) | Instalação Local |
|---------|--------------------|--------------------|
| **Facilidade de Setup** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Download Automático** | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| **Consistência entre SOs** | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| **Desenvolvimento/Debug** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Performance** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Requisitos de Sistema** | Docker + 2GB extra | Python + dependências |
| **Tempo de Setup** | ~2 minutos | ~10 minutos |

### 🐧 Configuração Adicional para Linux

Se estiver usando Docker no Linux, pode ser necessário configurar o X11:

```bash
# Permitir conexões X11
xhost +local:docker

# Executar o container
docker run --rm -it \
  --device=/dev/video0 \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
  fatigue-sensor
```

## 💻 Como Usar

### Execução Básica

```bash
python main.py
```

### Execução com Parâmetros Personalizados

```bash
# Ajustar limiar de detecção de olhos fechados
python main.py --ear-threshold 0.20

# Ajustar limiar de detecção de bocejo
python main.py --mar-threshold 0.70

# Combinar parâmetros
python main.py --ear-threshold 0.22 --mar-threshold 0.68
```

### Controles Durante a Execução

- **'q'**: Sair do sistema
- **'r'**: Resetar contadores de piscadas e bocejos

## ⚙️ Parâmetros

### Parâmetros de Linha de Comando

| Parâmetro | Descrição | Padrão | Faixa Recomendada |
|-----------|-----------|---------|-------------------|
| `--ear-threshold` | Limiar EAR para olhos fechados | 0.25 | 0.20 - 0.30 |
| `--mar-threshold` | Limiar MAR para detecção de bocejo | 0.65 | 0.60 - 0.75 |

### Parâmetros Internos Configuráveis

| Parâmetro | Descrição | Valor Padrão |
|-----------|-----------|--------------|
| `EAR_CONSEC_FRAMES` | Frames consecutivos para confirmar piscada | 20 |
| `MAR_CONSEC_FRAMES` | Frames consecutivos para confirmar bocejo | 15 |

## 🔬 Metodologia

### 1. Detecção Facial

- Utiliza Haar Cascades para detectar faces no frame
- Processa apenas a região da face para otimizar performance

### 2. Extração de Marcos Faciais

- Aplica o modelo de 68 pontos do dlib
- Identifica pontos específicos dos olhos (36-47) e boca (48-67)

### 3. Cálculo de Métricas

#### Eye Aspect Ratio (EAR)

```txt
EAR = (|p2-p6| + |p3-p5|) / (2 * |p1-p4|)
```

- Valores baixos indicam olhos fechados
- Limiar padrão: 0.25

#### Mouth Aspect Ratio (MAR)

```txt
MAR = (|p51-p59| + |p53-p57|) / (2 * |p49-p55|)
```

- Valores altos indicam boca aberta (bocejo)
- Limiar padrão: 0.65

### 4. Análise de Fadiga

- **Score de Fadiga**: Combinação ponderada de:
  - EAR baixo (40% do peso)
  - Taxa de piscadas baixa (30% do peso)
  - Frequência de bocejos alta (40% do peso)
  - Detecção de bocejo ativo (30% do peso)

## 🖥️ Interface

### Elementos da Interface

#### Painel de Informações (Superior Esquerdo)

- **FPS**: Taxa de frames por segundo
- **EAR**: Eye Aspect Ratio atual
- **MAR**: Mouth Aspect Ratio atual
- **Piscadas**: Contador total de piscadas
- **Bocejos**: Contador total de bocejos

#### Barra de Fadiga (Superior Direito)

- **Verde**: Estado normal (score < 0.3)
- **Amarelo**: Atenção (score 0.3-0.6)
- **Vermelho**: Fadiga detectada (score > 0.6)

#### Alertas Visuais

- **Contorno Vermelho**: Pisca quando fadiga é detectada
- **Texto de Alerta**: "ALERTA: FADIGA DETECTADA!"

#### Marcos Faciais

- **Pontos Verdes**: Contorno dos olhos
- **Pontos Vermelhos**: Contorno da boca
- **Retângulo Azul**: Área facial detectada

## 🔧 Resolução de Problemas

### Problemas Específicos do Docker

#### "Erro: não é possível acessar a câmera no container"

**Soluções**:
```bash
# Verificar se a câmera está disponível
ls -la /dev/video*

# Verificar se o usuário está no grupo video
sudo usermod -a -G video $USER

# Dar permissões ao X11 (Linux)
xhost +local:docker
```

#### "Interface gráfica não aparece"

**Soluções**:
```bash
# Para WSL2 (Windows)
# Instalar um servidor X11 como VcXsrv ou Xming
# Configurar DISPLAY=host.docker.internal:0.0

# Para macOS
# Instalar XQuartz e configurar
brew install --cask xquartz
xhost +localhost

# Para Linux
xhost +local:docker
```

#### "Container não constrói corretamente"

**Soluções**:
```bash
# Limpar cache do Docker
docker system prune -a

# Construir sem cache
docker build --no-cache -t fatigue-sensor .

# Verificar logs de construção
docker build -t fatigue-sensor . --progress=plain
```

### Problemas Comuns

#### "Erro ao inicializar detectores"

**Causa**: Arquivo `shape_predictor_68_face_landmarks.dat` não encontrado
**Solução**:

```bash
# Baixe o arquivo usando o link fornecido no código
wget https://huggingface.co/spaces/asdasdasdasd/Face-forgery-detection/resolve/ccfc24642e0210d4d885bc7b3dbc9a68ed948ad6/shape_predictor_68_face_landmarks.dat
```

#### "Erro: Não foi possível acessar a câmera"

**Causas Possíveis**:

- Câmera em uso por outro aplicativo
- Drivers de câmera desatualizados
- Permissões insuficientes

**Soluções**:

```bash
# Verificar câmeras disponíveis
python -c "import cv2; print(cv2.VideoCapture(0).isOpened())"

# Testar diferentes índices de câmera
python -c "import cv2; cap = cv2.VideoCapture(1); print(cap.isOpened())"
```

#### Performance Baixa (FPS < 15)

**Soluções**:

- Reduza a resolução da câmera no código
- Feche outros aplicativos que usam CPU
- Considere usar uma GPU para processamento

#### Detecção Inconsistente

**Ajustes Possíveis**:

```bash
# Para olhos mais sensíveis
python main.py --ear-threshold 0.20

# Para bocejo mais sensível  
python main.py --mar-threshold 0.60

# Para condições de pouca luz
# Ajuste a iluminação ou modifique os parâmetros de equalização
```

### Logs e Debug

O sistema fornece logs em tempo real no terminal:

- ✓ Indica operações bem-sucedidas
- ✗ Indica erros
- ⚠ Indica avisos

## 🤝 Contribuição

### Como Contribuir

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

### Áreas para Contribuição

- Otimização de performance
- Novos algoritmos de detecção
- Melhorias na interface
- Testes automatizados
- Documentação adicional

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👥 Autores

- **[Nome do Estudante]** - Desenvolvimento inicial - [GitHub Profile]

## 🙏 Agradecimentos

- OpenCV Community
- dlib Library Developers
- Disciplina de Visão Computacional
- Comunidade Python Brasil

---

### Desenvolvido com ❤️ para tornar as estradas mais seguras
