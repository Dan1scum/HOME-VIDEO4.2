from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.contrib import messages


class MovieOwnerTestMixin(UserPassesTestMixin):
    """
    Проверяет, является ли пользователь автором фильма или администратором
    """
    
    def test_func(self):
        movie = self.get_object()
        return movie.author == self.request.user or self.request.user.is_staff
    
    def handle_no_permission(self):
        messages.error(self.request, 'You do not have permission to perform this action')
        return redirect('movies:list')


class ProfileOwnerTestMixin(UserPassesTestMixin):
    """
    Проверяет, является ли пользователь владельцем профиля или администратором
    """
    
    def test_func(self):
        profile_user_id = self.kwargs.get('user_id')
        return str(self.request.user.id) == str(profile_user_id) or self.request.user.is_staff
    
    def handle_no_permission(self):
        messages.error(self.request, 'You can only edit your own profile')
        return redirect('movies:profile')
