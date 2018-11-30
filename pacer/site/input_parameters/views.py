from django.template import Context, loader
from django.http import HttpResponse
from input_parameters.models import AdditionalInfo, CaseDetails, PageContent, Extractor

def index(request):
    additional_info_list = AdditionalInfo.objects.all()
    case_details_list = CaseDetails.objects.all()
    page_content_list = PageContent.objects.all()
    extractor_data_list = Extractor.objects.all()
    html_template = loader.get_template('/home/mis/DjangoProject/pacer/site/input_parameters/Templates/index.html')
    contetnts = Context({'case_details_list': case_details_list,
                            'additional_info_list': additional_info_list,
                            'page_content_list': page_content_list,
                            'extractor_data_list': extractor_data_list,})
    return HttpResponse(html_template.render(contetnts))
