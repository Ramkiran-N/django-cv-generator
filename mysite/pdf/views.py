from django.shortcuts import render
from .models import Profile
import pdfkit
from django.http import HttpResponse
from django.template import loader
import os
path_wkhtmltopdf = r'C:\Program Files (x86)\wkhtmltopdf\bin\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
# Create your views here.
def index(request):
    if request.method == 'POST':
        name = request.POST.get('name','')
        email = request.POST.get('email','')
        phone = request.POST.get('phone','')
        summary = request.POST.get('summary','')
        degree = request.POST.get('degree','')
        university = request.POST.get('university','')
        skills = request.POST.get('skills','')
        data = Profile(name=name,email=email,phone=phone,summary=summary,degree=degree,university=university,skills=skills)
        data.save()
    return render(request,'pdf/accept.html')

def resume(request,id):
    resume = Profile.objects.get(id=id)
    template = loader.get_template('pdf/resume.html')
    html = template.render({'resume':resume})
    options = {
        'page-size':'Letter',
        'encoding':'UTF-8'
    }
    pdf = pdfkit.from_string(html, False, options, configuration=config)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="resume.pdf"'
    return response

def listprofiles(request):
    profiles = Profile.objects.all()
    return render(request,'pdf/list.html',{'profiles':profiles})