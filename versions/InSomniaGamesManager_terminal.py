######################### PROJETO APENAS TERMINAL, SEM INTERFACE ################################



import copy

def pedir_texto(mensagem):

    while True:
        texto = input(mensagem).strip().upper()

        if texto == "":
            print("O campo não pode estar vazio!")
            continue

        if "|" in texto:
            print("O caractere | não é permitido!")
            continue

        return texto


def pedir_texto_opcional(mensagem, valor_atual):

    while True:
        texto = input(mensagem).strip().upper()

        if texto == "":
            return valor_atual

        if "|" in texto:
            print("O caractere | não é permitido!")
            continue

        return texto



def pedir_nota():

    while True:
        try:
            nota = float(input("Digite a nota do jogo: "))

            if 0 <= nota <= 10:
                return nota

            print("A nota precisa estar entre 0 e 10!")

        except ValueError:
            print("Digite uma nota válida!")




def pedir_nova_nota(nota_atual):

    while True:
        entrada = input("Nova nota (Enter para manter nota atual): ").strip()

        if entrada == "":
            return nota_atual

        try:
            nota = float(entrada)

            if 0 <= nota <= 10:
                return nota

            print("A nota precisa estar entre 0 e 10!")

        except ValueError:
            print("Digite uma nota válida!")


def pedir_opcao(mensagem, opcoes):

    while True:
        resposta = input(mensagem).strip().upper()

        if resposta in opcoes:
            return resposta

        print("Opção inválida! Escolha entre:", ", ".join(opcoes))



def confirmar(mensagem):

    resposta = pedir_opcao(mensagem, ["S", "N"])

    if resposta == "S":
        return True

    return False


def buscar_jogo(jogos, nome):

    for jogo in jogos:
        if jogo["Nome"].upper() == nome.upper():
            return jogo

    return None


def buscar_por_campo(jogos, campo, valor):
    resultados = []

    for jogo in jogos:

        if campo == "Genero":
            generos = jogo["Genero"].split(",")

            for genero in generos:
                if genero.strip().upper() == valor.strip().upper():
                    resultados.append(jogo)
                    break

        elif jogo[campo].strip().upper() == valor.strip().upper():
            resultados.append(jogo)

    return resultados




def buscar_nome_parcial(jogos, trecho):
    resultados = []

    trecho = trecho.strip().upper()

    if trecho == "":
        return resultados

    for jogo in jogos:
        if trecho in jogo["Nome"].upper():
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

    if len(dados) != 4:
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

    if buscar_jogo(jogos, nome) is not None:
        print("Jogo duplicado ignorado:", nome)
        return None

    jogo = {
        "Nome": nome,
        "Genero": genero,
        "Plataforma": plataforma,
        "Nota": nota
    }

    return jogo


def carregar_jogos():

    jogos = []

    try:
        with open("jogo.txt", "r") as arquivo:

            for linha in arquivo:
                jogo = transformar_linha_em_jogo(linha, jogos)

                if jogo is not None:
                    jogos.append(jogo)

    except FileNotFoundError:
        print("jogo.txt ainda não existe")

    return jogos

#Fazendo a função contrária (Transformando o dicionário em linhas de novo)



def salvar_jogos(jogos):


    try:
        with open("jogo.txt", "w") as arquivo:
            for jogo in jogos:
                arquivo.write(
                    jogo["Nome"] + "|" +
                    jogo["Genero"] + "|" +
                    jogo["Plataforma"] + "|" +
                    str(jogo["Nota"]) + "\n"
                )

        return True

    except OSError:
        print("Não foi possível salvar os jogos no arquivo!")
        return False



