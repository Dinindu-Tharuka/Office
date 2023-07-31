
from django.contrib import admin
from import_export import resources
from .models import Client, Job, Sector, City, District, Province, Category



class ClientDetailResourse(resources.ModelResource):
    job = resources.Field(attribute='job__job_title')
    sector = resources.Field(attribute='sector__sector_title')
    city = resources.Field(attribute='city__city_title')
    district = resources.Field(attribute='district__district_title')
    province = resources.Field(attribute='province__province_title')
    category = resources.Field(attribute='category__category_title')
    first_name = resources.Field(attribute='user__first_name')
    last_name = resources.Field(attribute='user__last_name')
    class Meta:
        model = Client
        fields = ['id', "first_name", "last_name", "number", "nic", "date_of_issue", "address", "birthday", "gender", "precent_working_place", "is_sri_lanka", "remark", "job", "sector", "city", "district", "province", "category"]
        export_order = ['id', "first_name", "last_name", "number", "nic", "date_of_issue", "address", "birthday", "gender", "precent_working_place", "is_sri_lanka", "remark", "job", "sector", "city", "district", "province", "category"]

    
        


class SimpleFilter(admin.SimpleListFilter):
    pass

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display=['id', 'number', 'nic', 'date_of_issue', 'birthday', 'gender', 'precent_working_place', 'photo', 'is_sri_lanka', 'remark', 'job', 'sector', 'city', 'district', 'province', 'category']
    list_per_page = 5
    list_editable = ['precent_working_place', 'photo', 'is_sri_lanka', 'remark', 'job', 'sector', 'city', 'district', 'province', 'category']
    list_select_related = ['job', 'sector', 'city', 'district', 'province', 'category']

    list_filter = ['category', 'job', 'sector', 'province', 'district', 'city']
    search_fields = ['user__first_name__istartswith', 'user__last_name__istartswith'] 
   
    
   



@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    pass

@admin.register(Sector)
class SectorAdmin(admin.ModelAdmin):
    pass

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    pass

@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    pass

@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    pass

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


