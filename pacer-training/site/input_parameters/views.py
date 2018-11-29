from django.template import Context, loader
from django.http import HttpResponse
from input_parameters.models import AdditionalInfo, CaseDetails, PageContent, SearchCriteria

def index(request):

    html_template = loader.get_template('/home/mis/DjangoProject/pacer-training/site/my_app/Templates/index.html')
    contetnts = Context({})
    return HttpResponse(html_template.render(contetnts))

def search(request):
    html_template = loader.get_template('/home/mis/DjangoProject/pacer-training/site/my_app/Templates/search.html')
    search_criteria_list = SearchCriteria.objects.all()
    contents = Context({'search_criteria_list': search_criteria_list,})
    return HttpResponse(html_template.render(contents))

def content(request):
    html_template = loader.get_template('/home/mis/DjangoProject/pacer-training/site/my_app/Templates/contents.html')
    page_content_list = PageContent.objects.all()
    contents = Context({'page_content_list': page_content_list,})
    return HttpResponse(html_template.render(contents))

def details(request):
    html_template = loader.get_template('/home/mis/DjangoProject/pacer-training/site/my_app/Templates/details.html')
    case_details_list = CaseDetails.objects.all()
    contents = Context({'case_details_list': case_details_list,})
    return HttpResponse(html_template.render(contents))

def additional_info(request):
    html_template = loader.get_template('/home/mis/DjangoProject/pacer-training/site/my_app/Templates/additional_info.html')
    additional_info_list = AdditionalInfo.objects.all()
    contents = Context({'additional_info_list': additional_info_list,})
    return HttpResponse(html_template.render(contents))
