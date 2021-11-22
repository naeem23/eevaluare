import ast
import datetime
import json
from django.db.models.expressions import Value
from django.utils.translation import templatize
from django.utils.dateparse import parse_date
import requests
import string
import urllib.parse
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Q
from django.http import HttpResponse, JsonResponse, response
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from requests.api import get

from dashboard import models as db_model 
from valuation import models
from . import forms
User = get_user_model()


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
            data.assigned_to = request.user.get_full_name()
            data.save()

            # save compartimentare 
            compart = request.POST.getlist('compart[]')
            i = 0
            for c in compartments:
                res = models.CompartimentareValue.objects.create(ref_no=data, attr_id=c, attr_value=compart[i])
                success = True if res else False
                i += 1
            
            # save custom field 
            cf_name = request.POST.getlist('cf_name[]')
            cf_value = request.POST.getlist('cf_value[]')
            j = 0
            for cf in cf_name:
                if cf_value[j] != '0':
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
        'segment': 'initial',
        'form': form,
        'compartments': compartments,
    }
    return render(request, template, context)

@login_required(login_url='/signin/')
def get_city(request):
    area_id = request.GET.get('area_id')
    city = models.City.objects.filter(area__id=area_id).values_list('id', 'name')
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
    if valuation.valuation_date:
        yesterday = valuation.valuation_date - datetime.timedelta(1)
    else:
        yesterday = datetime.datetime.now() - datetime.timedelta(1)
    yesterday = datetime.datetime.strftime(yesterday, "%Y-%m-%d")
    url = 'https://api.exchangerate.host/convert?from=EUR&to=RON&date=' + yesterday
    response = requests.get(url)
    data = response.json()
    fer = "{:.2f}".format(data['info']['rate'])

    # check if valued propery has summary, summary value, photos
    try:
        cover_photo = models.Photo.objects.filter(ref_no=valuation, refer_to='cover')
        summary = models.ValuationSummary.objects.filter(ref_no=valuation).latest('id')
        summary_value = models.SummaryValue.objects.filter(summary=summary)
        summary_photo = models.Photo.objects.filter(ref_no=valuation, refer_to='summary')
    except:
        cover_photo = None
        summary = None 
        summary_value = None 
        summary_photo = None

    if request.method == 'POST':
        if summary:
            form = forms.AddValuationSummary(request.POST, instance=summary)
        else:
            form = forms.AddValuationSummary(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.ref_no = valuation
            data.save()
            # data.approach.set() to-do

            # save summary value 
            if summary_value:
                mv_name = request.POST.getlist('field_name_mv[]')
                mv_value = request.POST.getlist('field_value_mv[]')
                mi = 0
                for mv in summary_value:
                    if mv.approache == 'market':
                        mv.field_name = mv_name[mi]
                        mv.field_value = mv_value[mi]
                        mv.save()
                        mi += 1

                iv_name = request.POST.getlist('field_name_iv[]')
                iv_value = request.POST.getlist('field_value_iv[]')
                ii = 0
                for iv in summary_value:
                    if iv.approache == 'income':
                        iv.field_name = iv_name[ii]
                        iv.field_value = iv_value[ii] 
                        iv.save()
                        ii += 1
            else:
                mv_name = request.POST.getlist('field_name_mv[]')
                mv_value = request.POST.getlist('field_value_mv[]')
                for n, v in zip(mv_name, mv_value):
                    if v != None:
                        models.SummaryValue.objects.create(summary=data, field_name=n, field_value=v, approache="market")

                iv_name = request.POST.getlist('field_name_iv[]')
                iv_value = request.POST.getlist('field_value_iv[]')
                for name, val in zip(iv_name, iv_value):
                    if val != None:
                        models.SummaryValue.objects.create(summary=data, field_name=name, field_value=val, approache="income")
                        
            if request.POST.get("pre_url") == 'details':
                return redirect('dashboard:details', id=valuation.id)
            else:
                return redirect('valuation:add_construction', id=id)
    else:
        if summary:
            form = forms.AddValuationSummary(instance=summary)
        else:
            form = forms.AddValuationSummary()
    
    context = {
        'valuation': valuation,
        'above_parking': above_parking['above'],
        'below_parking': below_parking['below'],
        'boxa': boxa['boxa'],
        'camara': camara['camara'],
        'fer': fer,
        'yesterday': yesterday,
        'segment': 'summary',
        'pre_url': pre_url,
        'form': form,
        'cover_photo': cover_photo,
        'summary': summary,
        'summary_value': summary_value,
        'summary_photo': summary_photo,
    }
    return render(request, template, context)

@login_required(login_url='/signin/')
def save_photos(request):	
    if request.method == 'POST':
        valuation = get_object_or_404(models.ValuatedProperty, id=request.POST.get('vid'))
        file = request.FILES['file']
        image_order = request.POST.get('order')
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
    utila_filter = Q()
    for x in ['balcon','terasa','parcare','boxa']:
        utila_filter = utila_filter | Q(attr_id__name__icontains=x)
    rooms = models.CompartimentareValue.objects.filter(ref_no=valuation, attr_value__gte=1).exclude(utila_filter)
    customs = models.CustomFieldValue.objects.filter(ref_no=valuation)
    balcons = models.CompartimentareValue.objects.filter(ref_no=valuation, attr_id__id__in=[7,8], attr_value__gte=1)
    floor_type = models.FloorType.objects.all()
    pre_url = request.META.get("HTTP_REFERER")

    # check if valuation has construction, suprafete
    try:
        const = models.Construction.objects.filter(ref_no=valuation).latest('id')
    except:
        const = None 
    suprafete = models.Suprafete.objects.filter(ref_no=valuation)
    s_utila = models.Suprafete.objects.filter(ref_no=valuation, is_utila=True)
    s_nuutila = models.Suprafete.objects.filter(ref_no=valuation, is_utila=False)

    if request.method == 'POST':
        if const:
            form = forms.ConstructionForm(request.POST, instance=const)
        else:
            form = forms.ConstructionForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.ref_no = valuation
            data.conform_text = form.cleaned_data.get('conform_text') if request.POST.get('show_conform') == '1' else None 
            data.exterior_finishes = form.cleaned_data.get('exterior_finishes') if request.POST.get('show_ef') == '1' else None
            data.save()
            data.utilities.set(form.cleaned_data['utilities'])
            
            # create Suprafete
            nr_crt = request.POST.getlist('nr_crt[]')
            room_name = request.POST.getlist('room_name[]')
            areas = request.POST.getlist('area[]')
            is_utila = request.POST.getlist('is_utila[]')
            if suprafete:
                su_id = request.POST.getlist('su_id[]')
                for n, r, a, iu, su in zip(nr_crt, room_name, areas, is_utila, su_id):
                    if su != '0':
                        models.Suprafete.objects.filter(id=su).update(nr_crt=n, room_name=r, area=a, is_utila=iu)
                    else:
                        models.Suprafete.objects.create(ref_no=valuation, nr_crt=n, room_name=r, area=a, is_utila=iu)
            else:
                for n, r, a, iu in zip(nr_crt, room_name, areas, is_utila):
                    models.Suprafete.objects.create(ref_no=valuation, nr_crt=n, room_name=r, area=a, is_utila=iu)
            
            if request.POST.get('pre_url') == 'details':
                return redirect('dashboard:details', id=id)
            else:
                return redirect('valuation:add_presentation', id=id)
    else:
        if const:
            form = forms.ConstructionForm(instance=const)
        else:
            form = forms.ConstructionForm()

    context = {
        'valuation': valuation,
        'form': form,
        'rooms': rooms,
        'customs': customs,
        'balcons': balcons,
        'floor_type': floor_type,
        'const': const,
        's_utila': s_utila,
        's_nuutila': s_nuutila,
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
    camara = models.CompartimentareValue.objects.filter(ref_no=valuation,attr_id__pk__in=[1,3,4]).aggregate(camara=Sum('attr_value'))
    transport = models.Transport.objects.all()
    try:
        valued_property = models.ValuationSummary.objects.values('valued_property').filter(ref_no=valuation).latest('id')
    except:
        valued_property = None
    try:
        const = models.Construction.objects.filter(ref_no=valuation).latest('id')
    except:
        const = None
    pre_url = request.META.get("HTTP_REFERER")
    sources = models.SourceofInformation.objects.filter(ref_no=valuation)
    try:
        pdata = models.PresentationData.objects.filter(ref_no=valuation).latest('id')
    except:
        pdata = None

    if request.method == 'POST':
        if pdata:
            form = forms.PresentationForm(request.POST, instance=pdata)
        else:
            form = forms.PresentationForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.ref_no = valuation
            data.pt = request.POST.getlist('pt[]')
            data.legal_doc = request.POST.getlist('legal_doc[]')
            data.cadastral_text = form.cleaned_data.get('cadastral_text') if request.POST.get('show_cadastral') == '1' else None 
            data.access_text = form.cleaned_data.get('access_text') if request.POST.get('show_access') == '1' else None 
            data.identification = request.POST.getlist('identification[]')
            data.save()
            if request.POST.get('pre_url') == 'details':
                return redirect('dashboard:details', id=id)
            else:
                return redirect('valuation:add_market_analysis', id=id)
    else:
        if pdata:
            form = forms.PresentationForm(instance=pdata)
        else:
            form = forms.PresentationForm()

    context = {
        'valuation': valuation,
        'pdata': pdata,
        'sources': sources,
        'camara': camara['camara'],
        'const': const,
        'transport': transport,
        'valued_property': valued_property,
        'form': form,
        'segment': 'presentation',
        'pre_url': pre_url,
    }
    return render(request, template, context)

@login_required(login_url='/signin/')
def add_source(request):
    if request.method == 'POST':
        vid = request.POST.get('vid')
        valuation = get_object_or_404(models.ValuatedProperty, id=vid)
        source = request.POST.get('source')
        check_source = models.SourceofInformation.objects.filter(ref_no=valuation, source=source)
        if check_source:
            response = None
        else:
            response = models.SourceofInformation.objects.create(ref_no=valuation, source=source)
        
        if response:
            return JsonResponse({'success': 'true', 'id': response.id})
        else:
            return JsonResponse({'success': 'false', 'msg': 'exists'})
    else:
        return JsonResponse({'success': 'false', 'msg': 'none'})


# ============================================================
# =================== market analysis data ====================
# ============================================================
@login_required(login_url='/signin/')
def add_market_analysis(request, id):
    template = 'valuation/add_market.html'
    valuation = get_object_or_404(models.ValuatedProperty, id=id)
    camara = models.CompartimentareValue.objects.filter(ref_no=valuation,attr_id__pk__in=[1,3,4]).aggregate(camara=Sum('attr_value'))
    pre_url = request.META.get("HTTP_REFERER")
    try:
        analiza = models.MarketAnalysis.objects.filter(ref_no=valuation).latest('id')
    except:
        analiza = None 

    if request.method == "POST":
        if analiza:
            form = forms.MarketAnalysisForm(request.POST, instance=analiza)
        else:
            form = forms.MarketAnalysisForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.ref_no = valuation
            data.dps = form.cleaned_data.get('dps') if request.POST.get('show_dps') == '1' else None 
            data.ac = form.cleaned_data.get('ac') if request.POST.get('show_ac') == '1' else None
            data.ac_optional = request.POST.get('ac_opt') if request.POST.get('ac_opt_check') == 'on' else None
            data.af = form.cleaned_data.get('ac') if request.POST.get('show_af') == '1' else None 
            data.spi = form.cleaned_data.get('ac') if request.POST.get('show_spi') == '1' else None 
            data.forecast = form.cleaned_data.get('ac') if request.POST.get('show_forecast') == '1' else None 
            data.save()

            if request.POST.get('pre_url') == 'details':
                return redirect('dashboard:details', id=id)
            else:
                return redirect('valuation:select_comparable', id=id)
    else:
        if analiza:
            form = forms.MarketAnalysisForm(instance=analiza)
        else:
            form = forms.MarketAnalysisForm()

    context = {
        'valuation': valuation,
        'camara': camara['camara'],
        'form': form,
        'segment': 'market',
        'pre_url': pre_url,
        'analiza': analiza,
    }
    return render(request, template, context)


# =====================================================================
# =================== search and select comparable ====================
# =====================================================================
@login_required(login_url='/signin/')
def select_comparable(request, id):
    template = 'valuation/select_comparable.html'
    valuation = get_object_or_404(models.ValuatedProperty, id=id)
    comp_table = models.ComparableTable.objects.filter(ref_no=valuation).exclude(name=None)
    mvb_table = models.MvbTable.objects.filter(ref_no=valuation, sub_rent_sqm=None)

    if request.method == 'POST':
        comp = request.POST.get('comparable') 
        remove = request.POST.get('remove')
        nr_comp = request.POST.get('nr_comapratii')
        if comp_table:
            comp_del = comp_table.filter(comparable__id__in=ast.literal_eval(remove)).delete()
            mvb_del = mvb_table.filter(cp__id__in=ast.literal_eval(remove)).delete()
            return redirect(reverse('valuation:edit_comparable', args=[id])+'?comp='+str(comp)+'&nr_comp='+str(nr_comp))
        else:
            return redirect(reverse('valuation:add_comparable', args=[id])+'?comp='+str(comp)+'&nr_comp='+str(nr_comp))
        # return redirect(reverse('valuation:add_comparable', args=[id])+'?nr_comp='+str(nr_comp))
    context = {
        'valuation': valuation,
        'segment': 'comparable',
        'comp_table': comp_table,
    }
    return render(request, template, context)

@login_required(login_url='/signin/')
def search_comparable(request):
    location = request.GET.get('location')
    radius = request.GET.get('radius')
    vid = request.GET.get('vid') 
    comp_table = models.ComparableTable.objects.filter(ref_no__id=vid).values_list('comparable__id', flat=True)
    if comp_table:
        comparable = models.ComparableProperty.objects.filter(lc__icontains=location, is_comparable=1).exclude(id__in=list(comp_table)).values_list('id', 'lc', 'area', 'camara', 'cy')
    else:
        comparable = models.ComparableProperty.objects.filter(lc__icontains=location, is_comparable=1).values_list('id', 'lc', 'area', 'camara', 'cy')
    return JsonResponse({'comparable': list(comparable)})


# ========================================================
# =================== add comparable =====================
# ========================================================
@login_required(login_url='/signin/')
def add_comparable(request, id):
    valuation = get_object_or_404(models.ValuatedProperty, id=id) 
    if not request.GET.get('comp') or not request.GET.get('nr_comp'):
        return redirect('valuation:select_comparable', id=id)
    comp = ast.literal_eval(request.GET.get('comp'))
    nr_comp = request.GET.get('nr_comp')
    comparable = models.ComparableProperty.objects.filter(id__in=comp)
    template = 'valuation/add_comparable.html'
    
    pre_url = 'details' if request.GET.get('page') else None
    mobila = models.MobilaType.objects.all()
    prop_rights = models.PropertyRightType.objects.all()
    comp_type = models.CompartmentType.objects.all()
    finish_type = models.FinishType.objects.all()
    heating = models.HeatingSystem.objects.all()
    try:
        const = models.Construction.objects.filter(ref_no__id=id).latest('id')
    except:
        const = None
    letters = string.ascii_uppercase
    msg = None

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
        sub_camara = request.POST.get('sub_camara')
        camara = request.POST.getlist('camara[]')
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
        
        opt1_name = request.POST.get('opt1_name')
        sub_opt1_val = request.POST.get('sub_opt1_val')
        opt1_val = request.POST.getlist('opt1_val[]')
        opt2_name = request.POST.get('opt2_name')
        sub_opt2_val = request.POST.get('sub_opt2_val')
        opt2_val = request.POST.getlist('opt2_val[]')
        opt3_name = request.POST.get('opt3_name')
        sub_opt3_val = request.POST.get('sub_opt3_val')
        opt3_val = request.POST.getlist('opt3_val[]')

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
        
        sub_prop = models.ComparableProperty.objects.create(ref_no=valuation, is_comparable=0, ad=sub_avdata, pr=sub_pr, fc=sub_fc, sc=sub_sc, ape=sub_ape, me=sub_me,lc=sub_location, cp=sub_cp, cy=sub_cy, camara=sub_camara, area=subarea, finish=sub_finish, etaj=sub_etaj, balcon=subbalcon, hs=sub_hs)

        # add sub_prop to comparable table 
        models.ComparableTable.objects.create(ref_no=valuation, comparable=sub_prop, sub_ad=sub_avdata, sub_pr=sub_pr, sub_fc=sub_fc, sub_sc=sub_sc, sub_ape=sub_ape, sub_me=sub_me, sub_lc=sub_location, sub_cp=sub_cp, sub_cy=sub_cy, sub_area=subarea, sub_finish=sub_finish, sub_etaj=sub_etaj, sub_balcon=subbalcon, sub_hs=sub_hs, price_persqm=price_persqm,  opt1_name=opt1_name, sub_opt1=sub_opt1_val, opt2_name=opt2_name, sub_opt2=sub_opt2_val, opt3_name=opt3_name, sub_opt3=sub_opt3_val, motivation=motivation, pr_motivation=pr_motivation, fc_motivation=fc_motivation, sc_motivation=sc_motivation, ape_motivation=ape_motivation, me_motivation=me_motivation, lc_motivation=lc_motivation, cp_motivation=cp_motivation, cy_motivation=cy_motivation, su_motivation=su_motivation, finish_motivation=finish_motivation, etaj_motivation=etaj_motivation, balcon_motivation=balcon_motivation, hs_motivation=hs_motivation, opt1_motivation=opt1_motivation, opt2_motivation=opt2_motivation, opt3_motivation=opt3_motivation, estimated_value=estimated_value, smallest_gross=smallest_gross)

        comp_list = []
        if comparable:
            comp_list = list(comparable)  
            if len(comparable) != int(nr_comp):
                for i in range(len(comparable), int(nr_comp)):
                    prop = models.ComparableProperty.objects.create(sale_price=sale_price[i], mobila=mobila[i], ma=ma[i], parking_boxa=parking_boxa[i], pba=pba[i], ad=ad[i], pr=pr[i], fc=fc[i], sc=sc[i], ape=ape[i], me=me[i],lc=lc[i], cp=cp[i], cy=cy[i], camara=camara[i], area=area[i], finish=finish[i], etaj=etaj[i], balcon=balcon[i], hs=hs[i])
                    comp_list.append(prop)
        else:
            for i in range(int(nr_comp)):
                prop = models.ComparableProperty.objects.create(sale_price=sale_price[i], mobila=mobila[i], ma=ma[i], parking_boxa=parking_boxa[i], pba=pba[i], ad=ad[i], pr=pr[i], fc=fc[i], sc=sc[i], ape=ape[i], me=me[i],lc=lc[i], cp=cp[i], cy=cy[i], area=area[i], finish=finish[i], etaj=etaj[i], balcon=balcon[i], hs=hs[i])
                comp_list.append(prop)
        s = 0
        for cl in comp_list:
            models.ComparableTable.objects.create(ref_no=valuation, comparable=cl, name=letters[s], sale_price=sale_price[s], mobila=mobila[s], ma=ma[s], parking_boxa=parking_boxa[s], pba=pba[s], op=op[s], ad=ad[s], margin=margin[s], cv=cv[s], mp=mp[s], pr=pr[s], pr_percent=pr_percent[s], pr_euro=pr_euro[s], pr_price=pr_price[s], fc=fc[s], fc_percent=fc_percent[s], fc_euro=fc_euro[s], fc_price=fc_price[s], sc=sc[s], sc_percent=sc_percent[s], sc_euro=sc_euro[s], sc_price=sc_price[s], ape=ape[s], ape_percent=ape_percent[s], ape_euro=ape_euro[s], ape_price=ape_price[s], me=me[s], me_percent=me_percent[s], me_euro=me_euro[s], me_price=me_price[s], lc=lc[s], lc_percent=lc_percent[s], lc_euro=lc_euro[s], cp=cp[s], cp_percent=cp_percent[s], cp_euro=cp_euro[s], cy=cy[s], cy_percent=cy_percent[s], cy_euro=cy_euro[s], area=area[s], su_diff=su_diff[s], su_percent=su_percent[s], su_euro=su_euro[s], finish=finish[s], finish_percent=finish_percent[s], finish_euro=finish_euro[s], etaj=etaj[s], etaj_percent=etaj_percent[s], etaj_euro=etaj_euro[s], balcon=balcon[s], balcon_percent=balcon_percent[s], balcon_euro=balcon_euro[s], hs=hs[s], hs_percent=hs_percent[s], hs_euro=hs_euro[s], opt1_val=opt1_val[s], opt1_percent=opt1_percent[s], opt1_euro=opt1_euro[s], opt2_val=opt2_val[s], opt2_percent=opt2_percent[s], opt2_euro=opt2_euro[s], opt3_val=opt3_val[s], opt3_percent=opt3_percent[s], opt3_euro=opt3_euro[s], net_adjustment=net_adjustment[s], adjustment_price=adjustment_price[s], adjustment_no=adjustment_no[s], total_percent=total_percent[s], total_euro=total_euro[s], gross_percent=gross_percent[s], gross_euro=gross_euro[s])
            s+=1

        # mvb table creation 
        sub_rent_sqm = request.POST.get('sub_rent_sqm')
        sub_monthly_rent = request.POST.get('sub_monthly_rent')
        sub_vbp = request.POST.get('sub_vbp')
        vpcd = request.POST.get('vpcd')
        vpcd_rotund = request.POST.get('vpcd_rotund')
        monthly_rent = request.POST.getlist('monthly_rent[]')
        rent_sqm = request.POST.getlist('rent_sqm[]')
        vbp = request.POST.getlist('mvb_vbp[]')
        mvbp = request.POST.getlist('mvb_mvbp[]')
        min_mvbp = request.POST.get('mvb_min')
        
        mvbtbl = models.MvbTable.objects.create(ref_no=valuation, cp=sub_prop, sub_rent_sqm=sub_rent_sqm, sub_monthly_rent=sub_monthly_rent, sub_vbp=sub_vbp, vpcd=vpcd, vpcd_rotund=vpcd_rotund, min_mvbp=min_mvbp)
        
        for j in range(len(comp_list)):
            mvb_tbl = models.MvbTable.objects.create(ref_no=valuation, cp=comp_list[j], monthly_rent=monthly_rent[j], rent_sqm=rent_sqm[j], vbp=vbp[j], mvbp=mvbp[j])

        if request.POST.get('pre_url') == 'details':
            return redirect('dashboard:details', id=id)
        else:
            return redirect('valuation:add_anexa1', id=id)
            
    context = {
        'valuation': valuation,
        'comparable': comparable,
        'nr_comp': int(nr_comp),
        'mobila': mobila,
        'prop_rights': prop_rights,
        'comp_type': comp_type,
        'finish_type': finish_type,
        'heating': heating,
        'const': const,
        'msg': msg,
        'pre_url': pre_url,
        'segment': 'comparable',
        'letters': letters,
    }
    return render(request, template, context)

@login_required(login_url='/signin/')
def edit_comparable(request, id):
    valuation = get_object_or_404(models.ValuatedProperty, id=id)
    comp_table = models.ComparableTable.objects.filter(ref_no=valuation).exclude(name=None)
    try:
        sub_mvb = models.MvbTable.objects.filter(ref_no=valuation, monthly_rent=None).latest('id')
    except:
        sub_mvb = None
    comp_mvb = models.MvbTable.objects.filter(ref_no=valuation, sub_rent_sqm=None)
    comp = ast.literal_eval(request.GET.get('comp'))
    nr_comp = request.GET.get('nr_comp')
    comparable = models.ComparableProperty.objects.filter(id__in=comp)
    try:
        sub_comp = models.ComparableTable.objects.filter(ref_no=valuation, name=None).latest('id')
    except:
        sub_comp = None
    template = 'valuation/edit_comparable.html'
    
    pre_url = 'details' if request.GET.get('page') else None
    mobila = models.MobilaType.objects.all()
    prop_rights = models.PropertyRightType.objects.all()
    comp_type = models.CompartmentType.objects.all()
    finish_type = models.FinishType.objects.all()
    heating = models.HeatingSystem.objects.all()
    try:
        const = models.Construction.objects.filter(ref_no__id=id).latest('id')
    except:
        const = None
    letters = string.ascii_uppercase
    msg = None

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
        sub_camara = request.POST.get('sub_camara')
        camara = request.POST.getlist('camara[]')
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
        
        opt1_name = request.POST.get('opt1_name')
        sub_opt1_val = request.POST.get('sub_opt1_val')
        opt1_val = request.POST.getlist('opt1_val[]')
        opt2_name = request.POST.get('opt2_name')
        sub_opt2_val = request.POST.get('sub_opt2_val')
        opt2_val = request.POST.getlist('opt2_val[]')
        opt3_name = request.POST.get('opt3_name')
        sub_opt3_val = request.POST.get('sub_opt3_val')
        opt3_val = request.POST.getlist('opt3_val[]')

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
        
        sub_prop = models.ComparableTable.objects.filter(ref_no=valuation, name=None).update(sub_ad=sub_avdata, sub_pr=sub_pr, sub_fc=sub_fc, sub_sc=sub_sc, sub_ape=sub_ape, sub_me=sub_me, sub_lc=sub_location, sub_cp=sub_cp, sub_cy=sub_cy, sub_area=subarea, sub_finish=sub_finish, sub_etaj=sub_etaj, sub_balcon=subbalcon, sub_hs=sub_hs, price_persqm=price_persqm,  opt1_name=opt1_name, sub_opt1=sub_opt1_val, opt2_name=opt2_name, sub_opt2=sub_opt2_val, opt3_name=opt3_name, sub_opt3=sub_opt3_val, motivation=motivation, pr_motivation=pr_motivation, fc_motivation=fc_motivation, sc_motivation=sc_motivation, ape_motivation=ape_motivation, me_motivation=me_motivation, lc_motivation=lc_motivation, cp_motivation=cp_motivation, cy_motivation=cy_motivation, su_motivation=su_motivation, finish_motivation=finish_motivation, etaj_motivation=etaj_motivation, balcon_motivation=balcon_motivation, hs_motivation=hs_motivation, opt1_motivation=opt1_motivation, opt2_motivation=opt2_motivation, opt3_motivation=opt3_motivation, estimated_value=estimated_value, smallest_gross=smallest_gross)

        # update old comparable:
        k = 0
        for ot in comp_table:
            models.ComparableTable.objects.filter(id=ot.id).update(sale_price=sale_price[k], mobila=mobila[k], ma=ma[k], parking_boxa=parking_boxa[k], pba=pba[k], op=op[k], ad=ad[k], margin=margin[k], cv=cv[k], mp=mp[k], pr=pr[k], pr_percent=pr_percent[k], pr_euro=pr_euro[k], pr_price=pr_price[k], fc=fc[k], fc_percent=fc_percent[k], fc_euro=fc_euro[k], fc_price=fc_price[k], sc=sc[k], sc_percent=sc_percent[k], sc_euro=sc_euro[k], sc_price=sc_price[k], ape=ape[k], ape_percent=ape_percent[k], ape_euro=ape_euro[k], ape_price=ape_price[k], me=me[k], me_percent=me_percent[k], me_euro=me_euro[k], me_price=me_price[k], lc=lc[k], lc_percent=lc_percent[k], lc_euro=lc_euro[k], cp=cp[k], cp_percent=cp_percent[k], cp_euro=cp_euro[k], cy=cy[k], cy_percent=cy_percent[k], cy_euro=cy_euro[k], area=area[k], su_diff=su_diff[k], su_percent=su_percent[k], su_euro=su_euro[k], finish=finish[k], finish_percent=finish_percent[k], finish_euro=finish_euro[k], etaj=etaj[k], etaj_percent=etaj_percent[k], etaj_euro=etaj_euro[k], balcon=balcon[k], balcon_percent=balcon_percent[k], balcon_euro=balcon_euro[k], hs=hs[k], hs_percent=hs_percent[k], hs_euro=hs_euro[k], opt1_val=opt1_val[k], opt1_percent=opt1_percent[k], opt1_euro=opt1_euro[k], opt2_val=opt2_val[k], opt2_percent=opt2_percent[k], opt2_euro=opt2_euro[k], opt3_val=opt3_val[k], opt3_percent=opt3_percent[k], opt3_euro=opt3_euro[k], net_adjustment=net_adjustment[k], adjustment_price=adjustment_price[k], adjustment_no=adjustment_no[k], total_percent=total_percent[k], total_euro=total_euro[k], gross_percent=gross_percent[k], gross_euro=gross_euro[k])
            k+=1

        comp_list = []
        if comparable:
            comp_list = list(comparable)

        if (len(comp_table) + len(comparable)) != int(nr_comp):
            for i in range(k+len(comparable), int(nr_comp)):
                prop = models.ComparableProperty.objects.create(sale_price=sale_price[i], mobila=mobila[i], ma=ma[i], parking_boxa=parking_boxa[i], pba=pba[i], ad=ad[i], pr=pr[i], fc=fc[i], sc=sc[i], ape=ape[i], me=me[i],lc=lc[i], cp=cp[i], cy=cy[i], camara=camara[i], area=area[i], finish=finish[i], etaj=etaj[i], balcon=balcon[i], hs=hs[i])
                comp_list.append(prop)

        for cl in comp_list:
            models.ComparableTable.objects.create(ref_no=valuation, comparable=cl, name=letters[k], sale_price=sale_price[k], mobila=mobila[k], ma=ma[k], parking_boxa=parking_boxa[k], pba=pba[k], op=op[k], ad=ad[k], margin=margin[k], cv=cv[k], mp=mp[k], pr=pr[k], pr_percent=pr_percent[k], pr_euro=pr_euro[k], pr_price=pr_price[k], fc=fc[k], fc_percent=fc_percent[k], fc_euro=fc_euro[k], fc_price=fc_price[k], sc=sc[k], sc_percent=sc_percent[k], sc_euro=sc_euro[k], sc_price=sc_price[k], ape=ape[k], ape_percent=ape_percent[k], ape_euro=ape_euro[k], ape_price=ape_price[k], me=me[k], me_percent=me_percent[k], me_euro=me_euro[k], me_price=me_price[k], lc=lc[k], lc_percent=lc_percent[k], lc_euro=lc_euro[k], cp=cp[k], cp_percent=cp_percent[k], cp_euro=cp_euro[k], cy=cy[k], cy_percent=cy_percent[k], cy_euro=cy_euro[k], area=area[k], su_diff=su_diff[k], su_percent=su_percent[k], su_euro=su_euro[k], finish=finish[k], finish_percent=finish_percent[k], finish_euro=finish_euro[k], etaj=etaj[k], etaj_percent=etaj_percent[k], etaj_euro=etaj_euro[k], balcon=balcon[k], balcon_percent=balcon_percent[k], balcon_euro=balcon_euro[k], hs=hs[k], hs_percent=hs_percent[k], hs_euro=hs_euro[k], opt1_val=opt1_val[k], opt1_percent=opt1_percent[k], opt1_euro=opt1_euro[k], opt2_val=opt2_val[k], opt2_percent=opt2_percent[k], opt2_euro=opt2_euro[k], opt3_val=opt3_val[k], opt3_percent=opt3_percent[k], opt3_euro=opt3_euro[k], net_adjustment=net_adjustment[k], adjustment_price=adjustment_price[k], adjustment_no=adjustment_no[k], total_percent=total_percent[k], total_euro=total_euro[k], gross_percent=gross_percent[k], gross_euro=gross_euro[k])
            k+=1

        # mvb table creation 
        sub_rent_sqm = request.POST.get('sub_rent_sqm')
        sub_monthly_rent = request.POST.get('sub_monthly_rent')
        sub_vbp = request.POST.get('sub_vbp')
        vpcd = request.POST.get('vpcd')
        vpcd_rotund = request.POST.get('vpcd_rotund')
        monthly_rent = request.POST.getlist('monthly_rent[]')
        rent_sqm = request.POST.getlist('rent_sqm[]')
        vbp = request.POST.getlist('mvb_vbp[]')
        mvbp = request.POST.getlist('mvb_mvbp[]')
        min_mvbp = request.POST.get('mvb_min')
        
        sub_mvb.sub_rent_sqm=sub_rent_sqm
        sub_mvb.sub_monthly_rent=sub_monthly_rent
        sub_mvb.sub_vbp=sub_vbp
        sub_mvb.vpcd=vpcd
        sub_mvb.vpcd_rotund=vpcd_rotund
        sub_mvb.min_mvbp=min_mvbp
        sub_mvb.save()

        z = 0
        for cmv in comp_mvb:
            models.MvbTable.objects.filter(id=cmv.id).update(monthly_rent=monthly_rent[z], rent_sqm=rent_sqm[z], vbp=vbp[z], mvbp=mvbp[z])
            z+=1
        
        for m in comp_list:
            models.MvbTable.objects.create(ref_no=valuation, cp=m, monthly_rent=monthly_rent[z], rent_sqm=rent_sqm[z], vbp=vbp[z], mvbp=mvbp[z])
            z+=1

        if request.POST.get('pre_url') == 'details':
            return redirect('dashboard:details', id=id)
        else:
            return redirect('valuation:add_anexa1', id=id)
            
    context = {
        'valuation': valuation,
        'comp_table': comp_table,
        'sub_mvb': sub_mvb,
        'comp_mvb': comp_mvb,
        'comparable': comparable,
        'sub_comp': sub_comp,
        'comb_len': len(comp_table) + len(comparable),
        'len': int(nr_comp) - (len(comp_table) + len(comparable)),
        'nr_comp': int(nr_comp),
        'mobila': mobila,
        'prop_rights': prop_rights,
        'comp_type': comp_type,
        'finish_type': finish_type,
        'heating': heating,
        'const': const,
        'msg': msg,
        'pre_url': pre_url,
        'segment': 'comparable',
        'letters': letters,
    }
    return render(request, template, context)

# ==========================================================
# ====================== anexa data ========================
# ==========================================================
#milton
from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile
import random
import pyautogui 
from django.conf import settings
from django.db.models import Q
from pathlib import Path
import os
@login_required(login_url='/signin/')
def add_anexa1(request, id):
    template_name = 'valuation/add_anexa1.html'
    valuation = get_object_or_404(models.ValuatedProperty, id=id)
        
    if request.method == 'POST':
        img_id = json.loads(request.POST['image'])
        print(img_id)
        for img in img_id:
            ss = models.ScreenShot.objects.get(name=str(img))
            anexa1 = models.Anexa1.objects.create(ref_no=valuation,image=ss.image)

        response = {'status': 1, 'message': "ok"}
        return JsonResponse(response, safe=False)

    context = {
        'segment': 'anexa1',
        "valuation": valuation,
    }

    return render(request, template_name, context)

@login_required(login_url='/signin/')
def add_anexa2(request, id):
    template_name = 'valuation/add_anexa2.html'
    
    valuation = get_object_or_404(models.ValuatedProperty, id=id)
    comparable_table = get_object_or_404(models.ComparableTable, ref_no=valuation)
    
    # converting "[*,*,*,..]" text value to tuple for query
    s = "".join(comparable_table.comparable.split())
    s = s.replace(']', '')
    s = s.replace('[', '')
    table_set = s.split(',')

    comparable_propertys = models.ComparableProperty.objects.filter(id__in=table_set)

    if request.method=="POST":
        
        pid = json.loads(request.POST["pid"])
        if pid!=-1:
            # files in each form
            comparable_property = models.ComparableProperty.objects.get(id=request.POST["pid"])
            files = [request.FILES.get('file[%d]' % i) for i in range(0, len(request.FILES))]
            i = 0
            while i<len(files):
                anexa2 = models.Anexa2.objects.create(ref_no=valuation, compare_no=comparable_property, file = files[i])
                i+=1
        else:
            # data in each form
            form_data = json.loads(request.POST["formData"])
            for key, value in form_data.items():
                comparable_property = models.ComparableProperty.objects.get(id=key)
                print(models.Anexa2.objects.filter(ref_no=valuation, compare_no=comparable_property).all())
                if models.Anexa2.objects.filter(ref_no=valuation, compare_no=comparable_property).exists():
                    for m in models.Anexa2.objects.filter(ref_no=valuation, compare_no=comparable_property).all():
                        m.link=value[0]
                        m.optional_text=value[1]
                        m.save()
                else:
                    anexa2 = models.Anexa2.objects.create(ref_no=valuation, compare_no=comparable_property)
                    anexa2.link=value[0]
                    anexa2.optional_text=value[1]
                    anexa2.save()

            response = {'status': 1, 'message': "ok"}
            return JsonResponse(response, safe=False)

    context = {
        'segment': 'anexa2',
        "valuation":valuation,
        "comparable_propertys":comparable_propertys,
    }

    return render(request, template_name, context)

@login_required(login_url='/signin/')
def add_anexa3(request, id):
    template_name = 'valuation/add_anexa3.html'
    valuation = get_object_or_404(models.ValuatedProperty,id=id)
    anexa3 = models.Anexa3.objects.filter(ref_no = valuation)

    if request.method == 'POST':
        img_id = json.loads(request.POST['image'])

        for img_url in anexa3:
            if img_url.image.url not in img_id:
                obj = models.Anexa3.objects.get(ref_no=valuation, image = img_url.image)
                obj.delete()
                print("delete")

        response = {'status': 1, 'message': "ok"}
        return JsonResponse(response, safe=False)

    context = {
        'segment': 'anexa3',
        "valuation": valuation,
        "objects": anexa3,
    }

    return render(request, template_name, context)

@login_required(login_url='/signin/')
def add_anexa4(request, id):
    template_name = 'valuation/add_anexa4.html'
    valuation = get_object_or_404(models.ValuatedProperty, id=id)

    if request.method == 'POST':
        files = [request.FILES.get('file[%d]' % i) for i in range(0, len(request.FILES))]
        i = 0
        while i<len(files):
            anexa1 = models.Anexa4.objects.create(ref_no=valuation, file = files[i])
            i+=1
        return redirect('dashboard:details', id=id)
        
    context = {
        'segment': 'anexa4',
        "valuation": valuation,
    }
    return render(request, template_name, context)

import datetime
now = datetime.datetime.now()
import time

def delete_file(request):
    class_name = request.POST.get("class_name")
    file_name = request.POST.get("file_name")
    valuated_id = request.POST.get("valuated_id")

    # year month day of today
    strings = time.strftime("%Y,%m,%d,%H,%M,%S")
    t = strings.split(',')
    numbers = [ str(x) for x in t ]

    s = class_name +"/"+numbers[0]+"/"+numbers[1]+"/"+numbers[2] + "/" + file_name.replace(' ', '_')

    # file delete
    if os.path.isfile("media/"+s):
        p = os.remove("media/"+s)
        print("paise")
    else:
        print("nai")

    # delete object
    valuation = get_object_or_404(models.ValuatedProperty, id=valuated_id)
    if class_name=="anexa1":
        obj = models.Anexa1.objects.filter(ref_no=valuation, file=s)
    elif class_name=="anexa2":
        obj = models.Anexa2.objects.filter(ref_no=valuation, file=s)
    elif class_name=="anexa4":
        obj = models.Anexa4.objects.filter(ref_no=valuation, file=s)
    
    obj.delete()

    return HttpResponse("success")

from valuation.utils import get_image_from_data_url
def screenshot_html(request):
    class_name = request.POST.get('class_name')
    valuated_id = request.POST.get('valuated_id') 
    blob = request.POST.get('screenshot_blob')

    img = f'myimg{random.randint(1000,9999)}.png'    
    image = get_image_from_data_url(blob)[0]
    # saving the image to model
    p = models.ScreenShot.objects.create(name=img, image=image)
    p.name = str(p.image.url).split('/')[-1]
    p.save()

    msg = "Screenshot has been taken!"
    response = {
        "msg":msg, 
        "objects": '/media/'+str(p.image),
    }

    return JsonResponse(response)


# ========================== edit initial form ============================
# =========================================================================
@login_required(login_url='/signin/')
def edit_initial_data(request, id):
    template = 'valuation/edit_initial_form.html'
    valuation = get_object_or_404(models.ValuatedProperty, id=id)
    msg = None
    areas = models.Area.objects.all()
    compartments = models.Compartimentare.objects.filter(property_type__id=1)
    rooms = models.CompartimentareValue.objects.filter(ref_no=valuation)
    customs = models.CustomFieldValue.objects.filter(ref_no=valuation)
    camara = models.CompartimentareValue.objects.filter(ref_no=valuation,attr_id__pk__in=[1,3,4]).aggregate(camara=Sum('attr_value'))
    pre_url = request.META.get("HTTP_REFERER")

    if request.method == 'POST':
        form = forms.EditInitialForm(request.POST, instance=valuation)
        if form.is_valid():
            data = form.save(commit=False)
            data.assigned_to = request.user.get_full_name()
            data.valuation_date = parse_date(request.POST.get('valuation_date'))
            data.report_date = parse_date(request.POST.get('report_date'))
            data.save()

            # save compartimentare 
            compart = request.POST.getlist('compart[]')
            i = 0
            for c in rooms:
                c.attr_value=compart[i]
                c.save()
                i += 1
            
            # save custom field 
            cname = request.POST.getlist('cf_name_yes[]')
            cvalue = request.POST.getlist('cf_value_yes[]')
            cf_name = request.POST.getlist('cf_name[]')
            cf_value = request.POST.getlist('cf_value[]')
            j = 0
            for custom in customs:
                custom.attr_name = cname[j]
                custom.attr_value = cvalue[j]
                custom.save()
                j += 1
            k=0
            for cf in cf_name:
                if cf_value[k] != '0':
                    cf_res = models.CustomFieldValue.objects.create(ref_no=data, attr_name=cf, attr_value=cf_value[k])
                k += 1
            if request.POST.get('pre_url') == 'details':
                return redirect('dashboard:details', id=data.id)
            else:
                return redirect('valuation:add_summary', id=data.id)
        else:
            print('invalid')
    else:
        form = forms.EditInitialForm(instance=valuation)

    context = {
        'msg': msg,
        'areas': areas,
        'segment': 'initial',
        'form': form,
        'valuation': valuation,
        'rooms': rooms,
        'customs': customs, 
        'camara': camara,
        'compartments': compartments,
        'pre_url': pre_url,
    }
    return render(request, template, context)

@login_required(login_url='/signin/')
def delete_custom_field(request):
    id = request.GET.get('id')
    cf = get_object_or_404(models.CustomFieldValue, id=id)
    try:
        response = cf.delete()
        if response:
            return JsonResponse({'success': 'true'})
    except:
        return JsonResponse({'success': 'false'})


# ==================== manage photos reorder & delete ======================
# ==========================================================================
@login_required(login_url='/signin/')
def reorder_photos(request):
    if request.method == 'POST':
        imageIds = request.POST.get('ids')
        ids = imageIds.split(',')
        i = 1
        for id in ids:
            cover = get_object_or_404(models.Photo, id=id)
            cover.image_order = i
            cover.save()
            i+=1
        return JsonResponse({'response': 'true'})
    return JsonResponse({'response': 'false'})

@login_required(login_url='/signin/')
def delete_photos(request):
    id = request.GET.get('id')
    photo = get_object_or_404(models.Photo, id=id)
    try:
        response = 1 #photo.delete()
        if response:
            return JsonResponse({'success': 'true'})
    except:
        return JsonResponse({'success': 'false'})


# =========================== delete suprafete =============================
# ==========================================================================
@login_required(login_url='/signin/')
def delete_suprafete(request):
    id = request.GET.get('id')
    print(id)
    suprafete = get_object_or_404(models.Suprafete, id=id)
    try:
        response = suprafete.delete()
        if response:
            return JsonResponse({'success': 'true'})
    except:
        return JsonResponse({'success': 'false'})


# ============================= manage sources =============================
# ==========================================================================
@login_required(login_url='/signin/')
def update_sources(request):
    if request.method == 'POST':
        ids = request.POST.getlist('ids[]')
        sources = request.POST.getlist('sources[]')
        valuation = get_object_or_404(models.ValuatedProperty, id=request.POST.get('ref_no'))
        res_id = []
        for id, source in zip(ids, sources):
            if id == '0':
                res = models.SourceofInformation.objects.create(ref_no=valuation,source=source)
                if res:
                    res_id.append(res.id)
            else: 
                res_id.append(id)
                res = models.SourceofInformation.objects.filter(id=id).update(source=source)
        if res_id:
            return JsonResponse({'success': 'true', 'res_id': json.dumps(res_id)})
        else:
            return JsonResponse({'success': 'false'})
    return JsonResponse({'success': 'false'})

@login_required(login_url='/signin/')
def delete_source(request):
    id = request.GET.get('id')
    source = get_object_or_404(models.SourceofInformation, id=id)
    try:
        response = source.delete()
        if response:
            return JsonResponse({'success': 'true'})
    except:
        return JsonResponse({'success': 'false'})


# ==================== manage photos reorder & delete ======================
# ==========================================================================
@login_required(login_url='/signin/')
def add_comp_prop(request):
    template = 'valuation/add_comp_property.html'
    mobila = models.MobilaType.objects.all()
    prop_rights = models.PropertyRightType.objects.all()
    comp_type = models.CompartmentType.objects.all()
    finish_type = models.FinishType.objects.all()
    heating = models.HeatingSystem.objects.all()

    if request.method == 'POST':
        form = forms.ComparableForm(request.POST)
        if form.is_valid():
            form.save()
            request.session['comp_added'] = True
            return redirect('dashboard:comparable_list')
    else:
        form = forms.ComparableForm()

    context = {
        'segment': 'comparable',
        'mobila': mobila,
        'prop_rights': prop_rights,
        'comp_type': comp_type,
        'finish_type': finish_type,
        'heating': heating,
        'form': form,
    }
    return render(request, template, context)

@login_required(login_url='/signin/')
def comp_prop_details(request, id):
    template = 'valuation/add_comp_property.html'
    instance = get_object_or_404(models.ComparableProperty, id=id)
    mobila = models.MobilaType.objects.all()
    prop_rights = models.PropertyRightType.objects.all()
    comp_type = models.CompartmentType.objects.all()
    finish_type = models.FinishType.objects.all()
    heating = models.HeatingSystem.objects.all()

    if request.method == 'POST':
        form = forms.ComparableForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            request.session['comp_added'] = True
            return redirect('dashboard:comparable_list')
    else:
        form = forms.ComparableForm(instance=instance)

    context = {
        'segment': 'comparable',
        'instance': instance,
        'mobila': mobila,
        'prop_rights': prop_rights,
        'comp_type': comp_type,
        'finish_type': finish_type,
        'heating': heating,
        'form': form,
    }
    return render(request, template, context)


def test(request):
    return render(request, 'valuation/test.html')