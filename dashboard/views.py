import ast
import json
import datetime
from django import http
from django.db.models.expressions import Value
import requests
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.mail import send_mail
from django.db import connection
from django.db.models import Sum, Q
from django.http import HttpResponse, JsonResponse, response
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.template.loader import get_template, render_to_string
from django.utils import timezone
from django.views import View
from requests.sessions import HTTPAdapter
from xhtml2pdf import pisa

from valuation import models as vmodels
User = get_user_model()


# ========================== Dashboard page ===============================
# =========================================================================
@login_required(login_url="/signin/")
def dashboardView(request):
    if request.session.get('completed'):
        msg = 'marked'
        try:
            del request.session['completed']
        except KeyError:
            pass
    else:
        msg = None
    template_name = 'dashboard/evaluari_complete.html'
    complete = vmodels.ValuatedProperty.objects.filter(status__status__icontains="completed").order_by('-id')
    context = {
        'segment': 'complete',
        'msg': msg,
        'complete': complete,
    }
    return render(request, template_name, context)


# ========================== delete valuation =============================
# =========================================================================
@login_required(login_url='/signin/')
def delete_valuation(request):
	vid = request.GET.get('id')
	instance = get_object_or_404(vmodels.ValuatedProperty, id=vid)
	try:
		response = instance.delete()
		if response:
			return JsonResponse({'success': 'true'})
	except:
		return JsonResponse({'success': 'false'})


# ======================== complete evaluare map ==========================
# =========================================================================
@login_required(login_url='/signin/')
def evaluari_complete_map(request):
    data = vmodels.ValuatedProperty.objects.filter(status__status__icontains="completed")
    data = serializers.serialize("json", data)
    context = {
        'segment': 'complete',
        'addressPoints': data, 
    }
    return render(request, 'dashboard/evaluari_complete_map.html', context)


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

	incomplete = vmodels.ValuatedProperty.objects.exclude(status__status__icontains="completed").order_by('-id')
	status = vmodels.Status.objects.all()
	context = {
		'segment': 'incomplet',
		'msg': msg,
		'incomplete': incomplete,
		'status': status,
	}
	return render(request, 'dashboard/evaluari_incomplete.html', context)


# ========================== Incomplete map ===============================
# =========================================================================
@login_required(login_url='/signin/')
def evaluari_incomplete_map(request):
	data = vmodels.ValuatedProperty.objects.exclude(status__status__icontains="completed")
	data = serializers.serialize("json", data)
	context = {
		'segment': 'incomplet',
		'addressPoints': data, 
	}
	return render(request, 'dashboard/evaluari_incomplete_map.html', context)


# ============================ update status =====-========================
# =========================================================================
@login_required(login_url='/signin/')
def change_status(request, status, id):
    previous_url = request.META.get('HTTP_REFERER')
    status = get_object_or_404(vmodels.Status, id=status)
    instance = get_object_or_404(vmodels.ValuatedProperty, id=id)
    instance.status = status
    try: 
        if 'completed' in status.status:
            instance.report_date = timezone.now()
        instance.save()
        response = True
    except:
        response = False
    if response:
        if 'completed' in instance.status.status:
            request.session['completed'] = True
            if 'details' in previous_url:
                return redirect('dashboard:details', id=id)
            else:
                return redirect('dashboard:complete')
        else:
            request.session['status'] = True
            if 'details' in previous_url:
                return redirect('dashboard:details', id=id)
            else:
                return redirect('dashboard:incomplete')
    else:
        request.session['not_change'] = True
        if 'details' in previous_url:
            return redirect('dashboard:details', id=id)
        else:
            return redirect('dashboard:incomplete')
            

