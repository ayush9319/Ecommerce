from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Product,Order
from core.models import Customer
import datetime
from django.shortcuts import render, get_object_or_404

# Create your views here.
def test(request):
    return render (request, "product_app/test.html")

def home(request,customer=None):
    customer_id = request.GET.get('customer_id')  # Get from URL
    if customer_id:
        try:
            customer = Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            pass  # If ID is invalid, customer remains None

    return render (request, "product_app/home.html",{"customer":customer})

from django.shortcuts import render, redirect
from .models import Product

def add_product(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")  # Check if editing an existing product
        
        if product_id:
            product = Product.objects.get(id=product_id)
        else:
            product = Product()

        # Update product fields
        product.name = request.POST.get("name")
        product.descr = request.POST.get("descr")
        product.price = request.POST.get("price")
        product.stock = request.POST.get("stock")
        product.category = request.POST.get("category")

        # Handle Image Upload
        if "image" in request.FILES:  # If a new image is uploaded
            product.image = request.FILES["image"]
        else:  # If no new image, keep the existing one
            existing_image_url = request.POST.get("existing_image")
            if existing_image_url:
                product.image.name = existing_image_url.replace('/media/', '')  # Remove "/media/" part for saving

        product.save()
        return redirect("home")  # Redirect after saving

    return render(request, "product_app/add_product.html")



def category_products(request,customer=None):
    customer_id = request.GET.get('customer_id')  # Get from URL
    if customer_id:
        try:
            customer = Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            pass  # If ID is invalid, customer remains None
    
    category = request.GET.get("category")
    if category and category.strip():
        products = Product.objects.filter(category=category)
        if not products:
            products = Product.objects.all()   
    return render(request,"product_app/category_products.html",{"product":products,"customer":customer})
                        
   

def contact_details(request,customer=None):
    customer_id = request.GET.get('customer_id')  # Get from URL
    if customer_id:
        try:
            customer = Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            pass  # If ID is invalid, customer remains None

    return render(request, "product_app/contact.html",{"customer":customer})


def profile_details(request, customer=None):
    customer_id = request.GET.get('customer_id')  # Get customer_id from URL
    if customer_id:
        try:
            customer = Customer.objects.get(id=customer_id)
            orders = Order.objects.filter(customer_id=customer_id)
            print(orders)
            print(customer.image)
        except Customer.DoesNotExist:
            customer = None
            orders = []
            # You could optionally redirect the user or show an error message
            # return redirect('error_page') # Or return an error message in the context
    else:
        customer = None
        orders = []

    return render(request, "product_app/profile.html", {"customer": customer, "orders": orders})

def product_list(request,customer=None):
    query = request.GET.get("q","")
    products = Product.objects.filter(name__icontains = query) if query else Product.objects.all()
    customer_id = request.GET.get('customer_id')  # Get from URL
    if customer_id:
        try:
            customer = Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            pass  # If ID is invalid, customer remains None
    # product = Product.objects.all()
    return render(request, "product_app/product_list.html",{"product":products,"customer":customer,})

def about(request,customer=None):
    customer_id = request.GET.get('customer_id')  # Get from URL
    if customer_id:
        try:
            customer = Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            pass
    return render(request, "product_app/about.html",{"customer":customer})


def product_desc(request,product=None,customer=None):
    customer_id = request.GET.get('customer_id')  # Get from URL
    if customer_id:
        try:
            customer = Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            pass
    product_id = request.GET.get('product_id')
    if product_id :
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            pass  # If ID is invalid, product remains None
    return render(request, "product_app/product_desc.html",{"product":product,"customer":customer}) 


from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, render
import datetime
from django.conf import settings

def buying(request):
    customer = None
    product = None

    # Get customer_id and product_id from URL parameters (GET request)
    customer_id = request.GET.get("customer_id")
    product_id = request.GET.get("product_id")

    if customer_id:
        customer = get_object_or_404(Customer, id=customer_id)  # Ensures customer exists
    
    if product_id:
        product = get_object_or_404(Product, id=product_id)  # Ensures product exists

    if request.method == "POST":
        customer_id = request.POST.get("customer_id")
        product_id = request.POST.get("product_id")

        # Fetch instances again from POST data
        customer = get_object_or_404(Customer, id=customer_id)
        product = get_object_or_404(Product, id=product_id)
        print(product, customer)
    # Create order only if customer and product exist
    if customer and product:
        print("ok")
        order = Order.objects.create(
            customer=customer,  # Pass the instance, not the ID
            product=product,  # Pass the instance, not the ID
            date=datetime.datetime.now(),
            total_amount=product.price,
            status="placed"
        )

        # Reduce product stock
        product.stock -= 1
        product.save()

        # Send confirmation email
        send_mail(
            subject="Order Confirmation",
            message=f"Dear {customer.firstname},\n\nThank you for your purchase! Your order (ID: {order.id}) for {product.name} has been placed successfully.\nTotal Amount: ${product.price}\n\nBest regards,\nAyush Sales",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[customer.email_address],
            fail_silently=False,
        )

        return render(request, "product_app/buying.html", {"product": product, "customer": customer, "order": order.id})

    return render(request, "product_app/buying.html", {"error": "Invalid order details"})

def cart(request):
    if request.method == "POST":
        customer_id = request.POST.get("customer_id")
        product_id = request.POST.get("product_id")
        print(customer_id,product_id)
        
        products = Product.objects.get(id = product_id)
        customer = Customer.objects.get(id = customer_id)
        
        return render(request, "product_app/cart.html", {"products": products, "customer": customer})
    
    
