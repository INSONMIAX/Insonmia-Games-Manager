########################## GERENCIADOR DE JOGOS PYTHON #####################


import copy
import random
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

#Mensagens ao passar o mouse um tempo em cima de botoes

class Tooltip:

    def __init__(self, widget, texto):

        self.widget = widget
        self.texto = texto
        self.janela_tooltip = None
        self.agendamento = None

        self.widget.bind(
            "<Enter>",
            self.agendar,
            add="+"
        )

        self.widget.bind(
            "<Leave>",
            self.esconder,
            add="+"
        )


    def agendar(self, event=None):

        self.agendamento = self.widget.after(
            500,
            self.mostrar
        )


    def mostrar(self):

        if self.janela_tooltip is not None:
            return

        x = self.widget.winfo_rootx() + self.widget.winfo_width() + 5
        y = self.widget.winfo_rooty()

        self.janela_tooltip = tk.Toplevel(
            self.widget
        )

        self.janela_tooltip.overrideredirect(
            True
        )

        self.janela_tooltip.geometry(
            f"+{x}+{y}"
        )

        texto_tooltip = tk.Label(
            self.janela_tooltip,
            text=self.texto,
            background=tema_escolhido["card"],
            foreground=tema_escolhido["texto"],
            relief="solid",
            borderwidth=1,
            padx=8,
            pady=4,
            font=("Segoe UI", 9)
        )

        texto_tooltip.pack()


    def esconder(self, event=None):

        if self.agendamento is not None:

            self.widget.after_cancel(
                self.agendamento
            )

            self.agendamento = None

        if self.janela_tooltip is not None:

            self.janela_tooltip.destroy()

            self.janela_tooltip = None




def buscar_jogo(jogos, nome):

    for jogo in jogos:
        if jogo["Nome"].upper() == nome.upper():
            return jogo

    return None


def buscar_nome_parcial(jogos, trecho):
    resultados = []

    trecho = trecho.strip().upper()

    if trecho == "":
        return resultados

    for jogo in jogos:
        if trecho in jogo["Nome"].upper():
            resultados.append(jogo)

    return resultados


def buscar_por_campo(jogos, campo, valor):

    resultados = []

    for jogo in jogos:

        if campo == "Genero" or campo == "Plataforma":

            valores = jogo[campo].split(",")

            for item in valores:

                if item.strip().upper() == valor.strip().upper():
                    resultados.append(jogo)
                    break

        elif jogo[campo].strip().upper() == valor.strip().upper():
            resultados.append(jogo)

    return resultados


def buscar_por_nota(jogos, tipo):

    resultado = None

    for jogo in jogos:
        if resultado is None:
            resultado = jogo

        elif tipo == "MAIOR" and jogo["Nota"] > resultado["Nota"]:
            resultado = jogo

        elif tipo == "MENOR" and jogo["Nota"] < resultado["Nota"]:
            resultado = jogo

    return resultado


def transformar_linha_em_jogo(linha, jogos):

    dados = linha.split("|")

    if len(dados) != 4 and len(dados) != 5:
        print("Linha inválida ignorada:", linha.strip())
        return None

    nome = dados[0].strip()
    genero = dados[1].strip()
    plataforma = dados[2].strip()
    nota_texto = dados[3].strip()

    if nome == "" or genero == "" or plataforma == "" or nota_texto == "":
        print("Linha com campo vazio ignorada:", linha.strip())
        return None

    try:
        nota = float(nota_texto)

        if nota < 0 or nota > 10:
            print("Nota fora do intervalo ignorada:", linha.strip())
            return None

    except ValueError:
        print("Nota inválida ignorada:", linha.strip())
        return None

    if len(dados) == 5:

        favorito_texto = dados[4].strip().upper()

        if favorito_texto == "SIM":
            favorito = True
        else:
            favorito = False

    else:
        favorito = False

    if buscar_jogo(jogos, nome) is not None:
        print("Jogo duplicado ignorado:", nome)
        return None

    jogo = {
        "Nome": nome,
        "Genero": genero,
        "Plataforma": plataforma,
        "Nota": nota,
        "Favorito": favorito
    }

    return jogo


def carregar_jogos():

    jogos = []

    try:

        try:
            with open(
                "jogo.txt",
                "r",
                encoding="utf-8"
            ) as arquivo:
                linhas = arquivo.readlines()

        except UnicodeDecodeError:

            with open(
                "jogo.txt",
                "r",
                encoding="cp1252"
            ) as arquivo:
                linhas = arquivo.readlines()

        for linha in linhas:

            jogo = transformar_linha_em_jogo(
                linha,
                jogos
            )

            if jogo is not None:
                jogos.append(jogo)

    except FileNotFoundError:
        print("jogo.txt ainda não existe")

    return jogos


#Fazendo a função contrária (Transformando o dicionário em linhas de novo)


def salvar_jogos(jogos):

    try:

        with open(
                "jogo.txt",
                "w",
                encoding="utf-8"
        ) as arquivo:

            for jogo in jogos:

                if jogo["Favorito"]:
                    favorito = "SIM"
                else:
                    favorito = "NAO"

                arquivo.write(
                    jogo["Nome"] + "|" +
                    jogo["Genero"] + "|" +
                    jogo["Plataforma"] + "|" +
                    str(jogo["Nota"]) + "|" +
                    favorito + "\n"
                )

        return True

    except OSError:
        print("Não foi possível salvar os jogos no arquivo!")
        return False



def adicionar_jogo(jogos, nome, genero, plataforma, nota):

    nome = nome.strip().upper()
    genero = genero.strip().upper()
    plataforma = plataforma.strip().upper()

    if nome == "" or genero == "" or plataforma == "":
        return False

    if "|" in nome or "|" in genero or "|" in plataforma:
        return False

    if buscar_jogo(jogos, nome) is not None:
        return False

    try:
        nota = float(nota)
    except ValueError:
        return False

    if nota < 0 or nota > 10:
        return False

    jogo = {
        "Nome": nome,
        "Genero": genero,
        "Plataforma": plataforma,
        "Nota": nota,
        "Favorito": False
    }

    jogos.append(jogo)

    return True


