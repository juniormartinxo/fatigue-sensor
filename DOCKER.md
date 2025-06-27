# 🐳 Guia Docker - FatigueSensor

Este guia explica como executar o FatigueSensor utilizando Docker e Docker Compose de forma simples e eficiente.

## 📋 Pré-requisitos

- **Docker**: Versão 20.10 ou superior
- **Docker Compose**: Versão 2.0 ou superior  
- **Webcam**: Câmera USB ou integrada
- **Sistema de Áudio**: Para alertas sonoros
- **Linux/WSL2**: Sistema compatível com X11 (recomendado)

### Verificação dos Pré-requisitos

```bash
# Verificar versões instaladas
docker --version
docker-compose --version

# Verificar dispositivos de câmera
ls /dev/video*

# Verificar dispositivos de áudio
ls /dev/snd/

# Verificar sistema X11 (Linux)
echo $DISPLAY
```

## 🚀 Início Rápido

### 1. Setup Automático (Recomendado)

Execute o script de configuração automática que faz todo o trabalho pesado:

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/fatigue-sensor.git
cd fatigue-sensor

# Torne o script executável e execute
chmod +x install.sh
./install.sh
```

**O que o script faz automaticamente:**
- ✅ Verifica pré-requisitos (Docker, câmera, áudio)
- ✅ Configura permissões do X11 para interface gráfica
- ✅ Baixa o modelo de marcos faciais (shape_predictor_68_face_landmarks.dat)
- ✅ Cria arquivo de configuração (.env)
- ✅ Mostra todos os comandos disponíveis

### 2. Execução Manual

Se preferir configurar passo a passo:

```bash
# Permitir acesso ao X11 (Linux/WSL)
xhost +local:docker

# Criar arquivo .env
echo "DISPLAY=$DISPLAY" > .env

# Construir e executar
docker-compose up --build
```

## 🛠️ Comandos Principais

### Construção e Execução

```bash
# Construir e executar o serviço principal
docker-compose up --build

# Executar em background (daemon)
docker-compose up -d

# Forçar reconstrução completa
docker-compose build --no-cache
docker-compose up

# Executar apenas uma vez (sem restart automático)
docker-compose run --rm fatigue-sensor
```

### Controle de Serviços

```bash
# Parar todos os serviços
docker-compose down

# Parar e remover volumes persistentes
docker-compose down -v

# Reiniciar serviços específicos
docker-compose restart fatigue-sensor

# Parar apenas um serviço
docker-compose stop fatigue-sensor
```

### Logs e Monitoramento

```bash
# Ver logs em tempo real
docker-compose logs -f

# Ver logs de serviço específico
docker-compose logs -f fatigue-sensor

# Ver últimas 50 linhas dos logs
docker-compose logs --tail=50

# Logs sem timestamps
docker-compose logs --no-log-prefix
```

## ⚙️ Configurações Avançadas

### Parâmetros Personalizados

```bash
# Executar com limiares customizados
docker-compose run --rm fatigue-sensor python3 main.py --ear-threshold 0.22 --mar-threshold 0.70

# Executar exemplos de uso pré-configurados
docker-compose run --rm fatigue-sensor python3 exemplos_uso.py

# Executar exemplo específico (modo rigoroso)
docker-compose run --rm fatigue-sensor python3 -c "
import exemplos_uso
exemplos_uso.exemplo_deteccao_rigorosa()
"
```

### Perfis de Detecção Disponíveis

O sistema inclui diferentes perfis otimizados para cenários específicos:

```bash
# Modo Padrão - Uso geral
docker-compose run --rm fatigue-sensor python3 main.py

# Modo Sensível - Para motoristas experientes
docker-compose run --rm fatigue-sensor python3 main.py --ear-threshold 0.22 --mar-threshold 0.60

# Modo Rigoroso - Para situações de alto risco
docker-compose run --rm fatigue-sensor python3 main.py --ear-threshold 0.28 --mar-threshold 0.55

# Modo Permissivo - Para condições de pouca luz
docker-compose run --rm fatigue-sensor python3 main.py --ear-threshold 0.20 --mar-threshold 0.70
```

### Modo Desenvolvimento

```bash
# Ativar container de desenvolvimento com shell interativo
docker-compose --profile dev up fatigue-sensor-dev

# Executar bash no container em execução
docker-compose exec fatigue-sensor bash

