from django.template import Context, loader
from django.http import HttpResponse
from my_app.models import AdditionalInfo, CaseDetails, PageContent, SearchCriteria

def index(request):
    additional_info_list = AdditionalInfo.objects.all()
    case_details_list = CaseDetails.objects.all()
    page_content_list = PageContent.objects.all()
    search_criteria_list = SearchCriteria.objects.all()
    html_template = loader.get_template('/home/mis/DjangoProject/django-test/mysite/my_app/Templates/index.html')
    contetnts = Context({'case_details_list': case_details_list,
                            'additional_info_list': additional_info_list,
                            'page_content_list': page_content_list,
                            'search_criteria_list': search_criteria_list,})
    return HttpResponse(html_template.render(contetnts))