# ============================== details ===============================
# =========================================================================
@login_required(login_url='/signin/')
def evaluare_details(request, id):
	template = 'valuation/valuation_details.html'
	valuation = get_object_or_404(vmodels.ValuatedProperty, id=id)
	utila_filter = Q()
	for x in ['balcon','terasa','parcare','boxa']:
		utila_filter = utila_filter | Q(attr_id__name__icontains=x)
	rooms = vmodels.CompartimentareValue.objects.filter(ref_no=valuation).exclude(utila_filter)
	customs = vmodels.CustomFieldValue.objects.filter(ref_no=valuation)
	try:
		camara = vmodels.CompartimentareValue.objects.filter(ref_no=valuation,attr_id__pk__in=[1,3,4]).aggregate(camara=Sum('attr_value'))
	except:
		camara = None
	try:
		cover_photo = vmodels.Photo.objects.filter(ref_no__id=id, refer_to="cover").order_by('image_order')
		summary_photo = vmodels.Photo.objects.filter(ref_no__id=id, refer_to="summary").order_by('image_order')
	except:
		cover_photo = None
		summary_photo = None
	try:
		summary = vmodels.ValuationSummary.objects.filter(ref_no=valuation).latest('id')
		summary_value = vmodels.SummaryValue.objects.filter(summary=summary)
	except:
		summary = None
		summary_value = None 
	try:
		const = vmodels.Construction.objects.filter(ref_no=valuation).latest('id')
	except:
		const = None 
	suprafete = vmodels.Suprafete.objects.filter(ref_no=valuation)
	source = vmodels.SourceofInformation.objects.filter(ref_no=valuation)
	try:
		presentation = vmodels.PresentationData.objects.filter(ref_no=valuation).latest('id')
	except:
		presentation = None 
	try:
		market = vmodels.MarketAnalysis.objects.filter(ref_no=valuation).latest('id')
	except:
		market = None 

	comp_table = vmodels.ComparableTable.objects.filter(ref_no=valuation)
	try:
		sub_prop = vmodels.ComparableProperty.objects.filter(ref_no=valuation).latest('id')
	except:
		sub_prop = None
	try:
		sub_mvb = vmodels.MvbTable.objects.filter(ref_no=valuation, monthly_rent=None).latest('id')
	except:
		sub_mvb = None
	comp_mvb = vmodels.MvbTable.objects.filter(ref_no=valuation, sub_rent_sqm=None)
	utility = vmodels.Utility.objects.all()
	status = vmodels.Status.objects.all()
	context = {
		'valuation': valuation, 
		'rooms': rooms,
		'customs': customs,
		'camara': camara,
		'cover_photo': cover_photo,
		'summary_photo': summary_photo,
		'summary': summary,
		'summary_value': summary_value,
		'const': const,
		'suprafete': suprafete,
		'source': source,
		'pdata': presentation,
		'market': market,
		'comp_table': comp_table,
		'sub_prop': sub_prop,
		'sub_mvb': sub_mvb,
		'comp_mvb': comp_mvb,
		'utility': utility,
		'status': status,
	}
	return render(request, template, context)


# ============================== Modules ===============================
# =========================================================================
modules = {'area':'Area','city':'City','property-type':'Property Type','compartment-type':'Compartment Type','status':'Status','valuation-purpose':'Valuation Purpose','valuation-approach':'Valuation Approach','strada-type':'Strada Type','transport':'Transport','conform-type':'ConformType','structure-type':'Structure Type','foundation-type':'Foundation Type','floor-type':'Floor Type','clouser-type':'ClouserType','subcompartment-type':'Subcompartment Type','roof-type':'Roof Type','invelitoare-type':'Invelitoare Type','mobila-type':'Mobila Type','property-right-type':'Property Right Type','heating-system':'Heating System','finish-type':'FinishType'}

@login_required(login_url='/signin/')
def modules_list(request):
	template_name = 'dashboard/modules_list.html'
	modules = {'area':'Area','city':'City','property-type':'Property Type','compartment-type':'Compartment Type','status':'Status','valuation-purpose':'Valuation Purpose','valuation-approach':'Valuation Approach','strada-type':'Strada Type','transport':'Transport','conform-type':'ConformType','structure-type':'Structure Type','foundation-type':'Foundation Type','floor-type':'Floor Type','clouser-type':'ClouserType','subcompartment-type':'Subcompartment Type','roof-type':'Roof Type','invelitoare-type':'Invelitoare Type','mobila-type':'Mobila Type','property-right-type':'Property Right Type','heating-system':'Heating System','finish-type':'FinishType'}

	if request.session.get('success'):
		msg = 'deleted'
		try:
			del request.session['success']
		except KeyError:
			pass
	elif request.session.get('failed'):
		msg = 'not_deleted'
		try:
			del request.session['failed']
		except KeyError:
			pass
	elif request.session.get('added'):
		msg = 'added'
		try:
			del request.session['added']
		except KeyError:
			pass
	elif request.session.get('not_added'):
		msg = 'not_added'
		try:
			del request.session['not_added']
		except KeyError:
			pass
	else:
		msg = None

	context = {
		'modules': modules, 
		'segment': 'settings',
	}
	return render(request, template_name, context)

