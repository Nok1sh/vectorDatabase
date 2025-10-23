import shutil

path = "/Users/a1111/Desktop/Projects/vector_database/indicators_vector_database"
try:
    shutil.rmtree(path)
    print(f"Папка {path} удалена.")
except FileNotFoundError:
    print(f"Папка {path} не существует.")
except PermissionError:
    print(f"Ошибка: Нет прав для удаления {path}.")