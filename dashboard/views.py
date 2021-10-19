import ast
import json
import datetime
from json.decoder import JSONDecodeError
import requests
from decimal import Decimal
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.mail import send_mail
from django.db import connection
from django.db.models import Sum
from django.http import HttpResponse, JsonResponse, response
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.template.loader import get_template, render_to_string
from django.utils import timezone
from django.views import View
from xhtml2pdf import pisa

from dashboard.forms import * 
from dashboard.models import *
User = get_user_model()



# =========================================================================
# ========================== Dashboard page ===============================
# =========================================================================
@login_required(login_url="/signin/")
def dashboardView(request):
	template_name = 'dashboard/evaluari_complete.html'
	complete = EvaluareForm.objects.filter(status='completed').order_by('-id')
	context = {
		'segment': 'complete',
		'complete': complete,
	}
	return render(request, template_name, context)
	


# =========================================================================
# ========================== Add Valuation old ============================
# =========================================================================
@login_required(login_url="/signin/")
def add_valutation_old(request):
	template_name = 'dashboard/add_valuation.html'
	attrs = ResidentialAttr.objects.all()
	attrs = serializers.serialize('json', attrs)
	context = {'attrs': attrs,}
	return render(request, template_name, context)



# =========================================================================
# ======================== save basic form data ===========================
# =========================================================================
@login_required(login_url="/signin/")
def steponesave(request):
	if request.method == 'POST':
		address = request.POST.get('address')
		owner = request.POST.get('owner')
		property_type = request.POST.get('type')
		lat = request.POST.get('lat')
		lng = request.POST.get('lng')
		nume_client = request.POST.get('nume_client')
		report_recipient = request.POST.get('report_recipient')
		valuation = EvaluareForm.objects.create(valuatate_by=request.user, address=address, latitude=lat, longitude=lng, property_type=property_type, owner=owner, nume_client=nume_client, report_recipient=report_recipient, status='progress', inspection_date=timezone.now())
		if valuation:
			return JsonResponse({'success': 'true', 'id': valuation.id})
		else:
			return JsonResponse({'success': 'false'})
	return JsonResponse({'success': 'false'})



# =========================================================================
# ======================== save attributes photo ==========================
# =========================================================================
@login_required(login_url="/signin/")
def save_photos(request):
	if request.method == 'POST':
		valuation = get_object_or_404(EvaluareForm, id=request.POST.get('valuation_id'))
		attr = get_object_or_404(ResidentialAttr, id=request.POST.get('attr_id'))
		file = request.FILES['file']
		upload = ResidentialAttrFile.objects.create(ref_no=valuation, attr_id=attr, file_name=file)
		if upload:
			return JsonResponse({'success': 'true'})
		else: 
			return JsonResponse({'success': 'false'})
	return JsonResponse({'success': 'false'})



# =========================================================================
# ======================== save attributes data ===========================
# =========================================================================
@login_required(login_url="/signin/")
def steptwosave(request):
	if request.method == 'POST':
		valuation = get_object_or_404(EvaluareForm, id=request.POST.get('valuation_id'))
		attrs = ResidentialAttr.objects.filter(property_type=valuation.property_type)
		for attr in attrs:
			response = ResidentialAttrValue.objects.create(ref_no=valuation, attr_id=attr, attr_value=request.POST.get('name_' + str(attr.id)))
			success = True if response else False 
		if success:
			return JsonResponse({'success': 'true'})
		else: 
			return JsonResponse({'success': 'false'})
	return JsonResponse({'success': 'false'})



# =========================================================================
# ========================== add custom field =============================
# =========================================================================
@login_required(login_url="/signin/")
def add_custom_field(request):
	if request.method == 'POST':
		valuation = get_object_or_404(EvaluareForm, id=request.POST.get('vid'))
		name = request.POST.get('name')
		value = request.POST.get('value')
		cf = CustomFieldValue.objects.create(ref_no=valuation, attr_name=name, attr_value=value)
		if cf:
			return JsonResponse({'success': 'true', 'cf_id': cf.id})
	return JsonResponse({'success': 'false'})



# =========================================================================
# ======================== add custom fild image ==========================
# =========================================================================
@login_required(login_url="/signin/")
def save_cf_photos(request):
	if request.method == 'POST':
		valuation = get_object_or_404(EvaluareForm, id=request.POST.get('vid'))
		attr = get_object_or_404(CustomFieldValue, id=request.POST.get('attr_id'))
		file = request.FILES['file']
		upload = CustomFieldFile.objects.create(ref_no=valuation, attr_id=attr, file_name=file)
		if upload:
			return JsonResponse({'success': 'true'})
		else: 
			return JsonResponse({'success': 'false'})
	return JsonResponse({'success': 'false'})