@login_required(login_url='/signin/')
def go_module(request, key):
	template_name = 'dashboard/go_module.html'
	modules = {'area':'Area','city':'City','property-type':'Property Type','compartment-type':'Compartment Type','status':'Status','valuation-purpose':'Valuation Purpose','valuation-approach':'Valuation Approach','strada-type':'Strada Type','transport':'Transport','conform-type':'ConformType','structure-type':'Structure Type','foundation-type':'Foundation Type','floor-type':'Floor Type','clouser-type':'ClouserType','subcompartment-type':'Subcompartment Type','roof-type':'Roof Type','invelitoare-type':'Invelitoare Type','mobila-type':'Mobila Type','property-right-type':'Property Right Type','heating-system':'Heating System','finish-type':'FinishType'}

	if request.method=="POST":
		if 'add' in request.POST:
			if request.POST.get('add')=="area":
				area = vmodels.Area.objects.create(auto = request.POST.get('auto'), name = request.POST.get('name'))
			elif request.POST.get('add')=="city":
				city = vmodels.City.objects.create(area = request.POST.get('area'), name = request.POST.get('name'))
			elif request.POST.get('add')=="status":
				status = vmodels.Status.objects.create(status = request.POST.get('status'))
			elif request.POST.get('add')=="valuation-purpose":
				valuation_purpose = vmodels.ValuationPurpose.objects.create(purpose = request.POST.get('purpose'))
			elif request.POST.get('add')=="valuation-approach":
				valuation_approach = vmodels.ValuationApproach.objects.create(approach = request.POST.get('approach'))
			elif request.POST.get('add')=="transport":
				transport = vmodels.Transport.objects.create(name = request.POST.get('name'))
			elif request.POST.get('add')=="heating-system":
				heating_system = vmodels.HeatingSystem.objects.create(name = request.POST.get('name'))
			elif request.POST.get('add')=="finish-type":
				finish_type = vmodels.FinishType.objects.create(type = request.POST.get('type'))
			elif request.POST.get('add')=="property-right-type":
				property_right_type = vmodels.PropertyRightType.objects.create(type = request.POST.get('type'))
			elif request.POST.get('add')=="property-type":
				property_type = vmodels.PropertyType.objects.create(type = request.POST.get('type'))
			elif request.POST.get('add')=="compartment-type":
				compartment_type = vmodels.CompartmentType.objects.create(type = request.POST.get('type'))
			elif request.POST.get('add')=="strada-type":
				strada_type = vmodels.StradaType.objects.create(type = request.POST.get('type'))
			elif request.POST.get('add')=="conform-type":
				conform_type = vmodels.ConformType.objects.create(type = request.POST.get('type'))
			elif request.POST.get('add')=="structure-type":
				structure_type = vmodels.StructureType.objects.create(type = request.POST.get('type'))
			elif request.POST.get('add')=="mobila-type":
				mobila_type = vmodels.MobilaType.objects.create(type = request.POST.get('type'))
			elif request.POST.get('add')=="invelitoare-type":
				invelitoare_type = vmodels.InvelitoareType.objects.create(type = request.POST.get('type'))
			elif request.POST.get('add')=="roof-type":
				roof_type = vmodels.RoofType.objects.create(type = request.POST.get('type'))
			elif request.POST.get('add')=="subcompartment-type":
				subcompartment_type = vmodels.SubcompartmentType.objects.create(type = request.POST.get('type'))
			elif request.POST.get('add')=="clouser-type":
				clouser_type = vmodels.ClouserType.objects.create(type = request.POST.get('type'))
			elif request.POST.get('add')=="floor-type":
				floor_type = vmodels.FloorType.objects.create(type = request.POST.get('type'))
			elif request.POST.get('add')=="foundation-type":
				foundation_type = vmodels.FoundationType.objects.create(type = request.POST.get('type'))
			
		elif 'update' in request.POST:
			idd = request.POST.get('id')
			if request.POST.get('update')=="area":
				obj = vmodels.Area.objects.get(id = idd)
				obj.auto = request.POST.get('auto')
				obj.name = request.POST.get('name')
				obj.save()
			elif request.POST.get('update')=="city":
				obj = vmodels.City.objects.get(id = idd)
				obj.area = request.POST.get('area')
				obj.name = request.POST.get('name')
				obj.save()
			elif request.POST.get('update')=="status":
				obj = vmodels.Status.objects.get(id = idd)
				obj.status = request.POST.get('status')
				obj.save()
			elif request.POST.get('update')=="valuation-purpose":
				obj = vmodels.ValuationPurpose.objects.get(id = idd)
				obj.purpose = request.POST.get('purpose')
				obj.save()
			elif request.POST.get('update')=="valuation-approach":
				obj = vmodels.ValuationApproach.objects.get(id = idd)
				obj.approach = request.POST.get('approach')
				obj.save()
			elif request.POST.get('update')=="transport":
				obj = vmodels.Transport.objects.get(id = idd)
				obj.name = request.POST.get('name')
				obj.save()
			elif request.POST.get('update')=="heating-system":
				obj = vmodels.HeatingSystem.objects.get(id = idd)
				obj.name = request.POST.get('name')
				obj.save()
			elif request.POST.get('update')=="finish-type":
				obj = vmodels.FinishType.objects.get(id = idd)
				obj.type = request.POST.get('type')
				obj.save()
			elif request.POST.get('update')=="property-right-type":
				obj = vmodels.PropertyRightType.objects.get(id = idd)
				obj.type = request.POST.get('type')
				obj.save()
			elif request.POST.get('update')=="property-type":
				obj = vmodels.PropertyType.objects.get(id = idd)
				obj.type = request.POST.get('type')
				obj.save()
			elif request.POST.get('update')=="compartment-type":
				obj = vmodels.CompartmentType.objects.get(id = idd)
				obj.type = request.POST.get('type')
				obj.save()
			elif request.POST.get('update')=="strada-type":
				obj = vmodels.StradaType.objects.get(id = idd)
				obj.type = request.POST.get('type')
				obj.save()
			elif request.POST.get('update')=="conform-type":
				obj = vmodels.ConformType.objects.get(id = idd)
				obj.type = request.POST.get('type')
				obj.save()
			elif request.POST.get('update')=="structure-type":
				obj = vmodels.StructureType.objects.get(id = idd)
				obj.type = request.POST.get('type')
				obj.save()
			elif request.POST.get('update')=="mobila-type":
				obj = vmodels.MobilaType.objects.get(id = idd)
				obj.type = request.POST.get('type')
				obj.save()
			elif request.POST.get('update')=="invelitoare-type":
				obj = vmodels.InvelitoareType.objects.get(id = idd)
				obj.type = request.POST.get('type')
				obj.save()
			elif request.POST.get('update')=="roof-type":
				obj = vmodels.RoofType.objects.get(id = idd)
				obj.type = request.POST.get('type')
				obj.save()
			elif request.POST.get('update')=="subcompartment-type":
				obj = vmodels.SubcompartmentType.objects.get(id = idd)
				obj.type = request.POST.get('type')
				obj.save()
			elif request.POST.get('update')=="clouser-type":
				obj = vmodels.ClouserType.objects.get(id = idd)
				obj.type = request.POST.get('type')
				obj.save()
			elif request.POST.get('update')=="floor-type":
				obj = vmodels.FloorType.objects.get(id = idd)
				obj.type = request.POST.get('type')
				obj.save()
			elif request.POST.get('update')=="foundation-type":
				obj = vmodels.FoundationType.objects.get(id = idd)
				obj.type = request.POST.get('type')
				obj.save()

		return redirect('dashboard:go_module_view', key)

	module_keys = None
	areas = None
	if key=="area":
		module_keys = vmodels.Area.objects.all()
	elif key=="city":
		areas = vmodels.Area.objects.all()
		module_keys = vmodels.City.objects.all()
	elif key=="status":
		module_keys = vmodels.Status.objects.all()
	elif key=="valuation-purpose":
		module_keys = vmodels.ValuationPurpose.objects.all()
	elif key=="valuation-approach":
		module_keys = vmodels.ValuationApproach.objects.all()
	elif key=="transport":
		module_keys = vmodels.Transport.objects.all()
	elif key=="heating-system":
		module_keys = vmodels.HeatingSystem.objects.all()
	elif key=="finish-type":
		module_keys = vmodels.FinishType.objects.all()
	elif key=="property-right-type":
		module_keys = vmodels.PropertyRightType.objects.all()
	elif key=="property-type":
		module_keys = vmodels.PropertyType.objects.all()
	elif key=="compartment-type":
		module_keys = vmodels.CompartmentType.objects.all()
	elif key=="strada-type":
		module_keys = vmodels.StradaType.objects.all()
	elif key=="conform-type":
		module_keys = vmodels.ConformType.objects.all()
	elif key=="structure-type":
		module_keys = vmodels.StructureType.objects.all()
	elif key=="mobila-type":
		module_keys = vmodels.MobilaType.objects.all()
	elif key=="invelitoare-type":
		module_keys = vmodels.InvelitoareType.objects.all()
	elif key=="roof-type":
		module_keys = vmodels.RoofType.objects.all()
	elif key=="subcompartment-type":
		module_keys = vmodels.SubcompartmentType.objects.all()
	elif key=="clouser-type":
		module_keys = vmodels.ClouserType.objects.all()
	elif key=="floor-type":
		module_keys = vmodels.FloorType.objects.all()
	elif key=="foundation-type":
		module_keys = vmodels.FoundationType.objects.all()
	
	context = {
		'modules': modules,
		'key': key,
		'value': modules[key],
		'module_keys':module_keys,
		'areas':areas,
	}
	return render(request, template_name, context)

