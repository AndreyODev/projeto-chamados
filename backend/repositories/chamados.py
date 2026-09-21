from database import obter_conexao


def salvar_chamado(chamado):
    query = """
        INSERT INTO chamados (titulo, descricao)
        VALUES (%s, %s)
        RETURNING id, titulo, descricao, status, criado_em
    """

    with obter_conexao() as conexao:
        resultado = conexao.execute(
            query,
            (chamado["titulo"], chamado["descricao"]),
        ).fetchone()

    return dict(resultado)


def listar_chamados():
    query = """
        SELECT id, titulo, descricao, status, criado_em
        FROM chamados
        ORDER BY id
    """

    with obter_conexao() as conexao:
        resultados = conexao.execute(query).fetchall()

    return [dict(resultado) for resultado in resultados]


def buscar_chamado(chamado_id):
    query = """
        SELECT id, titulo, descricao, status, criado_em
        FROM chamados
        WHERE id = %s
    """

    with obter_conexao() as conexao:
        resultado = conexao.execute(query, (chamado_id,)).fetchone()

    return dict(resultado) if resultado else None