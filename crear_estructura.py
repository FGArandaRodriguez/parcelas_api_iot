import os

estructura = {
    "app": {
        "core": ["__init__.py", "database.py"],
        "domain": ["__init__.py", "models.py"],
        "infrastructure": ["__init__.py", "repositories.py"],
        "schemas": ["__init__.py"],
        "services": ["__init__.py"],
        "api": ["__init__.py", "socket.py"],
        "__init__.py": "",
        "main.py": ""
    },
    "alembic": {},
}

archivos_root = [
    "requirements.txt",
    "alembic.ini",
    "README.md",
    "crear_estructura.py"
]


def crear_directorio(path):
    if not os.path.exists(path):
        os.makedirs(path)


def crear_archivo(path):
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            f.write("")


def crear_estructura_directorio(base, estructura):
    for key, value in estructura.items():
        dir_path = os.path.join(base, key)
        crear_directorio(dir_path)

        if isinstance(value, list):
            for file in value:
                crear_archivo(os.path.join(dir_path, file))
        elif isinstance(value, dict):
            crear_estructura_directorio(dir_path, value)
        elif isinstance(value, str):
            crear_archivo(os.path.join(base, key))


if __name__ == "__main__":
    base_path = os.getcwd()
    crear_estructura_directorio(base_path, estructura)

    for archivo in archivos_root:
        crear_archivo(os.path.join(base_path, archivo))

    print("Estructura del proyecto creada exitosamente.")
