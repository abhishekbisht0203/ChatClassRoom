from django import forms
from .models import Note, Question, SubTopic, Comment, ChatMessage

class NoteForm(forms.ModelForm):
    subtopic = forms.ModelChoiceField(
        queryset=SubTopic.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Select Subtopic",
        required=True
    )

    class Meta:
        model = Note
        fields = ['subtopic', 'title', 'content']


class QuestionForm(forms.ModelForm):
    subtopic = forms.ModelChoiceField(
        queryset=SubTopic.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Select Subtopic",
        required=True
    )

    class Meta:
        model = Question
        fields = ['subtopic', 'question_text']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class ChatMessageForm(forms.ModelForm):
    class Meta:
        model = ChatMessage
        fields = ['receiver', 'content']