def editar_jogo(jogos, nome_atual, novo_nome, novo_genero, nova_plataforma, nova_nota):

    jogo = buscar_jogo(jogos, nome_atual)

    if jogo is None:
        return False

    novo_nome = novo_nome.strip().upper()
    novo_genero = novo_genero.strip().upper()
    nova_plataforma = nova_plataforma.strip().upper()

    if novo_nome == "":
        novo_nome = jogo["Nome"]

    if novo_genero == "":
        novo_genero = jogo["Genero"]

    if nova_plataforma == "":
        nova_plataforma = jogo["Plataforma"]

    if "|" in novo_nome or "|" in novo_genero or "|" in nova_plataforma:
        return False

    jogo_existente = buscar_jogo(jogos, novo_nome)

    if jogo_existente is not None and jogo_existente != jogo:
        return False

    if nova_nota == "":
        nova_nota = jogo["Nota"]

    else:
        try:
            nova_nota = float(nova_nota)
        except ValueError:
            return False

        if nova_nota < 0 or nova_nota > 10:
            return False

    if (
        novo_nome == jogo["Nome"]
        and novo_genero == jogo["Genero"]
        and nova_plataforma == jogo["Plataforma"]
        and nova_nota == jogo["Nota"]
    ):
        return False

    jogo["Nome"] = novo_nome
    jogo["Genero"] = novo_genero
    jogo["Plataforma"] = nova_plataforma
    jogo["Nota"] = nova_nota

    return True


def remover_jogo(jogos, nome):

    jogo = buscar_jogo(jogos, nome)

    if jogo is None:
        return False

    jogos.remove(jogo)
    return True


def ordenar_jogos(jogos, criterio, ordem=None):

    if criterio == "NOME":
        return sorted(
            jogos,
            key=lambda jogo: jogo["Nome"].upper()
        )

    elif criterio == "NOTA":

        if ordem == "MAIOR":
            return sorted(
                jogos,
                key=lambda jogo: jogo["Nota"],
                reverse=True
            )

        elif ordem == "MENOR":
            return sorted(
                jogos,
                key=lambda jogo: jogo["Nota"]
            )

    return jogos


def media_notas(jogos):

    if not jogos:
        return None

    soma = 0

    for jogo in jogos:
        soma = jogo["Nota"] + soma

    media = soma / len(jogos)

    return media


def quantidade_jogos(jogos):

    return len(jogos)



jogos = carregar_jogos()

nome_selecionado = None
jogos_exibidos = jogos.copy()



janela = tk.Tk()

janela.title("InSonmia Games Manager")

largura = 900
altura = 900

largura_tela = janela.winfo_screenwidth()
altura_tela = janela.winfo_screenheight()

pos_x = (largura_tela - largura) // 2
pos_y = (altura_tela - altura) // 2

janela.geometry(
    f"{largura}x{altura}+{pos_x}+{pos_y}"
)

janela.minsize(
    850,
    750
)

estilo = ttk.Style()

estilo.theme_use("clam")



def aplicar_tema(tema):

    janela.configure(
        bg=tema["fundo"]
    )

    estilo.configure(
        "TFrame",
        background=tema["fundo"]
    )

    estilo.configure(
        "TLabelframe",
        background=tema["card"],
        borderwidth=1,
        relief="solid"
    )

    estilo.configure(
        "TLabelframe.Label",
        background=tema["card"],
        foreground=tema["destaque"],
        font=("Segoe UI", 11, "bold")
    )

    estilo.configure(
        "TLabel",
        background=tema["card"],
        foreground=tema["texto"],
        font=("Segoe UI", 10)
    )

    estilo.configure(
        "TButton",
        background=tema["botao"],
        foreground=tema["texto_botao"],
        font=("Segoe UI", 10, "bold"),
        padding=(10, 7),
        borderwidth=0
    )

    estilo.configure(
        "Status.TLabel",
        background=tema["fundo"],
        foreground=tema["texto_secundario"] if "texto_secundario" in tema else tema["destaque"],
        font=("Segoe UI", 9)
    )

    estilo.map(
        "TButton",
        background=[
            ("active", tema["botao_hover"]),
            ("pressed", tema["botao_press"])
        ],
        foreground=[
            ("active", tema["texto_botao"]),
            ("pressed", tema["texto_botao"])
        ]
    )

    estilo.configure(
        "TEntry",
        fieldbackground=tema["campo"],
        foreground=tema["texto"],
        padding=5,
        bordercolor=tema["borda"]
    )

    estilo.configure(
        "BuscaFoco.TEntry",
        fieldbackground=tema["campo"],
        foreground=tema["texto"],
        bordercolor=tema["destaque"],
        lightcolor=tema["destaque"],
        darkcolor=tema["destaque"],
        borderwidth=2,
        padding=5
    )

    estilo.configure(
        "Tema.TCombobox",
        fieldbackground=tema["campo"],
        background=tema["botao"],
        foreground=tema["texto"],
        arrowcolor=tema["destaque"],
        bordercolor=tema["borda"],
        lightcolor=tema["borda"],
        darkcolor=tema["borda"],
        padding=5
    )

    estilo.map(
        "Tema.TCombobox",

        fieldbackground=[
            ("readonly", tema["campo"])
        ],

        foreground=[
            ("readonly", tema["texto"])
        ],

        selectbackground=[
            ("readonly", tema["campo"])
        ],

        selectforeground=[
            ("readonly", tema["texto"])
        ]
    )


    estilo.configure(
        "Treeview",
        background=tema["card"],
        fieldbackground=tema["card"],
        foreground=tema["texto"],
        font=("Segoe UI", 10),
        rowheight=28,
        borderwidth=0
    )

    estilo.configure(
        "Treeview.Heading",
        background=tema["cabecalho"],
        foreground=tema["cabecalho_texto"],
        font=("Segoe UI", 10, "bold"),
        padding=7
    )

    estilo.map(
        "Treeview.Heading",
        background=[
            ("active", tema["cabecalho_hover"])
        ],
        foreground=[
            ("active", tema["cabecalho_texto"])
        ]
    )

    estilo.map(
        "Treeview",
        background=[
            ("selected", tema["selecao"])
        ],
        foreground=[
            ("selected", tema["texto_selecao"])
        ]
    )

    estilo.configure(
        "Titulo.TLabel",
        background=tema["fundo"],
        foreground=tema["titulo"],
        font=("Segoe UI", 22, "bold")
    )

    estilo.configure(
        "TemaAtual.TLabel",
        background=tema["fundo"],
        foreground=tema["destaque"],
        font=("Segoe UI", 9, "italic")
    )

    janela.option_add(
        "*TCombobox*Listbox.background",
        tema["card"]
    )

    janela.option_add(
        "*TCombobox*Listbox.foreground",
        tema["texto"]
    )

    janela.option_add(
        "*TCombobox*Listbox.selectBackground",
        tema["selecao"]
    )

    janela.option_add(
        "*TCombobox*Listbox.selectForeground",
        tema["texto_selecao"]
    )

    estilo.configure(
        "TemaMenor.TButton",
        background=tema["botao"],
        foreground=tema["texto_botao"],
        font=("Segoe UI", 9, "bold"),
        padding=(6, 3),
        borderwidth=0
    )

    estilo.map(
        "TemaMenor.TButton",
        background=[
            ("active", tema["botao_hover"]),
            ("pressed", tema["botao_press"])
        ],
        foreground=[
            ("active", tema["texto_botao"]),
            ("pressed", tema["texto_botao"])
        ]
    )


