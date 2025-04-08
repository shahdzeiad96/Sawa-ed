from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.db import IntegrityError
from .models import *
import requests
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from django.contrib.auth import authenticate, login as auth_login

def index(request):
    services = ServiceListing.objects.all()
    context = {'services': services, 
               'service_types': ServiceListing.SERVICE_TYPES
               }

    return render(request,"index.html",context)


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

    services=ServiceListing.objects.all()
    handyman=HandymanProfile.objects.all()
    context={
        'services':services,
        'handyman':handyman,
        'service_types': ServiceListing.SERVICE_TYPES

    }
    return render(request,'userhome.html',context)

def add_service(request):
    services=ServiceListing.objects.all()
    if not request.user.is_authenticated:
        messages.error(request, "يحب تسجيل الدخول لاضافة خدمات")
        return redirect('login')
    
    if request.user.user_type != CustomUser.UserType.HANDYMAN:
        messages.error(request, "يجب ان تكون فني لاضافة خدمات")
        return redirect('userhome')
    
    if request.method == "POST":
        name = request.POST.get('name') 
        description = request.POST.get('description')
        price = request.POST.get('price')
        image = request.FILES.get('image')  

        if not name or not description or not price:
            messages.error(request, "يجب ادخال اسم ووصف وسعر الخدمة")
            return render(request, 'addservice.html')

        try:
            service = ServiceListing.objects.create(
                handyman=request.user,
                name=name,
                description=description,
                price=price,
                image=image
            )
            messages.success(request, "تم اضافة الخدمة بنجاح")
            return redirect('userhome')
        except Exception as e:
            messages.error(request, f"حدث خطأ اثناء اضافة الخدمة: {e}")
            return render(request, 'addservice.html')
    context={
        'services':services,
        'service_types': ServiceListing.SERVICE_TYPES

    }
    return render(request, 'addservice.html',context)

def service_detail(request, service_id,user_id):
    service =ServiceListing.objects.get(id=service_id)
    handyman = HandymanProfile.objects.get(user=service.handyman)
    user=CustomUser.objects.get(id=user_id)
    context = {
        'service': service,
        'handyman': handyman,
        'recipient': user
    }

    return render(request, 'service_details.html', context)

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CustomUser, Message

def send_message(request, recipient_id, service_id):
    recipient = CustomUser.objects.get(id=recipient_id)
    
    if request.method == 'POST':
        content = request.POST.get('content')
        if content.strip():  # التأكد من أن الرسالة ليست فارغة
            Message.objects.create(
                sender=request.user,
                receiver=recipient,
                content=content
            )
            messages.success(request, "تم إرسال الرسالة بنجاح.")
            return redirect('service_detail', service_id=service_id, user_id=recipient_id)
        else:
            messages.error(request, "لا يمكن إرسال رسالة فارغة.")
    
    return redirect('service_detail', service_id=service_id, user_id=recipient_id)


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

            # Only update availability for handymen
            if user.user_type == 'handyman':
                handyman_profile = user.handyman_profile
                handyman_profile.availability = availability
                handyman_profile.save() 

            user.save()

            messages.success(request, "تم حفظ التعديلات بنجاح!")
            return redirect('edit-profile') 

        except Exception as e:
            messages.error(request, "حدث خطأ أثناء حفظ التعديلات. يرجى المحاولة مرة أخرى.")
            return redirect('edit-profile')

    return render(request, 'profile.html')


def logout(request):
    request.session.flush() 
    return redirect('login')