# Montar código local para desenvolvimento (modo dev já configurado)
# O perfil 'dev' mapeia automaticamente o código local para /app
```

### Múltiplas Câmeras

Para sistemas com múltiplas câmeras, edite o `docker-compose.yml`:

```yaml
devices:
  - /dev/video0:/dev/video0    # Câmera principal
  - /dev/video1:/dev/video1    # Câmera secundária
  - /dev/video2:/dev/video2    # Câmera adicional
  # Adicione quantas câmeras precisar
```

### Configurações de Áudio Avançadas

```bash
# Verificar configuração atual do PulseAudio
docker-compose exec fatigue-sensor pulseaudio --check

# Testar áudio no container
docker-compose exec fatigue-sensor pactl list short sinks

# Para sistemas com PipeWire (alternativa ao PulseAudio)
# Editar docker-compose.yml para mapear sockets do PipeWire
```

## 🔧 Resolução de Problemas

### Problema: "Não foi possível acessar a câmera"

**Diagnóstico:**
```bash
# Verificar se câmera está disponível no host
ls -la /dev/video*
v4l2-ctl --list-devices  # Se disponível

# Verificar permissões
groups $USER | grep -E "(video|audio)"
```

**Soluções:**
```bash
# Adicionar usuário aos grupos necessários
sudo usermod -a -G video,audio $USER

# Dar permissões temporárias aos dispositivos
sudo chmod 666 /dev/video0
sudo chmod -R 666 /dev/snd/

# Reiniciar sessão para aplicar mudanças de grupo
# ou executar temporariamente com sudo
sudo docker-compose up
```

### Problema: "Display não encontrado" / "Interface não aparece"

**Para Linux/WSL2:**
```bash
# Verificar variável DISPLAY
echo $DISPLAY

# Reconfigurar X11
xhost +local:docker

# Para WSL2 especificamente
export DISPLAY=:0
# ou para Windows 11 com WSLg
export DISPLAY=:0.0
```

**Para Windows com WSL2:**
```bash
# Instalar servidor X11 (escolha um):
# VcXsrv, Xming, ou usar WSLg nativo (Windows 11)

# Configurar DISPLAY para servidor X externo
export DISPLAY=host.docker.internal:0.0
```

**Para macOS:**
```bash
# Instalar XQuartz
brew install --cask xquartz

# Configurar XQuartz
xhost +localhost
export DISPLAY=host.docker.internal:0
```

### Problema: "Som não funciona"

**Diagnóstico:**
```bash
# Verificar status do PulseAudio
pulseaudio --check
systemctl --user status pulseaudio

# Listar dispositivos de áudio
pactl list short sinks
```

**Soluções:**
```bash
# Reiniciar PulseAudio
pulseaudio --kill
pulseaudio --start

# Para sistemas sem PulseAudio (usar ALSA)
# Modificar docker-compose.yml para mapear dispositivos ALSA

# Verificar se container tem acesso ao áudio
docker-compose exec fatigue-sensor ls -la /dev/snd/
```

### Problema: "Permission denied" em dispositivos

**Solução temporária:**
```bash
sudo chmod 666 /dev/video0
sudo chmod -R 666 /dev/snd/
```

**Solução permanente (criar regras udev):**
```bash
# Criar arquivo de regras
sudo nano /etc/udev/rules.d/99-fatigue-sensor.rules

# Adicionar conteúdo:
SUBSYSTEM=="video4linux", GROUP="video", MODE="0666"
SUBSYSTEM=="sound", GROUP="audio", MODE="0666"
KERNEL=="controlC[0-9]*", GROUP="audio", MODE="0666"

# Recarregar regras
sudo udevadm control --reload-rules
sudo udevadm trigger
```

### Problema: "Modelo de marcos faciais não encontrado"

**Solução automática:**
```bash
# O install.sh baixa automaticamente, mas se precisar fazer manualmente:
wget -O shape_predictor_68_face_landmarks.dat \
  "https://huggingface.co/spaces/asdasdasdasd/Face-forgery-detection/resolve/ccfc24642e0210d4d885bc7b3dbc9a68ed948ad6/shape_predictor_68_face_landmarks.dat"

# Verificar se arquivo foi baixado corretamente (deve ter ~68MB)
ls -lh shape_predictor_68_face_landmarks.dat
```

## 🐛 Debug e Desenvolvimento

### Executar com Debug Avançado

```bash
# Habilitar logs verbose do Python
docker-compose run --rm fatigue-sensor python3 -u main.py

