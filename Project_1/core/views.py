from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Customer
from django.contrib.auth.hashers import make_password,check_password
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from product_app.models import Product,Order

# Create your views here.


def sign_up(request):
    if request.method == "POST":
        firstname = request.POST.get("firstname")
        last = request.POST.get("lastname")
        email = request.POST.get("email")
        address = request.POST.get("address")
        image = request.FILES.get("image")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        hashed_password = make_password(password)
        if password != confirm_password:
            messages.error(request, "Password doesn't match ")
            return redirect("signup")
        
        Customer.objects.create(firstname = firstname , lastname = last, email_address=email, image=image, address = address,password=hashed_password)
        messages.success(request, "Signup successful! You can now log in.")
        return render(request, "core/login.html")
    return render(request,"core/signup.html")


def log_in(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        try:
            customer = Customer.objects.get(email_address=email)
            if check_password(password, customer.password):
                request.session['customer_id'] = customer.id
                request.session['customer_email'] = customer.email_address
                return render(request, 'product_app/home.html', {"customer": customer})
            else:
                return HttpResponse("Invalid password ")
        except Customer.DoesNotExist:
            return HttpResponse("Invalid Email")
    
    return render(request, 'core/login.html')

def log_out(request):
    logout(request)
    # request.session.flush()  # Clears all session data
    return render(request, 'core/logout.html')
    
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def admin_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, username=email, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect("home")  # Redirect to admin dashboard
        else:
            messages.error(request, "Invalid email or password")
    return render(request, 'core/admin_login.html')

def admin_page(request):
    return render(request, 'core/admin_page.html')

def admin_customer(request):
    customer = Customer.objects.all()
    # product = Product.objects.all()
    return render(request, "core/admin_customer.html", {"customer": customer})

def admin_products(request):
    orders = Order.objects.all()
    return render(request, "core/admin_products.html", {"orders": orders})
   
def product_admin(request):
    products = Product.objects.all()
    return render(request, "core/product_admin.html", {"products": products})    

def delete_product(request):
    product_id = request.GET.get("product_id")
    product = Product.objects.get(id = product_id)
    product.delete()
    return redirect('product_admin')

def edit_product(request):
    product_id = request.GET.get("product_id")
    product = Product.objects.get(id = product_id)
    return render (request, "product_app/add_product.html" ,{"product":product})   