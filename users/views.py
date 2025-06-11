from datetime import timedelta
import logging
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages
from django.core.mail import EmailMultiAlternatives, send_mail
from django.db.models import Prefetch
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone

from carts.models import Cart
from orders.models import Order, OrderItem
from users.forms import ProfileForm, UserLoginForm, UserRegistrationForm
from users.models import User
from .forms import PasswordResetRequestForm, SetNewPasswordForm

def login(request):
    if request.method  == 'POST':
        form=UserLoginForm(data=request.POST)
        if form.is_valid():
            username=request.POST['username']
            password=request.POST['password']
            user=auth.authenticate(username=username,password=password)

            session_key=request.session.session_key

            if user:
                auth.login(request,user)
                messages.success(request, f"{username}, Вы вошли в аккаунт")

                if session_key:
                    Cart.odject.filter(session_key=session_key).update(user=user)

                redirect_page=request.POST.get('next',None)
                if redirect_page and redirect_page != reverse('user:logout'):
                    return HttpResponseRedirect(request.POST.get('next'))

                return HttpResponseRedirect(reverse('main:index'))
    else:
        form=UserLoginForm()
        
    context = {
        'title': 'ЕМЕХ-авто - Авторизация',
        'form': form
    }
    return render(request, 'users/login.html', context)

