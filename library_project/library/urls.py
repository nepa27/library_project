from django.urls import path

from . import views

app_name = 'library'

urlpatterns = [
    path('list/', views.BookListView.as_view(),
         name='list'),
    path('list/take_book/<int:pk>/', views.take_book,
         name='take_book'),
    path('list/return_book/<int:pk>/', views.return_book,
         name='return_book'),
    path('list/return_book/<int:pk>/<str:next_>/', views.return_book,
         name='return_book_with_next'),
    path('my_books/', views.MyBooksView.as_view(),
         name='my_books'),
    path('profile/', views.ProfileView.as_view(),
         name='profile'),
    path('books/<int:pk>/', views.BookDetailView.as_view(),
         name='book_detail'),
    path('books/<int:pk>/edit/', views.BookUpdateView.as_view(),
         name='book_update'),
    path('books/add/', views.BookCreateView.as_view(),
         name='book_add'),
    path('debtors/', views.DebtorsListView.as_view(),
         name='debtors'),
    path('books/delete/<int:pk>/', views.BookDeleteView.as_view(),
         name='book_delete')
]
