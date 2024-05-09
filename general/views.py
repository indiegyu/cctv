from django.http import JsonResponse
from .models import Location, CCTV
from django.shortcuts import render, get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
import requests

def index_view(request):
    area_all = Location.objects.all()
    return render(request, 'index.html', {"area_list": area_all})


def area(request):
    return render(request, "area_page.html")


def area_view(request, pk):
    area = Location.objects.get(area_id=pk)
    cctvs = area.area.all()  # 해당 지역의 모든 CCTV 가져오기
    return render(request, 'area_page.html', {'area': area, 'cctvs': cctvs})


def detail_area_view(request, pk, pk2):  
    area = get_object_or_404(Location, area_id=pk)
    cctv = get_object_or_404(CCTV, cctv_channel=pk2)
    return render(request, 'detail_area_page.html', {'cctv': cctv, 'area': area})


def statistics_view(request):
    return render(request, "statistics.html")


from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CCTV
import requests
# views.py
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from .models import Location, CCTV
from rest_framework.views import APIView
from rest_framework.response import Response

class ExternalAPIView(APIView):
    def get(self, request):
        try:
            # 모든 CCTV 객체 가져오기
            cctvs = CCTV.objects.all()
            
            # 모든 CCTV 객체에 대해 반복하면서 처리
            for cctv in cctvs:
                # CCTV 객체의 rtsp_url 가져오기
                rtsp_url = cctv.rtsp_url
                
                # 외부 API에 GET 요청 보내기
                response = requests.get(f'http://61.75.117.152:8080/analyze?rtsp_url={rtsp_url}')
                
                # 응답 데이터에서 감지된 사람 수 가져오기
                data = response.json()
                detected_people = data.get('number_of_object', 0)

                # 데이터베이스에 감지된 사람 수 업데이트
                cctv.detected_people = detected_people
                cctv.save()
                
            # 각 지역에 대해 반복하면서 감지된 사람 수 합산하여 업데이트
            areas = Location.objects.all()
            for area in areas:
                total_detected_people = CCTV.objects.filter(area=area).aggregate(Sum('detected_people'))['detected_people__sum'] or 0
                area.detected_people = total_detected_people
                area.save()
                
            # 처리 완료 후 응답 반환
            return Response({'message': 'CCTV data updated successfully'})
        except Exception as e:
            return Response({'error': str(e)}, status=500)

class UpdateAreaDetectedPeople(APIView):
    def get(self, request, area_id):
        # 해당 area_id에 해당하는 Location 객체 가져오기
        area = get_object_or_404(Location, area_id=area_id)

        # 해당 지역의 detected_people 값 가져오기
        detected_people = area.detected_people

        # detected_people 값을 JSON 형태로 반환
        return Response({'detected_people': detected_people})
