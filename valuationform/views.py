# import ast
# import datetime
# from django.http.response import HttpResponseBase
# import requests
# from django.contrib.auth.decorators import login_required
# from django.db.models import Sum
# from django.http import HttpResponse, JsonResponse
# from django.shortcuts import render, get_object_or_404, redirect
# from django.utils import timezone
# from requests.api import get

# from dashboard import models as db_model 
# from dashboard import forms as db_form


# # ========================================================
# # =================== inspection date ====================
# # ========================================================
# @login_required(login_url='/signin/')
# def add_valuation(request):
# 	template = 'valuationform/valuation_form.html'
# 	msg = None

# 	areas = db_model.Area.objects.all()

# 	if request.method == "POST":
# 		form = db_form.AddValuationForm(request.POST)
# 		if form.is_valid():
# 			valuation = form.save(commit=False)
# 			valuation.status='progress'
# 			valuation.locatie=request.POST.getlist('locatie[]')
# 			valuation.inspection_date=timezone.now()
# 			valuation.save()
# 			return redirect("dashboard:add_compartment", id=valuation.id)
# 		else:
# 			msg = form.errors
# 	else:
# 		form = db_form.AddValuationForm()

# 	context = {
# 		'form': form,
# 		'msg': msg,
# 		'areas': areas,
# 		'segment': 'inspection',
# 	}
	
# 	return render(request, template, context)



# # ========================================================
# # ===================== compartment ======================
# # ========================================================
# @login_required(login_url='/signin/')
# def add_compartment(request, id):
# 	template = 'valuationform/compartment.html'
# 	valuation = get_object_or_404(db_model.EvaluareForm, id=id)
# 	property_type = valuation.property_type
# 	msg = None
# 	referer_page = request.META.get('HTTP_REFERER')
# 	attrs = db_model.ResidentialAttr.objects.filter(property_type=property_type)

# 	if request.method == 'POST':
# 		for attr in attrs:
# 			response = db_model.ResidentialAttrValue.objects.create(ref_no=valuation, attr_id=attr, attr_value=request.POST.get('name_' + str(attr.id)))
# 			success = True if response else False 
# 		if success:
# 			if request.POST.get('pre_url') == 'details':
# 				return redirect('dashboard:details', id=valuation.id)
# 			else:
# 				return redirect('dashboard:add_customfield', id=valuation.id)
# 		else:
# 			msg = "Something went wrong"

# 	context = {
# 		'attrs': attrs,
# 		'msg': msg,
# 		'valuation_id': valuation.id,
# 		'pre_url': referer_page,
# 		'segment': 'compartment',
# 	}

# 	return render(request, template, context)


# @login_required(login_url='/signin/')
# def compartment_photos(request):
# 	if request.method == 'POST':
# 		valuation = get_object_or_404(db_model.EvaluareForm, id=request.POST.get('valuation_id'))
# 		attr = get_object_or_404(db_model.ResidentialAttr, id=request.POST.get('attr_id'))
# 		file = request.FILES['file']
# 		upload = db_model.ResidentialAttrFile.objects.create(ref_no=valuation, attr_id=attr, file_name=file)
# 		if upload:
# 			return JsonResponse({'success': 'true'})
# 		else: 
# 			return JsonResponse({'success': 'false'})
# 	return JsonResponse({'success': 'false'})



# # ========================================================
# # ==================== custom field ======================
# # ========================================================
# @login_required(login_url='/signin/')
# def add_customfield(request, id):
# 	template = 'valuationform/customfield.html'
# 	valuation = get_object_or_404(db_model.EvaluareForm, id=id)
# 	msg = None

# 	referer_page = request.META.get('HTTP_REFERER')
# 	context = {
# 		'referer_page': referer_page,
# 		'valuation_id': valuation.id,
# 		'segment': 'customattrs',
# 	}

# 	return render(request, template, context)


# @login_required(login_url="/signin/")
# def add_custom_field(request):
# 	if request.method == 'POST':
# 		valuation = get_object_or_404(db_model.EvaluareForm, id=request.POST.get('vid'))
# 		name = request.POST.get('name')
# 		value = request.POST.get('value')
# 		cf = db_model.CustomFieldValue.objects.create(ref_no=valuation, attr_name=name, attr_value=value)
# 		if cf:
# 			return JsonResponse({'success': 'true', 'cf_id': cf.id})
# 	return JsonResponse({'success': 'false'})


