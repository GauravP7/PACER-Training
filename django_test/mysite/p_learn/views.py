from django.template import Context, loader
from django.http import HttpResponse
from p_learn.models import CaseDetails

def index(request):
    case_details_list = CaseDetails.objects.all()
    #search_criteria_object[0].to_field_date
    html_template = loader.get_template('/home/mis/DjangoProject/django_test/Templates/index.html')
    contetnts = Context({'case_details_list': case_details_list,})
    return HttpResponse("html_template.render(contetnts)")
