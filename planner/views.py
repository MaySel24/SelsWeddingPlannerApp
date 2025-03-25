from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import user_passes_test, login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Sum, F
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Guest, Task, Vendor, Budget, WeddingColor, Profile, TotalBudget
from .forms import GuestForm, TaskForm, VendorForm, BudgetForm, WeddingColorForm, TaglineForm, TotalBudgetForm, \
    LoginForm

# ========================= DASHBOARD =========================
@login_required  # Now all authenticated users can access views
def dashboard_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    form = TaglineForm(instance=profile)

    if request.method == "POST":
        form = TaglineForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Tagline updated successfully!")
            return redirect('planner:dashboard')

    context = {
        'tasks_count': Task.objects.count(),
        'guests_count': Guest.objects.count(),
        'vendors_count': Vendor.objects.count(),
        'budgets_count': Budget.objects.count(),
        'form': form,
        'tagline': profile.tagline,
    }
    return render(request, 'planner/dashboard.html', context)

# ========================= GUESTS =========================
@login_required
def guests_view(request):
    guests = Guest.objects.all()

    # Calculate RSVP statistics
    total_guests = guests.count()
    total_accepted = guests.filter(rsvp_status='Yes').count()
    total_declined = guests.filter(rsvp_status='No').count()
    total_pending = guests.filter(rsvp_status='Pending').count()

    print(f"Total Guests: {total_guests}, Accepted: {total_accepted}, Declined: {total_declined}, Pending: {total_pending}")

    paginator = Paginator(guests, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'total_guests': total_guests,
        'total_accepted': total_accepted,
        'total_declined': total_declined,
        'total_pending': total_pending,
    }
    return render(request, 'planner/guests.html', context)


@login_required
def add_guest(request):
    if request.method == "POST":
        form = GuestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('planner:guest_list'))
    else:
        form = GuestForm()
    return render(request, 'planner/add_guest.html', {'form': form})


@login_required
def edit_guest(request, pk):
    guest = get_object_or_404(Guest, id=pk)
    if request.method == "POST":
        form = GuestForm(request.POST, instance=guest)
        if form.is_valid():
            form.save()
            return redirect(reverse('planner:guest_list'))
    else:
        form = GuestForm(instance=guest)
    return render(request, 'planner/edit_guest.html', {'form': form})

@login_required
def delete_guest(request, pk):
    guest = get_object_or_404(Guest, id=pk)
    if request.method == "POST":
        guest.delete()
        return redirect(reverse('planner:guest_list'))
    return render(request, 'planner/delete_guest.html', {'guest': guest})


# ========================= TASKS =========================
@login_required
def tasks_view(request):
    tasks = Task.objects.all().order_by(
        'status',  # Ensure 'Pending' tasks appear first
        'due_date'  # Then sort by closest due date
    )
    # Pagination: Display 5 tasks per page
    paginator = Paginator(tasks, 5)
    page_number = request.GET.get('page')
    page_tasks = paginator.get_page(page_number)

    context = {
        'tasks': page_tasks,
        'username': request.user.username if request.user.is_authenticated else None  # Safe check for username
    }

    return render(request, 'planner/tasks.html', context)

# ========================= ADD TASK =========================
@login_required
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Task added successfully!")
            return redirect('planner:task_list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = TaskForm()

    return render(request, 'planner/add_task.html', {'form': form})


# ========================= EDIT TASK =========================
@login_required
def edit_task(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, "Task updated successfully!")
            return redirect('planner:task_list')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = TaskForm(instance=task)

    return render(request, 'planner/edit_task.html', {'form': form, 'task': task})

# ========================= DELETE TASK =========================
@login_required
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.method == 'POST':
        task.delete()
        messages.success(request, "Task deleted successfully!")
        return redirect('planner:task_list')

    return render(request, 'planner/delete_task.html', {'task': task})


# ========================= COMPLETE TASK =========================
@login_required
def complete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if task.status != 'completed':  # Prevent redundant updates
        task.status = 'completed'
        task.save()
        messages.success(request, f"Task '{task.title}' marked as completed!")
    else:
        messages.info(request, "This task is already completed.")

    return redirect('planner:task_list')

# ========================= VENDORS =========================
@login_required
def vendors_view(request):
    vendors = Vendor.objects.all().order_by('name')
    paginator = Paginator(vendors, 10)  # Paginate vendors (10 per page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'planner/vendors.html', {'page_obj': page_obj})

@login_required
def add_vendor(request):
    if request.method == "POST":
        form = VendorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('planner:vendor_list')
    else:
        form = VendorForm()
    return render(request, 'planner/add_vendor.html', {'form': form})

@login_required
def edit_vendor(request, pk):
    vendor = get_object_or_404(Vendor, pk=pk)
    if request.method == "POST":
        form = VendorForm(request.POST, instance=vendor)
        if form.is_valid():
            form.save()
            return redirect('planner:vendor_list')
    else:
        form = VendorForm(instance=vendor)
    return render(request, 'planner/edit_vendor.html', {'form': form, 'vendor': vendor})

@login_required
def delete_vendor(request, pk):
    vendor = get_object_or_404(Vendor, pk=pk)
    if request.method == "POST":
        vendor.delete()
        return redirect('planner:vendor_list')
    return render(request, 'planner/delete_vendor.html', {'vendor': vendor})

    # ========================= BUDGETS =========================
@login_required
def budgets_view(request):
    query = request.GET.get('q', '')
    filter_type = request.GET.get('filter', '')

    budgets = Budget.objects.order_by('category')  # Order first
    if query:
        budgets = budgets.filter(category__icontains=query)
    if filter_type == "overspent":
        budgets = budgets.filter(amount_spent__gt=F('amount_allocated'))
    elif filter_type == "remaining_low":
        budgets = budgets.filter(remaining_balance__lt=500)

    total_allocated = budgets.aggregate(Sum('amount_allocated'))['amount_allocated__sum'] or 0
    total_spent = budgets.aggregate(Sum('amount_spent'))['amount_spent__sum'] or 0
    total_remaining = total_allocated - total_spent

    # Fetch the manually set total budget
    total_budget = TotalBudget.objects.first()
    if total_budget:
        budget_amount = total_budget.amount

        if total_spent > budget_amount:
            budget_status = "Over Budget"
        elif total_spent == budget_amount:
            budget_status = "Exact Budget"
        elif total_spent >= (budget_amount * Decimal("0.75")):  # 75% of budget
            budget_status = "Approaching Budget"
        else:
            budget_status = "Within Budget"

        # Calculate progress percentage
        budget_progress = min((total_spent / budget_amount) * 100 if budget_amount > 0 else 0, 100) # Cap at 100%
    else:
        budget_amount = None
        budget_status = "No Budget Set"
        budget_progress = 0  # No progress if no budget is set

    paginator = Paginator(budgets.order_by('category'), 10)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'planner/budgets.html', {
        'page_obj': page_obj,
        'total_allocated': total_allocated,
        'total_spent': total_spent,
        'total_remaining': total_remaining,
        'total_budget': budget_amount,
        'budget_status': budget_status,
        'budget_progress': budget_progress,  # Pass progress to the template
    })