def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            
            token = user.generate_verification_token()
            verification_url = request.build_absolute_uri(
                reverse('users:verify_email', kwargs={'token': token})
            )
            
            # Подготовка текстовой и HTML версий письма
            subject = 'Подтверждение регистрации на ЕМЕХ-авто'
            text_content = f"""
            Здравствуйте, {user.username}!
            
            Для подтверждения регистрации перейдите по ссылке:
            {verification_url}
            
            Если вы не регистрировались на нашем сайте, проигнорируйте это письмо.
            
            С уважением,
            Команда ЕМЕХ-авто
            """
            
            html_content = render_to_string('emails/verification_email.html', {
                'user': user,
                'verification_url': verification_url
            })
            
            try:
                msg = EmailMultiAlternatives(
                    subject=subject,
                    body=text_content,  # Текстовая версия
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[user.email],
                    reply_to=[settings.DEFAULT_FROM_EMAIL]
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                
                messages.success(
                    request,
                    'На вашу почту отправлено письмо с инструкциями для подтверждения регистрации.'
                )
                return redirect('users:login')
                
            except Exception as e:
                logger = logging.getLogger(__name__)
                logger.error(f"Ошибка отправки email: {str(e)}", exc_info=True)
                
                messages.error(
                    request,
                    'Произошла ошибка при отправке письма подтверждения. '
                    'Пожалуйста, попробуйте позже или свяжитесь с поддержкой.'
                )
                return redirect('users:registration')
    else:
        form = UserRegistrationForm()

    context = {'title': 'Регистрация', 'form': form}
    return render(request, 'users/registration.html', context)


def verify_email(request, token):
    try:
        # Находим пользователя по токену
        user = User.objects.get(verification_token=token)
        
        # Проверяем срок действия токена (24 часа)
        if user.token_created_at < timezone.now() - timedelta(hours=24):
            user.verification_token = None
            user.token_created_at = None
            user.save()
            
            messages.error(
                request,
                'Ссылка подтверждения истекла. Пожалуйста, зарегистрируйтесь снова.'
            )
            return redirect('users:registration')
        
        # Активируем аккаунт
        user.email_verified = True
        user.is_active = True
        user.verification_token = None
        user.token_created_at = None
        user.save()
        
        # Автоматический вход после подтверждения (опционально)
        from django.contrib.auth import login
        login(request, user)
        
        messages.success(
            request,
            f'{user.username}, ваш email успешно подтвержден! Добро пожаловать!'
        )
        return redirect('main:index')
    
    except User.DoesNotExist:
        messages.error(request, 'Неверная ссылка подтверждения.')
        return redirect('users:registration')


@login_required
def profile(request):
    if request.method  == 'POST':
        form=ProfileForm(data=request.POST, instance=request.user, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Профиль успешно обновлен")
            return HttpResponseRedirect(reverse('user:profile'))
    else:
        form=ProfileForm(instance=request.user)

    orders=(
        Order.objects.filter(user=request.user)
        .prefetch_related(
            Prefetch(
                "orderitem_set",
                queryset=OrderItem.objects.select_related("product"),
            )
        )
        .order_by("-id")
    )

    context = {
        'title': 'ЕМЕХ-авто - Кабинет',
        'form': form,
        'orders':orders
    }
    return render(request, 'users/profile.html', context)

def users_cart(request):
   return render(request, 'users/users_cart.html')

@login_required
def logout(request):
    messages.success(request, f"{request.user.username}, Вы вышли из аккаунта")
    auth.logout(request)
    return redirect(reverse('main:index'))


def password_reset_request(request):
    if request.method == "POST":
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email__iexact=email, is_active=True)
                token = user.generate_password_reset_token()
                
                # Добавьте проверку токена
                if not token:
                    messages.error(request, "Ошибка генерации токена. Пожалуйста, попробуйте позже.")
                    return redirect('users:password_reset')
                
                
                reset_url = request.build_absolute_uri(
                    reverse('users:password_reset_confirm', kwargs={'token': token})
                )
                
                
                # Подготовка письма
                subject = 'Восстановление пароля на ЕМЕХ-авто'
                text_content = f"""
                Здравствуйте, {user.username}!
                
                Для сброса пароля перейдите по ссылке:
                {reset_url}
                
                Ссылка действительна 24 часа.
                
                Если вы не запрашивали сброс пароля, проигнорируйте это письмо.
                
                С уважением,
                Команда ЕМЕХ-авто
                """
                
                html_content = render_to_string('emails/password_reset_email.html', {
                    'user': user,
                    'reset_url': reset_url
                })
                
                try:
                    msg = EmailMultiAlternatives(
                        subject=subject,
                        body=text_content,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        to=[user.email],
                        reply_to=[settings.DEFAULT_FROM_EMAIL]
                    )
                    msg.attach_alternative(html_content, "text/html")
                    msg.send()
                    
                    messages.success(
                        request,
                        'На вашу почту отправлена ссылка для сброса пароля. '
                        'Проверьте ваш email.'
                    )
                    return redirect('users:login')
                    
                except Exception as e:
                    logger = logging.getLogger(__name__)
                    logger.error(f"Ошибка отправки email: {str(e)}", exc_info=True)
                    messages.error(
                        request,
                        'Произошла ошибка при отправке письма. '
                        'Пожалуйста, попробуйте позже.'
                    )
            except User.DoesNotExist:
                messages.error(
                    request,
                    'Пользователь с таким email не найден или аккаунт не активирован.'
                )
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Ошибка в поле {form.fields[field].label}: {error}")
    else:
        form = PasswordResetRequestForm()
    
    context = {
        'title': 'Восстановление пароля',
        'form': form
    }
    return render(request, 'users/password_reset.html', context)

def password_reset_confirm(request, token):
    try:
        user = User.objects.get(password_reset_token=token)
        
        if not user.is_password_reset_token_valid():
            user.password_reset_token = None
            user.password_reset_token_created_at = None
            user.save()
            messages.error(
                request,
                'Ссылка для сброса пароля истекла. Пожалуйста, запросите новую.'
            )
            return redirect('users:password_reset')
        
        if request.method == 'POST':
            form = SetNewPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                user.password_reset_token = None
                user.password_reset_token_created_at = None
                user.save()
                
                # Обновляем сессию, если пользователь уже вошел в систему
                if request.user.is_authenticated:
                    auth.update_session_auth_hash(request, user)
                
                messages.success(
                    request,
                    'Ваш пароль успешно изменен. Теперь вы можете войти с новым паролем.'
                )
                return redirect('users:login')
        else:
            form = SetNewPasswordForm(user)
        
        context = {
            'title': 'Установка нового пароля',
            'form': form,
            'validlink': True
        }
        return render(request, 'users/password_reset_confirm.html', context)
    
    except User.DoesNotExist:
        messages.error(request, 'Неверная ссылка для сброса пароля.')
        return redirect('users:password_reset')