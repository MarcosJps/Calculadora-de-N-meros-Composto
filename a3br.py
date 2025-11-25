import ast
import math
import tkinter as tk
from tkinter import messagebox

IMAGINARY_UNIT_NAME = "__j__"

class Complexo:
    def __init__(self, real=0, imag=0):
        self.real = float(real)
        self.imag = float(imag)

    def __add__(self, o):
        return Complexo(self.real + o.real, self.imag + o.imag)

    def __sub__(self, o):
        return Complexo(self.real - o.real, self.imag - o.imag)

    def __mul__(self, o):
        r = self.real * o.real - self.imag * o.imag
        i = self.real * o.imag + self.imag * o.real
        return Complexo(r, i)

    def __truediv__(self, o):
        denom = o.real**2 + o.imag**2
        if denom == 0:
            raise ZeroDivisionError("Divisão por zero.")
        r = (self.real * o.real + self.imag * o.imag) / denom
        i = (self.imag * o.real - self.real * o.imag) / denom
        return Complexo(r, i)

    def __pow__(self, n):
        if not n.imag == 0 or not n.real == int(n.real):
            raise ValueError("Potência só aceita expoente inteiro.")
        result = Complexo(1, 0)
        exp_int = int(n.real)
        if exp_int < 0:
            base = Complexo(1, 0) / self
            exp_int = -exp_int
        else:
            base = self
        for _ in range(exp_int):
            result = result * base
        return result

    def conjugate(self):
        return Complexo(self.real, -self.imag)

    def sqrt(self):
        m = math.sqrt(self.real**2 + self.imag**2)
        r = math.sqrt((m + self.real) / 2)
        i = math.copysign(math.sqrt((m - self.real) / 2), self.imag)
        return Complexo(r, i)

    def __repr__(self):
        sinal = '+' if self.imag >= 0 else ''
        if self.imag == 0:
            return f"{self.real}"
        elif self.real == 0:
            return f"{self.imag}j"
        return f"{self.real}{sinal}{self.imag}j"

def parse_complexo(texto):
    texto = texto.replace(" ", "")
    if "j" not in texto:
        return Complexo(float(texto), 0)
    texto_sem_j = texto.replace("j", "")
    if all(c not in texto_sem_j for c in "+-") or (texto_sem_j.startswith(('-', '+')) and all(c not in texto_sem_j[1:] for c in "+-")):
        try:
            return Complexo(0, float(texto_sem_j))
        except ValueError:
            pass
    for i in range(len(texto_sem_j) - 1, -1, -1):
        if texto_sem_j[i] in "+-" and i != 0 and (texto_sem_j[i-1] not in ('e', 'E')):
            real = texto_sem_j[:i]
            imag = texto_sem_j[i:]
            return Complexo(float(real), float(imag))
    return Complexo(0, float(texto_sem_j))

class CalculadoraComplexa:
    def __init__(self):
        self.vars = {}
        self.funcoes = {
            "sqrt": lambda z: z.sqrt(),
            "conjugate": lambda z: z.conjugate()
        }

    def _eval(self, no):
        if isinstance(no, ast.Constant):
            if isinstance(no.value, (int, float)):
                return Complexo(no.value, 0)
            else:
                raise TypeError("Constante inválida.")

        elif isinstance(no, ast.BinOp):
            l = self._eval(no.left)
            r = self._eval(no.right)
            if isinstance(no.op, ast.Add): return l + r
            if isinstance(no.op, ast.Sub): return l - r
            if isinstance(no.op, ast.Mult): return l * r
            if isinstance(no.op, ast.Div): return l / r
            if isinstance(no.op, ast.Pow): return l ** r

        elif isinstance(no, ast.UnaryOp):
            v = self._eval(no.operand)
            if isinstance(no.op, ast.USub): return Complexo(-v.real, -v.imag)
            if isinstance(no.op, ast.UAdd): return v

        elif isinstance(no, ast.Name):
            nome = no.id
            if nome == IMAGINARY_UNIT_NAME:
                return Complexo(0, 1)
            if nome not in self.vars:
                raise NameError(f"Variável indefinida: {nome}")
            return self.vars[nome]

        elif isinstance(no, ast.Call):
            nome = no.func.id
            if nome not in self.funcoes:
                raise NameError(f"Função não permitida: {nome}")
            if len(no.args) != 1:
                raise TypeError("A função requer 1 argumento.")
            args = [self._eval(a) for a in no.args]
            return self.funcoes[nome](*args)

        raise TypeError("Operação inválida.")

    def executar(self, exp):
        try:
            exp_processada = exp.replace(" ", "")
            exp_processada = exp_processada.replace("j", f"*{IMAGINARY_UNIT_NAME}")
            if exp_processada.startswith(f"*{IMAGINARY_UNIT_NAME}"):
                exp_processada = "1" + exp_processada
            exp_processada = exp_processada.replace(f"**{IMAGINARY_UNIT_NAME}", f"*{IMAGINARY_UNIT_NAME}")
            arv = ast.parse(exp_processada, mode="eval")
            return self._eval(arv.body)
        except Exception as e:
            return f"Erro: {e}"

calc = CalculadoraComplexa()

def calcular():
    exp = entrada.get()
    resultado = calc.executar(exp)
    saida.config(state="normal")
    saida.delete(0, tk.END)
    saida.insert(0, str(resultado))
    saida.config(state="readonly")

janela = tk.Tk()
janela.title("Calculadora Complexa")

tk.Label(janela, text="Expressão:").grid(row=0, column=0)
entrada = tk.Entry(janela, width=40)
entrada.grid(row=0, column=1)

tk.Button(janela, text="Calcular", command=calcular).grid(row=1, column=0, columnspan=2)

tk.Label(janela, text="Resultado:").grid(row=2, column=0)
saida = tk.Entry(janela, width=40, state="readonly")
saida.grid(row=2, column=1)

janela.mainloop()