# -------------------- YATO - NORAGAMI --------------------

tema_yato = {
    "nome": "Five Yen",

    "fundo": "#0B0C12",
    "card": "#141720",
    "campo": "#222735",

    "botao": "#3F3752",
    "botao_hover": "#86697B",
    "botao_press": "#2A2438",

    "texto": "#F4F6F8",
    "texto_botao": "#E6F8EE",

    "destaque": "#8FDDF3",
    "borda": "#00AFEA",

    "cabecalho": "#2A2438",
    "cabecalho_hover": "#3F3752",
    "cabecalho_texto": "#8FDDF3",

    "selecao": "#00AFEA",
    "texto_selecao": "#0B0C12",

    "titulo": "#00AFEA"
}


# -------------------- KAGUYA SAMA --------------------

tema_kaguya = {
    "nome": "Student Council",

    "fundo": "#0A0C12",
    "card": "#15171D",
    "campo": "#23262E",

    "botao": "#A83245",
    "botao_hover": "#E56A7D",
    "botao_press": "#7E2433",

    "texto": "#F4F2F1",
    "texto_botao": "#F4F0E8",

    "destaque": "#E56A7D",
    "borda": "#641A26",

    "cabecalho": "#641A26",
    "cabecalho_hover": "#A83245",
    "cabecalho_texto": "#F4F0E8",

    "selecao": "#A83245",
    "texto_selecao": "#F4F0E8",

    "titulo": "#F4F0E8"
}


# -------------------- MITSURI - KIMETSU NO YAIBA --------------------

tema_mitsuri = {
    "nome": "Love Breathing",

    "fundo": "#101319",
    "card": "#1A1E27",
    "campo": "#252B36",

    "botao": "#F3A7C4",
    "botao_hover": "#FFD2E1",
    "botao_press": "#D97D9F",

    "texto": "#FFF8FB",
    "texto_botao": "#15171D",

    "destaque": "#C6E879",
    "borda": "#9FC94E",

    "cabecalho": "#725477",
    "cabecalho_hover": "#513B56",
    "cabecalho_texto": "#E3F7B6",

    "selecao": "#C6E879",
    "texto_selecao": "#15171D",

    "titulo": "#F3A7C4"
}


# -------------------- EVA-01 - EVANGELION --------------------

tema_eva01 = {
    "nome": "EVA-01",

    "fundo": "#090A0F",
    "card": "#13151D",
    "campo": "#20232E",

    "botao": "#5B3A8A",
    "botao_hover": "#3E285F",
    "botao_press": "#3E285F",

    "texto": "#F3F5F7",
    "texto_botao": "#FFFFFF",

    "destaque": "#86FF52",
    "borda": "#5FD132",

    "cabecalho": "#5B3A8A",
    "cabecalho_hover": "#3E285F",
    "cabecalho_texto": "#86FF52",

    "selecao": "#86FF52",
    "texto_selecao": "#090A0F",

    "titulo": "#86FF52"
}


# -------------------- ALUCARD - CASTLEVANIA --------------------

tema_alucard = {
    "nome": "Symphony at Midnight",

    "fundo": "#050404",
    "card": "#191715",
    "campo": "#322F2B",

    "botao": "#BE9263",
    "botao_hover": "#D1A777",
    "botao_press": "#8B6F52",

    "texto": "#EEE9E4",
    "texto_botao": "#15120F",

    "destaque": "#58787C",
    "borda": "#58787C",

    "cabecalho": "#354F4B",
    "cabecalho_hover": "#58787C",
    "cabecalho_texto": "#F1E9E2",

    "selecao": "#BE9263",
    "texto_selecao": "#15120F",

    "titulo": "#F1E9E2"
}


# -------------------- SAILOR MOON --------------------

