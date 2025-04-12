from django.urls import path
from app import views
from django.contrib.auth import views as auth_view
from . forms import LoginForm, MyPasswordResetForm, MyPasswordChangeForm, MyPasswordSetForm

urlpatterns = [
    path("", views.index, name="index"),
    path("category/<slug:val>", views.CategoryView.as_view(), name="category"),
    path("category-name/<val>", views.CategoryNameView.as_view(), name="category-name"),
    path("item-details/<int:pk>", views.ItemDetailsView.as_view(), name="item-details"),
    path("aboutus", views.about_us, name="about_us"),
    path("contact", views.contact, name="contact"),

    path("register", views.RegistrationView.as_view(), name="register"),
    path("accounts/login/", auth_view.LoginView.as_view(template_name="app/login.html", authentication_form=LoginForm), name="login"),
    path("password-change/", auth_view.PasswordChangeView.as_view(template_name="app/password_change.html", form_class=MyPasswordChangeForm, success_url="/passwordchangedone"), name="password-change"),
    path("passwordchangedone/", auth_view.PasswordResetDoneView.as_view(template_name="app/password_change_done.html"), name="password-change-done"),
    path("logout/", auth_view.LogoutView.as_view(next_page="login"), name="logout"),

    path("password-reset/", auth_view.PasswordResetView.as_view(template_name="app/password_reset.html", form_class=MyPasswordResetForm), name="password-reset"),
    path("password-reset/done/", auth_view.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'), name="password_reset_done"),
    path("password-reset-confirm/<uidb64>/<token>/", auth_view.PasswordResetConfirmView.as_view(template_name="app/password_reset_confirm.html", form_class=MyPasswordSetForm), name="password_reset_confirm"),
    path("password-reset-complete/", auth_view.PasswordResetCompleteView.as_view(template_name="app/password_reset_complete.html"), name="password_reset_complete"),

    path("profile/", views.profile, name="profile"),
    path("profile-setting/", views.ProfileSettingView.as_view(), name="profile-setting"),
    path("updateProfile/<int:pk>/", views.UpdateProfileView.as_view(), name="update-profile"),
    path("deleteaddress/<int:pk>/", views.delete_address, name="delete_address"),

    path("add-to-cart", views.add_to_cart, name="add-to-cart"),
    path("cart/", views.show_cart, name="show-cart"),
    path("increaseitem/", views.increase_item),
    path("decreaseitem/", views.decrease_item),
    path("removeitem/", views.remove_item),
    path("checkout/", views.CheckoutView.as_view(), name="checkout"),
    path("payment_success/", views.payment_success, name="payment_success"),
    path("orders/", views.orders, name="orders"),
    path("orders-status/<val>", views.OrderStatusView.as_view(), name="orders-status"),
    path("wishlist/", views.show_wishlist, name="show-wishlist"),
    path("addwishlist/", views.add_wishlist),
    path("removewishlist/", views.remove_wishlist),
    path("search/", views.search, name="search"),

]
