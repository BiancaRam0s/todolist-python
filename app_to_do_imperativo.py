"""To-Do List — Versão 1: Paradigma Imperativo com Armazenamento em .txt.

Implementa gerenciamento de tarefas estruturado utilizando funções procedurais,
dicionários nativos (dict) sem anotações de tipo (Type Hints) e persistência direta
em arquivo de texto plano (.txt).
"""

import os
from datetime import datetime

ARQUIVO_TXT = "tarefas.txt"
DELIMITADOR = "|"


def obter_caminho_arquivo(caminho_customizado=None):
    """Retorna o caminho absoluto para o arquivo tarefas.txt."""
    if caminho_customizado:
        return caminho_customizado
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(diretorio_atual, ARQUIVO_TXT)


def inicializar_arquivo(caminho_customizado=None):
    """Garante a existência do arquivo no disco com o cabeçalho de campos."""
    caminho = obter_caminho_arquivo(caminho_customizado)
    if not os.path.exists(caminho):
        with open(caminho, "w", encoding="utf-8") as f:
            f.write("# id|titulo|categoria|prioridade|status|data_criacao|data_conclusao\n")


def carregar_tarefas(caminho_customizado=None):
    """Lê o arquivo de texto plano e faz parsing dos registros para uma lista de dicionários."""
    inicializar_arquivo(caminho_customizado)
    caminho = obter_caminho_arquivo(caminho_customizado)
    tarefas = []

    with open(caminho, "r", encoding="utf-8") as f:
        for linha in f:
            linha_limpa = linha.strip()
            if not linha_limpa or linha_limpa.startswith("#"):
                continue

            partes = linha_limpa.split(DELIMITADOR)
            if len(partes) >= 6:
                conclusao = (
                    partes[6] if len(partes) > 6 and partes[6] != "-" else None
                )
                tarefa = {
                    "id": int(partes[0]),
                    "titulo": partes[1],
                    "categoria": partes[2],
                    "prioridade": partes[3],
                    "status": partes[4],
                    "data_criacao": partes[5],
                    "data_conclusao": conclusao,
                }
                tarefas.append(tarefa)

    return tarefas


def salvar_tarefas(tarefas, caminho_customizado=None):
    """Serializa a lista de tarefas para o formato delimitado por pipes no disco."""
    caminho = obter_caminho_arquivo(caminho_customizado)
    with open(caminho, "w", encoding="utf-8") as f:
        f.write("# id|titulo|categoria|prioridade|status|data_criacao|data_conclusao\n")
        for t in tarefas:
            conclusao = t["data_conclusao"] if t["data_conclusao"] else "-"
            linha = (
                f"{t['id']}{DELIMITADOR}{t['titulo']}{DELIMITADOR}{t['categoria']}{DELIMITADOR}"
                f"{t['prioridade']}{DELIMITADOR}{t['status']}{DELIMITADOR}{t['data_criacao']}{DELIMITADOR}{conclusao}\n"
            )
            f.write(linha)


def gerar_novo_id(tarefas):
    """Calcula o próximo ID sequencial."""
    if not tarefas:
        return 1
    return max(t["id"] for t in tarefas) + 1


def adicionar_tarefa(titulo, categoria="Geral", prioridade="Média", caminho_customizado=None):
    """Insere uma nova tarefa e persiste no arquivo .txt."""
    if not titulo.strip():
        raise ValueError("O título da tarefa não pode ser vazio.")

    tarefas = carregar_tarefas(caminho_customizado)
    novo_id = gerar_novo_id(tarefas)
    agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    nova_tarefa = {
        "id": novo_id,
        "titulo": titulo.strip(),
        "categoria": categoria.strip() or "Geral",
        "prioridade": prioridade.strip() or "Média",
        "status": "Pendente",
        "data_criacao": agora,
        "data_conclusao": None,
    }

    tarefas.append(nova_tarefa)
    salvar_tarefas(tarefas, caminho_customizado)
    return nova_tarefa


def listar_tarefas(filtro_status="Todos", caminho_customizado=None):
    """Filtra tarefas por status ('Todos', 'Pendente', 'Concluída')."""
    tarefas = carregar_tarefas(caminho_customizado)
    if filtro_status == "Todos":
        return tarefas
    return [t for t in tarefas if t["status"].lower() == filtro_status.lower()]


