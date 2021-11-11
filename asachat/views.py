from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
# Create your views here.
import random
import json
from PIL import Image
from io import BytesIO
from valuation import models
from django.http import JsonResponse

from valuation.utils import get_image_from_data_url

def chat_room(request,id):
	template_name = "asachat/myapp1.html"
	valuation = get_object_or_404(models.ValuatedProperty, id=id)

	if request.method == 'POST':
		print()
		blob = request.POST['blob']
		img = f'myimg{random.randint(1000,9999)}.png'    
		image = get_image_from_data_url(request.POST.get('blob'))[0]
		
		# saving the image to model
		p = models.Anexa3.objects.create(ref_no=valuation, image=image)
		p.save()
		response = {"status":1}
		print("kireeee")
		return JsonResponse(response, safe=False)

	context = {
		"valuation": valuation,
	}
	return render(request,template_name, context)


