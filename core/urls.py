from django.urls import path
#from django.conf.urls import url
from django.urls import re_path as url
from django.contrib.sitemaps.views import sitemap
import core.views
from .views import (
    ItemDetailView,
    CheckoutView,
    HomeView,
    OrderSummaryView,
    add_to_cart,
    remove_from_cart,
    remove_single_item_from_cart,
    payment_return,
    PaymentView,
    index_vnp,
    # VNPAYPaymentView,
    AddCouponView,
    RequestRefundView,
    ProductListView,
    robots_txt,
    cart_history_view
)
from core.sitemap import StaticViewSitemap, ProductSitemap

sitemaps = {
    'static': StaticViewSitemap,
    'products': ProductSitemap,
}
app_name = 'core'

urlpatterns = [
    path('products_list', ProductListView.as_view(), name='product_list'),
    path('', HomeView.as_view(), name='home'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('add-coupon/', AddCouponView.as_view(), name='add-coupon'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart,
         name='remove-single-item-from-cart'),
    path('payment/paypal/', PaymentView.as_view(), name='payment'),
    path('payment/stripe/', PaymentView.as_view(), name='payment'),
    #path('payment/vnpay/', VNPAYPaymentView.as_view(), name='vnpay_payment'),
    path('request-refund/', RequestRefundView.as_view(), name='request-refund'),
    path('cart-history/', cart_history_view, name='cart_history'),
    #path('payment/vnpay/return/', payment_return, name='vnpay_return'),


    path('vnpay', core.views.index_vnp, name='index'),
    path('payment_vnp', core.views.paymentVNP, name='payment_vnpay'),
    path('payment_ipn', core.views.payment_ipn, name='payment_ipn'),
    path('payment/vnpay_return', core.views.payment_return, name='vnpay_return'),
    path('query', core.views.query, name='query'),
    path('refund', core.views.refund, name='refund'),
    #path('admin/', admin.site.urls),

    path('contact', core.views.contact, name='contact'),
    #sitemap
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    #robot.txt
    path("robots.txt", robots_txt, name="robots_txt"),
]