# ============================= module delete view ============================
# ============================================================================
@login_required(login_url='/signin/')
def delete_module(request,key, id):
	print("aci???")
	if key=="area":
		module_obj = get_object_or_404(vmodels.Area, id=id)
	elif key=="city":
		module_obj = get_object_or_404(vmodels.City, id=id)
	elif key=="status":
		module_obj = get_object_or_404(vmodels.Status, id=id)
	elif key=="valuation-purpose":
		module_obj = get_object_or_404(vmodels.ValuationPurpose, id=id)
	elif key=="valuation-approach":
		module_obj = get_object_or_404(vmodels.ValuationApproach, id=id)
	elif key=="transport":
		module_obj = get_object_or_404(vmodels.Transport, id=id)
	elif key=="heating-system":
		module_obj = get_object_or_404(vmodels.HeatingSystem, id=id)
	elif key=="finish-type":
		module_obj = get_object_or_404(vmodels.FinishType, id=id)
	elif key=="property-right-type":
		module_obj = get_object_or_404(vmodels.PropertyRightType, id=id)
	elif key=="property-type":
		module_obj = get_object_or_404(vmodels.PropertyType, id=id)
	elif key=="compartment-type":
		module_obj = get_object_or_404(vmodels.CompartmentType, id=id)
	elif key=="strada-type":
		module_obj = get_object_or_404(vmodels.StradaType, id=id)
	elif key=="conform-type":
		module_obj = get_object_or_404(vmodels.ConformType, id=id)
	elif key=="structure-type":
		module_obj = get_object_or_404(vmodels.StructureType, id=id)
	elif key=="mobila-type":
		module_obj = get_object_or_404(vmodels.MobilaType, id=id)
	elif key=="invelitoare-type":
		module_obj = get_object_or_404(vmodels.InvelitoareType, id=id)
	elif key=="roof-type":
		module_obj = get_object_or_404(vmodels.RoofType, id=id)
	elif key=="subcompartment-type":
		module_obj = get_object_or_404(vmodels.SubcompartmentType, id=id)
	elif key=="clouser-type":
		module_obj = get_object_or_404(vmodels.ClouserType, id=id)
	elif key=="floor-type":
		module_obj = get_object_or_404(vmodels.FloorType, id=id)
	elif key=="foundation-type":
		module_obj = get_object_or_404(vmodels.FoundationType, id=id)
	
	try:
		response = module_obj.delete()
		if response:
			request.session['success'] = True
		else: 
			request.session['failed'] = True
	except:
		request.session['failed'] = True

	return redirect('dashboard:go_module_view', key)


