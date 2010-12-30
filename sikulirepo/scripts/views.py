# Create your views here.
from scripts.models import Script
from scripts.models import PatternImage
from scripts.models import import_skl

from django.http import HttpResponseRedirect, HttpResponse
from django.http import Http404
from django.core.urlresolvers import reverse

from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.template import RequestContext

def index(request):
   latest_script_list = Script.objects.all()
   return render_to_response('scripts/index.html', 
   		{'latest_script_list' : latest_script_list},
   		context_instance=RequestContext(request))

def showsource(request, script_id):
	script = get_object_or_404(Script, pk=script_id)
	return render_to_response('scripts/showsource.html', 
		{'script' : script},
		context_instance=RequestContext(request))
    

def detail(request, script_id):
#   try:
#      script = Script.objects.get(pk=script_id)
#   except Script.DoesNotExist:
#      raise Http404
 
	script = get_object_or_404(Script, pk=script_id)
	return render_to_response('scripts/detail.html', 
		{'script' : script,
			'patternimage_list' : script.patternimage_set.all()},
		context_instance=RequestContext(request))
      
      
      
def update(request, script_id):
   script = get_object_or_404(Script, pk=script_id)
   script.title = request.POST['title']
   script.save()
   # Always return an HttpResponseRedirect after successfully dealing
   # with POST data. This prevents data from being posted twice if a
   # user hits the Back button.
   return HttpResponseRedirect(reverse('scripts.views.detail', args=(script.id,)))


from django import forms
import datetime

class UploadFileForm(forms.Form):
	title = forms.CharField(max_length=50)
	file = forms.FileField()

def handle_uploaded_file(f):
	destination = open(f.name,'wb+')
	for chunk in f.chunks():
		destination.write(chunk)
	destination.close()

	import_skl(f.name)

def save_as_pattern_image(f):
	s = Script(title="test")
	s.pub_date = datetime.datetime.now()
	s.mod_date = datetime.datetime.now()
	s.save()
	p = PatternImage(file = f, script = s)
	p.save()

def upload_file(request):
	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid():
			print request.FILES['file']
			handle_uploaded_file(request.FILES['file'])
			#save_as_pattern_image(request.FILES['file'])
			return HttpResponseRedirect(reverse('scripts.views.index'))
	else:
		form = UploadFileForm()
	return render_to_response('scripts/upload.html', {'form' : form},
		context_instance=RequestContext(request))
 
