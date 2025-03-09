from django.shortcuts import render, get_object_or_404, redirect
from .forms import NoteForm
from .models import Note
from .services.elasticsearch_service import search_notes, index_note
from .services.llm_service import get_insights_from_notes

def note_interface(request):
    """
    Renders a page where users can create a new note and search for existing notes.
    """
    query = request.GET.get('q', '')
    form = NoteForm()
    notes = Note.objects.all().order_by('-created_at')

    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save()
            index_note(note)
            return redirect('note_interface')

    if query:
        notes = search_notes(query)

    context = {
        'form': form,
        'notes': notes,
        'query': query,
    }
    return render(request, 'diary/note_interface.html', context)


def note_detail(request, pk):
    """
    Retrieves and displays a single note based on its primary key.
    """
    note = get_object_or_404(Note, pk=pk)
    return render(request, 'diary/note_detail.html', {'note': note})


def note_detail_ajax(request, pk):
    """
    Returns note details as JSON for a given note primary key.
    """
    note = get_object_or_404(Note, pk=pk)
    data = {
        'title': note.title,
        'content': note.content,
        'created_at': note.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        'updated_at': note.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
    }
    from django.http import JsonResponse
    return JsonResponse(data)


def note_insights(request):
    """
    Retrieves all notes, calls the LLM service to generate insights,
    and renders a template displaying the insights.
    """
    notes = Note.objects.all().order_by('-created_at')
    insights = get_insights_from_notes(notes)
    return render(request, 'diary/note_insights.html', {'insights': insights})
