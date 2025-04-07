from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.db import IntegrityError
from .models import *
from django.contrib.auth import authenticate, login as auth_login

# Create your views here.
def index(request):
    return render(request,"index.html")


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        user_type = request.POST.get('user_type')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, "كلمتا المرور غير متطابقتين.")
            return render(request, "register.html")
        try:
            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password1,
                phone_number=phone_number,
                user_type=user_type
            )
            user.save()
            if user.user_type == CustomUser.UserType.HANDYMAN:
                HandymanProfile.objects.get_or_create(user=user)
                
            messages.success(request, "تم إنشاء الحساب بنجاح. يمكنك تسجيل الدخول الآن.")
            return redirect('login')

        except IntegrityError:
            messages.error(request, "اسم المستخدم أو البريد الإلكتروني مستخدم بالفعل.")
            return render(request, "register.html")

    return render(request, "register.html")
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user_obj = CustomUser.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)
        except CustomUser.DoesNotExist:
            user = None

        if user is not None:
            auth_login(request, user)
            messages.success(request, "Login successful.")
            return redirect('userhome') 
        
        messages.error(request, "بيانات تسجيل الدخول غير متطابقة, حاول مرة أخرى ")
        return render(request, "login.html")
    else:
        return render(request, "login.html")
    
def cart_view(request):
    return render(request, 'cart.html')

def user_home(request):
    return render(request,'userhome.html')

def add_service(request):
    if not request.user.is_authenticated:
        messages.error(request, "يحب تسجيل الدخول لاضافة خدمات")
        return redirect('login')
    
    if request.user.user_type != CustomUser.UserType.HANDYMAN:
        messages.error(request, "يجب ان تكون فني لاضافة خدمات")
        return redirect('userhome')
    
    if request.method == "POST":
        name = request.post.get('name')
        description =request.post.get('description')
        price = request.post.get('price')
        image = request.POST.get('image')

    if not name or not description or not price:
        messages.error("يجب ادخال اسم ووصف وسعر الخدمة")
        return render(request,'addservice.html')
    
    try:
        service = ServiceListing.objects.create(
            handyman=request.user,
            name = name,
            description= description,
            price=price,
            image=image

        )
        service.save()
        messages.success("تم اضافة الخدمة بنجاح")
        return redirect(request, 'userhome')
    except Exception as e:
        messages.error(request, f"حدث خطأ اثناء اضافة الخدمة: {e}")
        return render(request ,'addservice.html')
    
    return render(request, 'addservice.html')


def edit_profile(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        phone_number = request.POST.get("phone_number")
        bio = request.POST.get("bio")
        experience = request.POST.get("experience")
        field_of_expertise = request.POST.get("field_of_expertise")
        availability = request.POST.get("availability") == "True" 
        image = request.FILES.get("image")

        try:
            user = request.user
            user.username = username
            user.email = email
            user.phone_number = phone_number
            user.bio = bio
            user.experience = experience
            user.field_of_expertise = field_of_expertise
            

            if image:
                user.image = image

            handyman_profile = user.handyman_profile
            handyman_profile.availability = availability
            handyman_profile.save() 
            user.save()

            messages.success(request, "تم حفظ التعديلات بنجاح!")
            return redirect('userhome') 

        except Exception as e:
            messages.error(request, "حدث خطأ أثناء حفظ التعديلات. يرجى المحاولة مرة أخرى.")
            return redirect('edit-profile')

    return render(request, 'profile.html')

def logout(request):
    request.session.flush() 
    return redirect('login')