def adicionar_jogo(jogos):

    while True:
        nome = input("Digite o nome do jogo: ").strip().upper()
        print("\n")

        if nome == "":
            print("O campo nome não pode estar vazio!\n")
            continue

        if "|" in nome:
            print("O caractere | não é permitido!\n")
            continue

        jogo_existente = buscar_jogo(jogos, nome)

        if jogo_existente is not None:
            print("Jogo já cadastrado, informe outro\n")
            continue

        break

    genero = pedir_texto("Digite o gênero do jogo: ")
    plataforma = pedir_texto("Digite a plataforma do jogo: ")
    nota = pedir_nota()

    jogo = {
        "Nome": nome,
        "Genero": genero,
        "Plataforma": plataforma,
        "Nota": nota
    }

    jogos.append(jogo)

    return True



def mostrar_jogo(jogo):

    print("Nome: ", jogo["Nome"])
    print("Genero: ", jogo["Genero"])
    print("Plataforma: ", jogo["Plataforma"])
    print("Nota: ", jogo["Nota"])
    print("----------------------------------")


def listar_jogos(jogos):

    if not jogos:
        print("Ainda não há jogos nessa lista!")
    else:
        for jogo in jogos:
            mostrar_jogo(jogo)


def remover_jogo(jogos):

    nome = input("Digite o nome do jogo que deseja remover: ")

    jogo = buscar_jogo(jogos, nome)

    if jogo is None:
        print("Não encontrado!")
        return False

    if not confirmar("Deseja mesmo remover esse jogo? [S/N] "):
        print("Remoção cancelada!")
        return False

    jogos.remove(jogo)
    return True



def editar_jogo(jogos):

    nome = input("Digite o nome do jogo que deseja editar: ")

    jogo = buscar_jogo(jogos, nome)

    if jogo is None:
        print("Jogo não encontrado!")
        return False

    if not confirmar("Deseja mesmo editar esse jogo? [S/N] "):
        print("Edição cancelada!")
        return False

    while True:
        novo_nome = input("Novo Nome (Enter para manter nome atual): ").strip().upper()

        if novo_nome == "":
            novo_nome = jogo["Nome"]
            break

        if "|" in novo_nome:
            print("O caractere | não é permitido!")
            continue

        jogo_existente = buscar_jogo(jogos, novo_nome)

        if jogo_existente is not None and jogo_existente != jogo:
            print("Já existe um jogo com esse nome. Digite outro!")
            continue

        break

    novo_genero = pedir_texto_opcional(
        "Novo gênero (Enter para manter gênero atual): ",
        jogo["Genero"]
    )

    nova_plataforma = pedir_texto_opcional(
        "Nova plataforma (Enter para manter plataforma atual): ",
        jogo["Plataforma"]
    )

    nova_nota = pedir_nova_nota(jogo["Nota"])

    if (
            novo_nome == jogo["Nome"]
            and novo_genero == jogo["Genero"]
            and nova_plataforma == jogo["Plataforma"]
            and nova_nota == jogo["Nota"]
        ):

        print("Nenhuma alteração foi feita!")
        return False

    jogo["Nome"] = novo_nome
    jogo["Genero"] = novo_genero
    jogo["Plataforma"] = nova_plataforma
    jogo["Nota"] = nova_nota

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


def mostrar_menu(nome_user):

    print("\n--- OLÁAAA,", nome_user.upper(), "BEM VINDOOOO, O QUE DESEJA FAZER? ---")
    print("1 - Adicionar jogo")
    print("2 - Listar jogos")
    print("3 - Visualizar quantidade de jogos")
    print("4 - Organizar em ordem alfabetica")
    print("5 - Ordenar por nota")
    print("6 - Buscar jogo")
    print("7 - Editar jogo")
    print("8 - Remover jogo")
    print("9 - Buscar por genero")
    print("10 - Buscar por plataforma")
    print("11 - Buscar melhor jogo")
    print("12 - Buscar pior jogo")
    print("13 - Média de notas")
    print("14 - Sair")