def concluir_tarefa(tarefa_id, caminho_customizado=None):
    """Marca tarefa como concluída e registra data/hora."""
    tarefas = carregar_tarefas(caminho_customizado)
    encontrada = False
    agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for t in tarefas:
        if t["id"] == tarefa_id:
            t["status"] = "Concluída"
            t["data_conclusao"] = agora
            encontrada = True
            break

    if encontrada:
        salvar_tarefas(tarefas, caminho_customizado)
    return encontrada


def excluir_tarefa(tarefa_id, caminho_customizado=None):
    """Exclui registro pelo ID e regrava o arquivo .txt."""
    tarefas = carregar_tarefas(caminho_customizado)
    tarefas_filtradas = [t for t in tarefas if t["id"] != tarefa_id]

    if len(tarefas_filtradas) < len(tarefas):
        salvar_tarefas(tarefas_filtradas, caminho_customizado)
        return True
    return False


def exibir_tabela_terminal(tarefas):
    """Renderiza a listagem de tarefas no terminal."""
    if not tarefas:
        print("\n📭 Nenhuma tarefa encontrada.\n")
        return

    print("\n" + "=" * 85)
    print(f"{'ID':<4} | {'Status':<11} | {'Prioridade':<10} | {'Categoria':<12} | {'Título':<30} | {'Criado em'}")
    print("-" * 85)
    for t in tarefas:
        status_icon = "✅ Concluída" if t["status"] == "Concluída" else "⏳ Pendente"
        print(
            f"{t['id']:<4} | {status_icon:<11} | {t['prioridade']:<10} | {t['categoria']:<12} | {t['titulo'][:28]:<30} | {t['data_criacao']}"
        )
    print("=" * 85 + "\n")


def menu_terminal():
    """Loop de execução interativa no terminal (CLI)."""
    while True:
        print("\n==========================================")
        print("📋 TO-DO LIST — VERSÃO IMPERATIVA (.TXT)")
        print("==========================================")
        print("1. Listar todas as tarefas")
        print("2. Listar apenas tarefas pendentes")
        print("3. Adicionar nova tarefa")
        print("4. Concluir tarefa")
        print("5. Excluir tarefa")
        print("0. Sair")
        print("------------------------------------------")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            tarefas = listar_tarefas("Todos")
            exibir_tabela_terminal(tarefas)

        elif opcao == "2":
            tarefas = listar_tarefas("Pendente")
            exibir_tabela_terminal(tarefas)

        elif opcao == "3":
            titulo = input("Título da tarefa: ").strip()
            if not titulo:
                print("❌ Erro: O título não pode ser vazio.")
                continue
            categoria = input("Categoria [Geral]: ").strip() or "Geral"
            print("Prioridade: 1-Baixa, 2-Média, 3-Alta")
            prio_op = input("Escolha a prioridade [2]: ").strip()
            mapa_prio = {"1": "Baixa", "2": "Média", "3": "Alta"}
            prioridade = mapa_prio.get(prio_op, "Média")

            nova = adicionar_tarefa(titulo, categoria, prioridade)
            print(f"✅ Tarefa #{nova['id']} adicionada com sucesso!")

        elif opcao == "4":
            try:
                tarefa_id = int(input("Informe o ID da tarefa para concluir: ").strip())
                if concluir_tarefa(tarefa_id):
                    print(f"✅ Tarefa #{tarefa_id} marcada como Concluída!")
                else:
                    print(f"❌ Tarefa #{tarefa_id} não encontrada.")
            except ValueError:
                print("❌ ID inválido. Digite um número inteiro.")

        elif opcao == "5":
            try:
                tarefa_id = int(input("Informe o ID da tarefa para excluir: ").strip())
                if excluir_tarefa(tarefa_id):
                    print(f"🗑️ Tarefa #{tarefa_id} excluída com sucesso!")
                else:
                    print(f"❌ Tarefa #{tarefa_id} não encontrada.")
            except ValueError:
                print("❌ ID inválido. Digite um número inteiro.")

        elif opcao == "0":
            print("👋 Encerrando To-Do List Imperativo. Até logo!")
            break
        else:
            print("❌ Opção inválida, tente novamente.")


if __name__ == "__main__":
    menu_terminal()