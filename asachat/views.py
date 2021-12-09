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
		print("Nai?")
		print(request.POST['blob'], "keee");
		if request.POST['blob']:
			blob = request.POST['blob']
			img = f'myimg{random.randint(1000,9999)}.png'
			image = get_image_from_data_url(request.POST.get('blob'))[0]
			
			# saving the image to model
			p = models.Anexa3.objects.create(ref_no=valuation, image=image)
			p.save()
			response = {"status":1}
			return JsonResponse(response, safe=False)
		else:
			print("keda?")

	urban_transport = models.Transport.objects.all()
	structure_type = models.StructureType.objects.all()
	foundation = models.FoundationType.objects.all()
	plan_type = models.FloorType.objects.all()
	inchideri = models.ClouserType.objects.all()
	# inhabited_building = models.InhabitedBuildingType.objects.all()
	compartimentari = models.SubcompartmentType.objects.all()
	roof_type = models.RoofType.objects.all()
	interior_carpentry = models.InteriorCarpentry.objects.all()
	exterior_carpentry = models.ExteriorCarpentry.objects.all()
	invelitoare_type = models.InvelitoareType.objects.all()
	heating_system = models.HeatingSystem.objects.all()
	utilities_imobil = models.Utility.objects.all()
	utilities_apartament = models.Utility.objects.all()

	additional_equipment = models.AdditionalEquipment.objects.all()

	context = {
		"urban_transport":urban_transport,
		"structure_type":structure_type,
		"foundation": foundation,
		"plan_type": plan_type,
		"inchideri": inchideri,
		# "inhabited_building": inhabited_building,
		"compartimentari": compartimentari,
		"roof_type": roof_type,
		"interior_carpentry": interior_carpentry, 
		"exterior_carpentry": exterior_carpentry,
		"invelitoare_type": invelitoare_type,
		"heating_system": heating_system,
		"utilities_imobil": utilities_imobil,
		"utilities_apartament": utilities_apartament,
		"additional_equipment": additional_equipment,

		"valuation": valuation,
	}

	return render(request,template_name, context)


