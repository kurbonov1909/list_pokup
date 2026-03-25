from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from .models import Store, Purchase
from .forms import StoreForm, PurchaseForm, UserForm
from datetime import datetime


def is_admin(user):
    return user.is_authenticated and user.is_superuser


def is_worker(user):
    return user.is_authenticated and user.is_staff and not user.is_superuser


def home(request):
    return render(request, 'list/home.html')

@login_required
@user_passes_test(is_admin)
def add_store(request):
    if request.method == 'POST':
        form = StoreForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Magazin qo\'shildi!')
            return redirect('home')
    else:
        form = StoreForm()
    return render(request, 'list/add_store.html', {'form': form})

@login_required
def add_purchase(request):
    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        if form.is_valid():
            purchase = form.save(commit=False)
            purchase.user = request.user
            purchase.save()
            messages.success(request, 'Xarid qo\'shildi!')
            return redirect('home')
    else:
        form = PurchaseForm()
    return render(request, 'list/add_purchase.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def add_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_staff = True
            user.is_superuser = False
            user.save()
            messages.success(request, 'Foydalanuvchi qo\'shildi!')
            return redirect('home')
    else:
        form = UserForm()
    return render(request, 'list/add_user.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def monthly_report(request):
    month = request.GET.get('month', datetime.now().strftime('%Y-%m'))
    store_id = request.GET.get('store')
    year, mon = month.split('-')
    purchases = Purchase.objects.filter(date__year=year, date__month=mon)
    selected_store = None
    if store_id:
        purchases = purchases.filter(store_id=store_id)
        selected_store = Store.objects.get(id=store_id)
    
    total_purchase_cost = sum(purchase.total_cost for purchase in purchases)
    
    stores = Store.objects.all()
    
    context = {
        'purchases': purchases,
        'total_purchase_cost': total_purchase_cost,
        'month': month,
        'stores': stores,
        'selected_store': selected_store,
    }
    return render(request, 'list/monthly_report.html', context)

@login_required
def my_purchases(request):
    purchases = Purchase.objects.filter(user=request.user).order_by('-date')
    total_purchase_cost = sum(purchase.total_cost for purchase in purchases)
    
    context = {
        'purchases': purchases,
        'total_purchase_cost': total_purchase_cost,
    }
    return render(request, 'list/my_purchases.html', context)
