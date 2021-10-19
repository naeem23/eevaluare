import ast
import datetime
import json
from math import perm
from django import db
import requests
import string
import urllib.parse
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from requests.api import get

from dashboard import models as db_model 
from valuation import models
from . import forms 


# ========================================================
# =================== inspection date ====================
# ========================================================
@login_required(login_url='/signin/')
def initial_form(request):
    template = 'valuation/initial_form.html'
    msg = None
    areas = models.Area.objects.all()
    compartments = models.Compartimentare.objects.filter(property_type__id=1)

    if request.method == 'POST':
        form = forms.InitialForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.status = models.Status.objects.get(id=1)
            data.inspection_date = timezone.now()
            data.save()

            # save compartimentare 
            compart = request.POST.getlist('compart[]')
            i = 0
            for c in compartments:
                if compart[i] != '0':
                    res = models.CompartimentareValue.objects.create(ref_no=data, attr_id=c, attr_value=compart[i])
                    success = True if res else False
                i += 1
            
            # save custom field 
            cf_name = request.POST.getlist('cf_name[]')
            cf_value = request.POST.getlist('cf_value[]')
            j = 0
            for cf in cf_name:
                cf_res = models.CustomFieldValue.objects.create(ref_no=data, attr_name=cf, attr_value=cf_value[j])
                success = True if cf_res else False
                j += 1
            
            if success:
                return redirect('valuation:add_summary', id=data.id)
    else:
        form = forms.InitialForm()

    context = {
        'msg': msg,
        'areas': areas,
        'segment': 'inspection',
        'form': form,
        'compartments': compartments,
    }
    return render(request, template, context)


@login_required(login_url='/signin/')
def get_city(request):
    area_id = request.GET.get('area_id')
    city = db_model.City.objects.filter(area__id=area_id).values_list('id', 'name')
    return JsonResponse({'city': list(city)})


