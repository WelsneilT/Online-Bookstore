from django.urls import path
from .views import BooksListView, BooksDetailView, BookCheckoutView, paymentComplete, SearchResultsListView,SearchAuthorListView,SearchTitleListView


urlpatterns = [
    path('', BooksListView.as_view(), name = 'list'),
    path('<int:pk>/', BooksDetailView.as_view(), name = 'detail'),
    path('<int:pk>/checkout/', BookCheckoutView.as_view(), name = 'checkout'),
    path('complete/', paymentComplete, name = 'complete'),
    path('search/', SearchAuthorListView.as_view(), name = 'search_results'),
    path('search/', SearchTitleListView.as_view(), name = 'search_title'),
]