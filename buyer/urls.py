from django.urls import path
from .views import *

urlpatterns = [

    # Urls
    path('', BuyerView.as_view(), name='Buyer'),
    path('<str:pk_buyer>/', BuyerUpdateView.as_view(), name='Buyer-update'),
    # path('<str:pk_buyer>/summary/',
    #      BuyerSummaryView.as_view(), name='Buyer-update'),
    path('<str:pk_buyer>/profile/', BuyerDetailsView.as_view(), name='Buyer-more'),
    path('<str:pk_buyer>/profile/update/',
         BuyerDetailsUpdateView.as_view(), name='Buyer-more-update'),
]