tema_sailor_moon = {
    "nome": "Moon",

    "fundo": "#07152D",
    "card": "#102440",
    "campo": "#1B365C",

    "botao": "#E83F72",
    "botao_hover": "#FF789E",
    "botao_press": "#BC2D59",

    "texto": "#F8F8FC",
    "texto_botao": "#FFFDF8",

    "destaque": "#FF789E",
    "borda": "#D5AA1D",

    "cabecalho": "#174A8B",
    "cabecalho_hover": "#4C7FC0",
    "cabecalho_texto": "#FFE987",

    "selecao": "#E83F72",
    "texto_selecao": "#FFFDF8",

    "titulo": "#FFD83D"
}


# -------------------- RED DEAD REDEMPTION II --------------------

tema_red_dead = {
    "nome": "Dead Eye",

    "fundo": "#0A0908",
    "card": "#171310",
    "campo": "#282019",

    "botao": "#B62D24",
    "botao_hover": "#D94A3E",
    "botao_press": "#7F1F1A",

    "texto": "#F0E4CF",
    "texto_botao": "#F4E8CC",

    "destaque": "#E0BC7A",
    "borda": "#8E6A3C",

    "cabecalho": "#493020",
    "cabecalho_hover": "#6E4930",
    "cabecalho_texto": "#E0BC7A",

    "selecao": "#B62D24",
    "texto_selecao": "#F4E8CC",

    "titulo": "#D94A3E"
}


# -------------------- NOIR --------------------

tema_noir = {
    "nome": "Noir",

    "fundo": "#0B0C0E",
    "card": "#15171A",
    "campo": "#22252A",

    "botao": "#30343A",
    "botao_hover": "#454A52",
    "botao_press": "#1F2226",

    "texto": "#F2F2F2",
    "texto_botao": "#FFFFFF",

    "destaque": "#C9CDD2",
    "borda": "#555A61",

    "cabecalho": "#24272C",
    "cabecalho_hover": "#34383E",
    "cabecalho_texto": "#E6E8EB",

    "selecao": "#D9DCE0",
    "texto_selecao": "#111214",

    "titulo": "#F5F5F5"
}



temas = [
    tema_yato,
    tema_kaguya,
    tema_mitsuri,
    tema_eva01,
    tema_alucard,
    tema_sailor_moon,
    tema_red_dead,
    tema_noir
]


def salvar_tema(tema):

    try:
        with open("tema.txt", "w", encoding="utf-8") as arquivo:
            arquivo.write(tema["nome"])

        return True

    except OSError:
        return False


def carregar_tema_salvo(temas):

    try:
        with open("tema.txt", "r", encoding="utf-8") as arquivo:
            nome_tema = arquivo.read().strip()

        for tema in temas:

            if tema["nome"] == nome_tema:
                return tema

    except FileNotFoundError:
        pass

    except OSError:
        pass

    return None


tema_salvo = carregar_tema_salvo(temas)

if tema_salvo is None:
    tema_escolhido = random.choice(temas)

else:
    tema_escolhido = tema_salvo


aplicar_tema(tema_escolhido)


frame_principal = ttk.Frame(
    janela,
    padding=20
)

frame_principal.pack(
    fill="both",
    expand=True
)

titulo = ttk.Label(
    frame_principal,
    text="🎮 Games Manager",
    style="Titulo.TLabel"
)

titulo.pack(pady=(0, 3))


# -------------------- CONTROLE DE TEMAS --------------------


def trocar_tema(event=None):

    global tema_escolhido

    nome_tema = seletor_tema.get()

    for tema in temas:

        if tema["nome"] == nome_tema:

            tema_escolhido = tema

            aplicar_tema(tema_escolhido)

            salvar_tema(tema_escolhido)

            tema_atual.config(
                text="Tema atual: " + tema_escolhido["nome"]
            )

            break


def escolher_tema_aleatorio():

    global tema_escolhido

    tema_escolhido = random.choice(temas)

    aplicar_tema(tema_escolhido)

    salvar_tema(tema_escolhido)

    seletor_tema.set(
        tema_escolhido["nome"]
    )

    tema_atual.config(
        text="Tema atual: " + tema_escolhido["nome"]
    )


nomes_temas = []

for tema in temas:
    nomes_temas.append(
        tema["nome"]
    )


frame_tema = ttk.Frame(
    frame_principal
)

frame_tema.pack(
    pady=(0, 10)
)


tema_atual = ttk.Label(
    frame_tema,
    text="Tema atual: " + tema_escolhido["nome"],
    style="TemaAtual.TLabel"
)

tema_atual.grid(
    row=0,
    column=0,
    padx=(0, 10)
)


seletor_tema = ttk.Combobox(
    frame_tema,
    values=nomes_temas,
    state="readonly",
    width=20,
    style="Tema.TCombobox"
)

seletor_tema.set(
    tema_escolhido["nome"]
)

seletor_tema.grid(
    row=0,
    column=1,
    padx=5
)

seletor_tema.bind(
    "<<ComboboxSelected>>",
    trocar_tema
)


botao_tema_aleatorio = ttk.Button(
    frame_tema,
    text="🎲",
    command=escolher_tema_aleatorio,
    style="TemaMenor.TButton",
    width=3
)

botao_tema_aleatorio.grid(
    row=0,
    column=2,
    padx=(5, 0)
)

Tooltip(
    botao_tema_aleatorio,
    "Escolher um tema aleatório"
)



# Campos da interface

frame_dados = ttk.LabelFrame(
    frame_principal,
    text="Dados do jogo",
    padding=15
)

frame_dados.pack(
    fill="x",
    pady=(0, 15)
)

frame_acoes = ttk.Frame(
    frame_principal
)

frame_acoes.pack(
    fill="x",
    pady=(0, 15)
)

ttk.Label(
    frame_dados,
    text="Nome:"
).grid(
    row=0,
    column=0,
    padx=5,
    pady=5,
    sticky="w"
)

