#!encoding:utf-8
from django.shortcuts import render

# Create your views here.

from django.views.generic import View
from models import CourseOrg,CityDict

from django.shortcuts import render_to_response
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

class OrgView(View):
    '''
    课程机构列表功能
    '''
    def get(self,request):
        #课程机构
        all_orgs = CourseOrg.objects.all()
        hot_orgs = all_orgs.order_by("-click_number")[:3]

        #取出筛选城市
        city_id = request.GET.get('city','')
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))

        #城市
        all_citys = CityDict.objects.all()

        #类别筛选
        category  = request.GET.get('ct','')
        if category:
            all_orgs = all_orgs.filter(category=category)

        sort = request.GET.get('sort')
        if sort:
            if sort == "students":
                all_orgs = all_orgs.order_by("-students")
            elif sort == "courses":
                all_orgs = all_orgs.order_by("-courses_nums")

        #对课程机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_orgs, 5,request=request)
        orgs = p.page(page)
        org_nums = all_orgs.count()
        return render(request,'org-list.html',{
            "all_orgs":orgs,
            "all_citys":all_citys,
            "org_nums":org_nums,
            "city_id":city_id,
            "category":category,
            "hot_orgs":hot_orgs,
            "sort":sort
        })