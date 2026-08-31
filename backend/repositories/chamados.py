# Coleção temporária em memória para armazenar os chamados.
# A persistência definitiva será implementada em uma etapa posterior.

chamados = []

def salvar_chamado(chamado):
    chamados.append(chamado)
    return chamado