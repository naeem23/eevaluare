import ast
import json
import datetime
from django import http
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

from valuation import models
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
    complete = models.ValuatedProperty.objects.filter(status__status__icontains="completed").order_by('-id')
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
	instance = get_object_or_404(models.ValuatedProperty, id=vid)
	try:
		response = 1 #instance.delete()
		if response:
			return JsonResponse({'success': 'true'})
	except:
		return JsonResponse({'success': 'false'})


# ======================== complete evaluare map ==========================
# =========================================================================
@login_required(login_url='/signin/')
def evaluari_complete_map(request):
    data = models.ValuatedProperty.objects.filter(status__status__icontains="completed")
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

	incomplete = models.ValuatedProperty.objects.exclude(status__status__icontains="completed").order_by('-id')
	status = models.Status.objects.all()
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
	data = models.ValuatedProperty.objects.exclude(status__status__icontains="completed")
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
    status = get_object_or_404(models.Status, id=status)
    instance = get_object_or_404(models.ValuatedProperty, id=id)
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
    return HttpResponse('evaluare_details')


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
	properties = models.ComparableProperty.objects.all().order_by('-id')
	context = {
		'properties': properties,
		'msg': msg,
		'segment': 'comparable',
	}
	return render(request, template, context)

