import customtkinter as ctk
import ast
import cmath
import sys
import io 

# --- PARTE 1: LÓGICA DA CALCULADORA (Backend) ---
# (Nomes de classe e métodos traduzidos)
# ---

class CalculadoraComplexa:
    """
    Uma calculadora científica de números complexos baseada em Árvore de Sintaxe Abstrata (AST).
    (Regras 0, 1, 2, 4, 5, 7)
    """
    
    def __init__(self):
        # Dicionário para armazenar valores de variáveis (Req 7)
        self.variaveis = {}
        
        # Funções seguras permitidas (Req 1)
        self.funcoes_seguras = {
            'sqrt': cmath.sqrt,
            'conjugate': lambda z: z.conjugate()
        }

    def _avaliar(self, no):
        """Função recursiva interna para avaliar um nó da árvore AST."""
        
        if isinstance(no, ast.Constant):
            return no.value
        elif isinstance(no, ast.BinOp):
            esquerda = self._avaliar(no.left)
            direita = self._avaliar(no.right)
            if isinstance(no.op, ast.Add): return esquerda + direita
            if isinstance(no.op, ast.Sub): return esquerda - direita
            if isinstance(no.op, ast.Mult): return esquerda * direita
            if isinstance(no.op, ast.Pow): return esquerda ** direita
            if isinstance(no.op, ast.Div):
                if direita == 0: raise ZeroDivisionError("Divisão por zero.")
                return esquerda / direita
        elif isinstance(no, ast.UnaryOp):
            operando = self._avaliar(no.operand)
            if isinstance(no.op, ast.USub): return -operando
            if isinstance(no.op, ast.UAdd): return +operando
        elif isinstance(no, ast.Name):
            nome_var = no.id
            if nome_var in self.variaveis:
                return self.variaveis[nome_var]
            
            # (Req 7) - Pede a variável no CONSOLE
            print(f"--- [GUI] A Calculadora precisa da variável: '{nome_var}' ---")
            while True:
                try:
                    valor_str = input(f"Digite o valor para '{nome_var}' no CONSOLE (ex: '3+4j'): ")
                    valor = complex(valor_str) 
                    self.variaveis[nome_var] = valor
                    return valor
                except ValueError:
                    print(f"Entrada inválida. Use a notação 'a+bj'.", file=sys.stderr)
                except EOFError:
                    raise KeyboardInterrupt("Execução cancelada.")
        elif isinstance(no, ast.Call):
            nome_func = no.func.id
            if nome_func in self.funcoes_seguras:
                argumentos = [self._avaliar(arg) for arg in no.args]
                return self.funcoes_seguras[nome_func](*argumentos)
            else:
                raise NameError(f"Função não permitida: '{nome_func}'.")
        else:
            raise TypeError(f"Operação não suportada: {no.__class__.__name__}")

    def executar(self, expressao):
        """
        Analisa e executa uma expressão, retornando o resultado.
        (Req 4, Req 5)
        """
        try:
            # (Req 2)
            arvore = ast.parse(expressao, mode='eval')
            resultado = self._avaliar(arvore.body)
            return resultado
        except Exception as e:
            # Retorna a mensagem de erro formatada (Req 5)
            return f"Erro: {e}"

    def mostrar_arvore(self, expressao):
        """
        Mostra a árvore de execução (AST) da expressão.
        (Req 6)
        """
        try:
            arvore = ast.parse(expressao, mode='eval')
            # Captura a saída do 'ast.dump' para retornar como string
            stdout_antigo = sys.stdout
            saida_redirecionada = io.StringIO()
            sys.stdout = saida_redirecionada
            
            print(f"--- Árvore AST para: '{expressao}' ---")
            print(ast.dump(arvore, indent=4))
            
            sys.stdout = stdout_antigo
            return saida_redirecionada.getvalue()
        except SyntaxError as e:
            return f"Erro de Sintaxe: Não foi possível gerar a árvore. {e}"

    def limpar_variaveis(self):
        """Limpa as variáveis armazenadas."""
        self.variaveis.clear()
        print("Variáveis limpas.")


# --- PARTE 2: INTERFACE GRÁFICA (Frontend) ---
# (Nomes de classe, métodos e variáveis traduzidos)
# ---

