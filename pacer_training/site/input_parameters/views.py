from django.template import Context, loader
from django.http import HttpResponse
from input_parameters.models import AdditionalInfo, Courtcase, DownloadTracker, Extractor

def index(request):
    additional_info_list = AdditionalInfo.objects.all()
    courtcase_list = Courtcase.objects.all()
    download_tracker_list = DownloadTracker.objects.all()
    extractor_data_list = Extractor.objects.all()
    html_template = loader.get_template('/home/mis/DjangoProject/pacer/site/input_parameters/Templates/index.html')
    contetnts = Context({'case_details_list': courtcase_list,
                            'additional_info_list': additional_info_list,
                            'page_content_list': download_tracker_list,
                            'extractor_data_list': extractor_data_list,})
    return HttpResponse(html_template.render(contetnts))
