from django import forms
from .models import Students, Book, Book_Issue,BookInstance


#Ce formulaire est lié au modèle Students et permet de créer, mettre à jour ou supprimer des instances d'étudiants.
class StudentsForm(forms.ModelForm):
    class Meta:
        model = Students
        fields = '__all__'   #inclure tous les champs du modèle student

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
        
class Book_instanceForm(forms.ModelForm):
    class Meta:
        model=BookInstance
        fields = ['book','book_number']

class Book_IssueForm(forms.ModelForm):
    class Meta:
        model=Book_Issue
        exclude = ['issue_date', 'due_date','remarks_on_return','date_returned']

##Chaque classe de formulaire est une sous-classe de forms.ModelForm, ce qui signifie qu'elle est basée sur un modèle Django et générera automatiquement 
##des champs de formulaire correspondant aux champs du modèle spécifié dans la classe Meta.