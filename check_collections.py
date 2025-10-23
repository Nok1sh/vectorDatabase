import chromadb

client = chromadb.PersistentClient(path="indicators_vector_database", settings=chromadb.config.Settings(allow_reset=True))

categories = ["web", "economy", "psihology"]
for category in categories:
    try:
        collection = client.get_collection(f"{category}_indicators")
        count = collection.count()
        print(f"Количество индикаторов в коллекции {category}: {count}")
    except chromadb.errors.NotFoundError:
        print(f"Коллекция {category}_indicators не существует.")