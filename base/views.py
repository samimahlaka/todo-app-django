from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView , UpdateView, DeleteView
from django.contrib.auth.views import LoginView , LogoutView
from django.urls import reverse_lazy
from .models import Task
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class CustomLoginView(LoginView):
    fields = '__all__';
    redirect_authenticated_user = True;
    #success_url = reverse_lazy('tasks')    
    def get_success_url(self) :
       return reverse_lazy('tasks'); 
    template_name = 'base/login.html'

class CustomLogoutView(LogoutView):
    template_name = 'base/logout.html';
    def get_success_url(self):
        return reverse_lazy('')


class TaskList(LoginRequiredMixin,ListView):
    model = Task;
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user = self.request.user)   
        context['count'] = context['tasks'].filter(complete=False).count()
        return context

class TaskDetail(LoginRequiredMixin,DetailView):
    model=Task
    context_object_name = 'task'
    template_name = 'base/task.html'

class TaskCreate(LoginRequiredMixin,CreateView):
    model = Task;
    fields = '__all__';
    #success_url = reverse_lazy('tasks');
    success_url = reverse_lazy('tasks')

class TaskUpdate(LoginRequiredMixin,UpdateView):
    model = Task;
    fields = '__all__';
    success_url = reverse_lazy('tasks');

class TaskDelete(LoginRequiredMixin,DeleteView):
    model = Task;
    context_object_name = 'task';
    success_url= reverse_lazy('tasks');
