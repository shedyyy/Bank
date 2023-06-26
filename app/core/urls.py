from django.urls import path
from core import views

urlpatterns = [
    path("", views.home_view, name="index"),
    path("deposit/", views.deposit_view, name="deposit"),
    path("transfer/", views.transfer_view, name="transfer"),
    path("transactions/", views.transactions_view, name="transactions"),

    path("<int:t_id>/approve/", views.approve_view, name="approve"),
    path("<int:t_id>/reject/", views.reject_view, name="reject"),
]
