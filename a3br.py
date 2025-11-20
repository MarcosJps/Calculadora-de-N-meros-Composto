import ast
import math



class Complexo:
    def __init__(self, real=0, imag=0):
        self.real = float(real)
        self.imag = float(imag)

    # Soma
    def __add__(self, o):
        return Complexo(self.real + o.real, self.imag + o.imag)

    # Subtração
    def __sub__(self, o):
        return Complexo(self.real - o.real, self.imag - o.imag)

    # Multiplicação
    def __mul__(self, o):
        r = self.real * o.real - self.imag * o.imag
        i = self.real * o.imag + self.imag * o.real
        return Complexo(r, i)

    # Divisão
    def __truediv__(self, o):
        denom = o.real**2 + o.imag**2
        r = (self.real * o.real + self.imag * o.imag) / denom
        i = (self.imag * o.real - self.real * o.imag) / denom
        return Complexo(r, i)

    # Potência (somente expoente inteiro)
    def __pow__(self, n):
        result = Complexo(1, 0)
        for _ in range(int(n.real)):
            result = result * self
        return result

    # Conjugado
    def conjugate(self):
        return Complexo(self.real, -self.imag)

    # Raiz quadrada
    def sqrt(self):
        m = math.sqrt(self.real**2 + self.imag**2)
        r = math.sqrt((m + self.real) / 2)
        i = math.copysign(math.sqrt((m - self.real) / 2), self.imag)
        return Complexo(r, i)

    def __repr__(self):
        sinal = '+' if self.imag >= 0 else ''
        return f"{self.real}{sinal}{self.imag}j"

def parse_complexo(texto: str) -> Complexo:
    texto = texto.replace(" ", "")

    if "j" not in texto:
        return Complexo(float(texto), 0)

    texto = texto.replace("j", "")

    for i in range(len(texto) - 1, -1, -1):
        if texto[i] in "+-" and i != 0:
            real = texto[:i]
            imag = texto[i:]
            return Complexo(float(real), float(imag))

    return Complexo(0, float(texto))

class CalculadoraComplexa:
    def __init__(self):
        self.vars = {}
        self.funcoes = {
            "sqrt": lambda z: z.sqrt(),
            "conjugate": lambda z: z.conjugate()
        }

    def _eval(self, no):

        # Constante numérica
        if isinstance(no, ast.Constant):
            return Complexo(no.value, 0)

        # Operações binárias
        elif isinstance(no, ast.BinOp):
            l = self._eval(no.left)
            r = self._eval(no.right)

            if isinstance(no.op, ast.Add): return l + r
            if isinstance(no.op, ast.Sub): return l - r
            if isinstance(no.op, ast.Mult): return l * r
            if isinstance(no.op, ast.Div): return l / r
            if isinstance(no.op, ast.Pow): return l ** r

        # Operações unárias
        elif isinstance(no, ast.UnaryOp):
            v = self._eval(no.operand)
            if isinstance(no.op, ast.USub): return Complexo(-v.real, -v.imag)
            if isinstance(no.op, ast.UAdd): return v

        # Variáveis
        elif isinstance(no, ast.Name):
            nome = no.id
            if nome not in self.vars:
                val = input(f"Digite valor para {nome} (ex: 3+2j): ")
                self.vars[nome] = parse_complexo(val)
            return self.vars[nome]

        # Funções
        elif isinstance(no, ast.Call):
            nome = no.func.id
            if nome not in self.funcoes:
                raise NameError(f"Função não permitida: {nome}")
            args = [self._eval(a) for a in no.args]
            return self.funcoes[nome](*args)

        raise TypeError("Operação inválida")

    def executar(self, exp):
        try:
            
            exp = exp.replace("j", "*j")

            arv = ast.parse(exp, mode="eval")
            return self._eval(arv.body)

        except Exception as e:
            return f"Erro: {e}"

if __name__ == "__main__":
    calc = CalculadoraComplexa()

    while True:
        exp = input("\nExpressão (ou 'sair'): ")
        if exp.lower() == "sair":
            break

        resultado = calc.executar(exp)
        print("Resultado:", resultado)
