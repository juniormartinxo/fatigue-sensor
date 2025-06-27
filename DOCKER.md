# 🐳 Guia Docker - FatigueSensor

Este guia explica como executar o FatigueSensor utilizando Docker e Docker Compose.

## 📋 Pré-requisitos

- **Docker**: Versão 20.10 ou superior
- **Docker Compose**: Versão 2.0 ou superior  
- **Webcam**: Câmera USB ou integrada
- **Sistema de Áudio**: Para alertas sonoros
- **Linux/WSL**: Sistema compatível com X11

### Verificação dos Pré-requisitos

```bash
# Verificar versões instaladas
docker --version
docker-compose --version

# Verificar dispositivos de câmera
ls /dev/video*

# Verificar dispositivos de áudio
ls /dev/snd/
```

## 🚀 Início Rápido

### 1. Setup Automático

Execute o script de configuração automática:

```bash
# Torna o script executável (se necessário)
chmod +x docker-setup.sh

# Executa o setup
./docker-setup.sh
```

### 2. Execução Manual

Se preferir configurar manualmente:

```bash
# Permitir acesso ao X11
xhost +local:docker

# Criar arquivo .env
echo "DISPLAY=$DISPLAY" > .env

# Construir e executar
docker-compose up --build
```

## 🛠️ Comandos Principais

### Construção e Execução

```bash
# Construir imagem e executar serviço
docker-compose up --build

# Executar em background
docker-compose up -d

# Forçar reconstrução
docker-compose build --no-cache
```

### Controle de Serviços

```bash
# Parar serviços
docker-compose down

# Parar e remover volumes
docker-compose down -v

# Reiniciar serviços
docker-compose restart
```

### Logs e Monitoramento

```bash
# Ver logs em tempo real
docker-compose logs -f

# Ver logs de serviço específico
docker-compose logs fatigue-sensor

# Ver logs das últimas 50 linhas
docker-compose logs --tail=50
```

## ⚙️ Configurações Avançadas

### Parâmetros Personalizados

```bash
# Executar com parâmetros específicos
docker-compose run fatigue-sensor python3 main.py --ear-threshold 0.22 --mar-threshold 0.70

# Executar comando customizado
docker-compose run fatigue-sensor python3 exemplos_uso.py
```

### Modo Desenvolvimento

```bash
# Ativar modo desenvolvimento (bash interativo)
docker-compose --profile dev up fatigue-sensor-dev

# Executar bash no container em execução
docker-compose exec fatigue-sensor bash
```

### Múltiplas Câmeras

Se você possui múltiplas câmeras, edite o `docker-compose.yml`:

```yaml
devices:
  - /dev/video0:/dev/video0    # Câmera principal
  - /dev/video1:/dev/video1    # Câmera secundária
  - /dev/video2:/dev/video2    # Câmera adicional
```

## 🔧 Resolução de Problemas

### Problema: "Não foi possível acessar a câmera"

**Soluções:**

```bash
# Verificar permissões de dispositivos
ls -la /dev/video*

# Adicionar usuário aos grupos necessários
sudo usermod -a -G video $USER
sudo usermod -a -G audio $USER

# Reiniciar sessão ou executar com sudo temporariamente
```

### Problema: "Display não encontrado"

**Soluções:**

```bash
# Verificar variável DISPLAY
echo $DISPLAY

# Reconfigurar X11
xhost +local:docker

# Para WSL, pode ser necessário
export DISPLAY=:0
```

### Problema: "Som não funciona"

**Soluções:**

```bash
# Verificar PulseAudio
pulseaudio --check

# Reiniciar PulseAudio
pulseaudio --kill
pulseaudio --start

# Verificar dispositivos de áudio
pactl list short sinks
```

### Problema: "Permission denied" em dispositivos

**Soluções:**

```bash
# Dar permissões temporárias
sudo chmod 666 /dev/video0
sudo chmod 666 /dev/snd/*

# Solução permanente: adicionar regras udev
sudo nano /etc/udev/rules.d/99-webcam.rules
# Adicionar:
# SUBSYSTEM=="video4linux", GROUP="video", MODE="0664"
# SUBSYSTEM=="sound", GROUP="audio", MODE="0664"
```

## 🐛 Debug e Desenvolvimento

### Executar com Debug

```bash
# Habilitar logs verbose
docker-compose run fatigue-sensor python3 -u main.py

# Executar com Python em modo debug
docker-compose run fatigue-sensor python3 -m pdb main.py
```

### Inspeção do Container

```bash
# Listar containers
docker ps -a

# Executar bash no container
docker exec -it fatigue-sensor bash

# Verificar logs do sistema
docker logs fatigue-sensor
```

### Limpeza do Sistema

```bash
# Remover containers parados
docker container prune

# Remover imagens não utilizadas
docker image prune

# Limpeza completa (CUIDADO!)
docker system prune -a
```

## 📊 Monitoramento

### Recursos do Container

```bash
# Estatísticas em tempo real
docker stats fatigue-sensor

# Uso de recursos
docker-compose top
```

### Verificação de Saúde

```bash
# Status dos serviços
docker-compose ps

# Verificar se aplicação está respondendo
docker-compose exec fatigue-sensor ps aux
```

## 🔒 Segurança

### Usuário Não-Root

O container executa com usuário não-root (`appuser`) por segurança:

```bash
# Verificar usuário atual no container
docker-compose exec fatigue-sensor whoami
docker-compose exec fatigue-sensor id
```

### Limitação de Recursos

Para limitar recursos do container, edite `docker-compose.yml`:

```yaml
services:
  fatigue-sensor:
    # ... outras configurações
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 2G
        reservations:
          memory: 512M
```

## 📁 Estrutura de Arquivos Docker

```
sono/
├── Dockerfile              # Definição da imagem
├── docker-compose.yml      # Orquestração dos serviços
├── .dockerignore           # Arquivos excluídos do build
├── docker-setup.sh         # Script de configuração automática
├── DOCKER.md               # Este guia
└── .env                    # Variáveis de ambiente (criado automaticamente)
```

## 🤝 Contribuições

Para contribuir com melhorias no setup Docker:

1. Fork o projeto
2. Crie branch: `git checkout -b feature/docker-improvement`
3. Teste as mudanças: `docker-compose up --build`
4. Commit: `git commit -m 'Improve Docker setup'`
5. Push: `git push origin feature/docker-improvement`
6. Abra Pull Request

## 📞 Suporte

Se encontrar problemas com o Docker:

1. Verifique os logs: `docker-compose logs`
2. Execute o diagnóstico: `./docker-setup.sh`
3. Consulte a seção de resolução de problemas acima
4. Abra uma issue no repositório com detalhes do erro

---

**Desenvolvido com ❤️ para facilitar o desenvolvimento e implantação** 