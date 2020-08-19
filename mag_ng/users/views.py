from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.views.generic import DetailView
from django.contrib.auth import get_user_model
from django.contrib import messages
from articles.models import ArticleModel
from .forms import CustomUserChangeForm
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required

User = get_user_model()


def signup(request):
    if request.user.is_authenticated:
        return redirect('articles:home')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=user.email, password=raw_password)
            # login(request, user)
            messages.success(request,f'Your account has been created, you\'re now able to log in.')
            return redirect('users:login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/signup.html', {'form': form, 'title': 'Sign-Up'})


class Profile(DetailView):
    model = User
    template_name = 'users/profile.html'
    context_object_name = 'object'
    slug_field = 'slug'
    slug_url_kwarg = 'user'
    query_pk_and_slug = True

    def get_queryset(self, **kwargs):
        return User.objects.get(pk=self.kwargs['pk'])

    def get_object(self, **kwargs):
        return User.objects.get(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count'] = ArticleModel.objects.filter(publish=True, author=self.get_object()).count()
        context['articles'] = ArticleModel.objects.filter(publish=True, author=self.get_object())
        return context


@login_required
def edit(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f'You acccount has been updated')
            return redirect('users:profile', pk=request.user.id)
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        'form':form
    }
    return render(request, 'users/update_profile.html', context)
