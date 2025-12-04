import ast
import math

IMAGINARY_UNIT_NAME = "j"

class Complexo:
    def __init__(self, real=0, imag=0):
        self.real = float(real)
        self.imag = float(imag)

    def __add__(self, o):
        if isinstance(o, (int, float)): o = Complexo(o)
        return Complexo(self.real + o.real, self.imag + o.imag)

    def __sub__(self, o):
        if isinstance(o, (int, float)): o = Complexo(o)
        return Complexo(self.real - o.real, self.imag - o.imag)

    def __mul__(self, o):
        if isinstance(o, (int, float)): o = Complexo(o)
        r = self.real * o.real - self.imag * o.imag
        i = self.real * o.imag + self.imag * o.real
        return Complexo(r, i)

    def __truediv__(self, o):
        if isinstance(o, (int, float)): o = Complexo(o)
        denom = o.real**2 + o.imag**2
        if denom == 0:
            raise ZeroDivisionError("Divisão por zero.")
        r = (self.real * o.real + self.imag * o.imag) / denom
        i = (self.imag * o.real - self.real * o.imag) / denom
        return Complexo(r, i)

    def __pow__(self, n):
        if isinstance(n, (int, float)): n = Complexo(n)
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


# - ÁRVORE LISP -
def ast_to_lisp(node):
    if isinstance(node, ast.BinOp):
        op = {
            ast.Add: "+",
            ast.Sub: "-",
            ast.Mult: "*",
            ast.Div: "/",
            ast.Pow: "^"
        }.get(type(node.op), "?")
        return f"({op} {ast_to_lisp(node.left)} {ast_to_lisp(node.right)})"

    elif isinstance(node, ast.UnaryOp):
        op = "-" if isinstance(node.op, ast.USub) else "+"
        return f"({op} {ast_to_lisp(node.operand)})"

    elif isinstance(node, ast.Call):
        return f"({node.func.id} {ast_to_lisp(node.args[0])})"

    elif isinstance(node, ast.Name):
        return node.id

    elif isinstance(node, ast.Constant):
        return str(node.value)

    return "?"


class CalculadoraComplexa:
    def __init__(self):
        self.vars = {}
        self.funcoes = {
            "sqrt": lambda z: z.sqrt(),
            "conjugate": lambda z: z.conjugate(),
            "con": lambda z: z.conjugate()
        }

    def _eval(self, no):
        if isinstance(no, ast.Name):
            nome = no.id
            if nome == IMAGINARY_UNIT_NAME:
                return Complexo(0, 1)
            if nome in self.funcoes:
                return self.funcoes[nome]
            if nome in self.vars:
                return self.vars[nome]
            raise NameError(f"Variável indefinida: {nome}")

        elif isinstance(no, ast.Call):
            nome = no.func.id
            if nome not in self.funcoes:
                raise NameError(f"Função não permitida: {nome}")
            args = [self._eval(a) for a in no.args]
            return self.funcoes[nome](*args)

        elif isinstance(no, ast.Constant):
            if isinstance(no.value, (int, float)):
                return Complexo(no.value, 0)

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

        raise TypeError("Operação inválida.")

    def definir_variaveis_desconhecidas(self, node_tree):
        for node in ast.walk(node_tree):
            if isinstance(node, ast.Name):
                nome = node.id
                if nome == IMAGINARY_UNIT_NAME or nome in self.funcoes or nome in self.vars:
                    continue
                
                print(f"A variável '{nome}' não tem valor.")
                valor_str = input(f"Digite o valor para '{nome}': ")
                
                valor_calculado, _ = self.executar(valor_str, is_sub_call=True)
                
                if isinstance(valor_calculado, str) and valor_calculado.startswith("Erro"):
                    raise ValueError(f"Valor inválido para {nome}")
                    
                self.vars[nome] = valor_calculado

    def executar(self, exp, is_sub_call=False):
        try:
            exp_proc = exp.replace(" ", "").replace("j", f"*{IMAGINARY_UNIT_NAME}")

            if exp_proc.startswith(f"*{IMAGINARY_UNIT_NAME}"):
                exp_proc = "1" + exp_proc

            arv = ast.parse(exp_proc, mode="eval")
            
            if not is_sub_call:
                self.definir_variaveis_desconhecidas(arv.body)

            resultado = self._eval(arv.body)
            lisp = ast_to_lisp(arv.body) if not is_sub_call else ""

            return resultado, lisp

        except Exception as e:
            return f"Erro: {e}", ""


# INTERFACE
if __name__ == "__main__":
    calc = CalculadoraComplexa()
    
    while True:
        entrada = input("\nExpressão: ")
        if entrada.lower() in ["sair", "exit"]:
            break
        
        if not entrada.strip():
            continue

        resultado, lisp = calc.executar(entrada)
        
        print(f"Resultado: {resultado}")
        print(f"Árvore LISP: {lisp}")
            if isinstance(no.op, ast.Pow): return l ** r

        elif isinstance(no, ast.UnaryOp):
            v = self._eval(no.operand)
            if isinstance(no.op, ast.USub): return Complexo(-v.real, -v.imag)
            if isinstance(no.op, ast.UAdd): return v

        raise TypeError("Operação inválida.")

    def executar(self, exp):
        try:
            exp_proc = exp.replace(" ", "").replace("j", f"*{IMAGINARY_UNIT_NAME}")

            if exp_proc.startswith(f"*{IMAGINARY_UNIT_NAME}"):
                exp_proc = "1" + exp_proc

            arv = ast.parse(exp_proc, mode="eval")
            resultado = self._eval(arv.body)
            lisp = ast_to_lisp(arv.body)

            return resultado, lisp

        except Exception as e:
            return f"Erro: {e}", ""


calc = CalculadoraComplexa()


#  INTERFACE 
def calcular():
    exp = entrada.get()
    resultado, lisp = calc.executar(exp)

    saida_result.config(state="normal")
    saida_lisp.config(state="normal")

    saida_result.delete(0, tk.END)
    saida_lisp.delete(0, tk.END)

    saida_result.insert(0, str(resultado))
    saida_lisp.insert(0, lisp)

    saida_result.config(state="readonly")
    saida_lisp.config(state="readonly")


janela = tk.Tk()
janela.title("Calculadora Complexa com Árvore LISP")

tk.Label(janela, text="Expressão:").grid(row=0, column=0)
entrada = tk.Entry(janela, width=50)
entrada.grid(row=0, column=1)

tk.Button(janela, text="Calcular", command=calcular).grid(row=1, column=0, columnspan=2)

tk.Label(janela, text="Resultado:").grid(row=2, column=0)
saida_result = tk.Entry(janela, width=50, state="readonly")
saida_result.grid(row=2, column=1)

tk.Label(janela, text="Árvore LISP:").grid(row=3, column=0)
saida_lisp = tk.Entry(janela, width=50, state="readonly")
saida_lisp.grid(row=3, column=1)

janela.mainloop()

