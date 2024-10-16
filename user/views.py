from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordChangeForm
from user.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import LoginUserForm, RegisterUserForm, ProfileUserForm, UpdateUserForm, EmailForm
from django.contrib.auth.views import LoginView, PasswordChangeView
import random
from .tasks import send_verification_email
from django.contrib import messages


class UserLoginView(LoginView):
    form_class = LoginUserForm
    template_name = 'user/login.html'
    extra_context = {'title': 'Авторизация'}

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)

            if user is not None and user.is_active:
                if user.email_verified:
                    verification_code = random.randint(100000, 999999)
                    user.verification_code = verification_code
                    user.save()

                    try:
                        send_verification_email.delay(user.email, verification_code)
                    except Exception as e:
                        messages.error(request, 'Ошибка при отправке письма. Пожалуйста, попробуйте позже.')
                        print(f"Error sending email: {e}")
                        return render(request, 'user/login.html', {'form': form})

                    request.session['user_id'] = user.id
                    return redirect('users:verify_email')
                else:
                    messages.error(request, "Ваш email не подтвержден.")
            else:
                messages.error(request, 'Неправильные учетные данные или аккаунт не активирован.')

        return render(request, 'user/login.html', {'form': form})


class UserRegisterView(CreateView):
    form_class = RegisterUserForm
    template_name = 'user/register.html'
    success_url = reverse_lazy('users:verification_page')
    extra_context = {'title': 'Регистрация'}

    def form_valid(self, form):
        verification_code = random.randint(100000, 999999)
        user = form.save(commit=False)
        user.verification_code = verification_code
        user.email_verified = False
        user.save()
        self.request.session['user_id'] = user.id
        try:
            send_verification_email.delay(user.email, verification_code)
        except Exception as e:
            messages.error(self.request, 'Ошибка при отправке письма. Пожалуйста, попробуйте позже.')
            print(f"Error sending email: {e}")
            return render(self.request, 'user/register.html', {'form': form})

        return redirect(self.success_url)


def verify_email(request):
    if request.method == 'POST':
        verification_code = request.POST.get('verification_code')
        user_id = request.session.get('user_id')

        if not user_id:
            messages.error(request, 'Ошибка аутентификации. Пожалуйста, попробуйте снова.')
            return redirect('users:login')

        user = User.objects.filter(id=user_id, verification_code=verification_code).first()

        if user:
            user.email_verified = True
            user.verification_code = None
            user.save()

            print(f"Logging in user: {user.email}")
            login(request, user)  # Попробуем авторизовать пользователя
            request.session.pop('user_id', None)

            messages.success(request, 'Email успешно подтвержден.')
            return redirect('tasks:tasks')
        else:
            print(f"Failed verification for code: {verification_code}, user_id: {user_id}")
            messages.error(request, 'Неверный код подтверждения. Попробуйте еще раз.')

    return render(request, 'user/verification_page.html')


class UserProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileUserForm
    template_name = 'user/profile.html'
    extra_context = {'title': 'Профиль пользователя'}

    def get_object(self, queryset=None):
        return self.request.user


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UpdateUserForm
    template_name = 'user/profile_update.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class UserPasswordChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('users:password_change_done')
    template_name = 'user/password_change_form.html'
    extra_context = {'title': 'Изменение пароля'}


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('users:login'))