# @login_required(login_url='/signin/')
# def customfield_photos(request):
# 	if request.method == 'POST':
# 		valuation = get_object_or_404(db_model.EvaluareForm, id=request.POST.get('vid'))
# 		attr = get_object_or_404(db_model.CustomFieldValue, id=request.POST.get('attr_id'))
# 		file = request.FILES['file']
# 		upload = db_model.CustomFieldFile.objects.create(ref_no=valuation, attr_id=attr, file_name=file)
# 		if upload:
# 			return JsonResponse({'success': 'true'})
# 		else: 
# 			return JsonResponse({'success': 'false'})
# 	return JsonResponse({'success': 'false'})



# # ========================================================
# # ===================== cover photos =====================
# # ========================================================
# @login_required(login_url='/signin/')
# def add_cover_photos(request, id):	
# 	template = 'valuationform/cover_photos.html'
# 	valuation = get_object_or_404(db_model.EvaluareForm, id=id)

# 	context = {
# 		'valuation_id': valuation.id,
# 		'segment': 'cover',
# 	}

# 	return render(request, template, context)


# @login_required(login_url='/signin/')
# def save_cover_photos(request):
# 	if request.method == 'POST':
# 		valuation = get_object_or_404(db_model.EvaluareForm, id=request.POST.get('cover_vid'))
# 		image_order = request.POST.get('order')
# 		file = request.FILES['file']
# 		refer_to = request.POST.get('refer_to')
# 		save = db_model.Photo.objects.create(ref_no=valuation, refer_to=refer_to, image_order=image_order, image=file)
# 		if save:
# 			return JsonResponse({'success': 'true'})
# 		else: 
# 			return JsonResponse({'success': 'false'})
# 	return JsonResponse({'success': 'false'})



# # ========================================================
# # ==================== report summary ====================
# # ========================================================
# """@login_required(login_url='/signin/')
# def add_summary(request, id):
# 	template = 'valuationform/report_summary.html'
# 	valuation = get_object_or_404(db_model.EvaluareForm, id=id)
# 	valueattr = db_model.ResidentialAttrValue.objects.filter(ref_no=valuation, attr_value__gte=1).exclude(attr_value='none')
# 	pre_url = request.META.get("HTTP_REFERER")
# 	warning = None
# 	if len(valueattr) < 1:
# 		warning = True

# 	# get forex exchange rate of yesterday 
# 	yesterday = datetime.datetime.now() - datetime.timedelta(1)
# 	yesterday = datetime.datetime.strftime(yesterday, "%Y-%m-%d")
# 	url = 'https://api.exchangerate.host/convert?from=EUR&to=RON&date=' + yesterday
# 	response = requests.get(url)
# 	data = response.json()
# 	fer = "{:.2f}".format(data['info']['rate'])

# 	# post method control
# 	if request.method == 'POST':
# 		if request.POST.get('approach') == 'market':
# 			summary = db_model.ValuationSummary.objects.create(ref_no=valuation, purpose=request.POST['purpose'],approach='market', amav=request.POST['amav'], fer=request.POST['fer'], fer_date=yesterday)
# 		elif request.POST.get('approach') == 'income': 
# 			summary = db_model.ValuationSummary.objects.create(ref_no=valuation, purpose=request.POST['purpose'],approach="income", aiav=request.POST['aiav'], fer=request.POST['fer'], fer_date=yesterday)

# 		for key,value in request.POST.items():
# 			if 'mav_' in key and value != "":
# 				db_model.ResidentialAttrValue.objects.filter(id=key.split('_')[1]).update(mav=value)
# 			elif 'iav_' in key and value != "":
# 				db_model.ResidentialAttrValue.objects.filter(id=key.split('_')[1]).update(iav=value)

# 		if request.POST.get("pre_url") == 'details':
# 			return redirect('dashboard:details', id=valuation.id)
# 		else:
# 			return redirect('dashboard:add_presentation_data', id=valuation.id)

# 	context = {
# 		'valuation_id': valuation.id,
# 		'warning': warning,
# 		'valueattr': valueattr,
# 		'fer': fer,
# 		'segment': 'summary',
# 		'pre_url': pre_url,
# 	}
# 	return render(request, template, context)"""