# ========================= ADD BUDGET =========================
@login_required
def add_budget(request):
    if request.method == "POST":
        form = BudgetForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Budget added successfully!")
            return redirect('planner:budget_list')
        else:
            messages.error(request, "Error adding budget. Please check the form.")
    else:
        form = BudgetForm()

    return render(request, 'planner/add_budget.html', {'form': form})

# ========================= EDIT BUDGET =========================
@login_required
def edit_budget(request, pk):
    budget = get_object_or_404(Budget, id=pk)

    if request.method == "POST":
        form = BudgetForm(request.POST, instance=budget)
        if form.is_valid():
            form.save()
            messages.success(request, "Budget updated successfully!")
            return redirect('planner:budget_list')
        else:
            messages.error(request, "Error updating budget. Please check the form.")

    else:
        form = BudgetForm(instance=budget)

    return render(request, 'planner/edit_budget.html', {'form': form, 'budget': budget})

# ========================= DELETE BUDGET =========================
@login_required
def delete_budget(request, pk):
    budget = get_object_or_404(Budget, id=pk)

    if request.method == "POST":
        budget.delete()
        messages.success(request, "Budget deleted successfully!")
        return redirect('planner:budget_list')

    return render(request, 'planner/delete_budget.html', {'budget': budget})

# ========================= EDIT TOTAL BUDGET =========================
@login_required
def total_budget_view(request):
    budget, created = TotalBudget.objects.get_or_create(id=1)  # Ensure only one budget exists

    if request.method == 'POST':
        form = TotalBudgetForm(request.POST, instance=budget)
        if form.is_valid():
            form.save()
            return redirect('planner:budget_list')  # Redirect after saving

    else:
        form = TotalBudgetForm(instance=budget)

    return render(request, 'planner/total_budget.html', {'form': form, 'budget': budget})

# ========================= WEDDING COLOR =========================
# View to list all colors
@login_required
def color_list(request):
    colors = WeddingColor.objects.all()
    return render(request, 'planner/color_list.html', {'colors': colors})

# View to add a new color
@login_required
def add_color(request):
    if request.method == 'POST':
        form = WeddingColorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('planner:color_list')
    else:
        form = WeddingColorForm()
    return render(request, 'planner/add_color.html', {'form': form})

# View to edit an existing color
@login_required
def edit_color(request, color_id):
    color = get_object_or_404(WeddingColor, id=color_id)
    if request.method == 'POST':
        form = WeddingColorForm(request.POST, instance=color)
        if form.is_valid():
            form.save()
            return redirect('planner:color_list')
    else:
        form = WeddingColorForm(instance=color)
    return render(request, 'planner/edit_color.html', {'form': form, 'color': color})

# View to delete a color
@login_required
def delete_color(request, color_id):
    color = get_object_or_404(WeddingColor, id=color_id)
    if request.method == 'POST':
        color.delete()
        return redirect('planner:color_list')
    return render(request, 'planner/delete_color.html', {'color': color})

# Tagline
@login_required
def edit_tagline(request):
    profile, created = Profile.objects.get_or_create(user=request.user)  # Ensure Profile exists

    if request.method == 'POST':
        if 'reset' in request.POST:  # If Reset button was clicked
            profile.tagline = "Every love story is beautiful, but yours is our favorite"  # Set a default tagline
            profile.save()
            return redirect('planner:dashboard')  # Redirect after resetting

        form = TaglineForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('planner:dashboard')

    else:
        form = TaglineForm(instance=profile)

    return render(request, 'planner/edit_tagline.html', {'form': form, 'current_tagline': profile.tagline})


