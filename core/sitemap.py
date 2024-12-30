from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Item  # Thay thế bằng model của bạn

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['core:home', 'core:order-summary', 'core:contact']  # Tên các URL được đặt trong urls.py

    def location(self, item):
        return reverse(item)

class ProductSitemap(Sitemap):
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        return Item.objects.all()  # Lấy danh sách sản phẩm từ model

    def lastmod(self, obj):
        return obj.updated_at  # Trường ngày cập nhật cuối cùng trong model