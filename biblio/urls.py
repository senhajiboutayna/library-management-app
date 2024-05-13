from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_new_student', views.add_new_student, name='new_student'),
    path('add_new_book', views.add_new_book, name='new_book'),
    path('add_book_issue', views.add_book_issue, name='book_issue'),
    path('add_new_book_instance', views.add_new_book_instance, name='add_new_book_instance'),
    path('show_students', views.view_students, name='show_student_record'),
    path('view_books', views.view_books, name='show_book_record'),
    path('view_books_issued', views.view_issue, name='show_issue_record'),
    path('edit/student/<str:roll>',views.edit_student_data,name="Edit Student data"),
    path('delete/student/<str:roll>',views.delete_student,name="delete_student"),
    path('delete/book/<str:id>',views.delete_book,name="delete_book"),
    path('edit_issued/<int:id>',views.edit_issued,name="edit_issued"),

]