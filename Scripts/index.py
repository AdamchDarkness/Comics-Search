from elasticsearch import Elasticsearch

username = "elastic"
password = "lOf0*vttz9GwK3yUJhU="

es = Elasticsearch(
    "https://localhost:9200",
    basic_auth=(username, password),
    verify_certs=False  # Pour tests uniquement, activez la vérification en production
)

index_name = "comics"

mapping = {
    "settings": {
        "analysis": {
            "analyzer": {
                "my_custom_analyzer": {
                    "type": "custom",
                    "tokenizer": "standard",
                    "filter": ["lowercase", "asciifolding"]
                }
            }
        }
    },
    "mappings": {
        "properties": {
            "nom": {
                "type": "text",
                "analyzer": "my_custom_analyzer",
                "copy_to": "titre_saga"
            },
            "saga": {
                "type": "text",
                "analyzer": "my_custom_analyzer",
                "copy_to": "titre_saga"
            },
            "titre_saga": {
                "type": "text",
                "analyzer": "my_custom_analyzer"
            },
            "path": {"type": "keyword"},
            "extention": {"type": "keyword"},
            "maison_d_edition": {
                "type": "text",
                "analyzer": "my_custom_analyzer"
            },
            "run": {"type": "keyword"},
            "cover_path": {"type": "keyword"}
        }
    }
}

if es.indices.exists(index=index_name):
    es.indices.delete(index=index_name)
    print(f"Index '{index_name}' supprimé.")

response = es.indices.create(index=index_name, body=mapping)
print(f"Index '{index_name}' créé avec la réponse :")
print(response)
