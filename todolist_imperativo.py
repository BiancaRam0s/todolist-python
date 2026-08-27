# Trecho didático de carregamento e parsing
def carregar_tarefas(caminho_customizado=None):
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
                conclusao = partes[6] if len(partes) > 6 and partes[6] != "-" else None
                tarefas.append({
                    "id": int(partes[0]),
                    "titulo": partes[1],
                    "categoria": partes[2],
                    "prioridade": partes[3],
                    "status": partes[4],
                    "data_criacao": partes[5],
                    "data_conclusao": conclusao,
                })
    return tarefas