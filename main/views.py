from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Subject, Topic, SubTopic, Note, Question
from .forms import NoteForm, QuestionForm, CommentForm 
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import JsonResponse

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            return JsonResponse({'success': False, 'error': 'Passwords do not match.'}, status=400)

        form = UserCreationForm({
            'username': username,
            'email': email,
            'password1': password1,
            'password2': password2
        })

        if form.is_valid():
            user = form.save()
            login(request, user)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Form is not valid.'}, status=400)

    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid username or password.'}, status=400)
    
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to the login page after logout

def home(request):
    return render(request, "home.html")

# List all subjects
def subjects(request):
    subjects = Subject.objects.all()
    return render(request, 'subjects.html', {'subjects': subjects})

# Detail view of a subject including its topics
def subject_detail(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    topics = subject.topics.all()
    return render(request, 'subject_detail.html', {'subject': subject, 'topics': topics})

# List subtopics under a topic
def topic_detail(request, pk):
    topic = get_object_or_404(Topic, pk=pk)
    subtopics = topic.subtopics.all()
    return render(request, 'topic_detail.html', {'topic': topic, 'subtopics': subtopics})

# Detail view of a subtopic including notes and questions
def subtopic_detail(request, pk):
    subtopic = get_object_or_404(SubTopic, pk=pk)
    notes = subtopic.notes.all()
    questions = subtopic.questions.all()
    return render(request, 'subtopic_detail.html', {'subtopic': subtopic, 'notes': notes, 'questions': questions})

# Detail view of a note
def note_detail(request, pk):
    note = get_object_or_404(Note, pk=pk)

    # Get the previous note
    previous_note = Note.objects.filter(id__lt=note.id).order_by('-id').first()

    # Get the next note
    next_note = Note.objects.filter(id__gt=note.id).order_by('id').first()

    context = {
        'note': note,
        'previous_note': previous_note,
        'next_note': next_note,
    }
    return render(request, 'note_detail.html', context)

def chat(request):
    return render(request, 'chat.html')

@login_required
def create_note(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            # Retrieve subtopic from form data
            subtopic_id = request.POST.get('subtopic')
            note.subtopic = get_object_or_404(SubTopic, pk=subtopic_id)
            note.uploaded_by = request.user
            note.save()
            return redirect('dashboard')  # Redirect to dashboard or appropriate page
    else:
        form = NoteForm()
    subtopics = SubTopic.objects.all()
    return render(request, 'note_form.html', {'form': form, 'subtopics': subtopics})

@login_required
def create_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            # Retrieve subtopic from form data
            subtopic_id = request.POST.get('subtopic')
            question.subtopic = get_object_or_404(SubTopic, pk=subtopic_id)
            question.added_by = request.user
            question.save()
            return redirect('dashboard')  # Redirect to dashboard or appropriate page
    else:
        form = QuestionForm()
    subtopics = SubTopic.objects.all()
    return render(request, 'question_form.html', {'form': form, 'subtopics': subtopics})

# Create a new comment on a note
@login_required
def create_comment_note(request, note_pk):
    """
    Creates a comment for a specific note.

    Args:
        request (HttpRequest): The HTTP request object.
        note_pk (int): The primary key of the note.

    Returns:
        HttpResponse: The HTTP response object.

    Raises:
        Http404: If the note with the given primary key does not exist.

    """
    note = get_object_or_404(Note, pk=note_pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.note = note
            comment.commented_by = request.user
            comment.save()
            return redirect('subtopic_detail', pk=note.subtopic.pk)
    else:
        form = CommentForm()
    return render(request, 'comment_form.html', {'form': form})

# Create a new comment on a question
@login_required
def create_comment_question(request, question_pk):
    question = get_object_or_404(Question, pk=question_pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.question = question
            comment.commented_by = request.user
            comment.save()
            return redirect('subtopic_detail', pk=question.subtopic.pk)
    else:
        form = CommentForm()
    return render(request, 'comment_form.html', {'form': form})

def dashboard(request):
    return render(request, 'dashboard.html')