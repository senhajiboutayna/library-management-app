from django.shortcuts import render, redirect,HttpResponse
from .forms import StudentsForm, BookForm, Book_IssueForm,Book_instanceForm
from .models import Students, Book, Book_Issue,BookInstance


# Create your views here.

def index(request):     # Vue pour la page d'accueil
    return(render(request, 'index.html'))


def add_new_student(request):   # Vue pour ajouter un nouvel étudiant
    if request.method=="POST":
        form = StudentsForm((request.POST))
        if form.is_valid():
            form.save()
            return redirect('/show_students')
    else:
        form = StudentsForm
    return (render(request, 'add_new_student.html', {'form':form}))


def add_new_book(request):     # Vue pour ajouter un nouveau livre
    if request.method=="POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form=form.save()
            book_instance=BookInstance(book=form)
            book_instance.save()
            return redirect('/view_books')
    else:
        form = BookForm
        form_instance=Book_instanceForm
        return (render(request, 'add_new_book.html', {'form':form,"form_instance":form_instance}))

def add_new_book_instance(request):     # Vue pour ajouter une nouvelle instance de livre
    form=Book_instanceForm(request.POST)
    if form.is_valid():
        form.save()
    return redirect('/view_books')


def add_book_issue(request):     # Vue pour ajouter un emprunt de livre
    if request.method=="POST":
        form = Book_IssueForm(request.POST)
        if form.is_valid():
            # Sauvegarder les données du formulaire
            unsaved_form=form.save(commit=False)
            # Récupérer l'instance de livre à partir de l'ID et marquer le livre comme emprunté
            book_to_save=BookInstance.objects.get(id=unsaved_form.book_instance.id)
            book_to_save.Is_borrowed=True
            book_to_save.save()
            form.save()
            form.save_m2m()
        return redirect('/view_books_issued')
    else:
        context={'form':Book_IssueForm,"book":BookInstance.objects.filter(Is_borrowed=False)}
        return render(request, 'add_book_issue.html',context=context)

def view_students(request):    # Vue pour afficher les étudiants
    students = Students.objects.order_by('-id')
    return render(request,'students.html', {'students': students})

def view_books(request):      # Vue pour afficher les livres
    books=BookInstance.objects.order_by('id')
    return render(request,'books.html', {'books': books})

def view_issue(request):      # Vue pour afficher les enregistrements d'emprunt
    issue = Book_Issue.objects.order_by('-id')
    return render(request,'issue_records.html', {'issue': issue})


def edit_student_data(request,roll):    # Vue pour éditer les données d'un étudiant
    try:
        if request.method == "POST":
            std=Students.objects.get(id=request.session['id'])    
            form = StudentsForm((request.POST),instance=std)
            if form.is_valid():
                form.save()
            del request.session['id']
            return redirect("/show_students")
        else:
            student_to_edit=Students.objects.get(roll_number=roll)
            student=StudentsForm(instance=student_to_edit)
            request.session["id"]=student_to_edit.id
            return render(request,'edit_student_data.html',{'student':student})
    except Exception as error:
        print(f"{error} occured at edit_student_data view")

def edit_book_data(request,id):    
# Vue pour éditer les données d'un livre
    return HttpResponse(f"<label>A book with ID: {id} could not be edited...</label><h2>The feature is comming soon</h2>")

def delete_student(request,roll):   # Vue pour supprimer un étudiant
    return HttpResponse(f"<h2>Delete Student</h2><label>Student with Roll Number: {roll} could not be deleted...</label><h2>The feature is comming soon</h2>")
    

def delete_book(request,id):        # Vue pour supprimer un livre
    return HttpResponse(f"<h2>Delete Book</h2><label>Book with ID: {id} could not be deleted..</label><h2>The feature is comming soon</h2>")

def return_issued_book(request,id):     # Vue pour retourner un livre emprunté
    obj=Book_Issue.objects.get(id=id)
    return HttpResponse(f"<h2>Return Issued Book</h2><label>Book <i>{obj.book_instance.book.book_title}</i> issued to <i>{obj.student.fullname}</i> could not be returned..</label><h2>The feature is comming soon</h2>")

def edit_issued(request, id):         # Vue pour éditer un emprunt
    obj=Book_Issue.objects.get(id=id)
    return HttpResponse(f"<h2>Edit Issued Book</h2><label>Book <i>{obj.book_instance.book.book_title}</i> issued to <i>{obj.student.fullname}</i> could not be edited..</label><h2>The feature is comming soon</h2>")

