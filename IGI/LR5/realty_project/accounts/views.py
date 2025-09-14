from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate
from .forms import RegisterForm
from .models import User
import random
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from .forms import AvatarUploadForm
from datetime import timedelta
from realty.models import Buyer
import logging

logger = logging.getLogger('project')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            code = ''.join([str(random.randint(0,9)) for _ in range(6)])
            user.confirmation_code = code
            user.confirmation_expires = timezone.now() + timedelta(minutes=5)
            user.is_active = False
            user.save()

            # ✅ Сохраняем данные формы во временных данных
            request.session['registration_data'] = {
                'phone': form.cleaned_data.get('phone'),
                'budget': str(form.cleaned_data.get('budget')) if form.cleaned_data.get('budget') else None,
            }

            # Выводим код подтверждения в консоль
            print("\n" + "="*50)
            print(f"КОД ПОДТВЕРЖДЕНИЯ ДЛЯ {user.email}: {code}")
            print("="*50 + "\n")
            
            # Также логируем для записи в файл
            logger.info(f"Код подтверждения для {user.email}: {code}")

            return redirect('confirm_email', user_id=user.id)
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})




def confirm_email(request, user_id):
    user = get_object_or_404(User, id=user_id)
    registration_data = request.session.get('registration_data', {})

    if request.method == 'POST':
        code = request.POST.get('code')

        if user.confirmation_code == code and user.confirmation_expires > timezone.now():
            user.is_active = True
            user.confirmation_code = None
            user.confirmation_expires = None
            user.save()

            # ✅ Создаем Buyer из session
            Buyer.objects.create(
                user=user,
                phone=registration_data.get('phone', '+375290000000'),
                budget=registration_data.get('budget') or 0
            )

            # Очищаем session
            del request.session['registration_data']
            request.session.modified = True

            auth_login(request, user)
            messages.success(request, "Email успешно подтверждён!")
            return redirect('home')
        else:
            messages.error(request, "Неверный или истёкший код")

    return render(request, 'accounts/confirm_email.html', {'user_id': user_id})




def home(request):
    return render(request, 'home.html')


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=email, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Неверный email или пароль.")
        else:
            messages.error(request, "Ошибка валидации формы.")
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})

def user_logout(request):
    auth_logout(request)
    return redirect('home')


@login_required
def profile(request):
    if request.method == 'POST':
        form = AvatarUploadForm(request.POST, request.FILES)
        if form.is_valid():
            avatar = form.cleaned_data['avatar']
            request.user.avatar = avatar
            request.user.save()
            messages.success(request, 'Аватар успешно обновлён!')
            return redirect('profile')
    else:
        form = AvatarUploadForm()

    return render(request, 'accounts/profile.html', {
        'form': form
    })


@login_required
def update_avatar(request):
    if request.method == 'POST':
        form = AvatarUploadForm(request.POST, request.FILES)
        if form.is_valid():
            avatar = form.cleaned_data['avatar']
            user = request.user
            user.avatar = avatar
            user.save()
            messages.success(request, 'Аватар успешно обновлён')
            return redirect('profile')
    else:
        form = AvatarUploadForm()

    return render(request, 'accounts/update_avatar.html', {'form': form})


@property
def full_name(self):
    return f"{self.last_name} {self.first_name} {self.middle_name or ''}".strip()