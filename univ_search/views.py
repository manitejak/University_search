import json
from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from .models import University
# Create your views here.

from django.core.paginator import Paginator


def paginate_queryset(queryset, size, page_no):
    pagination_details = dict()
    try:
        pagination_details['total_count'] = queryset.count()
    except TypeError:
        pass
    paginator = Paginator(queryset, int(size))
    queryset = paginator.page(page_no)
    pagination_details['has_previous'] = queryset.has_previous()
    pagination_details['has_next'] = queryset.has_next()
    pagination_details['total_pages'] = paginator.num_pages
    pagination_details['current_page'] = page_no
    return queryset, pagination_details


class UniversitySearchInterface(View):

    def get(self, request):
        result = dict()
        try:
            country = request.GET.get('country',None)
            top_level_domain =  request.GET.get('domain',None)
            paginate = True if request.GET['paginate'].upper() == 'TRUE' else False
            search = True if request.GET['search'].upper() == 'TRUE' else False
            univ_objects = University.objects.filter().order_by('-id')
            print(univ_objects)
            if country:
                univ_objects = univ_objects.filter(country__icontains=country)
            if top_level_domain:
                univ_objects = univ_objects.filter(domain__icontains=top_level_domain)
            if search:
                search_query = request.GET['name']
                search_by_name = univ_objects.filter(name__icontains=search_query)
                univ_objects = search_by_name
            if paginate:
                page = request.GET['page']
                size = request.GET['size']
                univ_objects, pagination_details = paginate_queryset(univ_objects, size, page)
            result['data'] = [obj.get_model_as_json() for obj in univ_objects]
            if paginate:
                result['has_previous'] = pagination_details['has_previous']
                result['has_next'] = pagination_details['has_next']
                result['total_pages'] = pagination_details['total_pages']
                result['current_page'] = pagination_details['current_page']
                result['total_count'] = pagination_details['total_count']
            result['result'] = 'SUCCESS'
            result['status'] = 200

        except Exception as e:
            result['status'] = 500
            result['error_reason'] = str(e)
            result['result'] = 'FAILURE'
        return JsonResponse(result, safe=True, status=result['status'])

    def post(self, request):
        result = dict()
        try:
            post_data = json.loads(request.body)
            if len(post_data) != 0:
                for i in range(len(post_data)):
                    name = post_data[i]['name'].title()
                    country = post_data[i]['country'].upper()
                    domain = post_data[i]['domain'].lower()
                    alpha_two_code = post_data[i]['alpha_two_code'].upper()
                    web_page = post_data[i]['web_page'].lower()
                    univ = University(name=name,country=country,domain=domain,alpha_two_code=alpha_two_code,web_page=web_page)
                    univ.save()
                result['status'] = 200
                result['data'] = univ.pk
                result['result'] = 'SUCCESS'
            else:
                result['status'] = 500
                result['error_reason'] = 'list is empty'
                result['result'] = 'FAILURE'
        except KeyError as key:
            result['status'] = 400
            result['error_reason'] = 'Bad Request- Missing argument: ' + str(key)
            result['result'] = 'FAILURE'
        except Exception as e:
            result['status'] = 500
            result['error_reason'] = str(e)
            result['result'] = 'FAILURE'
        return JsonResponse(result, safe=True, status=result['status'])

    def put(self, request):
        result = dict()
        try:
            put_data = json.loads(request.body)
            univ_id = put_data['university_id']
            univ_object = University.objects.get(id=univ_id)
            try:
                name = put_data['name']
                try:
                    if name != "":
                        univ_object.name = name
                        univ_object.modified_on = datetime.now()
                        univ_object.save()
                except:
                    pass
            except KeyError:
                try:
                    country = put_data['country']
                    try:
                        if country != "":
                            univ_object.country = country
                            univ_object.modified_on = datetime.now()
                            univ_object.save()
                    except KeyError:
                        pass
                except KeyError:
                    try:
                        domain = put_data['domain']
                        try:
                            if domain != "":
                                univ_object.domain = domain
                                univ_object.modified_on = datetime.now()
                                univ_object.save()
                        except KeyError:
                            pass
                    except KeyError:
                        try:
                            alpha_two_code = put_data['alpha_two_code']
                            try:
                                if alpha_two_code != "":
                                    univ_object.alpha_two_code = alpha_two_code
                                    univ_object.modified_on = datetime.now()
                                    univ_object.save()
                            except KeyError:
                                pass
                        except KeyError:
                            try:
                                web_page = put_data['web_page']
                                try:
                                    if web_page != "":
                                        univ_object.web_page = web_page
                                        univ_object.modified_on = datetime.now()
                                        univ_object.save()
                                except KeyError:
                                    pass
                            except:
                                pass
            result['status'] = 200
            result['result'] = 'SUCCESS'
            result['message'] = 'university data updated successfully'
        except ObjectDoesNotExist as od:
            result['status'] = 500
            result['error_reason'] = str(od)
            result['result'] = 'FAILURE'
        except ValueError as ve:
            result['status'] = 500
            result['error_reason'] = str(ve)
            result['result'] = 'FAILURE'
        return JsonResponse(result, safe=True, status=result['status'])

    def delete(self, request):
        result = dict()
        put_data = json.loads(request.body)
        univ_id = put_data['university_id']
        try:
            univ_obj = University.objects.get(id=univ_id)
            univ_obj.delete()
            result['status'] = 200
            result['message'] = 'University deleted successfully'
            result['result'] = 'SUCCESS'
        except University.DoesNotExist:
            result['status'] = 404
            result['error_reason'] = 'University not found'
            result['result'] = 'FAILURE'
        return JsonResponse(result, safe=True, status=result['status'])