# def add_summary(request, id):
# 	template = 'valuationform/valuation_summary.html'
# 	valuation = get_object_or_404(db_model.EvaluareForm, id=id)
# 	valueattr = db_model.ResidentialAttrValue.objects.filter(ref_no=valuation, attr_value__gte=1).exclude(attr_value='none')
# 	pre_url = request.META.get("HTTP_REFERER")
# 	warning = None
# 	if len(valueattr) < 1:
# 		warning = True

# 	# get forex exchange rate of yesterday 
# 	yesterday = datetime.datetime.now() - datetime.timedelta(1)
# 	yesterday = datetime.datetime.strftime(yesterday, "%Y-%m-%d")
# 	url = 'https://api.exchangerate.host/convert?from=EUR&to=RON&date=' + yesterday
# 	response = requests.get(url)
# 	data = response.json()
# 	fer = "{:.2f}".format(data['info']['rate'])

# 	# post method control
# 	if request.method == 'POST':
# 		form = db_form.AddValuationSummary(request.POST)
# 	else:
# 		form = db_form.AddValuationSummary()

# 		# if request.POST.get("pre_url") == 'details':
# 		# 	return redirect('dashboard:details', id=valuation.id)
# 		# else:
# 		# 	return redirect('dashboard:add_presentation_data', id=valuation.id)

# 	context = {
# 		'valuation_id': valuation.id,
# 		'warning': warning,
# 		'valueattr': valueattr,
# 		'fer': fer,
# 		'yesterday': yesterday,
# 		'segment': 'summary',
# 		'pre_url': pre_url,
# 		'form': form,
# 	}
# 	return render(request, template, context)

# # ========================================================
# # ================== presentation date ===================
# # ========================================================
# @login_required(login_url='/signin/')
# def add_presentation_data(request, id):
# 	template = 'valuationform/presentation_data.html'
# 	valuation = get_object_or_404(db_model.EvaluareForm, id=id)
# 	msg = None
# 	pre_url = request.META.get("HTTP_REFERER")

# 	if request.method == 'POST':
# 		form = db_form.PresentationForm(request.POST)
# 		if form.is_valid():
# 			data = form.save(commit=False)
# 			data.ref_no = valuation
# 			data.pt = request.POST.getlist('pt[]')
# 			data.legal_doc = request.POST.getlist('legal_doc[]')
# 			data.save()
# 			if request.POST.get('pre_url') == 'details':
# 				return redirect('dashboard:details', id=valuation.id)
# 			else:
# 				return redirect('dashboard:add_construction', id=valuation.id)
# 		else:
# 			msg = 'Something went wrong.'
# 	else:
# 		form = db_form.PresentationForm()

# 	context = {
# 		'valuation_id': valuation.id,
# 		'form': form,
# 		'msg': msg,
# 		'segment': 'presentation',
# 		'pre_url': pre_url,
# 	}
# 	return render(request, template, context)



# # ========================================================
# # ===================== construction =====================
# # ========================================================
# @login_required(login_url='/signin/')
# def add_construction(request, id):
# 	template = 'valuationform/construction.html'
# 	valuation = get_object_or_404(db_model.EvaluareForm, id=id)
# 	rooms = db_model.ResidentialAttrValue.objects.exclude(attr_value='none').filter(ref_no=valuation, attr_value__gte=1)
# 	pre_url = request.META.get("HTTP_REFERER")
# 	# utila = ['Vestibul', 'Baie', 'Living', 'Bucatarie', 'Dormitor', 'Hol', 'Boxa']
# 	msg = None

# 	if request.method == 'POST':
# 		form = db_form.ConstructionForm(request.POST)
# 		if form.is_valid():
# 			data = form.save(commit=False)
# 			data.ref_no = valuation
# 			data.utilities = request.POST.getlist('utilities[]') if len(request.POST.getlist('utilities[]')) > 0 else None
# 			data.additional_equipment = request.POST.getlist('additional_equipment[]') if len(request.POST.getlist('additional_equipment[]')) > 0 else None
# 			data.save()

# 			# create floor 
# 			for r in rooms:
# 				r.floor_type = request.POST.get('floor_' + str(r.id))
# 				r.save()

# 			# crate Suprafete
# 			room_name = request.POST.getlist('room_name[]')
# 			areas = request.POST.getlist('area[]')
# 			utila = request.POST.getlist('utila[]')
# 			for r, a, u in zip(room_name, areas, utila):
# 				usable = True if u == '1' else False
# 				db_model.Suprafete.objects.create(ref_no=valuation, room_name=r, area=a, utila=usable)
# 			if request.POST.get('pre_url') == 'details':
# 				return redirect('dashboard:details', id=valuation.id)
# 			else:
# 				return redirect('dashboard:sub_comparable', id=valuation.id)
# 		else:
# 			msg = 'Something went wrong'
# 	else:
# 		form = db_form.ConstructionForm()

