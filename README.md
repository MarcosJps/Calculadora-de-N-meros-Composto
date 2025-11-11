🧮 Calculadora de Números Complexos (com Interface Gráfica)

Uma calculadora científica interativa** para expressões com números complexos, desenvolvida em Python com CustomTkinter.  
O projeto combina **análise sintática (AST)** para garantir segurança na execução das expressões e uma **interface moderna e funcional** para o usuário.

---

 📋 Funcionalidades

 🧠 Backend – Motor de Cálculo (`CalculadoraComplexa`)
- Avalia expressões matemáticas com **números complexos** usando `ast` (Árvore de Sintaxe Abstrata).
- Permite as operações básicas:
  - Soma (+), Subtração (-), Multiplicação (*), Divisão (/), Potência (**)
- Suporta funções seguras:
  - `sqrt(z)` → raiz quadrada complexa  
  - `conjugate(z)` → número conjugado
- Permite o uso de **variáveis** (ex: `x`, `y`) — os valores são solicitados via **console**.
- Gera a árvore AST da expressão para visualização.
- Retorna mensagens de erro formatadas para entradas inválidas.

---

💻 Frontend – Interface Gráfica (`Aplicativo`)
Interface feita com **CustomTkinter**, com modo escuro e abas organizadas.

🧮 Aba 1: “Calculadora”
- Caixa de texto com **histórico de expressões**.
- Entrada principal para digitar expressões matemáticas.
- Botões de ação:
  - **Executar (=)** – avalia a expressão.
  - **Mostrar Árvore (Req 6)** – exibe a AST.
  - **Limpar (C)** – limpa o campo de entrada.
  - **Limpar Histórico (AC)** – limpa o visor.
- Botões auxiliares para inserir símbolos e funções (`j`, `()`, `sqrt()`, `conjugate()`, `**`).
- Aviso de que variáveis são pedidas no **terminal**.

 ⚖️ Aba 2: “Verificar Igualdade”
- Permite comparar duas expressões (ex: `(1+2j)` e `(3+4j)/2`).
- Mostra se são **matematicamente iguais** (usando `cmath.isclose`).
- Exibe valores avaliados e resultado da comparação.

---

 🧩 Requisitos do Sistema

| Componente | Versão mínima |
|-------------|----------------|
| Python | 3.8 |
| customtkinter | 5.2+ |
| cmath | nativo |
| ast | nativo |

---

 ⚙️ Instalação

1. **Clone ou baixe** este repositório:
   ```bash
   git clone https://github.com/seuusuario/calculadora-complexa.git
   cd calculadora-complexa
   ```

2. **Instale as dependências**:
   ```bash
   pip install customtkinter
   ```

3. **Execute o programa**:
   ```bash
   python a3br.py
   ```

---

🚀 Exemplos de Uso

🧮 Cálculos simples
```
(3+2j) + (1-4j)
```
Resultado:
```
(4-2j)
```

 🧩 Potência
```
(1+2j)**2
```
Resultado:
```
(-3+4j)
```

 📐 Funções complexas
```
sqrt(4+9j)
```

 🔣 Uso de variáveis
```
(2*x) + (3*y)
```
👉 O programa solicitará os valores de `x` e `y` no **console**:
```
Digite o valor para 'x' no CONSOLE (ex: '3+4j'):
Digite o valor para 'y' no CONSOLE (ex: '1-2j'):
```

---

 🧾 Estrutura do Código

```
a3br.py
├── CalculadoraComplexa
│   ├── executar() → Avalia expressão
│   ├── mostrar_arvore() → Exibe AST
│   ├── limpar_variaveis() → Limpa variáveis
│   └── _avaliar() → Função recursiva para AST
│
└── Aplicativo (CustomTkinter)
    ├── configurar_aba_calculadora()
    ├── configurar_aba_igualdade()
    ├── ao_executar_calc()
    ├── ao_verificar_igualdade_calc()
    └── mainloop()
```

---

 🧠 Requisitos Atendidos (Projeto Original)

| Requisito | Descrição |
|------------|------------|
| **Req 0** | AST usada para execução segura |
| **Req 1** | Funções matemáticas seguras (sqrt, conjugate) |
| **Req 2** | Avaliação via `ast.parse` |
| **Req 3** | Verificação de igualdade entre expressões |
| **Req 4** | Execução completa de expressões complexas |
| **Req 5** | Tratamento e exibição de erros |
| **Req 6** | Exibição da árvore de execução (AST) |
| **Req 7** | Solicitação interativa de variáveis |

--- 
🏫 **Universidade Salvador (UNIFACS)**  
🗓️ Projeto acadêmico / educacional em Python (CustomTkinter + AST)
