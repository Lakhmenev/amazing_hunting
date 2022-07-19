import json

from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Count, Avg
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from amazing_hunting import settings
from vacancies.models import Vacancy, Skill
from vacancies.serializers import VacancyListSerializer, VacancyDetailSerializer, VacancyCreateSerializer, \
    VacancyUpdateSerializer, VacancyDestroySerializer


def hello(request):
    return HttpResponse("Hello world")


class VacancyListView(ListAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyListSerializer

    # def get(self, request, *args, **kwargs):
    #     super().get(request, *args, **kwargs)
    #
    #     search_text = request.GET.get("text", None)
    #     if search_text:
    #         self.object_list = self.object_list.filter(text=search_text)
    #
    #     # сортировка
    #     self.object_list = self.object_list.select_related("user").prefetch_related("skills").order_by("text")
    #
    #     # """
    #     # 1 - 0:10
    #     # 2 - 10:20
    #     # 3 - 20:30
    #     # ручная пагинация
    #     # """
    #     # total = self.object_list.count()
    #     # page_number = int(request.GET.get("page", 1))
    #     # offset = (page_number-1) * settings.TOTAL_ON_PAGE
    #     # if (page_number-1) * settings.TOTAL_ON_PAGE < total:
    #     #     self.object_list = self.object_list[offset:offset+settings.TOTAL_ON_PAGE]
    #     # else:
    #     #     self.object_list = self.object_list[offset:offset+total]
    #
    #     paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
    #     page_number = request.GET.get("page")
    #     page_obj = paginator.get_page(page_number)
    #
    #     list(map(lambda x: setattr(x, "username", x.user.username if x.user else None), page_obj))
    #
    #     response = {
    #         "items": VacancyListSerializer(page_obj, many=True).data,
    #         "num_pages": paginator.num_pages,
    #         "total": paginator.count
    #     }
    #
    #     # для избавления от крякозябр на русском в браузере
    #     # return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": False})
    #     return JsonResponse(response, safe=False)


class VacancyDetailView(RetrieveAPIView):
        queryset = Vacancy.objects.all()
        serializer_class = VacancyDetailSerializer

        # def get(self, request, *args, **kwargs):
        #     vacancy = self.get_object()
        #
        #     return JsonResponse(VacancyDetailSerializer(vacancy).data)


class VacancyCreateView(CreateAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyCreateSerializer

    # def post(self, request, *args, **kwargs):
    #     vacancy_data = VacancyCreateSerializer(data=json.loads(request.body))
    #     if vacancy_data.is_valid():
    #         vacancy_data.save()
    #     else:
    #         return JsonResponse(vacancy_data.errors)
    #
    #     return JsonResponse(vacancy_data.data)


class VacancyUpdateView(UpdateAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyUpdateSerializer

    # def patch(self, request, *args, **kwargs):
    #     super().post(request, *args, **kwargs)
    #
    #     vacancy_data = json.loads(request.body)
    #     self.object.slug = vacancy_data["slug"]
    #     self.object.text = vacancy_data["text"]
    #     self.object.status = vacancy_data["status"]
    #
    #     for skill in vacancy_data["skills"]:
    #         try:
    #             skill_obj = Skill.objects.get(name=skill)
    #         except Skill.DoesNotExist:
    #             return JsonResponse({"error": "Skill not found"}, status=404)
    #         self.object.skills.add(skill_obj)
    #
    #     self.object.save()
    #
    #     return JsonResponse({
    #         "id": self.object.id,
    #         "text": self.object.text,
    #         "slug": self.object.slug,
    #         "status": self.object.status,
    #         "created": self.object.created,
    #         "user": self.object.user_id,
    #         "skills": list(self.object.skills.all().values_list("name", flat=True)),
    #     })


class VacancyDeleteView(DestroyAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyDestroySerializer



    # def delete(self, request, *args, **kwargs):
    #     super().delete(request, *args, **kwargs)
    #
    #     return JsonResponse({"status": "ok"}, status=200)


class UserVacancyDetailView(View):
    def get(self, request):
        user_qs = User.objects.annotate(vacancies=Count('vacancy'))

        paginator = Paginator(user_qs, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        users = []
        for user in page_obj:
            users.append({
                "id": user.id,
                "name": user.username,
                "vacancies": user.vacancies
            })

        response = {
            "items": users,
            "total": paginator.count,
            "num_pages": paginator.num_pages,
            "avg": user_qs.aggregate(avg=Avg('vacancies'))["avg"]
        }

        return JsonResponse(response)