# 	context = {
# 		'valuation_id': valuation.id,
# 		'form': form,
# 		'msg': msg,
# 		'rooms': rooms,
# 		'pre_url': pre_url,
# 		'segment': 'construction',
# 	}
# 	return render(request, template, context)


# # ========================================================
# # ================ comparable property ===================
# # ========================================================
# @login_required(login_url='/signin/')
# def subject_comparable(request, id):
# 	template = 'valuationform/sub_comparable.html'
# 	valuation = get_object_or_404(db_model.EvaluareForm, id=id)
# 	try:
# 		const = db_model.Construction.objects.values('etaj', 'build_in', 'finish', 'heating').filter(ref_no__id=id)[0]
# 	except:
# 		const = None
# 	utila = db_model.Suprafete.objects.filter(ref_no__id=id, utila=True).aggregate(utila=Sum('area'))
# 	balcon = db_model.Suprafete.objects.filter(ref_no__id=id, utila=False).aggregate(balcon=Sum('area'))
# 	parking = db_model.ResidentialAttrValue.objects.filter(ref_no__id=id, attr_id__in=[7,8], attr_value__gte=1)
# 	msg = None

# 	if request.method == "POST":
# 		form = db_form.SubComparableForm(request.POST)
# 		if form.is_valid():
# 			data = form.save(commit=False)
# 			data.ref_no = valuation
# 			data.save()
# 			return redirect('dashboard:add_anexa', id=id)
# 		else:
# 			msg = "Something went wrong."
# 	else:
# 		form = db_form.SubComparableForm()
	
# 	context = {
# 		'valuation': valuation,
# 		'valuation_id': valuation.id,
# 		'const': const,
# 		'utila': utila,
# 		'balcon': balcon,
# 		'parking': parking,
# 		'msg': msg,
# 		'form': form,
# 		'segment': 'comparable',
# 	}
# 	return render(request, template, context)
	

# # ========================================================
# # ========================= anexa ========================
# # ========================================================
# @login_required(login_url='/signin/')
# def add_anexa(request, id):
# 	template = 'valuationform/anexa.html'
# 	valuation = get_object_or_404(db_model.EvaluareForm, id=id)
# 	pre_url = request.META.get('HTTP_REFERER')
# 	msg = None 
	
# 	context = {
# 		'valuation_id': valuation.id,
# 		'msg': msg,
# 		'segment': 'anexa',
# 		'pre_url': pre_url,
# 	}
# 	return render(request, template, context)


# @login_required(login_url='/signin/')
# def save_anexa(request):
# 	if request.method == 'POST':
# 		valuation = get_object_or_404(db_model.EvaluareForm, id=request.POST.get('vid'))
# 		refer_to = request.POST.get('refer_to')
# 		file = request.FILES['file']
# 		save = db_model.Anexa.objects.create(ref_no=valuation, refer_to=refer_to, file_name=file)
# 		if save:
# 			return JsonResponse({'success': 'true'})
# 		else: 
# 			return JsonResponse({'success': 'false'})
# 	return JsonResponse({'success': 'false'})


# # ========================================================
# # =================== edit inspection ====================
# # ========================================================
# @login_required(login_url='/signin/')
# def edit_valuation(request, id):
# 	template = 'valuationform/edit_inspection.html'
# 	valuation = get_object_or_404(db_model.EvaluareForm, id=id)
# 	camere = db_model.ResidentialAttrValue.objects.filter(ref_no=valuation,attr_id__pk=2).aggregate(camere=Sum('attr_value'))
# 	areas = db_model.Area.objects.all()
# 	msg = None

# 	if request.method == 'POST':
# 		form = db_form.EditValuationForm(request.POST, instance=valuation)
# 		if form.is_valid():
# 			instance = form.save(commit=False)
# 			instance.locatie = request.POST.getlist('locatie[]')
# 			instance.save()
# 			return redirect('dashboard:details', id=id)
# 		else:
# 			msg = 'Something went wrong'
# 	else:
# 		form = db_form.EditValuationForm(instance=valuation)

