import json

def comparison():
    categories = ["web", "economy", "psihology"]

    for category in categories:
        with open(f"embedding_datasets/{category}_dataset.json", "r", encoding="UTF-8") as dataset_orig, open(f"embedding_datasets/test_{category}.json", "r", encoding="UTF-8") as test_data:
          dataset_orig = json.load(dataset_orig)
          test_data = json.load(test_data)
          test_data_ind = 0
          comparison_data = []
    
          for data in dataset_orig:

              if data["question"] != test_data[test_data_ind]["question"]:
                  while data["question"] == test_data[test_data_ind]["question"]:
                      test_data_ind += 1

              orig_data_indicators = [x["text"] for x in data["indicators"]]
              relevante_indicators = 0

              for ind in test_data[test_data_ind]["indicators"]:
                  if ind["text"] in orig_data_indicators:
                      relevante_indicators += 1
                  
              comparison_data.append({"question": data["question"], "relevante": f"{relevante_indicators}/4"})
              
          with open(f"comparisons/{category}_comparison.json", "w", encoding="UTF-8") as file:
              json.dump(comparison_data, file, indent=2, ensure_ascii=False)
    
          relevante_counts = [int(x["relevante"].split("/")[0]) for x in comparison_data]
          avg_relevante = sum(relevante_counts) / len(relevante_counts) if relevante_counts else 0
          print(f"Category {category}: Average comparison indicators = {avg_relevante:.2f}/4")