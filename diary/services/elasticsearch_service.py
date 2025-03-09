from datetime import datetime

from django.conf import settings
from diary.models import Note
from diary.elasticsearch_client import es

INDEX_NAME = "notes"


def create_index():
    """
    Create the Elasticsearch index if it does not exist.
    """
    if not es.indices.exists(index=INDEX_NAME):
        mapping = {
            "mappings": {
                "properties": {
                    "title": {"type": "text"},
                    "content": {"type": "text"},
                    "created_at": {"type": "date"}
                }
            }
        }
        es.indices.create(index=INDEX_NAME, body=mapping)


def index_note(note: Note):
    """
    Index a Note instance into Elasticsearch.
    """
    # Ensure the index exists.
    create_index()
    doc = {
        "title": note.title,
        "content": note.content,
        "created_at": (
            note.created_at.isoformat()
            if note.created_at else datetime.now().isoformat()
        )
    }
    # Use note.pk as the document ID for easy updates/deletes later.
    es.index(index=INDEX_NAME, id=note.pk, document=doc, refresh=True)


def update_note_index(note: Note):
    """
    Update an existing note's document in Elasticsearch.
    """
    doc = {
        "title": note.title,
        "content": note.content,
        "created_at": (
            note.created_at.isoformat()
            if note.created_at else datetime.now().isoformat()
        )
    }
    es.update(index=INDEX_NAME, id=note.pk, body={"doc": doc})


def delete_note_index(note_id):
    """
    Delete a note from the Elasticsearch index.
    """
    es.delete(index=INDEX_NAME, id=note_id)


def search_notes(query: str, top_k: int = 5):
    """
    Perform a search against the Elasticsearch index for notes that match the query.
    Returns Django Note objects matching the top results.
    """
    search_query = {
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["title", "content"]
            }
        },
        "size": top_k
    }
    results = es.search(index=INDEX_NAME, body=search_query)
    note_ids = [hit["_id"] for hit in results["hits"]["hits"]]
    # Convert IDs to integers (if your model uses integer IDs)
    note_ids = [int(nid) for nid in note_ids]
    return Note.objects.filter(pk__in=note_ids)
