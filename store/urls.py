from django.urls import path, re_path
from .views import (cart_view, checkout_view, game_details_view, index_view, login_view, register_view,
                    user_details_view, store_view, logout_view, activate, forgot_password_view,
                    reset_password_view, add_game_view, delete_game_view, add_to_cart_view,
                    delete_from_cart_view, update_game_view)
from django.views.generic import TemplateView

urlpatterns = [
    path('', index_view, name='index'),
    path('store/', store_view, name='store'),
    path('store/add-game', add_game_view, name='add_game'),
    path('store/delete-game/<int:game_id>/', delete_game_view, name='delete_game'),
    path('store/update-game/<int:game_id>/', update_game_view, name='update_game'),
    path('store/game/<int:game_id>/', game_details_view, name='game_details'),
    path('cart/', cart_view, name='cart'),
    path('cart/add-to-cart/<int:game_id>/', add_to_cart_view, name='add_to_cart'),
    path('cart/delete/<int:cart_item_id>/', delete_from_cart_view, name='delete_from_cart'),
    path('cart/checkout/', checkout_view, name='checkout'),
    path('profile/', user_details_view, name='profile'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    # sign up validation path
    path('activate/<str:uidb64>/<str:token>/', activate, name='activate'),
]