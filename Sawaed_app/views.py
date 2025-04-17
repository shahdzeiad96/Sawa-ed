from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.db import IntegrityError
from .models import *
import requests
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .chatbot import get_chatbot_response
import json
from django.contrib.auth import authenticate, login as auth_login
from django.db.models import Q, Max
from django.shortcuts import get_object_or_404
from decimal import Decimal
import logging
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.hashers import check_password





def index(request):
    services = ServiceListing.objects.all()
    context = {'services': services, 
               'service_types': ServiceListing.SERVICE_TYPES
               }

    return render(request,"index.html",context)
def guest_home(request):
    services = ServiceListing.objects.all()
    context = {'services': services, 
               'service_types': ServiceListing.SERVICE_TYPES
               }
    return render(request,"guesthome.html",context)

def base_view_data(request):
    services=ServiceListing.objects.all()
    cart_count = 0
    if request.user.is_authenticated:
        cart_count = CartItem.objects.filter(user=request.user).count()


    
    data = {
        'services':services,
        'service_types': ServiceListing.SERVICE_TYPES,
        'cart_count': cart_count,
    }
    if request.user.is_authenticated:
        data['unread_messages_count'] = Message.objects.filter(receiver=request.user, is_read=False).count()
    else:
        data['unread_messages_count'] = 0
    return data

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
            request.session['user_logged'] = True
            return redirect('userhome') 
        
        messages.error(request, "بيانات تسجيل الدخول غير متطابقة, حاول مرة أخرى ")
        return render(request, "login.html")
    else:
        return render(request, "login.html")
    
@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    
    #to get the total price
    total_price = sum(item.service.price for item in cart_items)
    commission = total_price * Decimal('0.1')
    final_total=total_price+commission
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'commission': commission,
        'final_total': final_total,
    }

    context.update(base_view_data(request))

    return render(request, 'cart.html', context)

@login_required
def user_home(request):
    services = ServiceListing.objects.all().order_by('-created_at')
    service_added = request.session.pop('service_added', False)
    user_logged=request.session.pop('user_logged',False)
    handyman=HandymanProfile.objects.all()
    context={
        'handyman':handyman,
        'service_added': service_added,
        'user_logged':user_logged,
        'services':services
    
    }
    context.update(base_view_data(request))
    return render(request,'userhome.html',context)
@login_required
def add_service(request):
    services = ServiceListing.objects.all()

    if not request.user.is_authenticated:
        messages.error(request, "يجب تسجيل الدخول لإضافة خدمات")
        return redirect('login')

    if request.user.user_type != CustomUser.UserType.HANDYMAN:
        messages.error(request, "يجب أن تكون فنيًا لإضافة خدمات")
        return redirect('userhome')

    if request.method == "POST":
        name = request.POST.get('name')
        service_type = request.POST.get('service_type')  # capture  category
        description = request.POST.get('description')
        price = request.POST.get('price')
        image = request.FILES.get('image')

        if not name or not description or not price or not service_type:
            messages.error(request, "يجب إدخال اسم الخدمة، نوعها، وصفها وسعرها")
            return render(request, 'addservice.html')

        try:
            service = ServiceListing.objects.create(
                handyman=request.user,
                name=name,
                service_type=service_type,  #  save in DB
                description=description,
                price=price,
                image=image
            )
            request.session['service_added'] = True
            return redirect('userhome')
        except Exception as e:
            messages.error(request, f"حدث خطأ أثناء إضافة الخدمة: {e}")
            return render(request, 'addservice.html')

    context = {
        'services': services,
        'service_types': ServiceListing.SERVICE_TYPES,
    }
    context.update(base_view_data(request))  
    return render(request, 'addservice.html', context)
    
def service_detail(request, service_id,user_id):
    service =ServiceListing.objects.get(id=service_id)
    handyman = HandymanProfile.objects.get(user=service.handyman)
    user=CustomUser.objects.get(id=user_id)
    context = {
        'service': service,
        'handyman': handyman,
        'recipient': user
    }
    context.update(base_view_data(request))
    return render(request, 'service_details.html', context)

# Inbox: Display all messages (both sent and received)
@login_required
def inbox(request):
    user = request.user

    # Get all sent and received messages for the user
    messages = Message.objects.filter(Q(sender=user) | Q(receiver=user))

    # Dictionary to store the last message in each thread
    threads = {}
    for msg in messages:
        # Determine the other participant in the thread (sender or receiver)
        other_user = msg.receiver if msg.sender == user else msg.sender

        # Keep the most recent message in the thread
        if other_user not in threads or msg.timestamp > threads[other_user].timestamp:
            threads[other_user] = msg

    # Sort the threads by the timestamp of the last message
    sorted_threads = sorted(threads.items(), key=lambda x: x[1].timestamp, reverse=True)

    context = {
        'threads': sorted_threads,  # Threads sorted by the latest message timestamp
        'messages_ids': [message.id for message in messages]  # List of message IDs
    }

    return render(request, 'inbox.html', context)

