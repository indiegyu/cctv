from django.contrib import admin
from .models import Location, CCTV, Target_area, Target_area_point

class LocationAdmin(admin.ModelAdmin):
    list_display = ['area_name']

class CCTVAdmin(admin.ModelAdmin):
    list_display = ['area_name_cctv_channel']

    def area_name_cctv_channel(self, obj):
        return f"{obj.area.area_name} {obj.cctv_channel}"

class CCTVTargetAreaAdmin(admin.ModelAdmin):
    list_display = ['cctv_area_cnt']

    def cctv_area_cnt(self, obj):
        return f"{obj.cctv.area.area_name} {obj.cctv.cctv_channel} {obj.target_area_id}"

class TargetPointAdmin(admin.ModelAdmin):
    list_display = ['points_name']

    def points_name(self, obj):
        return f"{obj.target_area.cctv.area.area_name} {obj.target_area.cctv.cctv_channel} {obj.target_area.target_area_id} {obj.point_x}, {obj.point_y}"

admin.site.register(Location, LocationAdmin)
admin.site.register(CCTV, CCTVAdmin)
admin.site.register(Target_area, CCTVTargetAreaAdmin)
admin.site.register(Target_area_point, TargetPointAdmin)