# Executar com debugger interativo
docker-compose run --rm fatigue-sensor python3 -m pdb main.py

# Executar com logs de OpenCV detalhados
docker-compose run --rm -e OPENCV_LOG_LEVEL=DEBUG fatigue-sensor python3 main.py
```

### Inspeção do Container

```bash
# Listar todos os containers
docker ps -a

# Executar comandos no container ativo
docker exec -it fatigue-sensor bash
docker exec -it fatigue-sensor python3 --version

# Verificar logs detalhados do container
docker logs --details fatigue-sensor

# Inspecionar configuração do container
docker inspect fatigue-sensor
```

### Testes de Funcionalidade

```bash
# Testar detecção de câmera
docker-compose run --rm fatigue-sensor python3 -c "
import cv2
cap = cv2.VideoCapture(0)
print('Câmera disponível:', cap.isOpened())
cap.release()
"

# Testar carregamento do modelo dlib
docker-compose run --rm fatigue-sensor python3 -c "
import dlib
import os
if os.path.exists('shape_predictor_68_face_landmarks.dat'):
    predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
    print('Modelo carregado com sucesso')
else:
    print('Modelo não encontrado')
"

# Executar exemplos de uso para testes
docker-compose run --rm fatigue-sensor python3 exemplos_uso.py
```

### Limpeza do Sistema

```bash
# Remover containers parados
docker container prune -f

# Remover imagens não utilizadas
docker image prune -f

# Remover volumes órfãos
docker volume prune -f

# Limpeza completa (CUIDADO! Remove tudo não usado)
docker system prune -a -f

# Limpeza específica do projeto
docker-compose down -v --rmi all
```

## 📊 Monitoramento e Performance

### Recursos do Container

```bash
# Estatísticas em tempo real
docker stats fatigue-sensor

# Uso detalhado de recursos
docker-compose top

# Verificar limites de recurso
docker inspect fatigue-sensor | grep -A 10 "Memory"
```

### Verificação de Saúde do Sistema

```bash
# Status dos serviços
docker-compose ps

# Verificar processos em execução no container
docker-compose exec fatigue-sensor ps aux

# Teste de conectividade com dispositivos
docker-compose exec fatigue-sensor ls -la /dev/video* /dev/snd/

# Verificar variáveis de ambiente
docker-compose exec fatigue-sensor env | grep -E "(DISPLAY|PULSE)"
```

### Otimização de Performance

```bash
# Executar com diferentes resoluções (modificar main.py se necessário)
# Ou usar parâmetros para reduzir processamento

# Monitorar FPS em tempo real
docker-compose logs -f | grep "FPS"

# Para GPUs NVIDIA (se disponível)
# Instalar nvidia-docker2 e modificar docker-compose.yml:
#   runtime: nvidia
#   environment:
#     - NVIDIA_VISIBLE_DEVICES=all
```

## 🔒 Segurança e Boas Práticas

### Usuário Não-Root

O container executa com usuário não-privilegiado (`appuser`) por segurança:

```bash
# Verificar usuário atual no container
docker-compose exec fatigue-sensor whoami
docker-compose exec fatigue-sensor id

# Verificar proprietário dos arquivos
docker-compose exec fatigue-sensor ls -la /app
```

### Limitação de Recursos

Edite `docker-compose.yml` para limitar recursos:

```yaml
services:
  fatigue-sensor:
    # ... outras configurações
    deploy:
      resources:
        limits:
          cpus: '2.0'          # Máximo 2 CPUs
          memory: 2G           # Máximo 2GB RAM
        reservations:
          cpus: '0.5'          # Reserva mínima de 0.5 CPU
          memory: 512M         # Reserva mínima de 512MB
    
    # Alternativamente, usando sintaxe v2 do Compose:
    mem_limit: 2g
    memswap_limit: 2g
    cpus: 2.0
```

### Isolamento de Rede

```yaml
# Para maior segurança, use rede personalizada
networks:
  fatigue-sensor-net:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16

services:
  fatigue-sensor:
    networks:
      - fatigue-sensor-net
