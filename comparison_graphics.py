import json
import random
import matplotlib.pyplot as plt

def generate_colors(n):
    colors = []
    for i in range(n):
        color = '#{:06x}'.format(random.randint(0, 0xFFFFFF))
        colors.append(color)
    return colors

def load_comparison_data(categories):
    """Загружает данные сравнения из JSON-файлов и вычисляет средние совпадения."""
    avg_relevante_values = []
    for category in categories:
        try:
            with open(f"comparisons/{category}_comparison.json", "r", encoding="UTF-8") as file:
                comparison_data = json.load(file)
                relevante_counts = [int(x["relevante"].split("/")[0]) for x in comparison_data]
                avg_relevante = sum(relevante_counts) / len(relevante_counts) if relevante_counts else 0
                avg_relevante_values.append(avg_relevante)
                print(f"Категория {category}: Среднее совпадение индикаторов = {avg_relevante:.2f}/4")
        except FileNotFoundError:
            print(f"Ошибка: Файл comparisons/{category}_comparison.json не найден.")
            avg_relevante_values.append(0)
    return avg_relevante_values

def plot_comparison(categories, avg_relevante_values, save_path=None):
    """Строит столбчатую диаграмму для средних совпадений."""
    plt.figure(figsize=(8, 6))
    bars = plt.bar(categories, avg_relevante_values, color=generate_colors(len(categories)))
    plt.xticks(rotation=45)
    plt.title('Среднее совпадение индикаторов по категориям')
    plt.xlabel('Категория')
    plt.ylabel('Среднее совпадение (из 4)')
    plt.ylim(0, 4)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Добавление подписей значений над столбцами
    for i, v in enumerate(avg_relevante_values):
        plt.text(i, v + 0.1, f'{v:.2f}', ha='center', va='bottom')

    # Сохранение графика, если указан путь
    if save_path:
        plt.savefig(save_path)
        print(f"График сохранен в {save_path}")

    plt.show()
