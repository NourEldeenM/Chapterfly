from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import BookForm, CategoryForm, CheckoutForm, EditBookForm , SignupForm , loginForm, ProfilePhotoForm
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib import messages
import json
from django.db.models import Sum , Q

# Create your views here.

def view(request):
    search = Book.objects.all()
    query = request.GET.get('search')

    if query:
        search = search.filter(Q(name__icontains=query) | Q(author__icontains=query))

    isLogged = request.session.get('isLogged')
    is_admin = request.session.get('is_admin')

    if isLogged is False:
        return redirect('LoginSignup')

    context = {
        'category': Category.objects.all(),
        'books': search,
        'is_admin': is_admin,
        'isLogged': isLogged,
        'search_query': query,
    }
    return render(request, 'pages/views.html', context)

def render_add_book_page(request):
    context = {
        'form': BookForm(),
        'formCategory': CategoryForm(),
    }
    return render(request, 'pages/add_book.html', context)

def add_book(request):
    if request.method == 'POST':
        add_book_form = BookForm(request.POST, request.FILES)
        if add_book_form.is_valid():
            add_book_form.save()
            return JsonResponse({'message': 'Book added successfully'}, status=200)
        return JsonResponse({'message': 'Error adding book'}, status=400)

def add_category(request):
    if request.method == 'POST':
        add_category_form = CategoryForm(request.POST)
        if add_category_form.is_valid():
            add_category_form.save()
            return JsonResponse({'message': 'Category added successfully'}, status=200)
        return JsonResponse({'message': 'Error adding category'}, status=400)

def cart(request):
    isLogged = request.session.get('isLogged')
    is_admin = request.session.get('is_admin')
    user_id = request.session.get('user_id')
    user_cart = Signup.objects.get(id=user_id).cart.all()
    total_price = user_cart.aggregate(total_price=Sum('price'))['total_price'] or 0
    count_items = user_cart.count()
    cart_book_ids = [book.id for book in user_cart]
    
    if isLogged is False :
        return redirect('LoginSignup')
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            borrow_books(request)
            return redirect('account')
        
    context = {
        'form': CheckoutForm(),
        'isLogged':isLogged,
        'is_admin':is_admin,
        'cart_items': user_cart,
        'total_price': total_price,
        'count_itmes': count_items,
    }
    return render(request, 'pages/cart.html', context)

def remove_from_cart(request):
    if request.method == 'POST' and 'item_id' in request.POST:
        user_id = request.session.get('user_id')
        signup_user = Signup.objects.get(id=user_id)
        book_id = request.POST['item_id']
        book = Book.objects.get(id=book_id)
        signup_user.cart.remove(book)
        return JsonResponse({'message': 'Book removed from cart.'})
    else:
        return JsonResponse({'error': 'Invalid request.'}, status=400)
    
def remove_from_wishlist(request):
    if request.method == 'POST' and 'item_id' in request.POST:
        user_id = request.session.get('user_id')
        signup_user = Signup.objects.get(id=user_id)
        book_id = request.POST['item_id']
        book = Book.objects.get(id=book_id)
        signup_user.wishlist.remove(book)
        return JsonResponse({'message': 'Book removed from Wishlist.'})
    else:
        return JsonResponse({'error': 'Invalid request.'}, status=400)
    
def main(request):
    isLogged = request.session.get('isLogged')
    is_admin = request.session.get('is_admin')
    context = {
        'isLogged':isLogged,
        'is_admin':is_admin,
    }
    return render(request, 'pages/main.html' , context)

def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        form = EditBookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('view')  
    else:
        form = EditBookForm(instance=book)
    return render(request, 'pages/edit_book.html', {'form': form})

def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('view')
    return render(request, 'pages/delete_book.html', {'book': book})

def details(request, id):
    try:
        book = Book.objects.get(id=id)
    except Book.DoesNotExist:
        return HttpResponseBadRequest('Book does not exist')

    signup_user_id = request.session.get('user_id')
    if not signup_user_id:
        return HttpResponseBadRequest('User not authenticated')

    try:
        signup_user = Signup.objects.get(id=signup_user_id)
    except Signup.DoesNotExist:
        return HttpResponseBadRequest('User does not exist')

    if request.method == 'POST' and 'add-to-wishlist' in request.POST:
        signup_user.wishlist.add(book)
        return JsonResponse({'status': 'success'})

    is_loved = signup_user.wishlist.filter(id=book.id).exists()

    context = {
        'book': book,
        'is_loved': is_loved
    }
    return render(request, 'pages/details.html', context)

def add_to_cart(request, book_id):
    if request.method == 'POST':
        book = get_object_or_404(Book, id=book_id)
        if 'user_id' in request.session:
            signup_user = Signup.objects.get(id=request.session['user_id'])
            if book not in signup_user.cart.all():
                signup_user.cart.add(book)
                message = book.name + ' added to cart.'
            else:
                message = book.name + ' is already in the cart.'
        else:
            message = 'User is not logged in.'
        return JsonResponse({'message': message})
    else:
        return JsonResponse({'message': 'Invalid request.'})
    # return redirect(request.META.get('HTTP_REFERER', 'view'))
    
