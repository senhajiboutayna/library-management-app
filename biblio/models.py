from django.db import models
from datetime import datetime,timedelta   # Importation des modules datetime et timedelta pour la gestion des dates
import uuid    # Importation du module uuid pour générer des UUID

# Create your models here.

class Book(models.Model):
    book_title = models.CharField(max_length=200)
    book_author = models.CharField(max_length=100)
    book_pages = models.PositiveIntegerField()
    summary=models.TextField(max_length=500, help_text="Summary about the book",null=True,blank=True)
    def __str__(self):
        return self.book_title
    
class Students(models.Model):
    roll_number = models.CharField(max_length=100,unique=True)
    fullname = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    program = models.CharField(max_length=100)
    Email=models.EmailField(max_length=100,help_text="Student e-mail")
    def __str__(self):
        return self.fullname
    
class BookInstance(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,help_text="Book unique id across the Library")  #identifiant unique pour chaque instance de livre
    book=models.ForeignKey('Book', on_delete=models.CASCADE,null=True)  #associer l'instance de livre à un livre spécifique
    book_number=models.PositiveIntegerField(null=True,help_text="Book number for books of the save kind")  #pour stocker le numéro de livre, utile pour les livres identiques
    Is_borrowed = models.BooleanField(default=False)    #indiquer si le livre est emprunté ou non
    def __str__(self):
        return f"{self.id} {self.book}"

def get_returndate():       # Fonction pour obtenir la date de retour prévue pour un livre emprunté
    return datetime.today() + timedelta(days=8)


# Modèle pour enregistrer les emprunts de livres par les étudiants
class Book_Issue(models.Model):
    student = models.ForeignKey('Students', on_delete=models.CASCADE)   #associer l'emprunt à un étudiant
    book_instance = models.ForeignKey('BookInstance', on_delete=models.CASCADE)   #pour associer l'emprunt à une instance de livre spécifique
    issue_date = models.DateTimeField(auto_now=True,help_text="Date the book is issued")  #enregistrer la date de l'emprunt
    due_date = models.DateTimeField(default=get_returndate(),help_text="Date the book is due to")   #enregistrer la date d'échéance de retour du livre
    date_returned=models.DateField(null=True, blank=True,help_text="Date the book is returned")   #la date de retour réelle du livre
    # enregistrer les remarques sur l'état du livre lors de l'emprunt
    remarks_on_issue = models.CharField(max_length=100, default="Book in good condition", help_text="Book remarks/condition during issue")
    # enregistrer les remarques sur l'état du livre lors du retour
    remarks_on_return = models.CharField(max_length=100, default="Book in good condition", help_text="Book remarks/condition during return")

    def __str__(self):
        return self.student.fullname + " borrowed " + self.book.book_title
    
## borrowed : a emprunté