# =========================================================================
# ===================== save cover and summary photo ======================
# =========================================================================
@login_required(login_url='/signin/')
def save_cover_photos(request):
	if request.method == 'POST':
		valuation = get_object_or_404(EvaluareForm, id=request.POST.get('cover_vid'))
		image_order = request.POST.get('order')
		file = request.FILES['file']
		refer_to = request.POST.get('refer_to')
		save = Photo.objects.create(ref_no=valuation, refer_to=refer_to, image_order=image_order, image=file)
		if save:
			return JsonResponse({'success': 'true'})
		else: 
			return JsonResponse({'success': 'false'})
	return JsonResponse({'success': 'false'})



# =========================================================================
# ========================== add valuation new ============================
# =========================================================================
@login_required(login_url="/signin/")
def add_valuation(request):
	if request.GET.get('id'):
		valuation = get_object_or_404(EvaluareForm, id=request.GET.get('id'))
		property_type = valuation.property_type
	msg = None

	if request.GET.get('next') == None:
		template = 'dashboard/valuation_form.html'
		areas = Area.objects.all()
		cities = City.objects.all()

		if request.method == "POST":
			formOne = AddValuationForm(request.POST)
			if formOne.is_valid():
				vobj = formOne.save(commit=False)
				vobj.status='progress'
				vobj.inspection_date=timezone.now()
				vobj.save()
				return redirect("http://localhost:8000/add-valuation/?next=attrs&id="+str(vobj.id))
			else:
				msg = "Something went wrong"
		else:
			formOne = AddValuationForm()

		context = {
			'formone': formOne,
			'msg': msg,
			'areas': areas,
			'cities': cities,
		}
	
	elif request.GET.get('next') == 'attrs':
		template = 'dashboard/valuation_attrs.html'
		attr_pre_url = request.META.get('HTTP_REFERER')
		attrs = ResidentialAttr.objects.filter(property_type=property_type)

		if request.method == 'POST':
			for attr in attrs:
				response = ResidentialAttrValue.objects.create(ref_no=valuation, attr_id=attr, attr_value=request.POST.get('name_' + str(attr.id)))
				success = True if response else False 
			if success:
				if 'details' in attr_pre_url:
					return redirect('dashboard:details', id=valuation.id)
				else:
					return redirect('http://localhost:8000/add-valuation/?next=customattrs&id='+str(valuation.id))
			else:
				msg = "Something went wrong"

		context = {
			'attrs': attrs,
			'msg': msg,
			'valuation_id': valuation.id,
			'attr_pre_url': attr_pre_url,
		}

	elif request.GET.get('next') == 'customattrs':
		template = 'dashboard/valuation_customattr.html'
		custom_url = request.META.get('HTTP_REFERER')
		context = {
			'custom_url': custom_url,
			'valuation_id': valuation.id,
		}

	elif request.GET.get('next') == 'cover':
		template = 'dashboard/valuation_cover.html'
		context = {
			'valuation_id': valuation.id,
		}

	elif request.GET.get('next') == 'summary':
		template = 'dashboard/valuation_summary.html'
		valueattr = ResidentialAttrValue.objects.filter(ref_no=valuation, attr_value__gte=1).exclude(attr_value='none')
		warning = None
		if len(valueattr) < 1:
			warning = True

		# get forex exchange rate of yesterday 
		yesterday = datetime.datetime.now() - datetime.timedelta(1)
		yesterday = datetime.datetime.strftime(yesterday, "%Y-%m-%d")
		url = 'https://api.exchangerate.host/convert?from=EUR&to=RON&date=' + yesterday
		response = requests.get(url)
		data = response.json()
		fer = "{:.2f}".format(data['info']['rate'])

		# post method control
		if request.method == 'POST':
			yesterday = datetime.datetime.today() - datetime.timedelta(days=1)
			if request.POST.get('approach') == 'market':
				summary = ValuationSummary.objects.create(ref_no=valuation, purpose=request.POST['purpose'],approach='market', amav=request.POST['amav'], fer=request.POST['fer'], fer_date=yesterday)
			elif request.POST.get('approach') == 'income': 
				summary = ValuationSummary.objects.create(ref_no=valuation, purpose=request.POST['purpose'],approach="income", aiav=request.POST['aiav'], fer=request.POST['fer'], fer_date=yesterday)

			for key,value in request.POST.items():
				if 'mav_' in key and value != "":
					ResidentialAttrValue.objects.filter(id=key.split('_')[1]).update(mav=value)
				elif 'iav_' in key and value != "":
					ResidentialAttrValue.objects.filter(id=key.split('_')[1]).update(iav=value)

			return redirect('dashboard:details', id=valuation.id)
		context = {
			'valuation_id': valuation.id,
			'msg': msg,
			'warning': warning,
			'valueattr': valueattr,
			'fer': fer,
		}

	return render(request, template, context)