# ============================== comparable property ===============================
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
	properties = vmodels.ComparableProperty.objects.all().order_by('-id')
	context = {
		'properties': properties,
		'msg': msg,
		'segment': 'comparable',
	}
	return render(request, template, context)

@login_required(login_url='/signin/')
def delete_comp_prop(request):
	vid = request.GET.get('id')
	instance = get_object_or_404(vmodels.ComparableProperty, id=vid)
	try:
		response = instance.delete()
		if response:
			return JsonResponse({'success': 'true'})
	except:
		return JsonResponse({'success': 'false'})


def pdf(request, id):
	template_path = 'valuation/report.html'
	valuation = get_object_or_404(vmodels.ValuatedProperty, id=id)
	utila_filter = Q()
	for x in ['balcon','terasa','parcare','boxa']:
		utila_filter = utila_filter | Q(attr_id__name__icontains=x)
	rooms = vmodels.CompartimentareValue.objects.filter(ref_no=valuation).exclude(utila_filter)
	customs = vmodels.CustomFieldValue.objects.filter(ref_no=valuation)
	try:
		camara = vmodels.CompartimentareValue.objects.filter(ref_no=valuation,attr_id__pk__in=[1,3,4]).aggregate(camara=Sum('attr_value'))
	except:
		camara = None
	try:
		cover_photo = vmodels.Photo.objects.filter(ref_no__id=id, refer_to="cover").order_by('image_order')
		summary_photo = vmodels.Photo.objects.filter(ref_no__id=id, refer_to="summary").order_by('image_order')
	except:
		cover_photo = None
		summary_photo = None
	try:
		summary = vmodels.ValuationSummary.objects.filter(ref_no=valuation).latest('id')
		summary_value = vmodels.SummaryValue.objects.filter(summary=summary)
	except:
		summary = None
		summary_value = None 
	try:
		const = vmodels.Construction.objects.filter(ref_no=valuation).latest('id')
	except:
		const = None 
	suprafete = vmodels.Suprafete.objects.filter(ref_no=valuation)
	source = vmodels.SourceofInformation.objects.filter(ref_no=valuation)
	try:
		presentation = vmodels.PresentationData.objects.filter(ref_no=valuation).latest('id')
	except:
		presentation = None 
	try:
		market = vmodels.MarketAnalysis.objects.filter(ref_no=valuation).latest('id')
	except:
		market = None 
	comp_table = vmodels.ComparableTable.objects.filter(ref_no=valuation)
	try:
		sub_prop = vmodels.ComparableProperty.objects.filter(ref_no=valuation).latest('id')
	except:
		sub_prop = None
	try:
		sub_mvb = vmodels.MvbTable.objects.filter(ref_no=valuation, monthly_rent=None).latest('id')
	except:
		sub_mvb = None
	comp_mvb = vmodels.MvbTable.objects.filter(ref_no=valuation, sub_rent_sqm=None)
	utility = vmodels.Utility.objects.all()
	context = {
		'valuation': valuation, 
		'rooms': rooms,
		'customs': customs,
		'camara': camara,
		'cover_photo': cover_photo,
		'summary_photo': summary_photo,
		'summary': summary,
		'summary_value': summary_value,
		'const': const,
		'suprafete': suprafete,
		'source': source,
		'pdata': presentation,
		'market': market,
		'comp_table': comp_table,
		'sub_prop': sub_prop,
		'sub_mvb': sub_mvb,
		'comp_mvb': comp_mvb,
		'utility': utility,
	}

	# Create a Django response object, and specify content_type as pdf
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'filename="EPI-'+ valuation.reference_no + '-' + valuation.inspection_date.strftime("%d%m%y") + '.pdf"'
	# find the template and render it.
	template = get_template(template_path)
	html = template.render(context)
	# create a pdf
	pisa_status = pisa.CreatePDF(html, dest=response)
	# if error then show some funy view
	if pisa_status.err:
		return HttpResponse('We had some errors <pre>' + html + '</pre>')
	return response