campo_nome = ttk.Entry(
    frame_dados,
    width=30
)

campo_nome.grid(
    row=0,
    column=1,
    padx=5,
    pady=5,
    sticky="ew"
)


ttk.Label(
    frame_dados,
    text="Gênero:"
).grid(
    row=0,
    column=2,
    padx=5,
    pady=5,
    sticky="w"
)

campo_genero = ttk.Entry(
    frame_dados,
    width=25
)

campo_genero.grid(
    row=0,
    column=3,
    padx=5,
    pady=5,
    sticky="ew"
)


ttk.Label(
    frame_dados,
    text="Plataforma:"
).grid(
    row=1,
    column=0,
    padx=5,
    pady=5,
    sticky="w"
)

campo_plataforma = ttk.Entry(
    frame_dados,
    width=30
)

campo_plataforma.grid(
    row=1,
    column=1,
    padx=5,
    pady=5,
    sticky="ew"
)


ttk.Label(
    frame_dados,
    text="Nota:"
).grid(
    row=1,
    column=2,
    padx=5,
    pady=5,
    sticky="w"
)

campo_nota = ttk.Entry(
    frame_dados,
    width=25
)

campo_nota.grid(
    row=1,
    column=3,
    padx=5,
    pady=5,
    sticky="ew"
)


frame_dados.columnconfigure(
    1,
    weight=1
)

frame_dados.columnconfigure(
    3,
    weight=1
)


frame_busca = ttk.LabelFrame(
    frame_principal,
    text="Pesquisar jogos",
    padding=15
)

frame_busca.pack(
    fill="x",
    pady=(0, 15)
)

frame_organizacao = ttk.LabelFrame(
    frame_principal,
    text="Organizar e analisar",
    padding=10
)

frame_organizacao.pack(
    fill="x",
    pady=(0, 15)
)


ttk.Label(
    frame_busca,
    text="Nome:"
).grid(
    row=0,
    column=0,
    padx=5,
    pady=5,
    sticky="w"
)

campo_busca = ttk.Entry(
    frame_busca,
    width=25
)

campo_busca.grid(
    row=0,
    column=1,
    padx=5,
    pady=5,
    sticky="ew"
)


ttk.Label(
    frame_busca,
    text="Gênero:"
).grid(
    row=0,
    column=2,
    padx=5,
    pady=5,
    sticky="w"
)

campo_busca_genero = ttk.Entry(
    frame_busca,
    width=20
)

campo_busca_genero.grid(
    row=0,
    column=3,
    padx=5,
    pady=5,
    sticky="ew"
)


ttk.Label(
    frame_busca,
    text="Plataforma:"
).grid(
    row=1,
    column=0,
    padx=5,
    pady=5,
    sticky="w"
)

campo_busca_plataforma = ttk.Entry(
    frame_busca,
    width=25
)

campo_busca_plataforma.grid(
    row=1,
    column=1,
    padx=5,
    pady=5,
    sticky="ew"
)


frame_busca.columnconfigure(
    1,
    weight=1
)

frame_busca.columnconfigure(
    3,
    weight=1
)


# Funções da interface


def focar_busca():

    campo_busca.configure(
        style="BuscaFoco.TEntry"
    )

    campo_busca.focus_set()

    janela.after(
        1000,
        lambda: campo_busca.configure(
            style="TEntry"
        )
    )


def abrir_para_edicao(event):

    carregar_jogo_selecionado(event)

    campo_nome.focus_set()



def limpar_campos():

    campo_nome.delete(0, tk.END)
    campo_genero.delete(0, tk.END)
    campo_plataforma.delete(0, tk.END)
    campo_nota.delete(0, tk.END)


def limpar_selecao_lista():

    selecionados = lista_jogos.selection()

    if selecionados:
        lista_jogos.selection_remove(
            *selecionados
        )


def limpar_formulario():

    global nome_selecionado

    nome_selecionado = None

    limpar_campos()
    limpar_selecao_lista()

    botao_favoritar.config(
        text="☆ Favoritar"
    )


def obter_indice_selecionado():

    selecionados = lista_jogos.selection()

    if not selecionados:
        return None

    item = selecionados[0]

    indice = lista_jogos.index(item)

    return indice


status_label = ttk.Label(
    frame_principal,
    text="",
    style="Status.TLabel"
)

status_label.pack(
    pady=(3, 0)
)

def atualizar_lista(lista=None):

    global jogos_exibidos
    global nome_selecionado

    nome_selecionado = None

    if lista is None:
        jogos_exibidos = jogos.copy()

    else:
        jogos_exibidos = lista.copy()


    for item in lista_jogos.get_children():
        lista_jogos.delete(item)


    for jogo in jogos_exibidos:

        if jogo.get("Favorito", False):
            simbolo_favorito = "★"
            tag_jogo = ("favorito",)
        else:
            simbolo_favorito = "☆"
            tag_jogo = ()


        lista_jogos.insert(
            "",
            tk.END,
            values=(
                simbolo_favorito,
                jogo["Nome"],
                jogo["Genero"],
                jogo["Plataforma"],
                jogo["Nota"]

            ),
            tags=tag_jogo

        )

    atualizar_status()

def carregar_jogo_selecionado(event):

    global nome_selecionado

    indice = obter_indice_selecionado()

    if indice is None:
        return

    jogo = jogos_exibidos[indice]

    nome_selecionado = jogo["Nome"]

    limpar_campos()

    campo_nome.insert(0, jogo["Nome"])
    campo_genero.insert(0, jogo["Genero"])
    campo_plataforma.insert(0, jogo["Plataforma"])
    campo_nota.insert(0, str(jogo["Nota"]))

    atualizar_botao_favorito()