# =========================================================================
# ======================== Incomplete valuations ==========================
# =========================================================================
@login_required(login_url='/signin/')
def evaluari_incomplete(request):
	if request.session.get('status'): 
		msg = 'status'
		try:
			del request.session['status']
		except KeyError:
			pass 
	elif request.session.get('not_change'):
		msg = 'not_status'
		try:
			del request.session['not_change']
		except KeyError:
			pass 
	else:
		msg = None

	incomplete = EvaluareForm.objects.exclude(status='completed').order_by('-id')
	status = {'progress': 'In progress', 'completed': 'Completed', 'suspended': 'Suspended', 'cancelled': 'Cancelled'}
	context = {
		'segment': 'incomplet',
		'msg': msg,
		'incomplete': incomplete,
		'status': status,
	}
	return render(request, 'dashboard/evaluari_incomplete.html', context)



# =========================================================================
# ========================== Incomplete map ===============================
# =========================================================================
@login_required(login_url='/signin/')
def evaluari_incomplete_map(request):
	data = EvaluareForm.objects.exclude(status='completed')
	data = serializers.serialize("json", data)
	context = {
		'segment': 'incomplet',
		'addressPoints': data, 
	}
	return render(request, 'dashboard/evaluari_incomplete_map.html', context)



# =========================================================================
# ============================ update status =====-========================
# =========================================================================
@login_required(login_url='/signin/')
def change_status(request, status, id):
	previous_url = request.META.get('HTTP_REFERER')

	instance = get_object_or_404(EvaluareForm, id=id)
	instance.status = status
	try: 
		if status == 'completed':
			instance.report_date = timezone.now()
		instance.save()
		response = True
	except:
		response = False
	if response:
		if instance.status == 'completed':
			request.session['completed'] = True
			if 'details' in previous_url:
				vid = previous_url.rsplit('/', 2)[-2]
				return redirect('dashboard:details', id=vid)
			else:
				return redirect('dashboard:complete')
		else:
			request.session['status'] = True
			if 'details' in previous_url:
				vid = previous_url.rsplit('/', 2)[-2]
				return redirect('dashboard:details', id=vid)
			else:
				return redirect('dashboard:incomplete')
	else:
		request.session['not_change'] = True
		if 'details' in previous_url:
			vid = previous_url.rsplit('/', 2)[-2]
			return redirect('dashboard:details', id=vid)
		else:
			return redirect('dashboard:incomplete')


# =========================================================================
# ========================== Complete evaluare ============================
# =========================================================================
@login_required(login_url='/signin/')
def evaluari_complete(request):
	if request.session.get('completed'):
		msg = 'marked'
		try:
			del request.session['completed']
		except KeyError:
			pass
	else:
		msg = None

	complete = EvaluareForm.objects.filter(status='completed').order_by('-id')
	context = {
		'segment': 'complete',
		'msg': msg,
		'complete': complete,
	}
	return render(request, 'dashboard/evaluari_complete.html', context)



# =========================================================================
# ======================== complete evaluare map ==========================
# =========================================================================
@login_required(login_url='/signin/')
def evaluari_complete_map(request):
	data = EvaluareForm.objects.filter(status='completed')
	data = serializers.serialize("json", data)
	context = {
		'segment': 'complete',
		'addressPoints': data, 
	}
	return render(request, 'dashboard/evaluari_complete_map.html', context)



# =========================================================================
# ========================== delete valuation =============================
# =========================================================================
@login_required(login_url='/signin/')
def valuation_form_delete(request):
	vid = request.GET.get('id')
	instance = get_object_or_404(EvaluareForm, id=vid)
	try:
		response = instance.delete()
		if response:
			return JsonResponse({'success': 'true'})
	except:
		return JsonResponse({'success': 'false'})



