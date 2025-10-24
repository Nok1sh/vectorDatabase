import json

def comparison():
    categories = ["web", "economy", "psihology"]

    for category in categories:
        try:
            with open(f"datasets/{category}_dataset.json", "r", encoding="UTF-8") as dataset_orig, \
                    open(f"datasets/test_{category}.json", "r", encoding="UTF-8") as test_data:
                dataset_orig = json.load(dataset_orig)
                test_data = json.load(test_data)

                comparison_data = []
                test_data_ind = 0

                for data in dataset_orig:
                    comp_data = {"question": data["question"], "relevante": None}

                    # Поиск соответствующего вопроса в тестовом датасете
                    while test_data_ind < len(test_data) and data["question"] != test_data[test_data_ind]["question"]:
                        test_data_ind += 1

                    if test_data_ind >= len(test_data):
                        comp_data["relevante"] = "0/4"  # Вопрос не найден
                    else:
                        orig_data_indicators = [x["text"] for x in data["indicators"]]
                        relevante_indicators = 0
                        for ind in test_data[test_data_ind]["indicators"]:
                            if ind["text"] in orig_data_indicators:
                                relevante_indicators += 1
                        comp_data["relevante"] = f"{relevante_indicators}/4"

                    comparison_data.append(comp_data)

                # Сохранение результата
                with open(f"comparisons/{category}_comparison.json", "w", encoding="UTF-8") as file:
                    json.dump(comparison_data, file, indent=2, ensure_ascii=False)

                # Вывод статистики
                relevante_counts = [int(x["relevante"].split("/")[0]) for x in comparison_data]
                avg_relevante = sum(relevante_counts) / len(relevante_counts) if relevante_counts else 0
                print(f"Категория {category}: Среднее совпадение индикаторов = {avg_relevante:.2f}/4")

        except FileNotFoundError:
            print(f"Ошибка: Датасет для категории {category} не найден.")