# Send a new message
@login_required
def send_message(request, recipient_id):
    recipient = get_object_or_404(CustomUser, id=recipient_id)

    if request.method == 'POST':
        content = request.POST.get('content')
        sender = request.user

        if content:
            Message.objects.create(
                sender=sender,
                receiver=recipient,
                content=content,
 
            )

        return redirect('inbox')

# Count the number of unread messages
def unread_messages_count(request):
    if request.user.is_authenticated:
        count = Message.objects.filter(recipient=request.user, is_read=False).count()
    else:
        count = 0
    return {'unread_messages_count': count}  # Return the unread messages count

# Mark a message as read
@login_required
def mark_as_read(request, message_id):
    message = get_object_or_404(Message, id=message_id, receiver=request.user)
    
    if request.method == 'POST':
        message.is_read = True
        message.save()
    
    return redirect('inbox')  # Redirect to the inbox page after marking as read
@login_required
def chat_detail(request, user_id):
    other_user = get_object_or_404(CustomUser, id=user_id)
    
    # Get all messages between the two users
    messages = Message.objects.filter(
        (Q(sender=request.user) & Q(receiver=other_user)) | 
        (Q(sender=other_user) & Q(receiver=request.user))
    ).order_by('timestamp')

    # Mark messages as read if they were sent to the current user
    messages.filter(receiver=request.user, is_read=False).update(is_read=True)

    # Handle POST request to send a new message
    if request.method == 'POST':
        content = request.POST.get('content')

        if content.strip():
            new_message = Message(
                sender=request.user,
                receiver=other_user,
                content=content,
                is_read=False
            )
            new_message.save()
            messages = Message.objects.filter(
                (Q(sender=request.user) & Q(receiver=other_user)) | 
                (Q(sender=other_user) & Q(receiver=request.user))
            ).order_by('timestamp')  # Refresh the messages list

    context = {
        'messages': messages,
        'other_user': other_user
    }
    context.update(base_view_data(request))

    return render(request, 'chat_detail.html', context)
@login_required
def edit_profile(request):
    context={

    }
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
        
    context.update(base_view_data(request))
    return render(request, 'profile.html',context)


def logout(request):
    request.session.flush() 
    return redirect('login')
@login_required
def rate_service(request, service_id):
    service = ServiceListing.objects.get(id=service_id)
    context={"setvice":service}
    if not request.user.is_authenticated:
        messages.error(request, "الرجاء تسجيل الدخول أولاً")
        return redirect('login')
    
    if request.method == "POST":
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        if not rating or int(rating) < 1 or int(rating) > 5:
            messages.error(request,"الرجاء ادخال تقييم بين 1 و 5")
            return redirect('service_detail', service_id=service_id, user_id=service.handyman.id)
        
        Review.objects.create(
            client = request.user,
            service = service,
            rating=int(rating),
            comment = comment
        )
        messages.success(request,"نشكرك على تقييمك")
        return redirect('service_detail', service_id=service_id, user_id=service.handyman.id)
        
    return render(request,'rate_service.html', context)

#chatbot views
def chatbot_ui(request): #this to load the page only
    return render(request, "chatbot.html")


