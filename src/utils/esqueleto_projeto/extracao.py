import pandas as pd
import path_manager as pm

def carregar_csv(caminho):
    return pd.read_csv(caminho)


def carregar_bases():
    gestores = carregar_csv(pm.DATA_RAW_DIR / "gestores_projetos.csv")
    projetos = carregar_csv(pm.DATA_RAW_DIR / "status_projetos.csv")
    treinamentos = carregar_csv(pm.DATA_RAW_DIR / "rh_treinamentos.csv")

    return gestores, projetos, treinamentos