# ==========================================================
# =================== cover & summary  =====================
# ==========================================================
@login_required(login_url='/signin/')
def add_summary(request, id):
    template = 'valuation/add_summary.html'
    valuation = get_object_or_404(models.ValuatedProperty, id=id)
    above_parking = models.CompartimentareValue.objects.filter(ref_no=valuation,attr_id__pk=9).aggregate(above=Sum('attr_value'))
    below_parking = models.CompartimentareValue.objects.filter(ref_no=valuation,attr_id__pk=10).aggregate(below=Sum('attr_value')) 
    boxa = models.CompartimentareValue.objects.filter(ref_no=valuation,attr_id__pk=11).aggregate(boxa=Sum('attr_value')) 
    camara = models.CompartimentareValue.objects.filter(ref_no=valuation,attr_id__pk__in=[1,3,4]).aggregate(camara=Sum('attr_value'))
    pre_url = request.META.get("HTTP_REFERER")

    # get forex exchange rate of yesterday 
    yesterday = datetime.datetime.now() - datetime.timedelta(1)
    yesterday = datetime.datetime.strftime(yesterday, "%Y-%m-%d")
    url = 'https://api.exchangerate.host/convert?from=EUR&to=RON&date=' + yesterday
    response = requests.get(url)
    data = response.json()
    fer = "{:.2f}".format(data['info']['rate'])

    # post method control
    if request.method == 'POST':
        form = forms.AddValuationSummary(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.ref_no = valuation
            data.save()
            return redirect('valuatio:add_construction', id=id)
    else:
        form = forms.AddValuationSummary()

    context = {
        'valuation_id': valuation.id,
        'above_parking': above_parking['above'],
        'below_parking': below_parking['below'],
        'boxa': boxa['boxa'],
        'camara': camara['camara'],
        'fer': fer,
        'yesterday': yesterday,
        'segment': 'summary',
        'pre_url': pre_url,
        'form': form,
    }
    return render(request, template, context)


@login_required(login_url='/signin/')
def save_photos(request):	
	if request.method == 'POST':
		valuation = get_object_or_404(models.ValuatedProperty, id=request.POST.get('vid'))
		image_order = request.POST.get('order')
		file = request.FILES['file']
		refer_to = request.POST.get('refer_to')
		save = models.Photo.objects.create(ref_no=valuation, refer_to=refer_to, image_order=image_order, image=file)
		if save:
			return JsonResponse({'success': 'true'})
		else: 
			return JsonResponse({'success': 'false'})
	return JsonResponse({'success': 'false'})
    

# ==========================================================
# =================== cover & summary  =====================
# ==========================================================
@login_required(login_url='/signin/')
def add_construction(request, id):
    template = 'valuation/add_construction.html'
    valuation = get_object_or_404(models.ValuatedProperty, id=id)
    rooms = models.CompartimentareValue.objects.filter(ref_no=valuation)
    pre_url = request.META.get("HTTP_REFERER")

    if request.method == 'POST':
        form = forms.ConstructionForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
    else:
        form = forms.ConstructionForm()

    context = {
        'valuation_id': valuation.id,
        'form': form,
        'rooms': rooms,
        'pre_url': pre_url,
        'segment': 'construction',
    }
    return render(request, template, context)


# ==========================================================
# =================== presentation data ====================
# ==========================================================
@login_required(login_url='/signin/')
def add_presentation(request, id):
    template = 'valuation/add_presentation.html'
    valuation = get_object_or_404(models.ValuatedProperty, id=id)
    msg = None
    pre_url = request.META.get("HTTP_REFERER")

    if request.method == 'POST':
        form = forms.PresentationForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            # data = form.save(commit=False)
            # data.ref_no = valuation
            # data.save()
            if request.POST.get('pre_url') == 'details':
                return redirect('dashboard:details', id=valuation.id)
            else:
                return redirect('valuation:add_presentation', id=id)
    else:
        form = forms.PresentationForm()

    context = {
        'valuation_id': valuation.id,
        'form': form,
        'msg': msg,
        'segment': 'presentation',
        'pre_url': pre_url,
    }
    return render(request, template, context)


# =====================================================================
# =================== search and select comparable ====================
# =====================================================================
@login_required(login_url='/signin/')
def select_comparable(request, id):
    template = 'valuation/select_comparable.html'
    valuation = get_object_or_404(db_model.EvaluareForm, id=id)

    if request.method == 'POST':
        comp = request.POST.getlist('comp[]')
        nr_comp = request.POST.get('nr_comapratii')
        return redirect(reverse('valuation:add_comparable', args=[id])+'?comp='+urllib.parse.quote(str(comp))+'&nr_comp='+str(nr_comp))

    context = {
        'valuation': valuation,
    }
    return render(request, template, context)

@login_required(login_url='/signin/')
def search_comparable(request):
    location = request.GET.get('location')
    radius = request.GET.get('radius')
    comparable = db_model.ComparableProperty.objects.filter(location__icontains=location, is_comparable=1).values_list('id', 'location', 'camara', 'area', 'year_build')
    return JsonResponse({'comparable': list(comparable)})


# ========================================================
# =================== add comparable =====================
# ========================================================
@login_required(login_url='/signin/')
def add_comparable(request, id):
    template = 'valuation/add_comparable.html'
    valuation = get_object_or_404(db_model.EvaluareForm, id=id)
    comp = ast.literal_eval(request.GET.get('comp'))
    utila = db_model.Suprafete.objects.filter(ref_no__id=id, utila=True).aggregate(utila=Sum('area'))
    sbalcon = db_model.Suprafete.objects.filter(ref_no__id=id, utila=False).aggregate(balcon=Sum('area'))
    if comp:
        comparable = db_model.ComparableProperty.objects.filter(id__in=comp)
    else:
        comparable = None
    nr_comp = request.GET.get('nr_comp')
    letters = string.ascii_uppercase

    if request.method == 'POST':
        sale_price = request.POST.getlist('sale_price[]')
        mobila = request.POST.getlist('mobila[]')
        ma = request.POST.getlist('ma[]')
        parking_boxa = request.POST.getlist('parking_boxa[]')
        pba = request.POST.getlist('pba[]')
        sub_avdata = request.POST.get('sub_avdata')
        ad = request.POST.getlist('ad[]')
        sub_pr = request.POST.get('sub_pr')
        pr = request.POST.getlist('pr[]')
        sub_fc = request.POST.get('sub_fc')
        fc = request.POST.getlist('fc[]')
        sub_sc = request.POST.get('sub_sc')
        sc = request.POST.getlist('sc[]')
        sub_ape = request.POST.get('sub_ape')
        ape = request.POST.getlist('ape[]')
        sub_me = request.POST.get('sub_me')
        me = request.POST.getlist('me[]')
        sub_location = request.POST.get('sub_location')
        lc = request.POST.getlist('lc[]')
        sub_cp = request.POST.get('sub_cp')
        cp = request.POST.getlist('cp[]')
        sub_cy = request.POST.get('sub_cy')
        cy = request.POST.getlist('cy[]')
        subarea = request.POST.get('sub_area')
        area = request.POST.getlist('area[]')
        sub_finish = request.POST.get('sub_finish')
        finish = request.POST.getlist('finish[]')
        sub_etaj = request.POST.get('sub_etaj')
        etaj = request.POST.getlist('etaj[]')
        subbalcon = request.POST.get('sub_balcon')
        balcon = request.POST.getlist('balcon[]')
        price_persqm = request.POST.get('price_persqm')
        sub_hs = request.POST.get('sub_hs')
        hs = request.POST.getlist('hs[]')
        opt1_name = request.POST.get('opt1_name')
        sub_opt1_val = request.POST.get('sub_opt1_val')
        opt1_val = request.POST.getlist('opt1_val[]')
        opt2_name = request.POST.get('opt2_name')
        sub_opt2_val = request.POST.get('sub_opt2_val')
        opt2_val = request.POST.getlist('opt2_val[]')
        opt3_name = request.POST.get('opt3_name')
        sub_opt3_val = request.POST.get('sub_opt3_val')
        opt3_val = request.POST.getlist('opt3_val[]')

        op = request.POST.getlist('op[]')
        margin = request.POST.getlist('margin[]')
        cv = request.POST.getlist('cv[]')
        mp = request.POST.getlist('mp[]')
        motivation = request.POST.get('motivation')
        pr_percent = request.POST.getlist('pr_percent[]')
        pr_euro = request.POST.getlist('pr_euro[]')
        pr_price = request.POST.getlist('pr_price[]')
        pr_motivation = request.POST.get('pr_motivation')
        fc_percent = request.POST.getlist('fc_percent[]')
        fc_euro = request.POST.getlist('fc_euro[]')
        fc_price = request.POST.getlist('fc_price[]')
        fc_motivation = request.POST.get('fc_motivation')
        sc_percent = request.POST.getlist('sc_percent[]')
        sc_euro = request.POST.getlist('sc_euro[]')
        sc_price = request.POST.getlist('sc_price[]')
        sc_motivation = request.POST.get('sc_motivation')
        ape_percent = request.POST.getlist('ape_percent[]')
        ape_euro = request.POST.getlist('ape_euro[]')
        ape_price = request.POST.getlist('ape_price[]')
        ape_motivation = request.POST.get('ape_motivation')
        me_percent = request.POST.getlist('me_percent[]')
        me_euro = request.POST.getlist('me_euro[]')
        me_price = request.POST.getlist('me_price[]')
        me_motivation = request.POST.get('me_motivation')
        lc_percent = request.POST.getlist('lc_percent[]')
        lc_euro = request.POST.getlist('lc_euro[]')
        lc_motivation = request.POST.get('lc_motivation')
        cp_percent = request.POST.getlist('cp_percent[]')
        cp_euro = request.POST.getlist('cp_euro[]')
        cp_motivation = request.POST.get('cp_motivation')
        cy_percent = request.POST.getlist('cy_percent[]')
        cy_euro = request.POST.getlist('cy_euro[]')
        cy_motivation = request.POST.get('cy_motivation')
        su_diff = request.POST.getlist('su_diff[]')
        su_percent = request.POST.getlist('su_percent[]')
        su_euro = request.POST.getlist('su_euro[]')
        su_motivation = request.POST.get('su_motivation')
        finish_percent = request.POST.getlist('finish_percent[]')
        finish_euro = request.POST.getlist('finish_euro[]')
        finish_motivation = request.POST.get('finish_motivation')
        etaj_percent = request.POST.getlist('etaj_percent[]')
        etaj_euro = request.POST.getlist('etaj_euro[]')
        etaj_motivation = request.POST.get('etaj_motivation')
        balcon_percent = request.POST.getlist('balcon_percent[]')
        balcon_euro = request.POST.getlist('balcon_euro[]')
        balcon_motivation = request.POST.get('balcon_motivation')
        hs_percent = request.POST.getlist('hs_percent[]')
        hs_euro = request.POST.getlist('hs_euro[]')
        hs_motivation = request.POST.get('hs_motivation')
        opt1_percent = request.POST.getlist('opt1_percent[]')
        opt1_euro = request.POST.getlist('opt1_euro[]')
        opt1_motivation = request.POST.get('opt1_motivation')
        opt2_percent = request.POST.getlist('opt2_percent[]')
        opt2_euro = request.POST.getlist('opt2_euro[]')
        opt2_motivation = request.POST.get('opt2_motivation')
        opt3_percent = request.POST.getlist('opt3_percent[]')
        opt3_euro = request.POST.getlist('opt3_euro[]')
        opt3_motivation = request.POST.get('opt3_motivation')

        net_adjustment = request.POST.getlist('net_adjustment[]')
        adjustment_price = request.POST.getlist('adjustment_price[]')
        adjustment_no = request.POST.getlist('adjustment_no[]')
        total_percent = request.POST.getlist('total_percent[]')
        total_euro = request.POST.getlist('total_euro[]')
        gross_percent = request.POST.getlist('gross_percent[]')
        gross_euro = request.POST.getlist('gross_euro[]')
        estimated_value = request.POST.get('estimated_value')
        smallest_gross = request.POST.get('smallest_gross')

        sub_prop = models.ComparableProperty.objects.create(ref_no=valuation, is_comparable=0, ad=sub_avdata, pr=sub_pr, fc=sub_fc, sc=sub_sc, ape=sub_ape, me=sub_me,lc=sub_location, cp=sub_cp, cy=sub_cy, area=subarea, finish=sub_finish, etaj=sub_etaj, balcon=subbalcon, hs=sub_hs, opt1_name=opt1_name, opt1_val=sub_opt1_val, opt2_name=opt2_name, opt2_val=sub_opt2_val, opt3_name=opt3_name, opt3_val=sub_opt3_val)

        comp_list = []
        if comparable:
            comp_list = comp
            if len(comparable) != int(nr_comp):
                for i in range(len(comparable), int(nr_comp)):
                    prop = models.ComparableProperty.objects.create(sale_price=sale_price[i], mobila=mobila[i], ma=ma[i], parking_boxa=parking_boxa[i], pba=pba[i], ad=ad[i], pr=pr[i], fc=fc[i], sc=sc[i], ape=ape[i], me=me[i],lc=lc[i], cp=cp[i], cy=cy[i], area=area[i], finish=finish[i], etaj=etaj[i], balcon=balcon[i], hs=hs[i], opt1_name=opt1_name, opt1_val=opt1_val[i], opt2_name=opt2_name, opt2_val=opt2_val[i], opt3_name=opt3_name, opt3_val=opt3_val[i])
                    comp_list.append(prop.id)
        else:
            for i in range(int(nr_comp)):
                prop = models.ComparableProperty.objects.create(sale_price=sale_price[i], mobila=mobila[i], ma=ma[i], parking_boxa=parking_boxa[i], pba=pba[i], ad=ad[i], pr=pr[i], fc=fc[i], sc=sc[i], ape=ape[i], me=me[i],lc=lc[i], cp=cp[i], cy=cy[i], area=area[i], finish=finish[i], etaj=etaj[i], balcon=balcon[i], hs=hs[i], opt1_name=opt1_name, opt1_val=opt1_val[i], opt2_name=opt2_name, opt2_val=opt2_val[i], opt3_name=opt3_name, opt3_val=opt3_val[i])
                comp_list.append(prop.id)
                
        table = models.ComparableTable.objects.create(ref_no=valuation, comparable=comp_list, name=letters[:int(nr_comp)], op=op, margin=margin, cv=cv, mp=mp, motivation=motivation, pr_percent=pr_percent, pr_euro=pr_euro, pr_price=pr_price, pr_motivation=pr_motivation, fc_percent=fc_percent, fc_euro=fc_euro, fc_price=fc_price, fc_motivation=fc_motivation, sc_percent=sc_percent, sc_euro=sc_euro, sc_price=sc_price, sc_motivation=sc_motivation, ape_percent=ape_percent, ape_euro=ape_euro, ape_price=ape_price, ape_motivation=ape_motivation, me_percent=me_percent, me_euro=me_euro, me_price=me_price, me_motivation=me_motivation, lc_percent=lc_percent, lc_euro=lc_euro, lc_motivation=lc_motivation, cp_percent=cp_percent, cp_euro=cp_euro, cp_motivation=cp_motivation, cy_percent=cy_percent, cy_euro=cy_euro, cy_motivation=cy_motivation, su_diff=su_diff, su_percent=su_percent, su_euro=su_euro, su_motivation=su_motivation, finish_percent=finish_percent, finish_euro=finish_euro, finish_motivation=finish_motivation, etaj_percent=etaj_percent, etaj_euro=etaj_euro, etaj_motivation=etaj_motivation, price_persqm=price_persqm, balcon_percent=balcon_percent, balcon_euro=balcon_euro, balcon_motivation=balcon_motivation, hs_percent=hs_percent, hs_euro=hs_euro, hs_motivation=hs_motivation, opt1_percent=opt1_percent, opt1_euro=opt1_euro, opt1_motivation=opt1_motivation, opt2_percent=opt2_percent, opt2_euro=opt2_euro, opt2_motivation=opt2_motivation, opt3_percent=opt3_percent, opt3_euro=opt3_euro, opt3_motivation=opt3_motivation, net_adjustment=net_adjustment,adjustment_price=adjustment_price, adjustment_no=adjustment_no,total_percent=total_percent,total_euro=total_euro,gross_percent=gross_percent,gross_euro=gross_euro,estimated_value=estimated_value,smallest_gross=smallest_gross)

    context = {
        'valuation': valuation,
        's_area': utila['utila'],
        's_balcon': sbalcon['balcon'],
        'comparable': comparable,
        'nr_comp': int(nr_comp),
    }
    return render(request, template, context)