# =========================================================================
# ========================== evaluare details =============================
# =========================================================================
@login_required(login_url='/signin/')
def evaluare_details(request, id):
	if request.session.get('status'): 
		msg = 'status'
		try:
			del request.session['status']
		except KeyError:
			pass 
	elif request.session.get('completed'):
		msg = 'marked'
		try:
			del request.session['completed']
		except KeyError:
			pass
	elif request.session.get('not_change'):
		msg = 'not_status'
		try:
			del request.session['not_change']
		except KeyError:
			pass 
	else:
		msg = None

	valuation = get_object_or_404(EvaluareForm, id=id)
	camere = ResidentialAttrValue.objects.filter(ref_no=valuation, attr_id__pk=2).aggregate(camere=Sum('attr_value'))
	attrs = ResidentialAttr.objects.filter(property_type=valuation.property_type)
	vattrs = ResidentialAttrValue.objects.filter(ref_no=valuation) #valuation attrs
	custom_attrs = CustomFieldValue.objects.filter(ref_no=valuation)
	cover_photos = Photo.objects.filter(ref_no=valuation, refer_to="cover").order_by('image_order')
	inspectors = User.objects.filter(is_inspector=True).order_by('first_name')
	src_doc = SourceofInformation.objects.filter(ref_no=valuation)
	floors = ResidentialAttrValue.objects.filter(ref_no=valuation, floor_type='gresie')
	floors = [f.attr_id.name for f in floors]
	floor_data = ",".join(floors[:-1]) + " si " + floors[-1]
	try:
		pdata = PresentationData.objects.filter(ref_no=valuation)[0]
	except:
		pdata = None
	try:
		construction = Construction.objects.filter(ref_no=valuation)[0]
	except:
		construction = None	
	s_utila = Suprafete.objects.filter(ref_no=valuation, utila=True)
	s_neutila = Suprafete.objects.filter(ref_no=valuation, utila=False)
	utila = Suprafete.objects.filter(ref_no=valuation, utila=True).aggregate(utila = Sum('area'))
	totala = Suprafete.objects.filter(ref_no=valuation).aggregate(totala=Sum('area'))
	comparable_properties = ComparableProperty.objects.filter(is_comparable=True).exclude(ref_no=valuation)
	try:
		comparable_tbl = ComparableTable.objects.filter(ref_no=valuation)[0]
	except:
		comparable_tbl = None
	# Anexa

	# summary 
	try:
		summary = ValuationSummary.objects.filter(ref_no=valuation)[0]
		summary_photo = Photo.objects.filter(ref_no=valuation, refer_to="summary").order_by('image_order')
		mav = ResidentialAttrValue.objects.filter(ref_no=valuation).aggregate(Sum('mav'))
		iav = ResidentialAttrValue.objects.filter(ref_no=valuation).aggregate(Sum("iav"))
		mav_total = mav['mav__sum'] + summary.amav
		iav_total = iav['iav__sum'] + summary.aiav
		mav_ron = "{:.2f}".format(mav_total * summary.fer)
		iav_ron = "{:.2f}".format(iav_total * summary.fer)
	except:
		summary = summary_photo = mav = iav = mav_total = iav_total = mav_ron = iav_ron = None
	# summary 
	status = {'progress': 'In progress', 'completed': 'Completed', 'suspended': 'Suspended', 'cancelled': 'Cancelled'}

	context = {
		'valuation': valuation,
		'inspectors': inspectors,
		'attrs': attrs,
		'vattrs': vattrs,
		'custom': custom_attrs,
		'cover': cover_photos,
		'status': status,
		'summary': summary,
		'summary_photo': summary_photo,
		'mav_total': mav_total,
		'iav_total': iav_total,
		'mav_ron': mav_ron,
		'iav_ron': iav_ron,
		'pdata': pdata,
		'const': construction,
		's_utila': s_utila,
		's_neutila': s_neutila,
		'utila': utila,
		'totala': totala,
		'msg': msg,
		'camere': camere,
		'src_doc': src_doc,
		'floor_data': floor_data,
		'comparable_tbl': comparable_tbl,
		'cp': comparable_properties,
	}
	return render(request, 'dashboard/valuation_details.html', context)


# =========================================================================
# ==================== reorder cover & summary image ======================
# =========================================================================
@login_required(login_url='/signin/')
def reorder_cover_image(request):
	if request.method == 'POST':
		imageIds = request.POST.get('ids')
		ids = imageIds.split(',')
		i = 1
		for id in ids:
			cover = get_object_or_404(Photo, id=id)
			cover.image_order = i
			cover.save()
			i+=1
		return JsonResponse({'response': 'true'})
	return JsonResponse({'response': 'false'})