# 	context = {
# 		'valuation': valuation,
# 		'form': form,
# 		'msg': msg,
# 		'areas': areas,
# 		'camere': camere,
# 	}
# 	return render(request, template, context)


# # ========================================================
# # =================== edit inspection ====================
# # ========================================================
# @login_required(login_url='/signin/')
# def edit_summary(request, id):
# 	template = 'valuationform/report_summary.html'
# 	msg = None
# 	valuation = get_object_or_404(db_model.EvaluareForm, id=id)
# 	summary = db_model.ValuationSummary.objects.filter(ref_no=valuation)[0]
# 	valueattr = db_model.ResidentialAttrValue.objects.filter(ref_no=valuation, attr_value__gte=1).exclude(attr_value='none')
# 	warning = None
# 	if len(valueattr) < 1:
# 		warning = True

# 	# get forex exchange rate of yesterday 
# 	yesterday = datetime.datetime.now() - datetime.timedelta(1)
# 	yesterday = datetime.datetime.strftime(yesterday, "%Y-%m-%d")
# 	url = 'https://api.exchangerate.host/convert?from=EUR&to=RON&date=' + yesterday
# 	response = requests.get(url)
# 	data = response.json()
# 	fer = "{:.2f}".format(data['info']['rate'])

# 	# post method control
# 	if request.method == 'POST':
# 		summary.approach = request.POST['approach'] 
# 		summary.purpose = request.POST['purpose']
# 		summary.fer = request.POST['fer']
# 		summary.fer_date = yesterday
# 		summary.amav = request.POST['amav'] if request.POST.get('approach') == 'market' else 0.00 
# 		summary.aiav = request.POST['aiav'] if request.POST.get('approach') == 'income' else 0.00
# 		summary.save()

# 		for key,value in request.POST.items():
# 			if 'mav_' in key and value != '0.00':
# 				db_model.ResidentialAttrValue.objects.filter(id=key.split('_')[1]).update(mav=value, iav=0.00)
# 			elif 'iav_' in key and value != '0.00':
# 				db_model.ResidentialAttrValue.objects.filter(id=key.split('_')[1]).update(mav=0.00, iav=value)
# 		return redirect('dashboard:details', id=valuation.id)

# 	context = {
# 		'valuation_id': valuation.id,
# 		'msg': msg,
# 		'warning': warning,
# 		'summary': summary,
# 		'valueattr': valueattr,
# 		'fer': fer,
# 	}
# 	return render(request, template, context)



# # =========================================================================
# # ======================== edit compartimentare ===========================
# # =========================================================================
# @login_required(login_url='/signin/')
# def edit_compartment(request, id):
# 	template = 'valuationform/edit_compartment.html'
# 	msg = None
# 	valuation = get_object_or_404(db_model.EvaluareForm, id=id)
# 	attrs = db_model.ResidentialAttrValue.objects.filter(ref_no=valuation)

# 	if request.method == 'POST':
# 		for key,value in request.POST.items():
# 			if 'name_' in key:
# 				response = db_model.ResidentialAttrValue.objects.filter(id=key.split('_')[1]).update(attr_value=value)
# 				success = True if response else False 
# 		if success: 
# 			return redirect('dashboard:details', id=id)
# 		else:
# 			msg = "Something went wrong"

# 	context = {
# 		'attrs': attrs,
# 		'msg': msg,
# 		'valuation_id': valuation.id,
# 	}
# 	return render(request, template, context)


# # =========================================================================
# # ========================= edit custom field =============================
# # =========================================================================
# @login_required(login_url='/signin/')
# def edit_customattrs(request, id):
# 	template = 'valuationform/edit_customattrs.html'
# 	msg = None
# 	valuation = get_object_or_404(db_model.EvaluareForm, id=id)
# 	attrs = db_model.CustomFieldValue.objects.filter(ref_no=valuation)

# 	if request.method == 'POST':
# 		for key,value in request.POST.items():
# 			if 'name_' in key:
# 				response = db_model.CustomFieldValue.objects.filter(id=key.split('_')[1]).update(attr_value=value)
# 				success = True if response else False 
# 		if success: 
# 			return redirect('dashboard:details', id=id)
# 		else:
# 			msg = "Something went wrong"

# 	context = {
# 		'attrs': attrs,
# 		'msg': msg,
# 		'valuation_id': valuation.id,
# 	}
# 	return render(request, template, context)


