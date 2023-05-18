from django.contrib import admin

from .models import CarImages, CarIssues, FoodImages,ReportProduct, Address, Manufacturer, Warranty
# admin.site.register(CarIssues)
# admin.site.register(CarImages)
# admin.site.register(FoodImages)
# admin.site.register(ReportProduct)
admin.site.register(Address)
admin.site.register(Manufacturer)
admin.site.register(Warranty)