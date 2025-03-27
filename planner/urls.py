from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    dashboard_view,
    guests_view, add_guest, edit_guest, delete_guest,
    tasks_view, add_task, edit_task, delete_task, complete_task,
    vendors_view, add_vendor, edit_vendor, delete_vendor,
    budgets_view, add_budget, edit_budget, delete_budget,
    color_list, add_color, edit_color, delete_color, edit_tagline, total_budget_view
)

# Namespace for app (prevents conflicts in multi-app projects)
app_name = 'planner'

urlpatterns = [
    # ========================= DASHBOARD =========================
    path('', dashboard_view, name='dashboard'),

    # ========================= GUESTS =========================
    path('guests/', guests_view, name='guest_list'),
    path('guests/add/', add_guest, name='add_guest'),
    path('guests/edit/<int:pk>/', edit_guest, name='edit_guest'),
    path('guests/delete/<int:pk>/', delete_guest, name='delete_guest'),

    # ========================= TASKS =========================
    path('tasks/', tasks_view, name='task_list'),
    path('tasks/add/', add_task, name='add_task'),
    path('tasks/edit/<int:pk>/', edit_task, name='edit_task'),
    path('tasks/delete/<int:pk>/', delete_task, name='delete_task'),
    path('tasks/complete/<int:pk>/', complete_task, name='complete_task'),

    # ========================= VENDORS =========================
    path('vendors/', vendors_view, name='vendor_list'),
    path('vendors/add/', add_vendor, name='add_vendor'),
    path('vendors/edit/<int:pk>/', edit_vendor, name='edit_vendor'),
    path('vendors/delete/<int:pk>/', delete_vendor, name='delete_vendor'),

    # ========================= BUDGETS =========================
    path('budgets/', budgets_view, name='budget_list'),
    path('budgets/add/', add_budget, name='add_budget'),
    path('budgets/edit/<int:pk>/', edit_budget, name='edit_budget'),
    path('budgets/delete/<int:pk>/', delete_budget, name='delete_budget'),
    path('budgets/total/', total_budget_view, name='total_budget'),

    # ========================= WEDDING COLORS =========================
    path('colors/', color_list, name='color_list'),
    path('colors/add/', add_color, name='add_color'),
    path('colors/edit/<int:pk>/', edit_color, name='edit_color'),
    path('colors/delete/<int:pk>/', delete_color, name='delete_color'),

    # ========================= TAGLINE =========================
    path('tagline/edit/', edit_tagline, name='edit_tagline'),

    # ========================= TOTAL BUDGET =========================
    path('set-budget/', total_budget_view, name='set_budget'),
    
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]