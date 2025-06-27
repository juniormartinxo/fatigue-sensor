#!/bin/bash

# Script de configuração para o Sistema de Detecção de Fadiga
# Autor: Setup automático para Docker

set -e

echo "🚀 Configurando Sistema de Detecção de Fadiga com Docker..."

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Função para imprimir mensagens coloridas
print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Verifica se Docker está instalado
if ! command -v docker &> /dev/null; then
    print_error "Docker não está instalado. Instale o Docker primeiro."
    exit 1
fi

# Verifica se Docker Compose está instalado
if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose não está instalado. Instale o Docker Compose primeiro."
    exit 1
fi

print_status "Docker e Docker Compose encontrados"

# Configura variáveis de ambiente
print_status "Configurando variáveis de ambiente..."

# Permite acesso ao X11 para GUI
print_status "Configurando acesso ao X11..."
xhost +local:docker

# Verifica dispositivos de vídeo
print_status "Verificando dispositivos de câmera..."
if [ -e /dev/video0 ]; then
    print_status "Câmera encontrada em /dev/video0"
else
    print_warning "Nenhuma câmera encontrada em /dev/video0"
    print_warning "Verifique se sua webcam está conectada"
fi

# Verifica dispositivos de áudio
print_status "Verificando dispositivos de áudio..."
if [ -e /dev/snd ]; then
    print_status "Dispositivos de áudio encontrados"
else
    print_warning "Dispositivos de áudio não encontrados"
fi

# Cria arquivo .env se não existir
if [ ! -f .env ]; then
    print_status "Criando arquivo .env..."
    cat > .env << EOL
# Variáveis de ambiente para Docker Compose
DISPLAY=${DISPLAY}
EOL
fi

print_status "Setup concluído!"
echo ""
echo "🔧 Comandos disponíveis:"
echo ""
echo "  # Construir e executar a aplicação:"
echo "  docker-compose up --build"
echo ""
echo "  # Executar em background:"
echo "  docker-compose up -d"
echo ""
echo "  # Modo desenvolvimento (bash interativo):"
echo "  docker-compose --profile dev up fatigue-detector-dev"
echo ""
echo "  # Parar serviços:"
echo "  docker-compose down"
echo ""
echo "  # Ver logs:"
echo "  docker-compose logs -f"
echo ""
echo "  # Executar com parâmetros personalizados:"
echo "  docker-compose run fatigue-detector python3 main.py --ear-threshold 0.22"
echo ""
echo "📱 Controles na aplicação:"
echo "  - 'q': Sair do sistema"
echo "  - 'r': Resetar contadores"
echo ""
print_status "Sistema pronto para uso!" 