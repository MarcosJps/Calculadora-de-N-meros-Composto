# 🧮 Calculadora de Números Complexos (AST Interpreter)

Uma calculadora de números complexos criada em Python, capaz de interpretar
expressões matemáticas usando análise sintática (AST).  
O projeto permite somar, subtrair, multiplicar, dividir, elevar potências,
usar parênteses e calcular o número conjugado.

---

## ✨ Funcionalidades

- Suporte a números complexos no formato **a + bi**
- Operações:
  - Adição: `(2 + 3i) + (4 - i)`
  - Subtração: `(5 - 2i) - (1 + 7i)`
  - Multiplicação: `(3 + 2i) * (1 - 4i)`
  - Divisão: `(6 + 3i) / (2 - i)`
  - Potência: `(2 + i) ** 3`
  - Conjugado: `con(4 - 9i)`
- Analisador próprio sem usar a lib `cmath`
- Interface gráfica simples feita com Tkinter

---

## ▶️ Como executar

1. Instale o Python 3.10+  
2. Salve o arquivo como `calculadora_complexa.py`  
3. Execute:

```bash
python calculadora_complexa.py

🧪 Exemplos para testar
Expressão	Resultado
3 + 2i + 5 - i	   8 + 1i
(2 + 3i) * (1 - 4i)	   14 - 5i
(5 - 2i) / (1 + i)	   1.5 - 3.5i
con(7 - 9i)	   7 + 9i
(2 + i) ** 4	   -7 + 24i
(10 + 8i) - (3 - 6i)	   7 + 14i

📂 Estrutura do projeto
📦 Calculadora Complexa
 ┣ 📜 calculadora_complexa.py
 ┣ 📜 README.md