# =========================================================================
# ========================= Edit valuation page ===========================
# =========================================================================
@login_required(login_url='/signin/')
def edit_valuation(request, id):
	template = 'dashboard/edit_valuation.html'
	valuation = get_object_or_404(EvaluareForm, id=id)
	areas = Area.objects.all()
	msg = None

	if request.method == 'POST':
		form = EditValuationForm(request.POST, instance=valuation)
		if form.is_valid():
			form.save()
			return redirect('dashboard:details', id=id)
		else:
			msg = 'Something went wrong'
	else:
		form = EditValuationForm(instance=valuation)

	context = {
		'valuation': valuation,
		'form': form,
		'msg': msg,
		'areas': areas,
	}
	return render(request, template, context)


# =========================================================================
# ======================== edit valuation summary =========================
# =========================================================================
@login_required(login_url='/signin/')
def edit_summary(request, id):
	template = 'dashboard/valuation_summary.html'
	msg = None
	valuation = get_object_or_404(EvaluareForm, id=id)
	summary = ValuationSummary.objects.filter(ref_no=valuation)[0]
	valueattr = ResidentialAttrValue.objects.filter(ref_no=valuation, attr_value__gte=1).exclude(attr_value='none')
	warning = None
	if len(valueattr) < 1:
		warning = True

	# get forex exchange rate of yesterday 
	yesterday = datetime.datetime.now() - datetime.timedelta(1)
	yesterday = datetime.datetime.strftime(yesterday, "%Y-%m-%d")
	url = 'https://api.exchangerate.host/convert?from=EUR&to=RON&date=' + yesterday
	response = requests.get(url)
	data = response.json()
	fer = "{:.2f}".format(data['info']['rate'])

	# post method control
	if request.method == 'POST':
		yesterday = datetime.datetime.today() - datetime.timedelta(days=1)
		if request.POST.get('approach') == 'market':
			summary = ValuationSummary.objects.create(ref_no=valuation, purpose=request.POST['purpose'],approach='market', amav=request.POST['amav'], fer=request.POST['fer'], fer_date=yesterday)
		elif request.POST.get('approach') == 'income': 
			summary = ValuationSummary.objects.create(ref_no=valuation, purpose=request.POST['purpose'],approach="income", aiav=request.POST['aiav'], fer=request.POST['fer'], fer_date=yesterday)

		for key,value in request.POST.items():
			if 'mav_' in key and value != "":
				ResidentialAttrValue.objects.filter(id=key.split('_')[1]).update(mav=value)
			elif 'iav_' in key and value != "":
				ResidentialAttrValue.objects.filter(id=key.split('_')[1]).update(iav=value)

		return redirect('dashboard:details', id=valuation.id)

	context = {
		'valuation_id': valuation.id,
		'msg': msg,
		'warning': warning,
		'summary': summary,
		'valueattr': valueattr,
		'fer': fer,
	}
	return render(request, template, context)


# =========================================================================
# ====================== edit valuation attributes ========================
# =========================================================================
@login_required(login_url='/signin/')
def edit_attrs(request, id):
	template = 'dashboard/edit_attrs.html'
	msg = None
	valuation = get_object_or_404(EvaluareForm, id=id)
	attrs = ResidentialAttrValue.objects.filter(ref_no=valuation)

	if request.method == 'POST':
		for key,value in request.POST.items():
			if 'name_' in key:
				response = ResidentialAttrValue.objects.filter(id=key.split('_')[1]).update(attr_value=value)
				success = True if response else False 
		if success: 
			return redirect('dashboard:details', id=id)
		else:
			msg = "Something went wrong"

	context = {
		'attrs': attrs,
		'msg': msg,
		'valuation_id': valuation.id,
	}
	return render(request, template, context)


# =========================================================================
# ========================= edit custom field =============================
# =========================================================================
@login_required(login_url='/signin/')
def edit_customattrs(request, id):
	template = 'dashboard/edit_customattrs.html'
	msg = None
	valuation = get_object_or_404(EvaluareForm, id=id)
	attrs = CustomFieldValue.objects.filter(ref_no=valuation)

	if request.method == 'POST':
		for key,value in request.POST.items():
			if 'name_' in key:
				response = CustomFieldValue.objects.filter(id=key.split('_')[1]).update(attr_value=value)
				success = True if response else False 
		if success: 
			return redirect('dashboard:details', id=id)
		else:
			msg = "Something went wrong"

	context = {
		'attrs': attrs,
		'msg': msg,
		'valuation_id': valuation.id,
	}
	return render(request, template, context)