# # =========================================================================
# # ========================= edit custom field =============================
# # =========================================================================
# @login_required(login_url='/signin/')
# def edit_presentation(request, id):
# 	template = 'valuationform/edit_presentation.html'
# 	valuation = get_object_or_404(db_model.EvaluareForm, id=id)
# 	camere = db_model.ResidentialAttrValue.objects.filter(ref_no=valuation, attr_id__pk=2).aggregate(camere=Sum('attr_value'))
# 	pdata = db_model.PresentationData.objects.filter(ref_no=valuation)[0]
# 	src_doc = db_model.SourceofInformation.objects.filter(ref_no=valuation)
# 	utila = db_model.Suprafete.objects.filter(ref_no=valuation, utila=True).aggregate(utila = Sum('area'))
# 	totala = db_model.Suprafete.objects.filter(ref_no=valuation).aggregate(totala=Sum('area'))
# 	msg = None

# 	if request.method == 'POST':
# 		form = db_form.PresentationForm(request.POST, instance=pdata)
# 		if form.is_valid():
# 			data = form.save(commit=False)
# 			data.pt = request.POST.getlist('pt[]')
# 			data.legal_doc = request.POST.getlist('legal_doc[]')
# 			data.sub_identi = request.POST.get('sub_identi')
# 			data.save()
# 			return redirect('dashboard:details', id=valuation.id)
# 		else:
# 			msg = 'Something went wrong.'
# 	else:
# 		form = db_form.PresentationForm(instance=pdata)

# 	context = {
# 		'apartment_no': valuation.apartment_no,
# 		'pdata': pdata,
# 		'form': form,
# 		'msg': msg,
# 		'src_doc': src_doc,
# 		'camere': camere,
# 		'utila': utila,
# 		'totala': totala,
# 	}
# 	return render(request, template, context)


# # =========================================================================
# # ========================= edit custom field =============================
# # =========================================================================
# @login_required(login_url='/signin/')
# def edit_construction(request, id):
# 	template = 'valuationform/edit_construction.html'
# 	valuation = get_object_or_404(db_model.EvaluareForm, id=id)
# 	rooms = db_model.ResidentialAttrValue.objects.exclude(attr_value='none').filter(ref_no=valuation, attr_value__gte=1)
# 	const = db_model.Construction.objects.filter(ref_no=valuation)[0]
# 	suprafete = db_model.Suprafete.objects.filter(ref_no=valuation)
# 	# utila = ['Vestibul', 'Baie', 'Living', 'Bucatarie', 'Dormitor', 'Hol', 'Boxa']
# 	msg = None

# 	if request.method == 'POST':
# 		form = db_form.ConstructionForm(request.POST, instance=const)
# 		if form.is_valid():
# 			data = form.save(commit=False)
# 			data.utilities = request.POST.getlist('utilities[]') if len(request.POST.getlist('utilities[]')) > 0 else None
# 			data.additional_equipment = request.POST.getlist('additional_equipment[]') if len(request.POST.getlist('additional_equipment[]')) > 0 else None
# 			data.save()

# 			# create floor 
# 			for r in rooms:
# 				r.floor_type = request.POST.get('floor_'+str(r.id))
# 				r.save()

# 			# crate Suprafete
# 			room_name = request.POST.getlist('room_name[]')
# 			areas = request.POST.getlist('area[]')
# 			utilas = request.POST.getlist('utila[]')
# 			for r, a, u in zip(room_name, areas, utilas):
# 				usable = True if u == '1' else False
# 				if request.POST.get('update') == '1':
# 					db_model.Suprafete.objects.filter(ref_no=valuation, room_name=r).update(area=a, utila=usable)
# 				else:
# 					db_model.Suprafete.objects.create(ref_no=valuation, room_name=r, area=a, utila=usable)
# 			return redirect('dashboard:details', id=valuation.id)
# 		else:
# 			msg = 'Something went wrong.'
# 	else:
# 		form = db_form.ConstructionForm(instance=const)

# 	context = {
# 		'const': const,
# 		'suprafete': suprafete,
# 		'rooms': rooms,
# 		'form': form,
# 		'msg': msg,
# 	}
# 	return render(request, template, context)


