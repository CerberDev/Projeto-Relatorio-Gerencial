from pathlib import Path

# Corrigido: adicionado o nome da variável e os sublinhados duplos em __file__
PROJECT_ROOT = Path(__file__).resolve().parents[2]

def resolve_path(relative_path: str) -> Path:
    return PROJECT_ROOT / relative_path

CONFIG_DIR = resolve_path('config')

# Corrigido: renomeado de RAW_DIIR para RAW_DIR
RAW_DIR = resolve_path('data/raw')