def executar_menu(jogos, nome_user):


    while True:
        mostrar_menu(nome_user)

        print("\n")
        opcao = pedir_opcao(
            "Me diz o que você quer fazer: \n",
            ["1", "2", "3", "4", "5", "6", "7",
             "8", "9", "10", "11", "12", "13", "14"]
        )

        if opcao == "1":

            copia_jogos = copy.deepcopy(jogos)

            adicionado = adicionar_jogo(jogos)

            if adicionado:

                if salvar_jogos(jogos):

                    print("Jogo adicionado com sucesso!")


                else:
                    jogos.clear()
                    jogos.extend(copia_jogos)

                    print("Não foi possível salvar. A adição foi desfeita.")



        elif opcao == "2":

            listar_jogos(jogos)


        elif opcao == "3":

            quantidade = quantidade_jogos(jogos)

            print("Quantidade de jogos cadastrados: ", quantidade)


        elif opcao == "4":

            jogos_ordenados = ordenar_jogos(jogos, "NOME")

            listar_jogos(jogos_ordenados)


        elif opcao == "5":

            ordem = pedir_opcao(
                "Deseja ordenar partindo da maior ou menor nota? ",
                ["MAIOR", "MENOR"]
            )

            jogos_ordenados = ordenar_jogos(jogos, "NOTA", ordem)

            listar_jogos(jogos_ordenados)


        elif opcao == "6":

            trecho = input("Digite parte do nome do jogo: ")

            resultados = buscar_nome_parcial(jogos, trecho)

            if not resultados:

                print("Nenhum jogo encontrado!")

            else:

                print("Jogos encontrados:")
                listar_jogos(resultados)


        elif opcao == "7":

            copia_jogos = copy.deepcopy(jogos)
            editado = editar_jogo(jogos)

            if editado:

                if salvar_jogos(jogos):

                    print("Alterações salvas no arquivo com sucesso!")

                else:

                    jogos.clear()
                    jogos.extend(copia_jogos)

                    print("Não foi possível salvar. A edição foi desfeita.")


        elif opcao == "8":

            copia_jogos = copy.deepcopy(jogos)
            removido = remover_jogo(jogos)

            if removido:

                if salvar_jogos(jogos):

                    print("Alterações salvas no arquivo com sucesso!")

                else:

                    jogos.clear()
                    jogos.extend(copia_jogos)

                    print("Não foi possível salvar. A remoção foi desfeita.")

        elif opcao == "9":

            genero_busca = pedir_texto("\nDigite o gênero: ")

            resultado = buscar_por_campo(jogos, "Genero", genero_busca)

            if not resultado:

                print("Não localizei nenhum jogo desse gênero\n")

            else:

                print("Segue abaixo todos os jogos deste gênero:\n")
                listar_jogos(resultado)


        elif opcao == "10":

            plataforma_busca = pedir_texto("Digite a plataforma: ")

            resultado = buscar_por_campo(jogos, "Plataforma", plataforma_busca)

            if not resultado:

                print("Não localizei nenhum jogo dessa plataforma")

            else:

                print("Segue abaixo todos os jogos desta plataforma")
                listar_jogos(resultado)


        elif opcao == "11":

            resultado = buscar_por_nota(jogos, "MAIOR")

            if resultado is None:
                print("Não há jogos aqui")

            else:
                print("Melhor jogo: ")

                mostrar_jogo(resultado)


        elif opcao == "12":

            resultado = buscar_por_nota(jogos, "MENOR")

            if resultado is None:
                print("Não há jogos aqui")

            else:
                print("Pior jogo: ")

                mostrar_jogo(resultado)


        elif opcao == "13":

            resultado = media_notas(jogos)

            if resultado is None:
                print("Não há notas ainda")

            else:
                print("Média das notas: ", round(resultado, 2)) # <---------------- arredonda o resultado

        elif opcao == "14":
            print("Programa encerrado!")

            break


# Gerenciador pobre, não é a versão final pell amor de deus

jogos = carregar_jogos()

nome_user = input("Me diz seu nome :P : ")

executar_menu(jogos, nome_user)