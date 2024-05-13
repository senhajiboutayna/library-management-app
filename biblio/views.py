from django.shortcuts import render, redirect,get_object_or_404, HttpResponse
from .forms import StudentsForm, BookForm, Book_IssueForm,Book_instanceForm
from .models import Students, Book, Book_Issue,BookInstance
from time import timezone

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

def edit_student_data(request,roll):    # Vue pour éditer les données d'un étudiant
    try:
        if request.method == "POST":
            # Récupérer l'instance de l'étudiant à partir de la session
            student_instance = Students.objects.get(id=request.session.get('id'))
            # Créer le formulaire avec les données de la requête et l'instance de l'étudiant à éditer
            form = StudentsForm(request.POST, instance=student_instance)
            if form.is_valid():
                # Enregistrer les modifications apportées à l'instance de l'étudiant
                form.save()
                # Supprimer l'ID de l'étudiant de la session
                del request.session['id']
                # Rediriger vers la page affichant tous les étudiants
                return redirect("/show_students")
        else:
            # Récupérer l'instance de l'étudiant à éditer
            student_to_edit = Students.objects.get(roll_number=roll)
            # Créer le formulaire avec l'instance de l'étudiant à éditer
            form = StudentsForm(instance=student_to_edit)
            # Stocker l'ID de l'étudiant dans la session
            request.session["id"] = student_to_edit.id
            # Rendre le template pour l'édition de l'étudiant avec le formulaire pré-rempli
            return render(request, 'add_new_student.html', {'form': form})
    # Gérer les erreurs potentielles et afficher les messages d'erreur
    except Exception as error:
        print(f"{error} occurred at edit_student_data view")

def delete_student(request,roll):   # Vue pour supprimer un étudiant
    try:
        student = Students.objects.get(roll_number=roll)
        student.delete_student()
        return redirect('/show_students')
    except Students.DoesNotExist:
        # Gérer le cas où l'étudiant n'existe pas
        return render(request, 'error_page.html', {'message': 'Étudiant non trouvé'})
    except Exception as e:
        # Gérer d'autres erreurs possibles
        return render(request, 'error_page.html', {'message': str(e)})


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
    
def delete_book(request,id):        # Vue pour supprimer un livre
    try:
        book = book.objects.get(id=id)
        book.delete_book()
        return redirect('/view_books')
    except book.DoesNotExist:
        # Gérer le cas où le livre n'existe pas
        return render(request, 'error_page.html', {'message': 'livre non trouvé'})
    except Exception as e:
        # Gérer d'autres erreurs possibles
        return render(request, 'error_page.html', {'message': str(e)})

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

def edit_issued(request, id):         # Vue pour éditer un emprunt
    issued_book = get_object_or_404(Book_Issue, id=id)
    if request.method == "POST":
        form = Book_IssueForm(request.POST, instance=issued_book)
        if form.is_valid():
            form.save()
            return redirect('/view_books_issued')  # Redirige vers la vue qui affiche les livres empruntés
    else:
        form = Book_IssueForm(instance=issued_book)
    return render(request, 'issue_records.html', {'form': form, 'issued_book_id': id})