class Aplicativo(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- 1. Configuração da Aparência ---
        ctk.set_appearance_mode("dark")  # Modo "preto"
        ctk.set_default_color_theme("blue") # Tema de cor

        # --- 2. Configuração da Janela ---
        self.title("Calculadora de Números Complexos")
        self.geometry("600x650")

        # Instancia a lógica da calculadora
        self.calculadora = CalculadoraComplexa()

        # Configura o layout principal (grid)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- 3. Criação das Abas (Tabs) ---
        self.abas = ctk.CTkTabview(self, anchor="w")
        self.abas.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.abas.add("Calculadora")
        self.abas.add("Verificar Igualdade")
        
        # Chama as funções para popular cada aba
        self.configurar_aba_calculadora()
        self.configurar_aba_igualdade()
        
        # Adiciona a nota sobre variáveis no console
        self.rotulo_aviso = ctk.CTkLabel(
            self,
            text="(!) ATENÇÃO: Se usar variáveis (x, y), o valor será pedido no CONSOLE/TERMINAL.",
            text_color="gray",
            font=ctk.CTkFont(size=12, slant="italic")
        )
        self.rotulo_aviso.grid(row=1, column=0, padx=15, pady=(0, 10), sticky="w")


    def configurar_aba_calculadora(self):
        """ Popula a aba 'Calculadora' com o layout de calculadora """
        aba = self.abas.tab("Calculadora")
        
        # Configura o grid da aba
        aba.grid_columnconfigure(0, weight=1)
        aba.grid_rowconfigure(0, weight=1) # Visor (Display)
        aba.grid_rowconfigure(1, weight=0) # Entrada (Input)
        aba.grid_rowconfigure(2, weight=0) # Botões (Buttons)

        # --- Visor (Histórico) ---
        self.visor_historico = ctk.CTkTextbox(
            aba,
            wrap="word",
            font=ctk.CTkFont(family="Monospace", size=14),
            state="disabled" # Começa desabilitado (apenas leitura)
        )
        self.visor_historico.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.adicionar_ao_visor("Bem-vindo à Calculadora de Complexos!\nDigite uma expressão abaixo.")

        # --- Entrada (Input) ---
        self.entrada_principal = ctk.CTkEntry(
            aba,
            placeholder_text="Digite a expressão (ex: (1+2j) * x)",
            font=ctk.CTkFont(size=16)
        )
        self.entrada_principal.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")
        # Atalho: Pressionar 'Enter' na caixa de entrada executa o cálculo
        self.entrada_principal.bind("<Return>", lambda event: self.ao_executar_calc())

        # --- Frame de Botões ---
        frame_botoes = ctk.CTkFrame(aba)
        frame_botoes.grid(row=2, column=0, padx=10, pady=0, sticky="ew")
        # Configura 5 colunas de igual largura
        frame_botoes.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

        # --- Botões de Ação (Linha 1) ---
        self.btn_exec = ctk.CTkButton(
            frame_botoes, text="Executar (=)",
            command=self.ao_executar_calc,
            font=ctk.CTkFont(weight="bold")
        )
        self.btn_exec.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        self.btn_tree = ctk.CTkButton(
            frame_botoes, text="Mostrar Árvore (Req 6)",
            command=self.ao_mostrar_arvore_calc
        )
        self.btn_tree.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        self.btn_clear = ctk.CTkButton(
            frame_botoes, text="Limpar (C)",
            command=self.ao_limpar_entrada
        )
        self.btn_clear.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        self.btn_clear_all = ctk.CTkButton(
            frame_botoes, text="Limpar Hist. (AC)",
            command=self.ao_limpar_visor,
            fg_color="darkred", hover_color="red"
        )
        self.btn_clear_all.grid(row=0, column=4, padx=5, pady=5, sticky="ew")

        # --- Botões de Ajuda (Linha 2) ---
        self.btn_j = ctk.CTkButton(
            frame_botoes, text="Inserir 'j'",
            command=lambda: self.inserir_texto("j")
        )
        self.btn_j.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        
        self.btn_paren = ctk.CTkButton(
            frame_botoes, text="Inserir '( )'",
            command=lambda: self.inserir_texto("()", mover_cursor=True)
        )
        self.btn_paren.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        self.btn_sqrt = ctk.CTkButton(
            frame_botoes, text="Inserir 'sqrt()'",
            command=lambda: self.inserir_texto("sqrt()", mover_cursor=True)
        )
        self.btn_sqrt.grid(row=1, column=2, padx=5, pady=5, sticky="ew")

        self.btn_conj = ctk.CTkButton(
            frame_botoes, text="Inserir 'conjugate()'",
            command=lambda: self.inserir_texto("conjugate()", mover_cursor=True)
        )
        self.btn_conj.grid(row=1, column=3, padx=5, pady=5, sticky="ew")
        
        self.btn_pow = ctk.CTkButton(
            frame_botoes, text="Inserir '**' (potência)",
            command=lambda: self.inserir_texto("**")
        )
        self.btn_pow.grid(row=1, column=4, padx=5, pady=5, sticky="ew")


    def configurar_aba_igualdade(self):
        """ Popula a aba 'Verificar Igualdade' (Req 3) """
        aba = self.abas.tab("Verificar Igualdade")
        
        aba.grid_columnconfigure(0, weight=1)
        
        self.frame_igualdade = ctk.CTkFrame(aba)
        self.frame_igualdade.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.frame_igualdade.grid_columnconfigure(0, weight=1)

        self.rotulo_igualdade = ctk.CTkLabel(self.frame_igualdade, text="Verificar se Expressão 1 == Expressão 2")
        self.rotulo_igualdade.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.eq_expr1_entry = ctk.CTkEntry(self.frame_igualdade, placeholder_text="Expressão 1")
        self.eq_expr1_entry.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        self.eq_expr2_entry = ctk.CTkEntry(self.frame_igualdade, placeholder_text="Expressão 2")
        self.eq_expr2_entry.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

        self.botao_igualdade = ctk.CTkButton(
            self.frame_igualdade,
            text="Verificar Igualdade (Req 3)",
            command=self.ao_verificar_igualdade_calc
        )
        self.botao_igualdade.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

        self.rotulo_resultado_igualdade = ctk.CTkLabel(
            self.frame_igualdade,
            text="Resultado: ",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.rotulo_resultado_igualdade.grid(row=4, column=0, padx=10, pady=10, sticky="w")


    # --- Funções de Callback (Eventos da GUI) ---

    def adicionar_ao_visor(self, texto):
        """ Adiciona texto ao visor (histórico) e rola para o final """
        self.visor_historico.configure(state="normal") # Habilita
        self.visor_historico.insert(ctk.END, texto + "\n" + "-"*30 + "\n")
        self.visor_historico.configure(state="disabled") # Desabilita
        self.visor_historico.see(ctk.END) # Rola para o fim

    def inserir_texto(self, texto, mover_cursor=False):
        """ Insere texto na caixa de entrada principal """
        posicao_atual = self.entrada_principal.index(ctk.INSERT)
        self.entrada_principal.insert(posicao_atual, texto)
        
        if mover_cursor:
            # Move o cursor para dentro dos parênteses
            self.entrada_principal.icursor(self.entrada_principal.index(ctk.INSERT) - 1)
        
        self.entrada_principal.focus() # Devolve o foco para a entrada

    def ao_executar_calc(self):
        """ Executa a expressão da entrada principal (Req 4) """
        self.calculadora.limpar_variaveis()
        expressao = self.entrada_principal.get()
        if not expressao:
            self.adicionar_ao_visor(">>> (vazio)\nErro: Nenhuma expressão digitada.")
            return
        
        # A lógica de pedir variáveis (Req 7) será ativada AQUI, no CONSOLE
        resultado = self.calculadora.executar(expressao)
        
        # Mostra no visor (Req 5 - mostra erro se 'resultado' for string de erro)
        self.adicionar_ao_visor(f">>> {expressao}\n{resultado}")
        
        # Limpa a entrada para o próximo cálculo
        if not (isinstance(resultado, str) and resultado.startswith("Erro:")): # Se não for um erro
             self.ao_limpar_entrada()

    def ao_mostrar_arvore_calc(self):
        """ Mostra a árvore AST da expressão principal (Req 6) """
        expressao = self.entrada_principal.get()
        if not expressao:
            self.adicionar_ao_visor("Erro: Nenhuma expressão para mostrar a árvore.")
            return
        
        texto_arvore = self.calculadora.mostrar_arvore(expressao)
        self.adicionar_ao_visor(texto_arvore) # Adiciona a árvore ao visor

    def ao_limpar_entrada(self):
        """ Limpa a caixa de entrada principal """
        self.entrada_principal.delete(0, ctk.END)

    def ao_limpar_visor(self):
        """ Limpa o visor (histórico) """
        self.visor_historico.configure(state="normal")
        self.visor_historico.delete("1.0", ctk.END)
        self.visor_historico.configure(state="disabled")

    def ao_verificar_igualdade_calc(self):
        """ Executa a verificação de igualdade da outra aba (Req 3) """
        self.calculadora.limpar_variaveis()
        
        expr1 = self.eq_expr1_entry.get()
        expr2 = self.eq_expr2_entry.get()
        
        if not expr1 or not expr2:
            self.rotulo_resultado_igualdade.configure(text="Resultado: (digite ambas expressões)")
            return

        print("\n--- Iniciando Verificação de Igualdade ---")
        
        print("--- Avaliando Expressão 1 ---")
        val1 = self.calculadora.executar(expr1)
        
        print("--- Avaliando Expressão 2 ---")
        val2 = self.calculadora.executar(expr2)

        tipos_permitidos = (int, float, complex)
        
        if isinstance(val1, tipos_permitidos) and isinstance(val2, tipos_permitidos):
            sao_iguais = cmath.isclose(val1, val2)
            texto_resultado = f"Iguais: {sao_iguais}  ({val1} vs {val2})"
            self.rotulo_resultado_igualdade.configure(text=texto_resultado)
        else:
            texto_resultado = f"Erro na avaliação. V1: {val1} | V2: {val2}"
            self.rotulo_resultado_igualdade.configure(text=texto_resultado)


if __name__ == "__main__":
    app = Aplicativo()
    app.mainloop()