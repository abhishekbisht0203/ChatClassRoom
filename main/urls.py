from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path('subjects/', views.subjects, name='subjects'),
    path('subject_detail/<int:pk>/', views.subject_detail, name='subject_detail'),
    path('topics/<int:pk>/', views.topic_detail, name='topic_detail'),
    path('subtopics/<int:pk>/', views.subtopic_detail, name='subtopic_detail'),
    path('notes/<int:pk>/', views.note_detail, name='note_detail'),
    path('create_note/', views.create_note, name='create_note'),
    path('create_question/', views.create_question, name='create_question'),
    path('notes/<int:note_pk>/comments/create/', views.create_comment_note, name='create_comment_note'),
    path('questions/<int:question_pk>/comments/create/', views.create_comment_question, name='create_comment_question'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('chat/', views.chat, name='chat'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
