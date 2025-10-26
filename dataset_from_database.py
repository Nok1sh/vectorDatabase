import json
import re
from vector_database import Database

def create_datasets(categories):

    for category in categories:
        database = Database(category)
        database.analyze_questions()

        questions_list = []
        with open(f"questions/questions_{category}.txt", encoding="UTF-8") as questions:
            for question in questions:
                start_string = re.search(r'\D\w\S', question)
                edit_question = question[start_string.span()[0]+1:].replace("\n", "") if start_string else question.replace("\n", "")
                questions_list.append(edit_question)

        results = database.get_results_for_all_questions

        result_json = []
        for question, indicat, metadata, result in zip(questions_list, results["documents"], results["metadatas"], results["distances"]):
            analyze_qustion = {"question": question, "indicators": []}
            for i in range(database.n_indicators_per_question):
                data = {
                    "compentency_code": metadata[i]["compentency_code"],
                    "code": metadata[i]["code_indicator"],
                    "text": indicat[i],
                    "score": result[i]
                }
                analyze_qustion["indicators"].append(data)
            result_json.append(analyze_qustion)

        with open(f"embedding_datasets/test_{category}.json", "w", encoding="UTF-8") as file:
            json.dump(result_json, file, indent=2, ensure_ascii=False)