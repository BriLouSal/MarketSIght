from django.urls import path, include
from django.http import HttpResponse
from django.conf import settings
from . import views, MSOAI
import yfinance as yf



#  Append stock list when users add stock


#  We wanna get user information based on stocks


urlpatterns = [
    path('', views.search, name='search'),
    path('room/',  views.portfolio_room, name='room'),
    path('stock/<str:stock_tick>/', views.stock, name='stock'),
    # path("api/stock/<str:stock_tick>/", views.json_api, name="stock_json"), Not sure about this one, I will add this if I need to create an API gateway for graph
    path('login/', views.loginpage, name='login'),
    path('signup/',views.signup, name='signup'),
    path('support/',views.assistance, name='assistance'),
    path('logout/', views.logout_page, name='logout_page'),
    # Create a autoupdating stock path for Javascript, AND ALSO FOR STOCK ORDERS
    # URL FOR API CALLS FOR JS
    path("api/json_data_api/<str:stock>/<str:interval>/", views.json_data_view, name="json_data_view"),
    path("api/latest-price/<str:stock>/", views.latest_price, name="latest_price"),
    path("api/autocomplete/<str:letters>/", views.information_letter, name="information_letter"),
    path("api/capm/<str:tickers>/", views.capital_asset_pricing_models, name="capital_asset_pricing_models"),
    
    # SO we can directly interact with views.py and work with our database from the models
    path("trade/<str:ticker>/<str:order_type>/", views.stockOrder, name="stockOrder"),
    




]




if settings.DEBUG:
    # Include django_browser_reload URLs only in DEBUG mode
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
    ]




# room/<str:room_number> - This will match URLs like /room/1, /room/2, and so on. The <str:room_number> part of the URL captures the room number as a string.