@csrf_exempt 
def chatbot_response(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get('message')

            api_url = 'https://api.aimlapi.com/v1/chat/completions'
            headers = {
                'Authorization': 'Bearer 17c7002d4b0b4654ac1642929c14c89e', 
                'Content-Type': 'application/json',
            }

            payload = {
                "model": "gpt-4-0125-preview",
                "messages": [
                    {
                        "role": "system",
                        "content": (
    "أنت مساعد ذكي خاص بمنصة إلكترونية تُدعى 'سواعد'. "
    "سواعد هي موقع إلكتروني يربط بين الحرفيين (مثل السباكين، الكهربائيين، النجارين...) وبين العملاء الذين يحتاجون إلى خدماتهم. "
    "أجب دائمًا باللغة العربية فقط، وقدم معلومات دقيقة ومبسطة عن المنصة وخدماتها."

)
                    },
                    {
                        "role": "user",
                        "content": user_message
                    }
                ],
                "max_tokens": 300,
                "temperature": 0.7
            }

            response = requests.post(api_url, headers=headers, json=payload)
            response_data = response.json()

            chatbot_response = response_data.get('choices', [{}])[0].get('message', {}).get('content', 'عذرًا، لم أتمكن من فهم سؤالك.')

            return JsonResponse({'response': chatbot_response})

        except Exception as e:
            return JsonResponse({'response': f"خطأ: {str(e)}"})

    return JsonResponse({'response': 'طلب غير صالح'})


# Add to cart function
@login_required
def add_to_cart(request, service_id):
    service = get_object_or_404(ServiceListing, id=service_id)

    # Check if the service is already in the cart
    existing_order = CartItem.objects.filter(
        user=request.user, service=service
    ).first()

    if existing_order:
        messages.info(request, "هذه الخدمة موجودة بالفعل في السلة.")
    else:
        CartItem.objects.create(user=request.user, service=service)
        messages.success(request, "تمت إضافة الخدمة إلى السلة")

    # Redirect to the cart view
    return redirect('cart')


#remove from cart function
@login_required
def remove_from_cart(request, order_id):
    order = get_object_or_404(CartItem, id=order_id, user=request.user)
    order.delete()
    messages.success(request, "تمت إزالة الخدمة من السلة.")
    return redirect('cart')

# search engine 
def search_services(request):
    query = request.GET.get('q', '')
    if query:
        services = ServiceListing.objects.filter(name__icontains=query)
    else:
        services = ServiceListing.objects.all()

    # Collect distinct service types from the choices
    service_types = ServiceListing.SERVICE_TYPES

    return render(request, 'service_search.html', {
        'services': services,
        'service_types': service_types,
        'query': query
        
    })

logger = logging.getLogger(__name__) 
@login_required
def checkout(request):
    if request.method == 'POST':
        cart_items= CartItem.objects.filter(user=request.user)
        if not cart_items.exists():
            messages.error(request, "سلة الخدمات فارغة")
            return redirect('cart')
        for item in cart_items:
            service = item.service
            order = ServiceOrder.objects.create(
                client = request.user,
                service = service,
                handyman = service.handyman,
                status = 'Pending'
            )
            Notifications.objects.create(
                recipient = service.handyman,
                actor = request.user,
                verb = "طلب جديد",
                service_order = order,
                message = f"طلب جديد لخدمة '{service.name}' من العميل '{request.user.username}'."
            )
        
        cart_items.delete()
        messages.success(request,"تم ارسال الطلب بنجاح وسيتم اعلام الفني")
        return redirect('checkout')
    else:
        cart_items = CartItem.objects.filter(user=request.user)
        context = {"cart_items": cart_items}
        return render(request,'checkout.html', context)

# services by type filter 
def services_by_type(request, service_type):
    services = ServiceListing.objects.filter(service_type=service_type)
    return render(request, 'service_by_type.html', {
        'services': services,
        'selected_type': service_type
    })
#delete the service only by the handyman who post it 
@require_POST
@login_required
def delete_service_ajax(request):
    service_id = request.POST.get('service_id')
    try:
        service = ServiceListing.objects.get(id=service_id, handyman=request.user)
        service.delete()
        return JsonResponse({'success': True})
    except ServiceListing.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Service not found or unauthorized.'})
    
@login_required
def reject_order(request, order_id):
    order= get_object_or_404(ServiceOrder, id=order_id, status='Pending')
    if order.handyman != request.user:
        messages.error(request,"ليس لديك صلاحية رفض أو قبول هذا الطلب")
        return redirect('userhome')
    # delete the older notification
    Notifications.objects.filter(service_order=order).delete()

    # creat a new notification of status of order
    Notifications.objects.create(
        recipient=order.client,
        actor=request.user,
        verb='رفض الطلب',
        service_order=order,
        message=f"عذرًا، تم رفض طلبك من قبل {request.user.username}"
    )

    # change status of the order
    order.status = 'Rejected'
    order.save()

    messages.success(request, "تم رفض الطلب بنجاح")
    return redirect('my_orders')
@login_required
def accept_order(request, order_id):
    order = get_object_or_404(ServiceOrder, id=order_id, status='Pending')

    if order.handyman != request.user:
        messages.error(request, "ليس لديك صلاحية قبول هذا الطلب")
        return redirect('userhome')
    #delete the old notification    
    Notifications.objects.filter(service_order=order).delete()
    #create a new one for acceptance
    Notifications.objects.create(
        recipient=order.client,
        actor=request.user,
        verb='قبول الطلب',
        service_order=order,
        message=f"تم قبول طلبك من قبل {request.user.username}"
    )
    #change the status
    order.status = 'Accepted'
    order.save()

    messages.success(request, "تم قبول الطلب بنجاح")
    return redirect('my_orders')

@login_required
def notifications_view(request):
    notifications = Notifications.objects.filter(recipient=request.user).order_by('-created_at')
    context= {
        'notifications': notifications
        }
    Notifications.objects.filter(recipient=request.user, is_read=False).update(is_read=True)
    
    return render(request, 'notifications.html',context)


def password_reset_request(request):
    if request.method == 'POST':
        email = request.POST.get('email')  

        if email:
            try:
                user = CustomUser.objects.get(email=email)
                token = default_token_generator.make_token(user) 
                uid = urlsafe_base64_encode(str(user.pk).encode()) 
                reset_url = f"{request.scheme}://{request.get_host()}/password-reset/{uid}/{token}/"
                
                send_mail(
                    'إعادة تعيين كلمة المرور',
                    f'إضغط على الرابط التالي لإعادة تعيين كلمة المرور: {reset_url}',
                    'noreply@yourwebsite.com',
                    [email],
                    fail_silently=False,
                )
                messages.success(request, 'تم إرسال بريد إلكتروني لإعادة تعيين كلمة المرور.')
                return render(request,"password_reset_done.html")
            except CustomUser.DoesNotExist:
                messages.error(request, 'البريد الإلكتروني غير مسجل لدينا.')
                return redirect('password_reset_request')
        else:
            messages.error(request, 'الرجاء إدخال بريد إلكتروني صحيح.')
            return redirect('password_reset_request')
    
    return render(request, 'password_reset_form.html')

def password_reset_confirm(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, CustomUser.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            new_password = request.POST.get('new_password')  
            confirm_password = request.POST.get('confirm_password')  

            if new_password and confirm_password:
                if new_password == confirm_password:
                    user.set_password(new_password)
                    user.save()
                    messages.success(request, 'تم تحديث كلمة المرور بنجاح.')
                    return redirect('login')
                else:
                    messages.error(request, 'كلمات المرور غير متطابقة.')
            else:
                messages.error(request, 'الرجاء إدخال جميع الحقول.')
        return render(request, 'password_reset_confirm.html')
    else:
        messages.error(request, 'رابط إعادة تعيين كلمة المرور غير صالح أو منتهي الصلاحية.')
        return redirect('password_reset_request')
    
def password_change(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        user = request.user

        if not check_password(old_password, user.password):
            messages.error(request, "كلمة المرور الحالية غير صحيحة.")
            return redirect('password_change')

        if new_password != confirm_password:
            messages.error(request, "كلمة المرور الجديدة وتأكيدها غير متطابقين.")
            return redirect('password_change')

        if len(new_password) < 8:
            messages.error(request, "يجب أن تكون كلمة المرور الجديدة مكونة من 8 أحرف على الأقل.")
            return redirect('password_change')

        user.set_password(new_password)
        user.save()
        messages.success(request, "تم تغيير كلمة المرور بنجاح. يرجى تسجيل الدخول مرة أخرى.")
        return redirect('login')

    return render(request, 'change_password.html')


#the orders display views 

@login_required
def my_orders(request):
    if request.user.user_type == 'client':
        orders = ServiceOrder.objects.filter(client=request.user)
    elif request.user.user_type == 'handyman':
        orders = ServiceOrder.objects.filter(service__handyman=request.user)
    else:
        orders = ServiceOrder.objects.none()
    context={'orders': orders}
    return render(request, 'my_orders.html', context)

@login_required
def complete_order(request, order_id):
    # Get  order by  ID
    order = ServiceOrder.objects.get(id=order_id)

    # Check if the the status already  'Completed'
    if order.status == 'Completed':
        messages.info(request, "الطلب تم إنجازه بالفعل.")
        return redirect('my_orders')  # Redirect to  my orders page
    # Mark order as 'Completed'
    order.status = 'Completed'
    order.save()
    #  success message to  the user
    messages.success(request, "تم إنهاء الطلب بنجاح.")
    
    # Redirect  to my orders page
    return redirect('my_orders')

def about_us(request):
    return render(request, 'about_us.html')
def contact_us(request):
    return render(request, 'contact_us.html')

@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(ServiceOrder, id=order_id)

    if request.user == order.client and order.status == 'Pending':
        order.delete()
        messages.success(request, "تم حذف الطلب بنجاح.")
    else:
        messages.error(request, "لا يمكنك حذف هذا الطلب.")

    return redirect('my_orders') 