# =========================================================================
# ============================== pdf report ===============================
# =========================================================================
@login_required(login_url='/signin/')
def generate_pdf(request, id):
	template_path = 'dashboard/report.html'
	valuation = get_object_or_404(EvaluareForm, id=id)
	pdata = get_object_or_404(PresentationData, ref_no__id=id)
	camere = ResidentialAttrValue.objects.filter(ref_no=valuation, attr_id__pk=2).aggregate(camere=Sum('attr_value'))
	const = get_object_or_404(Construction, ref_no__id=id)
	s_utila = Suprafete.objects.filter(ref_no__id=id, utila=True)
	s_neutila = Suprafete.objects.filter(ref_no__id=id, utila=False)
	utila = Suprafete.objects.filter(ref_no__id=id, utila=True).aggregate(utila = Sum('area'))
	totala = Suprafete.objects.filter(ref_no__id=id).aggregate(totala=Sum('area'))
	anexa = Anexa.objects.filter(ref_no__id=id)
	rooms = ResidentialAttrValue.objects.filter(ref_no__id=id)
	room_photo = ResidentialAttrFile.objects.filter(ref_no__id=id)
	cf_file = CustomFieldFile.objects.filter(ref_no__id=id)
	cover_img = Photo.objects.filter(ref_no__id=id, refer_to="cover").order_by('image_order')
	summary_img = Photo.objects.filter(ref_no__id=id, refer_to="summary").order_by('image_order')
	summary = get_object_or_404(ValuationSummary, ref_no__id=id)
	source_info = SourceofInformation.objects.filter(ref_no__id=id)
	sub = get_object_or_404(ComparableProperty, ref_no__id=id)
	ct = ComparableTable.objects.filter(ref_no__id=id)
	floors = ResidentialAttrValue.objects.filter(ref_no=valuation, floor_type='gresie')
	floors = [f.attr_id.name for f in floors]
	floor_data = ",".join(floors[:-1]) + " si " + floors[-1]

	context = {
		'valuation': valuation, 
		'pdata': pdata,
		'camere': camere,
		'const': const,
		's_utila': s_utila,
		's_neutila': s_neutila,
		'utila': utila,
		'totala': totala,
		'anexa': anexa,
		'rooms': rooms,
		'room_photo': room_photo,
		'cf_file': cf_file,
		'cover_img': cover_img,
		'summary_img': summary_img,
		'summary': summary,
		'source_info': source_info,
		'sub': sub,
		'ct': ct,
		'floor_data': floor_data,
	}

	# Create a Django response object, and specify content_type as pdf
	response = HttpResponse(content_type='application/pdf')
	# if download:
	# response['Content-Disposition'] = 'attachment; filename="report.pdf"'
	# else:
	response['Content-Disposition'] = 'filename="EPI-'+ valuation.reference_no + '-' + valuation.inspection_date.strftime("dmy") + '.pdf"'
	# find the template and render it.
	template = get_template(template_path)
	html = template.render(context)

	# create a pdf
	pisa_status = pisa.CreatePDF(html, dest=response)
	# if error then show some funy view
	if pisa_status.err:
		return HttpResponse('We had some errors <pre>' + html + '</pre>')
	return response



# =========================================================================
# ============================== pdf report ===============================
# =========================================================================
@login_required(login_url='/signin/')
def comparable_properties(request):
	if request.session.get('comp_added'): 
		msg = 'added'
		try:
			del request.session['comp_added']
		except KeyError:
			pass 
	else:
		msg = None

	template = 'dashboard/comparable_list.html'
	properties = ComparableProperty.objects.all().order_by('-id')
	context = {
		'properties': properties,
		'msg': msg,
		'segment': 'comparable',
	}
	return render(request, template, context)


def test(request):
	vid = request.GET.get('id')
	instance = get_object_or_404(EvaluareForm, id=vid)
	return JsonResponse({'success': 'false'})
	# valuation = get_object_or_404(EvaluareForm, id=1)
	# sub = get_object_or_404(ComparableProperty, ref_no=valuation)
	# ct = ComparableTable.objects.filter(ref_no=valuation)

	# context = {
	# 	'valuation': valuation,
	# 	'ct': ct,
	# 	'sub': sub,
	# }
	# return render(request, 'dashboard/test.html', context)