# @login_required(login_url='/signin/')
# def add_source_doc(request):
# 	if request.method == 'POST':
# 		vid = request.POST.get('vid')
# 		valuation = get_object_or_404(db_model.EvaluareForm, id=vid)
# 		source = request.POST.get('source')
# 		response = db_model.SourceofInformation.objects.create(ref_no=valuation, source=source)
# 		if response:
# 			return JsonResponse({'success': 'true', 'id': response.id})
# 		else:
# 			return JsonResponse({'success': 'false'})
# 	else:
# 		return JsonResponse({'success': 'false'})


# # =========================================================================
# # ===================== manage comparable properties ======================
# # =========================================================================
# @login_required(login_url='/signin/')
# def add_comparable(request):
# 	template = 'valuationform/add_comparable.html'
# 	msg = None

# 	if request.method == 'POST':
# 		form = db_form.ComparableForm(request.POST)
# 		if form.is_valid():
# 			form.save()
# 			request.session['comp_added'] = True
# 			return redirect('dashboard:comparable_list')
# 		else:
# 			msg = "Something went wrong."
# 	else:
# 		form = db_form.ComparableForm()

# 	context = {
# 		'segment': 'comparable',
# 		'form': form,
# 	}
# 	return render(request, template, context)


# @login_required(login_url='/signin/')
# def comparable_details(request, id):
# 	if request.session.get('comp_edit'):
# 		msg = 'updated'
# 		try:
# 			del request.session['updated']
# 		except KeyError:
# 			pass 
# 	else:
# 		msg = None

# 	template = 'valuationform/comparable_details.html'
# 	comparable = get_object_or_404(db_model.ComparableProperty, id=id)
# 	context = {
# 		'comparable': comparable,
# 		'segment': 'comparable',
# 		'msg': msg,
# 	}
# 	return render(request, template, context)
	

# @login_required(login_url='/signin/')
# def delete_comparable(request):
# 	cid = request.GET.get('id')
# 	instance = get_object_or_404(db_model.ComparableProperty, id=cid)
# 	try:
# 		response = instance.delete()
# 		if response:
# 			return JsonResponse({'success': 'true'})
# 	except:
# 		return JsonResponse({'success': 'false'})


# @login_required(login_url='/signin/')
# def edit_comparable(request, id):
# 	template = 'valuationform/add_comparable.html'
# 	msg = None
# 	instance = get_object_or_404(db_model.ComparableProperty, id=id)

# 	if request.method == 'POST':
# 		form = db_form.ComparableEditForm(request.POST, instance=instance)
# 		if form.is_valid():
# 			form.save()
# 			request.session['comp_edit'] = True
# 			return redirect('dashboard:comparable_details', id=id)
# 		else:
# 			msg = "Something went wrong."
# 	else:
# 		form = db_form.ComparableEditForm(instance=instance)

# 	context = {
# 		'instance': instance,
# 		'segment': 'comparable',
# 		'form': form,
# 		'msg': msg,
# 	}
# 	return render(request, template, context)


# # ========================================================
# # ================ add comparable table ==================
# # ======================================================== 
# @login_required(login_url='/signin/')
# def add_comptable(request, id):
# 	valuation = get_object_or_404(db_model.EvaluareForm, id=id)
# 	if request.method == "POST":
# 		properties = request.POST.getlist('properties[]')
# 		success = False
# 		letters = ['A', 'B', 'C', 'D', 'E']
# 		i = 0
# 		for p in properties:
# 			prop = get_object_or_404(db_model.ComparableProperty, id=p)
# 			response = db_model.ComparableTable.objects.create(ref_no=valuation, comparable=prop, name=letters[i])
# 			success = True if response else False	
# 			i += 1	
# 		if success:
# 			return redirect('dashboard:comparable_table', id=id)
# 	return redirect('dashboard:details', id=id)


