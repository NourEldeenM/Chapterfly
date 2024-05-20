from django.shortcuts import render
from .models import *
from .forms import BookForm, CategoryForm

# Create your views here.

def view(request):
    context = {
        'category': Category.objects.all(),
        'books': Book.objects.all(),
    }
    return render(request, 'pages/views.html', context)

def add_book(request):
    if request.method == 'POST':
        if 'add_book' in request.POST:
            add_book = BookForm(request.POST, request.FILES) # request.FILES  to save images
            if add_book.is_valid():
                add_book.save()

        elif 'add_category' in request.POST:
            add_category = CategoryForm(request.POST)
            if add_category.is_valid():
                add_category.save()
        
    context = {
        'form': BookForm(),
        'formCategory': CategoryForm(),
    }
    return render(request, 'pages/add_book.html', context)

def cart(request):
    return render(request, 'pages/cart.html')

def main(request):
    return render(request, 'pages/main.html')

def details(request, id):
    bookID = Book.objects.get(id=id)
    context = {
        'book': bookID
    }
    return render(request, 'pages/details.html', context)


def account(request):
    #get username
    #get profile picture
    context = { #will be updated after setting a model for acc data
        # 'name' : 'default'
        #'username' : username
        #'profilepic' : profilepic
    }
    return render(request, 'pages/accountUser.html', context)