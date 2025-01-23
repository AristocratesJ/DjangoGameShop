from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.http import HttpResponseRedirect
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse

from .models import Game, Developer, Category, CartItem, Order, OrderItem
from .tokens import account_activation_token
from .forms import RegisterForm, ForgotPasswordForm, ResetPasswordForm, GameForm


def index_view(request):
    return render(request, 'index.html')


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('index')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            # logic of validation token
            current_site = get_current_site(request)
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            print(message)
            return render(request, 'register_check_email.html')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def cart_view(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
    else:
        cart_items = []
    context = {
        'cart_items': cart_items
    }
    return render(request, 'cart.html', context)


@login_required
def add_to_cart_view(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    existing_item = CartItem.objects.filter(user=request.user, game=game).first()

    if game.seller == request.user:
        messages.error(request, "You cannot add your own game to your cart.")
        return redirect('game_details', game_id=game.id)

    if existing_item:
        messages.info(request, "This game is already in your cart.")
    else:
        # If not in cart, add new item
        CartItem.objects.create(user=request.user, game=game)
        messages.success(request, f'"{game}" added to your cart!')

    return redirect('game_details', game_id=game.id)


@login_required
def delete_from_cart_view(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, user=request.user)
    cart_item.delete()
    messages.success(request, "The item was removed from your cart!")
    return redirect('cart')


@login_required
def checkout_view(request):
    cart_items = CartItem.objects.filter(user=request.user)

    if not cart_items:
        messages.info(request, "Your cart is empty. Add some games to check out.")
        return redirect('cart')

    for item in cart_items:
        if item.game.quantity < 1:
            messages.error(
                request,
                f'Sorry, "{item.game}" is out of stock. Remove it from your cart to proceed.'
            )
            return redirect('cart')

    order = Order.objects.create(user=request.user)

    for item in cart_items:
        item.game.quantity -= 1
        item.game.save()

        OrderItem.objects.create(
            order=order,
            game=item.game
        )

    cart_items.delete()

    messages.success(request, "Checkout successful! Your order has been placed.")
    return redirect('store')


def user_details_view(request):
    added_games = Game.objects.filter(seller=request.user)

    # adding quantity logic
    if request.method == 'POST':
        game_id = request.POST.get('game_id')
        new_quantity = request.POST.get('quantity')

        try:
            game = get_object_or_404(Game, id=game_id, seller=request.user)
            if new_quantity.isdigit() and int(new_quantity) > 0:
                game.quantity = int(new_quantity) + game.quantity
                game.save()
                messages.success(request, f'Updated quantity of "{game}" to {game.quantity}.')
            else:
                messages.error(request, 'Invalid quantity. Please enter a positive number.')
        except Exception as e:
            messages.error(request, 'An error occurred while updating the quantity.')

    context = {
        'added_games': added_games
    }
    return render(request, 'user_details.html', context)


def game_details_view(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    context = {
        'game': game,
        'dev': Developer.objects.get(id=game.developer.id),
    }
    return render(request, 'game_details.html', context)


def store_view(request):
    context = {
        'games': Game.objects.all()
    }
    return render(request, 'store.html', context)


def logout_view(request):
    logout(request)
    return redirect('index')


@login_required
def add_game_view(request):
    form = GameForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        game = form.save(commit=False)
        game.seller = request.user
        game.save()
        # if form is valid
        return redirect('store')
    context = {
        'form': form,
        'devs': Developer.objects.all(),
        'categories': Category.objects.all()
    }
    return render(request, "game_add.html", context)

@login_required
def update_game_view(request, game_id):
    game = get_object_or_404(Game, id=game_id, seller=request.user)
    form = GameForm(request.POST or None, request.FILES or None, instance=game)
    if form.is_valid():
        game = form.save(commit=False)
        game.save()
        return redirect('profile')
    return render(request, "game_update.html", {'form': form, 'game': game})


@login_required
def delete_game_view(request, game_id):
    game = get_object_or_404(Game, id=game_id, seller=request.user)

    if request.method == "POST":
        game.delete()
        return redirect('profile')

    return redirect('profile')


# Function for validation email by "sending" token
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'register_check_confirmed.html')
    else:
        return HttpResponse('Activation link is invalid!')


# Forgot password (send email with reset link)
def forgot_password_view(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                current_site = get_current_site(request)
                domain = current_site.domain
                # Generate the reset link
                uid = urlsafe_base64_encode(force_bytes(str(user.pk)))
                token = default_token_generator.make_token(user)
                reset_url = f"http://{domain}/reset_password/{uid}/{token}/"
                print(f"Reset password link: {reset_url}")
                return HttpResponseRedirect(reverse('reset_password_link_sent'))
            except User.DoesNotExist:
                form.add_error('email', 'No user with this email exists.')
    else:
        form = ForgotPasswordForm()

    return render(request, 'forgot_password.html', {'form': form})


# Reset password (form)
def reset_password_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        print(uid)
        user = User.objects.get(pk=uid)
        # Validate the token
        if not default_token_generator.check_token(user, token):
            return render(request, "invalid_reset_token.html")
    except (User.DoesNotExist, ValueError, TypeError):
        return render(request, "invalid_reset_token.html")

    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            user.password = make_password(password)
            user.save()
            return redirect('login')
    else:
        form = ResetPasswordForm()

    return render(request, 'reset_password.html', {'form': form})