def adicionar_pela_interface():

    copia_jogos = copy.deepcopy(jogos)

    nome = campo_nome.get()
    genero = campo_genero.get()
    plataforma = campo_plataforma.get()
    nota = campo_nota.get()

    adicionado = adicionar_jogo(
        jogos,
        nome,
        genero,
        plataforma,
        nota
    )

    if adicionado:

        if salvar_jogos(jogos):

            atualizar_lista()

            messagebox.showinfo(
                "Sucesso",
                "Jogo adicionado com sucesso!"
            )

            limpar_campos()

        else:

            jogos.clear()
            jogos.extend(copia_jogos)
            atualizar_lista()

            messagebox.showerror(
                "Erro",
                "Não foi possível salvar o jogo no arquivo."
            )

    else:
        messagebox.showerror(
            "Erro",
            "Não foi possível adicionar o jogo!"
        )


def editar_pela_interface():

    global nome_selecionado

    if nome_selecionado is None:
        messagebox.showwarning(
            "Atenção",
            "Selecione um jogo para editar!"
        )
        return

    copia_jogos = copy.deepcopy(jogos)

    novo_nome = campo_nome.get()
    novo_genero = campo_genero.get()
    nova_plataforma = campo_plataforma.get()
    nova_nota = campo_nota.get()

    jogo_atual = buscar_jogo(
        jogos,
        nome_selecionado
    )

    if jogo_atual is None:
        return

    nome_comparacao = novo_nome.strip().upper()
    genero_comparacao = novo_genero.strip().upper()
    plataforma_comparacao = nova_plataforma.strip().upper()

    if nome_comparacao == "":
        nome_comparacao = jogo_atual["Nome"]

    if genero_comparacao == "":
        genero_comparacao = jogo_atual["Genero"]

    if plataforma_comparacao == "":
        plataforma_comparacao = jogo_atual["Plataforma"]

    if nova_nota.strip() == "":
        nota_comparacao = jogo_atual["Nota"]

    else:
        try:
            nota_comparacao = float(nova_nota)
        except ValueError:
            nota_comparacao = None

    if (
            nome_comparacao == jogo_atual["Nome"]
            and genero_comparacao == jogo_atual["Genero"]
            and plataforma_comparacao == jogo_atual["Plataforma"]
            and nota_comparacao == jogo_atual["Nota"]
    ):
        messagebox.showinfo(
            "Edição",
            "Nenhuma alteração foi feita."
        )
        return

    confirmar = messagebox.askyesno(
        "Confirmar edição",
        "Deseja salvar as alterações em "
        + jogo_atual["Nome"]
        + "?"
    )

    if not confirmar:
        return

    editado = editar_jogo(

        jogos,
        nome_selecionado,
        novo_nome,
        novo_genero,
        nova_plataforma,
        nova_nota
    )

    if editado:

        if salvar_jogos(jogos):


            atualizar_lista()

            messagebox.showinfo(
                "Sucesso",
                "Jogo editado com sucesso!"
            )

            nome_selecionado = None
            limpar_campos()
            limpar_selecao_lista()

        else:

            jogos.clear()
            jogos.extend(copia_jogos)
            atualizar_lista()

            messagebox.showerror(
                "Erro",
                "Não foi possível salvar a edição."
            )

    else:
        messagebox.showerror(
            "Erro",
            "Não foi possível editar o jogo!"
        )


def remover_pela_interface():

    global nome_selecionado

    indice = obter_indice_selecionado()

    if indice is None:
        messagebox.showwarning(
            "Atenção",
            "Selecione um jogo para remover!"
        )
        return



    nome = jogos_exibidos[indice]["Nome"]

    confirmar = messagebox.askyesno(
        "Confirmar remoção",
        "Deseja realmente remover " + nome + "?"
    )

    if not confirmar:
        return

    copia_jogos = copy.deepcopy(jogos)

    removido = remover_jogo(jogos, nome)

    if removido:

        if salvar_jogos(jogos):


            atualizar_lista()

            nome_selecionado = None
            limpar_campos()
            limpar_selecao_lista()

            messagebox.showinfo(
                "Sucesso",
                "Jogo removido com sucesso!"
            )

        else:

            jogos.clear()
            jogos.extend(copia_jogos)
            atualizar_lista()

            messagebox.showerror(
                "Erro",
                "Não foi possível salvar a remoção."
            )


def favoritar_pela_interface():

    indice = obter_indice_selecionado()

    if indice is None:
        messagebox.showwarning(
            "Nenhum jogo selecionado",
            "Selecione um jogo para favoritar ou desfavoritar."
        )
        return

    jogo = jogos_exibidos[indice]

    estado_anterior = jogo.get("Favorito", False)

    jogo["Favorito"] = not estado_anterior

    if not salvar_jogos(jogos):

        jogo["Favorito"] = estado_anterior

        messagebox.showerror(
            "Erro",
            "Não foi possível salvar os favoritos."
        )

        return

    atualizar_lista(jogos_exibidos)

    atualizar_botao_favorito()


def mostrar_favoritos():

    favoritos = []

    for jogo in jogos:

        if jogo.get("Favorito", False):
            favoritos.append(jogo)

    if not favoritos:
        messagebox.showinfo(
            "Favoritos",
            "Você ainda não favoritou nenhum jogo!"
        )
        return

    atualizar_lista(favoritos)

    atualizar_status(
        "Mostrando favoritos"
    )


def atualizar_botao_favorito():

    indice = obter_indice_selecionado()

    if indice is None:
        botao_favoritar.config(
            text="☆ Favoritar"
        )
        return

    jogo = jogos_exibidos[indice]

    if jogo.get("Favorito", False):
        botao_favoritar.config(
            text="★ Desfavoritar"
        )
    else:
        botao_favoritar.config(
            text="☆ Favoritar"
        )


