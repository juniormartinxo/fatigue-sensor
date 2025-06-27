# Exemplos - FatigueSensor

Este diretório contém exemplos práticos de como usar o FatigueSensor em diferentes cenários.

## 📁 Organização dos Arquivos

```txt
examples/
├── 📄 index.py                     # Menu principal para executar qualquer exemplo
├── 📄 basico.py                    # Uso básico do sistema
├── 📄 configuracao_personalizada.py # Configurações personalizadas
├── 📄 monitoramento_metricas.py    # Monitoramento de métricas
├── 📄 configuracao_ambiente.py    # Configurações por ambiente
├── 📄 tratamento_erros.py         # Tratamento robusto de erros
├── 📄 basic.py                    # ⚠️ DEPRECIADO (arquivo original)
└── 📄 README.md                   # Este arquivo
```

## 🚀 Como Usar

### Opção 1: Menu Interativo

```bash
cd examples
python index.py
```

Permite escolher e executar qualquer exemplo através de um menu interativo.

### Opção 2: Exemplo Específico via Menu

```bash
cd examples
python index.py 1    # Executa exemplo básico
python index.py 2    # Executa configuração personalizada
python index.py 3    # Executa monitoramento de métricas
python index.py 4    # Executa configurações por ambiente
python index.py 5    # Executa tratamento de erros
```

### Opção 3: Execução Direta

```bash
cd examples
python basico.py
python configuracao_personalizada.py
python monitoramento_metricas.py
python configuracao_ambiente.py
python tratamento_erros.py
```

## 📋 Descrição dos Exemplos

### 1. **Exemplo Básico** (`basico.py`)

- Uso padrão do sistema com configurações default
- Ideal para começar a usar o FatigueSensor
- Requer câmera funcionando

### 2. **Configuração Personalizada** (`configuracao_personalizada.py`)

- Demonstra como ajustar limiares de sensibilidade
- Personalização de parâmetros EAR e MAR
- Útil para ambientes específicos

### 3. **Monitoramento de Métricas** (`monitoramento_metricas.py`)

- Como acessar e interpretar as métricas do sistema
- Cálculo de taxas de piscadas e bocejos
- Demonstração do score de fadiga

### 4. **Configurações por Ambiente** (`configuracao_ambiente.py`)

- Configurações otimizadas para diferentes ambientes:
  - **Pouca luz**: Parâmetros mais permissivos
  - **Detecção rigorosa**: Máxima sensibilidade
  - **Uso prolongado**: Configuração balanceada
- Não requer câmera (apenas demonstra configurações)

### 5. **Tratamento de Erros** (`tratamento_erros.py`)

- Implementação robusta de tratamento de erros
- Verificação de componentes do sistema
- Dicas de troubleshooting

## ⚠️ Requisitos

Para executar os exemplos que usam a câmera, certifique-se de que:

1. **Dependências instaladas**:

   ```bash
   pip install -r ../requirements.txt
   ```

2. **Arquivo de landmarks**:
   - Tenha o arquivo `shape_predictor_68_face_landmarks.dat` no diretório raiz

3. **Câmera disponível**:
   - Webcam funcionando e acessível
   - Permissões de acesso à câmera configuradas

## 🔧 Personalização

Cada exemplo pode ser facilmente modificado para suas necessidades:

- **Ajustar limiares**: Modifique `EAR_THRESHOLD`, `MAR_THRESHOLD`
- **Configurar frames**: Altere `EAR_CONSEC_FRAMES`, `MAR_CONSEC_FRAMES`
- **Adicionar funcionalidades**: Extend as classes ou adicione novos callbacks

## 📝 Histórico

- **Versão 2.0**: Exemplos reorganizados em arquivos separados (Junho 2025)
- **Versão 1.0**: Arquivo único `basic.py` (depreciado)

---

Para mais informações sobre o FatigueSensor, consulte a documentação principal do projeto.
