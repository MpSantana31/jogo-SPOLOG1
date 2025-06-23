# Sudoku 8-bit

Um jogo de Sudoku com estilo retrô desenvolvido em Python usando Pygame.

## 📦 Pré-requisitos

- Python 3.8 ou superior
- Pip (gerenciador de pacotes do Python)

## 🛠️ Instalação

1. Clone o repositório:
```bash
git clone https://github.com/MpSantana31/jogo-SPOLOG1.git
cd jogo-SPOLOG1
```

2. Crie e ative um ambiente virtual (recomendado):
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

## 🎮 Como Jogar

1. Execute o jogo:
```bash
python main.py
```

2. No menu principal:
   - Selecione 'Jogar'
   - Escolha uma dificuldade (Fácil, Médio ou Difícil)
   - Opção 'Resolver' para ver a solução automática

3. No jogo:
   - Clique em uma célula para selecioná-la
   - Digite um número de 1-9 para preencher
   - Backspace/Delete para apagar
   - ESC para voltar ao menu

4. Objetivo:
   - Preencher todo o tabuleiro sem repetir números nas linhas, colunas ou quadrantes

## 🎨 Features

- Interface estilo 8-bit
- Três níveis de dificuldade
- Sistema de dicas
- Contador de erros

## ⚙️ Algoritmos do Jogo

### Geração do Tabuleiro

O jogo utiliza um algoritmo para gerar tabuleiros Sudoku válidos e com dificuldade controlada:

1. **Preenchimento Inicial**:
   - Preenche os blocos diagonais 3x3 com números aleatórios (cada bloco contém números 1-9 sem repetição)

2. **Resolução do Tabuleiro**:
   - Utiliza backtracking com randomização para garantir variedade
   - Verifica cada posição vazia e tenta números válidos

3. **Remoção de Células**:
   - Remove células baseado no nível de dificuldade:
     - Fácil: ~40 células vazias (5 por bloco 3x3)
     - Médio: ~50 células vazias (6 por bloco 3x3)
     - Difícil: ~60 células vazias (7 por bloco 3x3)
   - Garante que cada bloco tenha um número mínimo de células vazias

### Resolução Automática (Solver)

O solver implementa técnicas avançadas para eficiência e visualização:

1. **Heurística MRV (Minimum Remaining Values)**:
   - Prioriza células com menos opções disponíveis

2. **Backtracking Otimizado**:
   - Memoriza números inválidos para evitar verificações repetidas
   - Permite visualização passo-a-passo

3. **Sistema de Dicas Inteligente**:
   - Identifica células com apenas uma possibilidade
   - Fornece sugestões válidas para qualquer célula

### Como Usar o Solver

1. No menu principal, inicie o jogo normalmente
2. Durante o jogo, clique no botão "Resolver"
3. Assista o algoritmo preenchendo o tabuleiro passo-a-passo
4. Acompanhe o backtracking (em vermelho) quando necessário
