from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category, Project, ContactRequest, Review
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django import forms
from django.contrib.auth.models import User

class RegistracijaSuEmail(UserCreationForm):
    email = forms.EmailField(required=True, label="El. paštas")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

def home(request):
    featured_products = Product.objects.all()[:6]
    return render(request, 'home.html', {'products': featured_products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_detail.html', {'product': product})

def about(request):
    description = """
    MB „Olrosta“ – tai šeimos vertybėmis grįstas verslas, kurio pamatas yra saugumas ir ilgaamžiškumas. 
    Mes specializuojamės aukščiausios kokybės tvorų gamyboje bei preciziškuose stogo lankstinių sprendimuose. 
    Mūsų tikslas – suteikti Jūsų namams ne tik estetinį vientisumą, bet ir ramybės jausmą, 
    žinant, kad pasirinkti sprendimai tarnaus dešimtmečius.
    """
    return render(request, 'about.html', {'content': description})

def product_list(request):
    categories = Category.objects.prefetch_related('products').all()
    return render(request, 'products.html', {'categories': categories})

def projects(request):
    all_projects = Project.objects.all()
    return render(request, 'projects.html', {'projects': all_projects})

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        interest = request.POST.get('interest', 'Bendra užklausa')
        message = request.POST.get('message')
        
        ContactRequest.objects.create(
            name=name, email=email, phone=phone, 
            product_interest=interest, message=message
        )
        messages.success(request, 'Dėkojame! Jūsų užklausa gauta, susisieksime artimiausiu metu.')
        return redirect('contact')
        
    return render(request, 'contact.html')

def category_detail(request, pk):
    cat = get_object_or_404(Category, pk=pk)
    return render(request, 'category.html', {'category': cat})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    related_products = Product.objects.filter(category=product.category).exclude(pk=pk)[:3]
    
    return render(request, 'product_detail.html', {
        'product': product,
        'related_products': related_products
    })

def register(request):
    if request.method == 'POST':
        form = RegistracijaSuEmail(request.POST) # Naudojame naują formą
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegistracijaSuEmail() 
    return render(request, 'registration/register.html', {'form': form})

def add_review(request, product_id):
    if request.method == 'POST' and request.user.is_authenticated:
        product = get_object_or_404(Product, pk=product_id)
        content = request.POST.get('content')
        
        Review.objects.create(
            product=product,
            user=request.user,
            content=content
        )
        return redirect('product_detail', pk=product_id)
    return redirect('home')
