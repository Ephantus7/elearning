from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import PasswordChangeView
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from django_messages.forms import ComposeForm
from .models import CustomUser, Student, Teacher, Course, Subject


def lockout(request, credentials, *args, **kwargs):
    return JsonResponse({"status": "Locked out due to too many login failures"}, status=403)


class UserLoginView(LoginView):
    template_name = 'registration/login.html'

    def get(self, request, *args, **kwargs):
        form = AuthenticationForm()
        return render(request, 'registration/login.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                
                messages.success(request, 'Login successful')
                return HttpResponseRedirect(reverse('dashboard'))
            else:
                messages.error(request, 'Invalid username or password')
                return HttpResponseRedirect(reverse('login'))
        else:
            messages.error(request, 'Invalid username or password')
            return HttpResponseRedirect(reverse('login'))
        

class UserPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    login_url = 'login'
    redirect_field_name = 'redirect_to'
    template_name = 'registration/password_change_form.html'
    success_url = reverse_lazy('profile')

    def get(self, request, *args, **kwargs):
        form = PasswordChangeForm(request.user)
        user = get_object_or_404(CustomUser, id=request.user.id)

        if user.is_superuser:
            return HttpResponseRedirect(reverse('admin:index'))
        elif user.user_type == 2:
            base_template = 'teachers/teacher_base.html'
        elif user.user_type == 3:
            base_template = 'students/student_base.html'
        return render(request, 'registration/password_change_form.html', {'form': form, 'base_template': base_template})

    def post(self, request, *args, **kwargs):
        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)

            messages.success(self.request, 'Password changed successfully')
            return HttpResponseRedirect(reverse('profile'))

        else:
            messages.error(self.request, 'Password change failed')
            return HttpResponseRedirect(reverse('password_change'))


class HomePageView(TemplateView):
    template_name = 'home.html'
    

class DashboardView(LoginRequiredMixin, TemplateView):
    login_url = 'login'
    redirect_field_name = 'redirect_to'
    
    def get(self, request, *args, **kwargs):
        user = get_object_or_404(CustomUser, id=request.user.id)
        user_type = user.user_type

        if user.is_superuser:
            return HttpResponseRedirect(reverse('admin:index'))

        elif user_type == 2:
            return HttpResponseRedirect(reverse_lazy('teacher_home'))

        elif user_type == 3:
            return HttpResponseRedirect(reverse_lazy('student_home'))

        else:
            return HttpResponseRedirect(reverse_lazy('home'))


class ProfilePageView(LoginRequiredMixin, TemplateView):
    login_url = 'login'
    redirect_field_name = 'redirect_to'

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(CustomUser, id=request.user.id)
        user_type = user.user_type

        if user.is_superuser:
            return HttpResponseRedirect(reverse('admin:index'))

        elif user_type == 2:
            template_name = 'teachers/teacher_profile.html'
            context = {
                'teacher': get_object_or_404(Teacher, user=request.user.id),
            }
            return render(request, template_name, context)

        elif user_type == 3:
            template_name = 'students/student_profile.html'
            context = {
                'student': get_object_or_404(Student, user=request.user.id),
            }
            return render(request, template_name, context)

        else:
            template_name = 'home.html'

        return render(request, template_name, {'user': user})
    
    
class CoursesView(LoginRequiredMixin, TemplateView):
    login_url = 'login'
    redirect_field_name = 'redirect_to'
    template_name = 'courses/courses.html'
    
    def get(self, request, *args, **kwargs):
        user = get_object_or_404(CustomUser, id=request.user.id)
        user_type = user.user_type
        
        if user_type == 2:
            base_template = "teachers/teacher_base.html"
            context = {
                'courses': get_object_or_404(Course, teacher__user=user),
                'base_template': base_template,
            }
            return render(request, self.template_name, context)
        
        elif user_type == 3:
            base_template = "students/student_base.html"
            context = {
                'courses': get_object_or_404(Course, student__user=user),
                'base_template': base_template,
            }
            return render(request, self.template_name, context)

  
class ContactView(LoginRequiredMixin, TemplateView):
    login_url = 'login'
    redirect_field_name = 'redirect_to'
    template_name = 'contact.html'
    
    def get(self, request, *args, **kwargs):
        user = get_object_or_404(CustomUser, id=request.user.id)
        user_type = user.user_type
        form = ComposeForm()
        
        if user_type == 1:
            return HttpResponseRedirect(reverse('admin:index'))        
        elif user_type == 2:
            base_template = "teachers/teacher_base.html"
            context = {
                'base_template': base_template,
                'form': form,
            }
            return render(request, self.template_name, context)
    
        elif user_type == 3:
            base_template = "students/student_base.html"
            context = {
                'base_template': base_template,
                'form': form,
            }
            return render(request, self.template_name, context)
        
        elif user_type == 4:
            base_template = "hod/hod_base.html"
            context = {
                'base_template': base_template,
                'form': form,
            }
            return render(request, self.template_name, context)
        
        return render(request, 'home.html')
    

class StudentProfileView(LoginRequiredMixin, TemplateView):
    login_url = 'login'
    redirect_field_name = 'redirect_to'
    template_name = 'profile/student_profile.html'
    
    def get(self, request, *args, **kwargs):
        user = get_object_or_404(CustomUser, id=request.user.id)
        user_type = user.user_type
        
        student = get_object_or_404(pk=self.kwargs['pk'], user=user)
        
        if user_type == 1:
            return HttpResponseRedirect(reverse('admin:index'))
        
        elif user_type == 2:
            base_template = "teachers/teacher_base.html"
            context = {
                'student': student,
                'base_template': base_template,
            }
            return render(request, self.template_name, context)
        
        elif user_type == 3:
            base_template = "students/student_base.html"
            context = {
                'student': student,
                'base_template': base_template,
            }
            return render(request, self.template_name, context)

        return render(request, 'home.html')
    

class TeacherProfileView(LoginRequiredMixin, TemplateView):
    login_url = 'login'
    redirect_field_name = 'redirect_to'
    template_name = 'profile/teacher_profile.html'
    
    def get(self, request, *args, **kwargs):
        user = get_object_or_404(CustomUser, id=request.user.id)
        user_type = user.user_type
        
        teacher = get_object_or_404(Teacher, pk=self.kwargs['pk'])
        
        if user.is_superuser:
            return HttpResponseRedirect(reverse('admin:index'))
        
        elif user_type == 2:
            base_template = "teachers/teacher_base.html"
            context = {
                'teacher': teacher,
                'base_template': base_template,
            }
            return render(request, self.template_name, context)
        
        elif user_type == 3:
            base_template = "students/student_base.html"
            context = {
                'teacher': teacher,
                'base_template': base_template,
            }
            return render(request, self.template_name, context)
        return render(request, 'home.html')
    
    
class UserLogoutView(TemplateView):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(self.request, f"You have successfully logged out.")
        return redirect(request, 'home.html', {'messages': messages})


class SignupView(TemplateView):
    template_name = 'registration/signup.html'
