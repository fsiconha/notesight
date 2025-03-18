from django.core.management.base import BaseCommand
from diary.models import Note
from diary.services.elasticsearch_service import index_note

class Command(BaseCommand):
    help = "Indexes all notes from the database into Elasticsearch."

    def handle(self, *args, **options):
        notes = Note.objects.all()
        count = 0
        for note in notes:
            index_note(note)
            count += 1
            self.stdout.write(self.style.SUCCESS(f"Indexed note {note.pk}: {note.title}"))
        self.stdout.write(self.style.SUCCESS(f"Successfully indexed {count} notes."))
