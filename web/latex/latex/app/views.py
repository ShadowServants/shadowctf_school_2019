from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView, ListView, DetailView

from app.models import Document
from app.jobs import render_document


class RegisterView(TemplateView):
    template_name = 'register.html'

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        if username is None or password is None:
            return render(request, self.template_name, {'message': 'Both fields are required!'})
        if User.objects.filter(username=username).exists():
            return render(request, self.template_name, {"message": "Username already taken!"})
        user = User(username=username)
        user.set_password(password)
        user.save()
        return redirect('/login')


@login_required
def logout_view(response):
    logout(response)
    return redirect('/')


class LoginView(TemplateView):
    template_name = "login.html"

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            path = request.GET.get('next', '/')
            return redirect(path)
        else:
            return render(request, self.template_name, {'message': "Username or password not correct!"})


class DocumentCreateView(LoginRequiredMixin, CreateView):
    fields = ['title', 'text']
    model = Document
    template_name = 'create.html'

    def form_valid(self, form):
        document = form.save(commit=False)
        document.owner_id = self.request.user.id
        document.save()
        render_document.delay(document.id)
        return redirect('/list')


class IndexView(TemplateView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/home')
        return super().get(request, *args, **kwargs)


class DocumentListView(LoginRequiredMixin, ListView):
    template_name = "list.html"
    context_object_name = "docs"

    def get_queryset(self):
        return Document.objects.filter(owner_id=self.request.user.id)


class HomeView(TemplateView):
    template_name = 'home.html'