```

## 📁 Estrutura de Arquivos Docker

```txt
fatigue-sensor/
├── 📁 Arquivos Docker
│   ├── Dockerfile                    # Definição da imagem principal
│   ├── docker-compose.yml            # Orquestração dos serviços
│   ├── .dockerignore                 # Arquivos excluídos do build
│   └── install.sh                    # Script de instalação automática
├── 📁 Código Principal
│   ├── main.py                       # Aplicação principal
│   ├── exemplos_uso.py               # Exemplos e perfis de detecção
│   └── requirements.txt              # Dependências Python
├── 📁 Modelos e Dados
│   └── shape_predictor_68_face_landmarks.dat  # Modelo de marcos faciais
├── 📁 Configuração
│   ├── .env                          # Variáveis de ambiente (criado automaticamente)
│   └── .gitignore                    # Arquivos ignorados pelo Git
└── 📁 Documentação
    ├── README.md                     # Documentação principal
    ├── DOCKER.md                     # Este guia Docker
    └── LICENSE                       # Licença do projeto
```

## 🎯 Casos de Uso Específicos

### Ambiente de Produção

```bash
# Para uso em produção, configure:
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# docker-compose.prod.yml example:
# version: '3.8'
# services:
#   fatigue-sensor:
#     restart: always
#     logging:
#       driver: "json-file"
#       options:
#         max-size: "10m"
#         max-file: "3"
```

### Desenvolvimento e Testes

```bash
# Usar perfil de desenvolvimento
docker-compose --profile dev up fatigue-sensor-dev

# Executar testes unitários (se implementados)
docker-compose run --rm fatigue-sensor python3 -m pytest tests/

# Verificar diferentes cenários
docker-compose run --rm fatigue-sensor python3 exemplos_uso.py
```

### Integração Contínua

```yaml
# Exemplo para .github/workflows/docker.yml
name: Docker Build and Test
on: [push, pull_request]
jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build Docker image
        run: docker build -t fatigue-sensor .
      - name: Test container
        run: |
          docker run --rm fatigue-sensor python3 -c "import main; print('Import successful')"
```

## 🤝 Contribuições

Para contribuir com melhorias no setup Docker:

1. **Fork o projeto**
```bash
git clone https://github.com/seu-usuario/fatigue-sensor.git
cd fatigue-sensor
```

2. **Crie uma branch para sua feature**
```bash
git checkout -b feature/docker-improvement
```

3. **Teste suas mudanças extensivamente**
```bash
# Teste build limpo
docker-compose build --no-cache

# Teste execução
docker-compose up --build

# Teste diferentes cenários
docker-compose --profile dev up fatigue-sensor-dev
```

4. **Commit suas mudanças**
```bash
git commit -m 'feat: improve Docker configuration for better audio support'
```

5. **Push e abra Pull Request**
```bash
git push origin feature/docker-improvement
```

### Checklist para Contribuições Docker

- [ ] Dockerfile funciona em diferentes arquiteturas (x86_64, ARM64)
- [ ] docker-compose.yml está bem documentado
- [ ] install.sh funciona em diferentes distribuições Linux
- [ ] Testes passam no container
- [ ] Documentação atualizada
- [ ] Exemplo de uso funciona corretamente

## 📞 Suporte e Ajuda

### Diagnóstico Rápido

Execute o diagnóstico automático:

```bash
# Script de diagnóstico completo
./install.sh

# Ou verificação manual rápida
docker --version && docker-compose --version
ls /dev/video* /dev/snd/
echo $DISPLAY
xhost +local:docker 2>/dev/null || echo "X11 não configurado"
```

### Onde Buscar Ajuda

1. **Logs do sistema**: `docker-compose logs -f`
2. **Documentação oficial**: Este arquivo e README.md
3. **Issues no GitHub**: Para problemas específicos
4. **Comunidade Docker**: Para problemas gerais de containerização

### Informações Úteis para Reportar Problemas

Ao reportar um problema, inclua:

```bash
# Informações do sistema
uname -a
docker --version
docker-compose --version

# Status dos dispositivos
ls -la /dev/video* 2>/dev/null || echo "Nenhuma câmera encontrada"
ls -la /dev/snd/ 2>/dev/null || echo "Nenhum dispositivo de áudio"

# Variáveis de ambiente relevantes
echo "DISPLAY: $DISPLAY"
echo "XDG_RUNTIME_DIR: $XDG_RUNTIME_DIR"

# Logs do container
docker-compose logs --tail=50
```

---

### 🎉 Desenvolvido com ❤️ para facilitar o desenvolvimento e implantação

**Versão da documentação**: 2.0  
**Última atualização**: 2024  
**Compatibilidade**: Docker 20.10+, Docker Compose 2.0+

> 💡 **Dica**: Execute `./install.sh` para configuração automática e rápida!
