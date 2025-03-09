from django.test import TestCase
from diary.models import Note
from diary.services.elasticsearch_service import (
    create_index, index_note, search_notes, delete_note_index
)


class ElasticsearchServiceTestCase(TestCase):
    def setUp(self):
        # Ensure the index exists before each test
        create_index()

    def test_index_and_search_note(self):
        # Create a test note
        note = Note.objects.create(
            title="Test Note",
            content="Testing Elasticsearch integration in notesight."
        )
        # Index the note
        index_note(note)
        # Perform a search
        results = search_notes("Elasticsearch", top_k=10)
        self.assertIn(note, results)
        # Clean up by deleting the note from the Elasticsearch index
        delete_note_index(note.pk)