def buscar_pela_interface():

    trecho = campo_busca.get()

    if trecho.strip() == "":
        atualizar_lista()
        return

    resultados = buscar_nome_parcial(jogos, trecho)

    if not resultados:
        messagebox.showinfo(
            "Busca",
            "Nenhum jogo encontrado!"
        )
        return

    atualizar_lista(resultados)

    atualizar_status(
        str(len(resultados)) + " resultados encontrados"
    )


def buscar_genero_pela_interface():

    genero = campo_busca_genero.get()

    if genero.strip() == "":
        atualizar_lista()
        return

    resultados = buscar_por_campo(
        jogos,
        "Genero",
        genero
    )

    if not resultados:
        messagebox.showinfo(
            "Busca",
            "Nenhum jogo encontrado com esse gênero!"
        )
        return

    atualizar_lista(resultados)

    atualizar_status(
        str(len(resultados)) + " resultados encontrados"
    )


def buscar_plataforma_pela_interface():

    plataforma = campo_busca_plataforma.get()

    if plataforma.strip() == "":
        atualizar_lista()
        return

    resultados = buscar_por_campo(
        jogos,
        "Plataforma",
        plataforma
    )

    if not resultados:
        messagebox.showinfo(
            "Busca",
            "Nenhum jogo encontrado nessa plataforma!"
        )
        return

    atualizar_lista(resultados)

    atualizar_status(
        str(len(resultados)) + " resultados encontrados"
    )


def mostrar_todos():

    campo_busca.delete(0, tk.END)
    campo_busca_genero.delete(0, tk.END)
    campo_busca_plataforma.delete(0, tk.END)

    atualizar_lista()


def ordenar_alfabeticamente():

    jogos_ordenados = ordenar_jogos(
        jogos,
        "NOME"
    )

    atualizar_lista(jogos_ordenados)


def ordenar_maior_nota():

    jogos_ordenados = ordenar_jogos(
        jogos,
        "NOTA",
        "MAIOR"
    )

    atualizar_lista(jogos_ordenados)


def ordenar_menor_nota():

    jogos_ordenados = ordenar_jogos(
        jogos,
        "NOTA",
        "MENOR"
    )

    atualizar_lista(jogos_ordenados)


def mostrar_estatisticas():

    quantidade = quantidade_jogos(jogos)
    media = media_notas(jogos)
    melhor = buscar_por_nota(jogos, "MAIOR")
    pior = buscar_por_nota(jogos, "MENOR")

    if quantidade == 0:
        messagebox.showinfo(
            "Estatísticas",
            "Ainda não há jogos cadastrados!"
        )
        return

    texto = (
        "Quantidade de jogos: " + str(quantidade) +
        "\nMédia das notas: " + str(round(media, 2)) +
        "\nMelhor jogo: " + melhor["Nome"] +
        " - Nota " + str(melhor["Nota"]) +
        "\nPior jogo: " + pior["Nome"] +
        " - Nota " + str(pior["Nota"])
    )

    messagebox.showinfo(
        "Estatísticas",
        texto
    )

#Ordenar clicando no cabeçalho

ordem_nota_cabecalho = "MAIOR"


def ordenar_nome_pelo_cabecalho():

    ordenar_alfabeticamente()

    lista_jogos.heading(
        "nome",
        text="Nome ▲"
    )

    lista_jogos.heading(
        "nota",
        text="Nota"
    )


def ordenar_nota_pelo_cabecalho():

    global ordem_nota_cabecalho

    if ordem_nota_cabecalho == "MAIOR":

        ordenar_maior_nota()

        lista_jogos.heading(
            "nota",
            text="Nota ▼"
        )

        ordem_nota_cabecalho = "MENOR"

    else:

        ordenar_menor_nota()

        lista_jogos.heading(
            "nota",
            text="Nota ▲"
        )

        ordem_nota_cabecalho = "MAIOR"

    lista_jogos.heading(
        "nome",
        text="Nome"
    )



def atualizar_status(mensagem=None):

    favoritos = 0

    for jogo in jogos:
        if jogo.get("Favorito", False):
            favoritos += 1

    if mensagem is None:

        status_label.config(
            text=str(len(jogos)) + " jogos • " +
                 str(favoritos) + " favoritos"
        )

    else:

        status_label.config(
            text=mensagem + " • " +
                 str(favoritos) + " favoritos"
        )


# Elementos que usam as funções


frame_lista = ttk.LabelFrame(
    frame_principal,
    text="Jogos cadastrados",
    padding=10
)

frame_lista.pack(
    fill="both",
    expand=True,
    pady=(0, 15)
)

colunas = ("favorito", "nome", "genero", "plataforma", "nota")

lista_jogos = ttk.Treeview(
    frame_lista,
    columns=colunas,
    show="headings",
    height=10
)

lista_jogos.tag_configure(
    "favorito",
    font=("Segoe UI", 10, "bold")
)

lista_jogos.heading(
    "favorito",
    text="★",
    anchor="center")

lista_jogos.heading(
    "nome",
    text="Nome",
    command=ordenar_nome_pelo_cabecalho
)

lista_jogos.heading(
    "genero",
    text="Gênero"
)

lista_jogos.heading(
    "plataforma",
    text="Plataforma"
)

lista_jogos.heading(
    "nota",
    text="Nota",
    anchor="center",
    command=ordenar_nota_pelo_cabecalho
)

lista_jogos.column(
    "favorito",
    width=55,
    minwidth=55,
    anchor="center",
    stretch=False
)

lista_jogos.column(
    "nome",
    width=260,
    minwidth=180,
    anchor="w"
)

lista_jogos.column(
    "genero",
    width=180,
    minwidth=120,
    anchor="w"
)

lista_jogos.column(
    "plataforma",
    width=180,
    minwidth=120,
    anchor="w"
)

lista_jogos.column(
    "nota",
    width=80,
    minwidth=60,
    anchor="center",
    stretch=False
)

