from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView , UpdateView, DeleteView, FormView
from django.contrib.auth.views import LoginView 
from django.urls import reverse_lazy
from .models import Task
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# Create your views here.

class CustomLoginView(LoginView):
    fields = '__all__';
    redirect_authenticated_user = True;
    #success_url = reverse_lazy('tasks')    
    def get_success_url(self) :
       return reverse_lazy('tasks'); 
    template_name = 'base/login.html'

class Register(FormView):
    form_class = UserCreationForm;
    template_name = 'base/register.html';
    redirect_authenticated_user = True;
    success_url= reverse_lazy('login'); 

    def form_valid(self, form):
        user = form.save();
        return super(Register,self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(Register, self).get(*args, **kwargs)


class TaskList(LoginRequiredMixin,ListView):
    model = Task;
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user = self.request.user)   
        context['count'] = context['tasks'].filter(complete=False).count()
        search_input = self.request.GET.get('search-area') or '';
        if search_input :
            context['tasks']= context['tasks'].filter(title__startswith = search_input)

        else:
            context['search_input']=  search_input


        return context

class TaskDetail(LoginRequiredMixin,DetailView):
    model=Task
    context_object_name = 'task'
    template_name = 'base/task.html'
    

class TaskCreate(LoginRequiredMixin,CreateView):
    model = Task;
    fields = '__all__';
    success_url = reverse_lazy('tasks')
    fields = ['title', 'description','complete' ]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate,self).form_valid(form)


class TaskUpdate(LoginRequiredMixin,UpdateView):
    model = Task;
    fields = '__all__';
    success_url = reverse_lazy('tasks');
    fields = ['title', 'description','complete' ]

class TaskDelete(LoginRequiredMixin,DeleteView):
    model = Task;
    context_object_name = 'task';
    success_url= reverse_lazy('tasks');
   





