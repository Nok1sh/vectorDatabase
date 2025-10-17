import json

with open("datasets/web_dataset.json", "r", encoding="UTF-8") as dataset_orig, open("datasets/test_web.json", "r", encoding="UTF-8") as test_data:
    dataset_orig = json.load(dataset_orig)
    test_data = json.load(test_data)
    test_data_ind = 0
    comparison_data = []
    for data in dataset_orig:
        comp_data = {"question": data["question"], "comparison": None}
        if data["question"] != test_data[test_data_ind]["question"]:
            while data["question"] == test_data[test_data_ind]["question"]:
                test_data_ind += 1
        orig_data_indicators = [x["text"] for x in data["indicators"]]
        relevante_indicators = 0
        for ind in test_data[test_data_ind]["indicators"]:
            if ind["text"] in orig_data_indicators:
                relevante_indicators += 1
            
        comparison_data.append({"question": data["question"], "relevante": f"{relevante_indicators}/4"})
        
with open("comparisons/web_comparison.json", "w", encoding="UTF-8") as file:
    json.dump(comparison_data, file, indent=2, ensure_ascii=False)

print(comparison_data)
