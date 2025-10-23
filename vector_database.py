import chromadb
import json
import uuid
import re
import shutil
from chromadb.utils import embedding_functions
from typing import List, Dict


class Database:

    TRANSFORMER = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L12-v2")

    def __init__(self, collection: str, path_database="indicators_vector_database"):
        self.path_database = path_database
        self.name: str = collection
        self.database = chromadb.PersistentClient(self.path_database, settings=chromadb.config.Settings(allow_reset=True))
        self.collection = self.database.get_or_create_collection(name=f"{self.name}_indicators", embedding_function=Database.TRANSFORMER)

        self.n_indicators_per_question: int = 4

        self.text_indicators: List[str] = []
        self.code_indicators: List[Dict[str, str]] = []
        
        self.text_questions: List[str] = []
    
    @property
    def update_parameters(self):
        self.text_indicators: List[str] = []
        self.code_indicators: List[Dict[str, str]] = []
        self.text_questions: List[str] = []
    
    def add_new_collection(self, collection):
        self.update_parameters
        self.name: str = collection
        self.collection = self.database.get_or_create_collection(name=f"{self.name}_indicators", embedding_function=Database.TRANSFORMER)


    def add_indicators_in_database_from_json(self, path=None):
        """
        Structure indicatrs:
        [
            {
                "compentency_code": ... ("ПК-9.1", "ОПК-1"...),
                "indicators": [
                    {
                        "code": ... ("У-1", "З-2"...),
                        "text": ...
                    },
                    {
                        ...
                    }
                ]
            },
            {
                ...
            }
        ]
        """
        if self.collection.count():
            return

        if path is None:
            path = f"indicators/indicators_{self.name}.json"

        with open(path, "r", encoding="utf-8") as indicators:
            indicators = json.load(indicators)

            for i in indicators:
                for j in i["indicators"]:
                    self.text_indicators.append(j["text"])
                    self.code_indicators.append({"code_indicator": j["code"], "compentency_code": i["compentency_code"]})
        
        self.collection.add(
            ids=[str(uuid.uuid4()) for _ in self.text_indicators],
            documents=self.text_indicators,
            metadatas=self.code_indicators
        )
    

    def analyze_questions(self, path=None):
        if path is None:
            path = f"questions/questions_{self.name}.txt"
        
        with open(path, "r", encoding="utf-8") as questions:
            for question in questions:
                if question:
                    start_string = re.search(r'\D\w\S', question)
                    edit_question = question[start_string.span()[0]+1:].replace("\n", "") if start_string else question.replace("\n", "")
                    self.text_questions.append(edit_question)

    def delete_collection(self, path=None):
        if path is None:
            path = f"{self.name}_indicators"
        self.database.delete_collection(path)
    
    def delete_database(self, code=None):
        if code == "delete_database":
            self.database.reset()
            # shutil.rmtree(self.path_database)

    @property
    def get_names_collections(self):
        collections: List[str] = []
        for collection in self.database.list_collections():
            collections.append(collection.name)

        return collections

    @property
    def get_results_for_all_questions(self):
        results = self.collection.query(
            query_texts=self.text_questions,
            n_results=self.n_indicators_per_question,
            include=["distances", "embeddings", "documents", "metadatas"]
        )
        return results

    def get_results_for_one_question(self, number_question=0):
        results = self.collection.query(
            query_texts=self.text_questions[number_question],
            n_results=self.n_indicators_per_question,
            include=["distances", "embeddings", "documents", "metadatas"]
        )
        return results


#database = Database("web")
#print("web")

# database.delete_database("delete_database")
#database.add_indicators_in_database_from_json()

# database.analyze_questions()

# print(database.get_results_for_one_question(5))

#print("economy")
#database.add_new_collection("economy")

#database.add_indicators_in_database_from_json()

# database.analyze_questions()

# print(database.get_results_for_all_questions)

#print("psihology")
#database.add_new_collection("psihology")

#database.add_indicators_in_database_from_json()

# database.analyze_questions()

# print(database.get_results_for_all_questions)
