# Calculadora de Números Complexos 

Uma calculadora completa para expressões com números complexos, desenvolvida em Python usando Tkinter e avaliação segura via AST.

## Funcionalidades

### Motor Matemático
- Soma, subtração, multiplicação, divisão, potência.
- Funções: sqrt(z), conjugate(z).
- Avaliação segura via ast.parse.
- Conversão automática da unidade imaginária j → __j__.

### Interface Gráfica
- Campo de entrada de expressão.
- Botão Calcular.
- Campo de saída somente leitura.
- Tratamento de erros via messagebox.

## Exemplos para Testar

### Operações básicas
3+2j + 1+5j → 4+7j

10-4j - (3+1j) → 7-5j

### Multiplicação / Divisão
(3+4j) * (2-j) → 10+5j  
(6+2j) / (1-j) → 2+4j

### Potência
(1+2j)**3 → -11+2j

### Funções especiais
sqrt(5j) → 1.5811+1.5811j  
conjugate(3-4j) → 3+4j

### Extras
2j * (1 + j) → -2+2j  
sqrt(4+9j)  
(2+3j) / (1+1j)  
(3j) * (4j)

## Estrutura
calculadora.py  
├── Classe Complexo  
├── Parser de números complexos  
├── CalculadoraComplexa  
└── Interface Tkinter

## Universidade Salvador – UNIFACS
Projeto acadêmico desenvolvido em Python.
