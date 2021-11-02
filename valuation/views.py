import ast
import datetime
import json
from django.utils.translation import templatize
import requests
import string
import urllib.parse
from django.contrib.auth import get_user_model
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
            data.status = models.Status.objects.get(status__icontains='progress')
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
        form = forms.AddValuationSummary(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.ref_no = valuation
            data.save()
            # data.approach.set() to-do

            # save summary value 
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
    rooms = models.CompartimentareValue.objects.filter(ref_no=valuation).exclude(utila_filter)
    customs = models.CustomFieldValue.objects.filter(ref_no=valuation)
    balcons = models.CompartimentareValue.objects.filter(ref_no=valuation, attr_id__name__icontains='balcon')
    floor_type = models.FloorType.objects.all()
    pre_url = request.META.get("HTTP_REFERER")

    if request.method == 'POST':
        form = forms.ConstructionForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.ref_no = valuation
            data.dps = form.cleaned_data.get('conform_text') if request.POST.get('show_conform') == '1' else None 
            data.ac = form.cleaned_data.get('exterior_finishes') if request.POST.get('show_ef') == '1' else None
            data.save()
            data.utilities.set(form.cleaned_data['utilities'])
            
            # create Suprafete
            nr_crt = request.POST.getlist('nr_crt[]')
            room_name = request.POST.getlist('room_name[]')
            areas = request.POST.getlist('area[]')
            is_utila = request.POST.getlist('is_utila[]')

            for n, r, a, iu in zip(nr_crt, room_name, areas, is_utila):
                models.Suprafete.objects.create(ref_no=valuation, nr_crt=n, room_name=r, area=a, is_utila=iu)
            
            if request.POST.get('pre_url') == 'details':
                return redirect('dashboard:details', id=id)
            else:
                return redirect('valuation:add_presentation', id=id)
    else:
        form = forms.ConstructionForm()

    context = {
        'valuation': valuation,
        'form': form,
        'rooms': rooms,
        'customs': customs,
        'balcons': balcons,
        'floor_type': floor_type,
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
    
    print('const ====== '+ str(const))
    pre_url = request.META.get("HTTP_REFERER")

    if request.method == 'POST':
        form = forms.PresentationForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.ref_no = valuation
            data.pt = request.POST.getlist('pt[]')
            data.legal_doc = request.POST.getlist('legal_doc[]')
            data.identification = request.POST.getlist('identification[]')
            data.save()
            if request.POST.get('pre_url') == 'details':
                return redirect('dashboard:details', id=id)
            else:
                return redirect('valuation:add_market_analysis', id=id)
    else:
        form = forms.PresentationForm()

    context = {
        'valuation': valuation,
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

    if request.method == "POST":
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
        form = forms.MarketAnalysisForm()

    context = {
        'valuation': valuation,
        'camara': camara['camara'],
        'form': form,
        'segment': 'market',
        'pre_url': pre_url,
    }
    return render(request, template, context)


# =====================================================================
# =================== search and select comparable ====================
# =====================================================================
@login_required(login_url='/signin/')
def select_comparable(request, id):
    template = 'valuation/select_comparable.html'
    valuation = get_object_or_404(models.ValuatedProperty, id=id)
    pre_url = request.META.get("HTTP_REFERER")

    if request.method == 'POST':
        comp = request.POST.getlist('comp[]')
        nr_comp = request.POST.get('nr_comapratii')

        if request.POST.get('pre_url') == 'details':
            return redirect(reverse('valuation:add_comparable', args=[id])+'?comp='+urllib.parse.quote(str(comp))+'&nr_comp='+str(nr_comp)+'?page=details')
        else:
            return redirect(reverse('valuation:add_comparable', args=[id])+'?comp='+urllib.parse.quote(str(comp))+'&nr_comp='+str(nr_comp))

    context = {
        'valuation': valuation,
        'pre_url': pre_url,
        'segment': 'comparable',
    }
    return render(request, template, context)

@login_required(login_url='/signin/')
def search_comparable(request):
    location = request.GET.get('location')
    radius = request.GET.get('radius')
    comparable = models.ComparableProperty.objects.filter(lc__icontains=location, is_comparable=1).values_list('id', 'lc', 'area', 'cy')
    return JsonResponse({'comparable': list(comparable)})


# ========================================================
# =================== add comparable =====================
# ========================================================
@login_required(login_url='/signin/')
def add_comparable(request, id):
    template = 'valuation/add_comparable.html'
    valuation = get_object_or_404(models.ValuatedProperty, id=id)
    comp = ast.literal_eval(request.GET.get('comp'))
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
    if comp:
        comparable = models.ComparableProperty.objects.filter(id__in=comp)
    else:
        comparable = None
    nr_comp = request.GET.get('nr_comp')
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
        mvb_table = models.MvbTable.objects.create(ref_no=valuation, sub_rent_sqm=sub_rent_sqm, sub_monthly_rent=sub_monthly_rent, sub_vbp=sub_vbp,vpcd=vpcd, vpcd_rotund=vpcd_rotund,monthly_rent=monthly_rent,rent_sqm=rent_sqm,vbp=vbp,mvbp=mvbp,min_mvbp=min_mvbp)
    
        if table and mvb_table:
            if request.POST.get('pre_url') == 'details':
                return redirect('dashboard:details', id=id)
            else:
                return redirect('valuation:add_anexa', id=id)
        else:
            msg = 'Something went wrong.'

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
    }
    return render(request, template, context)


# ==========================================================
# ====================== anexa data ========================
# ==========================================================
@login_required(login_url='/signin/')
def add_anexa(request, id):
    return HttpResponse('soemthing')


# =========================================================================
# ========================== edit initial form ============================
# =========================================================================



# =========================================================================
# ========================== evaluare details =============================
# =========================================================================
@login_required(login_url='/signin/')
def valuation_details(request, id):
    template = 'valuation/valuation_details.html'
    valuation = get_object_or_404(models.ValuatedProperty, id=id)
    compartments = models.CompartimentareValue.objects.filter(ref_no=valuation)
    camara = models.CompartimentareValue.objects.filter(ref_no=valuation,attr_id__pk__in=[1,3,4]).aggregate(camara=Sum('attr_value'))
    custom_fields = models.CustomFieldValue.objects.filter(ref_no=valuation)
    photos = models.Photo.objects.filter(ref_no=valuation)
    try:
        summary = models.ValuationSummary.objects.filter(ref_no=valuation).latest('id')
    except:
        summary = None 
    try:
        const = models.Construction.objects.filter(ref_no=valuation).latest('id')
    except:
        const = None 
    source = models.SourceofInformation.objects.filter(ref_no=valuation)
    try:
        presentation = models.PresentationData.objects.filter(ref_no=valuation).latest('id')
    except:
        presentation = None 
    try:
        market = models.MarketAnalysis.objects.filter(ref_no=valuation).latest('id')
    except:
        market = None 
    status = models.Status.objects.all()
    context = {
        'valuation': valuation,
        'compartments': compartments,
        'camara': camara,
        'custom_fields': custom_fields,
        'photos': photos,
        'summary': summary,
        'const': const,
        'source': source,
        'presentation': presentation,
        'market': market,
        'status': status,
    }
    return render(request, template, context)


# =========================================================================
# ===================== manage comparable properties ======================
# =========================================================================
# @login_required(login_url='/signin/')
# def add_comparable(request):
#     template = 'valuation/add_comp_property.html'
#     mobila = models.MobilaType.objects.all()
#     prop_rights = models.PropertyRightType.objects.all()
#     comp_type = models.CompartmentType.objects.all()
#     finish_type = models.FinishType.objects.all()
#     heating = models.HeatingSystem.objects.all()

#     if request.method == 'POST':
#         form = models.ComparableForm(request.POST)
#         if form.is_valid():
#             form.save()
#             request.session['comp_added'] = True
#             return redirect('dashboard:comparable_list')
#     else:
#         form = models.ComparableForm()

#     context = {
#         'segment': 'comparable',
#         'mobila': mobila,
#         'prop_rights': prop_rights,
#         'comp_type': comp_type,
#         'finish_type': finish_type,
#         'heating': heating,
#         'form': form,
#     }
#     return render(request, template, context)


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


# ==========================================================================
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
