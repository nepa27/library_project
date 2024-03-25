from django.contrib.auth.mixins import (
    LoginRequiredMixin, UserPassesTestMixin)
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.db import models
from django.utils import timezone
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView)
from django.shortcuts import redirect, get_object_or_404

from .models import Book, Status, HistoryMove
from .forms import BookForm

User = get_user_model()


class BookDetailView(LoginRequiredMixin, DetailView):
    model = Book
    context_object_name = 'book'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                models.Q(title__icontains=query)
                | models.Q(author__icontains=query))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_admin'] = self.request.user.is_superuser
        if self.request.user.is_superuser:
            context['book_movements'] = HistoryMove.objects.filter(
                book=self.object
            ).order_by('-action_date')
        return context


class BookListView(LoginRequiredMixin, ListView):
    model = Book
    context_object_name = 'book_list'
    ordering = 'title'
    paginate_by = 10


def take_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if not book.is_taken:
        status, created = Status.objects.get_or_create(
            book=book,
            defaults={'user': request.user, 'taken_at': timezone.now()}
        )
        if not created:
            status.user = request.user
            status.taken_at = timezone.now()
            status.returned_at = None
            status.save()
        HistoryMove.objects.create(
            book=book,
            user=request.user,
            action='Взята'
        )
        book.is_taken = True
        book.save()
    return redirect(reverse_lazy('library:list'))


def return_book(request, pk, next_=None):
    book = get_object_or_404(Book, pk=pk)
    if book.is_taken and book.status.user == request.user:
        status = book.status
        status.returned_at = timezone.now()
        status.save()
        HistoryMove.objects.create(
            book=book,
            user=request.user,
            action='Возвращена'
        )
        book.is_taken = False
        book.save()
        if next_ == 'profile':
            return redirect(
                reverse_lazy('library:profile')
            )
        if next_ == 'my_books':
            return redirect(
                reverse_lazy('library:my_books')
            )
        else:
            return redirect(
                reverse_lazy('library:list')
            )


class MyBooksView(LoginRequiredMixin, ListView):
    model = Status
    template_name = 'library/my_books.html'
    context_object_name = 'my_books'
    paginate_by = 10

    def get_queryset(self):
        queryset = Status.objects.filter(
            user=self.request.user,
            returned_at__isnull=True
        ).order_by('-taken_at')
        query = self.request.GET.get('q')
        if query:
            queryset = (queryset.filter(
                book__title__icontains=query)
                        | queryset.filter(book__author__icontains=query)
                        )
        return queryset


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'library/profile.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_books_list = Status.objects.filter(
            user=self.request.user,
            returned_at__isnull=True
        ).order_by('-taken_at')
        paginator = Paginator(user_books_list, 4)

        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        return context


class BookUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Book
    fields = ['title', 'author', 'year']
    template_name = 'library/book_edit.html'
    context_object_name = 'book'
    success_url = reverse_lazy('library:list')

    def test_func(self):
        return self.request.user.is_superuser


class DebtorsListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'library/debtors_list.html'
    context_object_name = 'debtors'
    paginate_by = 5

    def test_func(self):
        return self.request.user.is_superuser

    def get_queryset(self):
        return User.objects.filter(
            books_taken__returned_at__isnull=True
        ).distinct()


class BookCreateView(UserPassesTestMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = 'library/book_add.html'
    success_url = reverse_lazy('library:list')

    def test_func(self):
        return self.request.user.is_superuser


class BookDeleteView(UserPassesTestMixin, DeleteView):
    model = Book
    template_name = 'library/book_confirm_delete.html'
    success_url = reverse_lazy('library:list')

    def test_func(self):
        return self.request.user.is_superuser
