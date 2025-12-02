# 🧮 Calculadora de Números Complexos 

Uma calculadora interativa de linha de comando (CLI) em Python que interpreta e resolve expressões envolvendo números complexos usando `ast` para parse seguro (evita `eval`).

**Funcionalidades**

* Operações aritméticas com complexos: `+`, `-`, `*`, `/`, `**`
* Funções nativas: `sqrt(z)`, `conjugate(z)`
* Variáveis dinâmicas: caso uma variável apareça na expressão, a calculadora pede o valor ao usuário
* Suporte à notação `j` (ex: `3+2j`)

---

## Arquivos

* `a3br.py` — implementa a calculadora e o REPL (prompt `calc>`).

---

## ⚙️ Pré-requisitos

* Python 3.x

> Não há dependências externas além da biblioteca padrão.

---

## 🚀 Como Executar

1. Clone o repositório ou baixe os arquivos.

```bash
git clone <seu-repo.git>
cd <seu-repo>
```

2. Execute o script:

```bash
python a3br.py
```

3. No prompt digite expressões. Exemplos:

```
 3+2j
= 3.0+2.0j

 (1+1j)*(1-1j)
= 2.0

(-4)
= 2.0j

 2*Z
Valor para 'Z' (ex: 3+2j): 5+1j
= 10.0+2.0j
```

---

## 🛠️ Detalhes Técnicos

* O parser substitui unidades imaginárias (sufixo `j`) por um token interno `*__j__` para compatibilizar com a AST.
* A avaliação percorre a AST e usa a classe `Complexo` para todas as operações, garantindo controle sobre operações e permitindo validações.
* Chamadas de função são limitadas a `sqrt` e `conjugate` por segurança.

---

## 🤝 Contribuição

1. Faça um fork do repositório.
2. Crie uma branch: `git checkout -b feat/minha-melhoria`.
3. Commit suas mudanças: `git commit -am 'Adiciona X'`.
4. Push: `git push origin feat/minha-melhoria`.
5. Abra um Pull Request.
