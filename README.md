# 🎮 InSomnia Games Manager

Aplicação desktop desenvolvida em **Python com Tkinter** para organizar e gerenciar uma coleção pessoal de jogos.

O projeto permite cadastrar jogos, editar informações, pesquisar, ordenar, favoritar e acompanhar estatísticas da coleção através de uma interface gráfica com diferentes temas visuais.

## 🖼️ Interface

![Interface do InSomnia Games Manager](screenshots/interface1.png)
![Interface do InSomnia Games Manager](screenshots/interface3.png)
![Interface do InSomnia Games Manager](screenshots/interface4.png)

## ✨ Funcionalidades

- ➕ Adicionar novos jogos
- ✏️ Editar jogos cadastrados
- 🗑️ Remover jogos
- ⭐ Adicionar e remover jogos dos favoritos
- 🔎 Pesquisar jogos por:
  - Nome
  - Gênero
  - Plataforma
- 📊 Visualizar estatísticas da coleção
- 🔤 Ordenar jogos alfabeticamente
- 🔢 Ordenar por maior ou menor nota
- 🖱️ Ordenar clicando diretamente nos cabeçalhos da tabela
- ⭐ Destacar visualmente os jogos favoritos
- 💾 Salvar os jogos localmente
- 🎨 Escolher entre diferentes temas visuais
- 🎲 Selecionar um tema aleatório
- 💡 Tooltips explicativos em alguns botões
- ⌨️ Atalhos de teclado
- 🖱️ Duplo clique para carregar rapidamente um jogo para edição

## 🎨 Temas disponíveis

O programa possui vários temas personalizados:

- Five Yen
- Student Council
- Love Breathing
- EVA-01
- Symphony at Midnight
- Moon
- Dead Eye
- Noir

O último tema utilizado é salvo localmente no computador.

## ⌨️ Atalhos

| Atalho | Função |
|---|---|
| `Ctrl + N` | Limpar formulário |
| `Ctrl + F` | Focar no campo de busca por nome |
| `Ctrl + S` | Salvar/confirmar edição |
| `Delete` | Remover o jogo selecionado |
| `Enter` | Executar a busca no campo selecionado |
| `Esc` | Limpar buscas e mostrar todos os jogos |
| Duplo clique | Carregar o jogo selecionado para edição |

## 💾 Armazenamento

Os dados são armazenados localmente em arquivos `.txt`.

O arquivo `jogo.txt` guarda os jogos cadastrados e o arquivo `tema.txt` guarda a preferência de tema.

Esses arquivos são criados e atualizados pelo próprio programa e não fazem parte do repositório.

## 🛠️ Tecnologias utilizadas

- Python
- Tkinter
- ttk
- Manipulação de arquivos TXT
- Git e GitHub

## ▶️ Como executar

1. Tenha o **Python 3** instalado no computador.
2. Clone ou baixe este repositório.
3. Abra a pasta do projeto.
4. Execute:

```bash
python InSomniaGamesManager.py
```

Também é possível abrir o arquivo diretamente através de uma IDE como o PyCharm.

## 📁 Estrutura do projeto

```text
Insonmia-Games-Manager/
│
├── InSomniaGamesManager.py
├── README.md
└── .gitignore
```

Durante o uso, o programa também pode criar:

```text
jogo.txt
tema.txt
```

Esses arquivos são locais e estão configurados no `.gitignore`.

## 📚 Sobre o projeto

O InSomnia Games Manager foi desenvolvido como um projeto de estudo em Python.

Durante o desenvolvimento foram praticados conceitos como:

- Variáveis e tipos de dados
- Condicionais
- Laços de repetição
- Listas e dicionários
- Funções
- Tratamento de erros
- Manipulação de arquivos
- Interface gráfica com Tkinter
- Eventos de teclado e mouse
- Organização de dados
- Persistência local
- Git e GitHub

O projeto começou como um gerenciador executado pelo terminal e evoluiu para uma aplicação desktop completa com interface gráfica.

## 🕹️ Evolução do projeto

O **InSomnia Games Manager** começou como um projeto executado inteiramente pelo terminal.

Na primeira versão, toda a interação era feita através de menus numéricos e entradas pelo console. Conforme meus estudos em Python avançaram, o projeto foi sendo expandido e posteriormente ganhou uma interface gráfica utilizando Tkinter.

### 🖥️ Primeira versão — Terminal

A versão original inclui recursos como:

- Cadastro de jogos
- Listagem da coleção
- Busca por nome, gênero e plataforma
- Edição e remoção de jogos
- Ordenação por nome e nota
- Estatísticas básicas
- Persistência dos dados em arquivo TXT
- Navegação através de menu no terminal

O código dessa versão está disponível em:

`versions/InSomniaGamesManager_terminal.py`

### 🎮 Versão atual — Interface gráfica

A versão atual mantém a ideia original do projeto, mas adiciona uma experiência visual mais completa, incluindo:

- Interface gráfica com Tkinter
- Tabela interativa para visualizar os jogos
- Sistema de favoritos
- Temas personalizados
- Buscas por nome, gênero e plataforma
- Ordenação interativa
- Estatísticas da coleção
- Atalhos de teclado
- Tooltips
- Persistência local dos dados

Essa evolução representa o progresso do projeto durante meus estudos de Python, partindo de conceitos fundamentais até a criação de uma aplicação desktop com interface gráfica.

## 🚀 Melhorias futuras

Algumas ideias para versões futuras:

- Salvar filtros e ordenação entre sessões
- Adicionar ícone personalizado ao programa
- Criar instalador ou versão executável para distribuição
- Migrar o armazenamento para JSON ou banco de dados
- Adicionar novas estatísticas
- Expandir as opções de personalização da interface

## 👩‍💻 Autora

Desenvolvido por **Ana Júlia** como projeto de estudo e prática de Python.