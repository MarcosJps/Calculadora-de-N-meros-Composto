🧮 Calculadora de Números Complexos com Árvore LISP

Uma calculadora interativa em Python, agora com interface gráfica (Tkinter), capaz de interpretar expressões matemáticas envolvendo números complexos usando AST para análise segura e geração automática da Árvore LISP da expressão.

✨ Funcionalidades

Operações com números complexos: +, -, *, /, **

Suporte às funções:

sqrt(z)

conjugate(z)

con(z) (atalho para o conjugado)

Processamento manual de números complexos (não usa cmath)

Interpretador próprio usando AST (evita eval)

Exibição automática da Árvore Sintática em formato LISP

Interface gráfica completa com Tkinter

Aceita notação natural de complexo: 3+2j, -4j, 2-7j, etc.

📁 Arquivos

a3br.py — contém toda a calculadora, interpretação da expressão, geração da árvore LISP e interface gráfica Tkinter.

⚙️ Pré-Requisitos

Python 3.x instalado

Não usa nenhuma biblioteca externa além da biblioteca padrão.

🚀 Como Executar

Baixe ou clone o projeto:

git clone <seu-repo.git>
cd <seu-repo>


Execute o script:

python a3br.py


A interface gráfica será aberta.
Basta digitar uma expressão e clicar Calcular.

🧪 Exemplos de uso
Entrada:
3+2j


Saída:

Resultado: 3.0+2.0j
Árvore LISP: (+ 3 2*j)

Entrada:
(1+1j)*(1-1j)


Saída:

Resultado: 2.0
Árvore LISP: (* (+ 1 1*j) (- 1 1*j))

Entrada:
conjugate(5-3j)


Saída:

Resultado: 5.0+3.0j
Árvore LISP: (conjugate (- 5 (* 3 j)))

Entrada:
sqrt(9-16j)


Saída:

Resultado: 4.0-2.0j
Árvore LISP: (sqrt (- 9 (* 16 j)))

🛠️ Como o sistema funciona internamente
🔹 Processamento da expressão

A expressão digitada passa por:

Limpeza de espaços

Conversão de j para *j (para a AST interpretar corretamente)

Geração da árvore AST do Python

Conversão paralela para Árvore LISP

Avaliação usando a classe Complexo

🔹 Avaliação segura

Somente os operadores permitidos e funções da calculadora podem ser usados.

🔹 Classe Complexo

Implementa manualmente:

Soma

Subtração

Multiplicação

Divisão

Potência inteira

Conjugado

Raiz quadrada

🔹 Árvore LISP

A expressão é convertida para uma estrutura do tipo:

(op esquerda direita)


Exemplo:

( * (+ 2 j) (^ 3 2) )

🤝 Contribuição