def add_love(request, book_id):
    if request.method == 'POST':
        book = get_object_or_404(Book, id=book_id)
        if 'user_id' in request.session:
            signup_user = Signup.objects.get(id=request.session['user_id'])
            if book not in signup_user.wishlist.all():
                signup_user.wishlist.add(book)
                message = book.name + ' is added to your loved books.'
                status = 'success'
            else:
                message = book.name + ' is already in your loved books.'
                status = 'already_in_wishlist'
        else:
            message = 'User is not logged in.'
            status = 'login_required'
        return JsonResponse({'message': message, 'status': status})
    else:
        return JsonResponse({'message': 'Invalid request.'}, status=400)

def wishlist(request):
    isLogged = request.session.get('isLogged')
    is_admin = request.session.get('is_admin')

    user_name = request.session.get('username')
    
    if not user_name:
        return redirect('LoginSignup')
    
    user = Signup.objects.get(username=user_name)
    wishlist_items = user.wishlist.all()

    context = {
        'wishlist_items': wishlist_items,
        'isLogged':isLogged,
        'is_admin':is_admin,
    }
    return render(request, 'pages/wishlist.html', context)

def signup(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'redirect': True})
        else:
            errors = form.errors.get_json_data()
            return JsonResponse({'success': False, 'errors': errors})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request'})

def login(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        login_form = loginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['usernameLogin']
            password = login_form.cleaned_data['passwordLogin']
            try:
                signup_user = Signup.objects.get(username=username)
                if signup_user.password == password:
                    request.session['user_id'] = signup_user.id
                    request.session['username'] = signup_user.username
                    request.session['is_admin'] = signup_user.isAdmin
                    request.session['isLogged'] = True
                    return JsonResponse({'success': True, 'redirect': '/view/'})
                else:
                    return JsonResponse({'success': False, 'message': 'Invalid username or password'})
            except Signup.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'Invalid username or password'})
        else:
            pass
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request'})

def render_login_signup_page(request):
    # if request.method == 'GET':
        form = SignupForm()
        login_form = loginForm()
        return render(request, 'pages/LoginSignup.html', {
            'SignupForm': form,
            'loginForm': login_form
        })

def account(request):
    isLogged = request.session.get('isLogged')
    is_admin = request.session.get('is_admin')
    if isLogged:
        username = request.session.get('username', 'default')
        user = Signup.objects.get(username=username)
        profile_picture_url = user.profilePicture.url if user.profilePicture else None

        if request.method == 'POST':
            profile_photo_form = ProfilePhotoForm(request.POST, request.FILES, instance=user)
            if profile_photo_form.is_valid():
                profile_photo_form.save()
                messages.success(request, 'Profile photo updated successfully.')
                return redirect('account')
        else:
            profile_photo_form = ProfilePhotoForm(instance=user)

        borrowed_books = user.borrowed_books.filter(status='borrowed')
        
        context = {
            'username': username,
            'profilePicture': profile_picture_url,
            'profilePhotoForm': profile_photo_form,
            'isLogged': isLogged,
            'is_admin': is_admin,
            'borrowed_books': borrowed_books,
        }
        return render(request, 'pages/accountUser.html', context)
    else:
        return redirect('LoginSignup')

def logout(request):
    request.session['isLogged'] = False
    return redirect('LoginSignup') 

def navbarAdmin(request):
    isLogged = request.session.get('isLogged')
    is_admin = request.session.get('is_admin')
    context = {
        'is_admin' : is_admin,
        'isLogged' : isLogged,
    }
    return render(request, 'parts/nav.html', context)

def status_details(request, book_id):
    if request.method == 'POST':
        new_status = request.POST.get('new_status')

        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            pass
        else:
            book.status = new_status
            book.save()
            return JsonResponse({'message': 'Status updated successfully'})
    return HttpResponseBadRequest('Invalid request')

def status_views(request, book_id):
    if request.method == 'POST':
        new_status = request.POST.get('new_status')

        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            pass
        else:
            book.status = new_status
            book.save()
            return JsonResponse({'message': 'Status updated successfully'})
    return HttpResponseBadRequest('Invalid request')

def borrow_books(request):
    if request.method == 'POST':
        username = request.session.get('username')
        user = Signup.objects.get(username=username)
        cart_books = user.cart.filter(status='available')
        
        if not cart_books:
            return JsonResponse({'error': 'No available books in the cart'}, status=400)
        
        for book in cart_books:
            book.status = 'borrowed'
            book.save()
            user.cart.remove(book)
            user.borrowed_books.add(book)

        return JsonResponse({'success': 'Books successfully borrowed'})
    return JsonResponse({'error': 'Invalid request'}, status=400)
