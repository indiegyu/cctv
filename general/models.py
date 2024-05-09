from django.utils import timezone
import os
from uuid import uuid4
from django.db import models

class Location(models.Model):
    area_id = models.AutoField(primary_key=True)
    area_location_latitude = models.DecimalField(max_digits=50, decimal_places=30)
    area_location_longitude = models.DecimalField(max_digits=50, decimal_places=30)
    area_name = models.CharField(max_length=50)
    detected_people = models.IntegerField()
    risk_point = models.CharField(max_length=10)
    
    def __str__(self):
        return self.area_name

class CCTV(models.Model):
    cctv_id = models.AutoField(primary_key=True)
    area = models.ForeignKey('Location',related_name = 'area', on_delete=models.CASCADE)
    cctv_channel = models.IntegerField()
    detected_people = models.IntegerField()
    risk_point = models.CharField(max_length=10)
    rtsp_url = models.CharField(max_length=2048, blank=True)
    http_url = models.CharField(max_length=2048, blank=True)
    #function that helps to upload the image
    def upload_to_func(self, filename):
        prefix = os.path.join(timezone.now().strftime("%Y/%m/%d"))
        # change the file name into uuid form
        file_name = timezone.now().strftime("%H%M%S")
        extension = os.path.splitext(filename)[-1].lower() # 확장자 추출
        return "/".join(
            [prefix, file_name + extension,]
        )
        
    cctv_image = models.ImageField(blank=True, upload_to='upload_to_func')
    

class Target_area(models.Model):
    target_area_id = models.AutoField(primary_key=True)
    cctv = models.ForeignKey('CCTV',related_name = 'cctv', on_delete=models.CASCADE)
    risk_point = models.CharField(max_length=10)

class Target_area_point(models.Model):
    target_area = models.ForeignKey('Target_area',related_name = "target_area", on_delete=models.CASCADE)
    point_x = models.DecimalField(max_digits=50, decimal_places=30)
    point_y = models.DecimalField(max_digits=50, decimal_places=30)