scroll_lista = ttk.Scrollbar(
    frame_lista,
    orient="vertical",
    command=lista_jogos.yview
)

lista_jogos.configure(
    yscrollcommand=scroll_lista.set
)

lista_jogos.grid(
    row=0,
    column=0,
    sticky="nsew"
)

scroll_lista.grid(
    row=0,
    column=1,
    sticky="ns"
)

frame_lista.columnconfigure(
    0,
    weight=1
)

frame_lista.rowconfigure(
    0,
    weight=1
)

lista_jogos.bind(
    "<<TreeviewSelect>>",
    carregar_jogo_selecionado
)

lista_jogos.bind(
    "<Delete>",
    lambda event: remover_pela_interface()
)

lista_jogos.bind(
    "<Double-1>",
    abrir_para_edicao
)

botao_adicionar = ttk.Button(
    frame_acoes,
    text="Adicionar jogo",
    command=adicionar_pela_interface
)


botao_editar = ttk.Button(
    frame_acoes,
    text="Editar jogo",
    command=editar_pela_interface
)


botao_remover = ttk.Button(
    frame_acoes,
    text="Remover jogo",
    command=remover_pela_interface
)


botao_limpar = ttk.Button(
    frame_acoes,
    text="Limpar campos",
    command=limpar_formulario
)


botao_favoritar = ttk.Button(
    frame_acoes,
    text="☆ Favoritar",
    command=favoritar_pela_interface
)

botao_favoritar.grid(
    row=0,
    column=4,
    padx=5,
    sticky="ew"
)

Tooltip(
    botao_favoritar,
    "Adicionar ou remover o jogo dos favoritos"
)


botao_adicionar.grid(
    row=0,
    column=0,
    padx=5,
    sticky="ew"
)


botao_editar.grid(
    row=0,
    column=1,
    padx=5,
    sticky="ew"
)


botao_remover.grid(
    row=0,
    column=2,
    padx=5,
    sticky="ew"
)


botao_limpar.grid(
    row=0,
    column=3,
    padx=5,
    sticky="ew"
)



for coluna in range(5):
    frame_acoes.columnconfigure(
        coluna,
        weight=1
    )


botao_buscar = ttk.Button(
    frame_busca,
    text="Buscar nome",
    command=buscar_pela_interface
)


botao_buscar_genero = ttk.Button(
    frame_busca,
    text="Buscar gênero",
    command=buscar_genero_pela_interface
)


botao_buscar_plataforma = ttk.Button(
    frame_busca,
    text="Buscar plataforma",
    command=buscar_plataforma_pela_interface
)


botao_mostrar_todos = ttk.Button(
    frame_busca,
    text="Mostrar todos",
    command=mostrar_todos
)


botao_favoritos = ttk.Button(
    frame_busca,
    text="★ Mostrar favoritos",
    command=mostrar_favoritos
)


botao_buscar.grid(
    row=2,
    column=0,
    padx=5,
    pady=(10, 5)
)


botao_buscar_genero.grid(
    row=2,
    column=1,
    padx=5,
    pady=(10, 5)
)


botao_buscar_plataforma.grid(
    row=2,
    column=2,
    padx=5,
    pady=(10, 5)
)


botao_mostrar_todos.grid(
    row=2,
    column=3,
    padx=5,
    pady=(10, 5)
)


botao_favoritos.grid(
    row=3,
    column=0,
    columnspan=4,
    padx=5,
    pady=(5, 0),
    sticky="ew"
)


botao_ordenar_nome = ttk.Button(
    frame_organizacao,
    text="Ordenar A-Z",
    command=ordenar_alfabeticamente
)


botao_maior_nota = ttk.Button(
    frame_organizacao,
    text="Maior nota",
    command=ordenar_maior_nota
)


botao_menor_nota = ttk.Button(
    frame_organizacao,
    text="Menor nota",
    command=ordenar_menor_nota
)


botao_estatisticas = ttk.Button(
    frame_organizacao,
    text="Ver estatísticas",
    command=mostrar_estatisticas
)

botao_estatisticas.grid(
    row=0,
    column=3,
    padx=5,
    sticky="ew"
)

Tooltip(
    botao_estatisticas,
    "Ver resumo e estatísticas dos jogos cadastrados"
)

botao_ordenar_nome.grid(
    row=0,
    column=0,
    padx=5,
    sticky="ew"
)


botao_maior_nota.grid(
    row=0,
    column=1,
    padx=5,
    sticky="ew"
)


botao_menor_nota.grid(
    row=0,
    column=2,
    padx=5,
    sticky="ew"
)

botao_limpar_busca = ttk.Button(
    frame_busca,
    text="✕",
    command=mostrar_todos,
    style="TemaMenor.TButton",
    width=3
)

botao_limpar_busca.grid(
    row=1,
    column=3,
    padx=5,
    pady=5,
    sticky="e"
)

Tooltip(
    botao_limpar_busca,
    "Limpar buscas e mostrar todos os jogos"
)


for coluna in range(4):
    frame_organizacao.columnconfigure(
        coluna,
        weight=1
    )


# -------------------- ATALHOS DE TECLADO --------------------

janela.bind(
    "<Control-f>",
    lambda event: focar_busca()
)

janela.bind(
    "<Control-n>",
    lambda event: limpar_formulario()
)

janela.bind(
    "<Control-s>",
    lambda event: editar_pela_interface()
)

campo_busca.bind(
    "<Return>",
    lambda event: buscar_pela_interface()
)

campo_busca_genero.bind(
    "<Return>",
    lambda event: buscar_genero_pela_interface()
)

campo_busca_plataforma.bind(
    "<Return>",
    lambda event: buscar_plataforma_pela_interface()
)

janela.bind(
    "<Escape>",
    lambda event: mostrar_todos()
)

atualizar_lista()


janela.mainloop()