# def comparable_table(request, id):
# 	template = 'valuationform/comparable_table.html'
# 	msg = None
# 	ct = db_model.ComparableTable.objects.filter(ref_no__pk=id)
# 	if request.method == "POST":
# 		i = 0
# 		for c in ct:
# 			c.mobila_ajustare = request.POST.getlist('mobila_ajustare[]')[i]
# 			c.pb_ajustare = request.POST.getlist('pb_ajustare[]')[i]
# 			c.margin = request.POST.getlist('margin[]')[i]
# 			c.property_percent = request.POST.getlist('property_percent[]')[i] if request.POST.getlist('property_percent[]')[i] != '' else None
# 			c.property_euro = request.POST.getlist('property_euro[]')[i] if request.POST.getlist('property_euro[]')[i] != '' else None
# 			c.fc_percent = request.POST.getlist('fc_percent[]')[i] if request.POST.getlist('fc_percent[]')[i] != '' else None
# 			c.fc_euro = request.POST.getlist('fc_euro[]')[i] if request.POST.getlist('fc_euro[]')[i] != '' else None
# 			c.sc_percent = request.POST.getlist('sc_percent[]')[i] if request.POST.getlist('sc_percent[]')[i] != '' else None
# 			c.sc_euro = request.POST.getlist('sc_euro[]')[i] if request.POST.getlist('sc_euro[]')[i] != '' else None
# 			c.ape_percent = request.POST.getlist('ape_percent[]')[i] if request.POST.getlist('ape_percent[]')[i] != '' else None
# 			c.ape_euro = request.POST.getlist('ape_euro[]')[i] if request.POST.getlist('ape_euro[]')[i] != '' else None
# 			c.me_percent = request.POST.getlist('me_percent[]')[i] if request.POST.getlist('me_percent[]')[i] != '' else None
# 			c.me_euro = request.POST.getlist('me_euro[]')[i] if request.POST.getlist('me_euro[]')[i] != '' else None
# 			c.lc_percent = request.POST.getlist('lc_percent[]')[i] if request.POST.getlist('lc_percent[]')[i] != '' else None
# 			c.lc_euro = request.POST.getlist('lc_euro[]')[i] if request.POST.getlist('lc_euro[]')[i] != '' else None
# 			c.cp_percent = request.POST.getlist('cp_percent[]')[i] if request.POST.getlist('cp_percent[]')[i] != '' else None
# 			c.cp_euro = request.POST.getlist('cp_euro[]')[i] if request.POST.getlist('cp_euro[]')[i] != '' else None
# 			c.cy_percent = request.POST.getlist('cy_percent[]')[i] if request.POST.getlist('cy_percent[]')[i] != '' else None
# 			c.cy_euro = request.POST.getlist('cy_euro[]')[i] if request.POST.getlist('cy_euro[]')[i] != '' else None
# 			c.finish_percent = request.POST.getlist('finish_percent[]')[i] if request.POST.getlist('finish_percent[]')[i] != '' else None
# 			c.finish_euro = request.POST.getlist('finish_euro[]')[i] if request.POST.getlist('finish_euro[]')[i] != '' else None
# 			c.etaj_percent = request.POST.getlist('etaj_percent[]')[i] if request.POST.getlist('etaj_percent[]')[i] != '' else None
# 			c.etaj_euro = request.POST.getlist('etaj_euro[]')[i] if request.POST.getlist('etaj_euro[]')[i] != '' else None
# 			c.hs_percent = request.POST.getlist('hs_percent[]')[i] if request.POST.getlist('hs_percent[]')[i] != '' else None
# 			c.hs_euro = request.POST.getlist('hs_euro[]')[i] if request.POST.getlist('hs_euro[]')[i] != '' else None
# 			c.parking_percent = request.POST.getlist('parking_percent[]')[i] if request.POST.getlist('parking_percent[]')[i] != '' else None
# 			c.parking_euro = request.POST.getlist('parking_euro[]')[i] if request.POST.getlist('parking_euro[]')[i] != '' else None
# 			c.save()
# 			i += 1
# 		response = db_model.ComparableProperty.objects.filter(ref_no__id=id).update(motivation = request.POST.get('motivation'), property_motivation = request.POST.get('property_motivation'), fc_motivation = request.POST.get('fc_motivation'), sc_motivation = request.POST.get('sc_motivation'), ape_motivation = request.POST.get('ape_motivation'), me_motivation = request.POST.get('me_motivation'), lc_motivation = request.POST.get('lc_motivation'), cp_motivation = request.POST.get('cp_motivation'), cy_motivation = request.POST.get('cy_motivation'), su_motivation = request.POST.get('su_motivation'), finish_motivation = request.POST.get('finish_motivation'),etaj_motivation = request.POST.get('etaj_motivation'), balcon_motivation = request.POST.get('balcon_motivation'), hs_motivation = request.POST.get('hs_motivation'), parking_motivation = request.POST.get('parking_motivation'))
# 		if response:
# 			return redirect('dashboard:details', id=id)
# 		else:
# 			msg = "Something went wrong."
	
# 	context = {
# 		'msg': msg,
# 		'ct': ct,
# 	}
# 	return render(request, template, context)


			