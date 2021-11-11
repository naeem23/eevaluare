import ast
import math
import re
import string
from decimal import Decimal
from django import template
from django.db.models import Sum
from valuation import models
from valuation import choices
register = template.Library()

@register.filter(name='myrange')
def myrange(number):
    return range(1, int(number)+1)


@register.filter(name='list_range')
def list_range(n):
    return range(n)


@register.filter(name='get_extra_length')
def get_extra_length(comp, n):
    return range(len(comp)+1, n+1)


@register.filter(name='covertlist')
def covertlist(str):
    return str.split(',')


@register.filter(name='speciallist')
def speciallist(str):
    data = re.sub(r"[' ]", '', str)
    return data[1:-1].split(',')


@register.filter(name='get_public_transport')
def get_public_transport(str):
    data = ast.literal_eval(str)
    transport = models.Transport.objects.filter(id__in=data)
    return transport

@register.filter(name='get_identification')
def get_identification(str):
    data = ast.literal_eval(str)
    iden = choices.IDENTIFICATION_CHOICE
    if len(data) == 2:
        identification = iden[0][1] + " si " + iden[1][1]
    else:
        if data[0] == iden[0][0]:
            identification = iden[0][1]
        else:
            identification = iden[1][1]
    return identification

@register.filter(name="in_list")
def in_list(var, the_list):
    return any(val in var for val in the_list)


@register.filter(name="sub")
def sub(var1, var2):
    if var1 != None and var2 != None and var1 > var2:
        return var1 - var2 
    elif var1 != None and var2 != None and var2 > var1:
        return var2 - var1 
    

@register.filter(name="tip_parcare")
def tip_parcare(parking):
    p_list = []
    for p in parking:
        if p.attr_id == 7:
            p_list.append("Da " + p.attr_value + " suprateran")
        else:
            p_list.append("Da " + p.attr_value + " subteran")
    return ",".join(p_list)

# new comparatii table calculation
@register.filter(name="get_offer_price")
def get_offer_price(prop):
    return round((prop.sale_price + prop.ma + prop.pba), 0)

@register.filter(name="get_area_diff")
def get_area_diff(var1, var2):
    return round(var1-var2,2)

# get above parking no 
@register.filter(name="get_suprateran_nr")
def get_suprateran_nr(compartment):
    nr = compartment.filter(attr_id__id=9).aggregate(nr=Sum('attr_value'))
    return nr['nr']
    
# get above parking no 
@register.filter(name="get_subteran_nr")
def get_subteran_nr(compartment):
    nr = compartment.filter(attr_id__id=10).aggregate(nr=Sum('attr_value'))
    return nr['nr']
    
# get above parking no 
@register.filter(name="get_boxa_nr")
def get_boxa_nr(compartment):
    nr = compartment.filter(attr_id__id=11).aggregate(nr=Sum('attr_value'))
    return nr['nr']


# ============================ new report ===============================
# convert to list 
@register.filter(name="list_convert")
def list_convert(var):
    return ast.literal_eval(var)

# get_corresponding_letter 
@register.filter(name="get_corresponding_letter")
def get_corresponding_letter(sub_prop):
    pos = int(sub_prop.smallest_gross[-1]) - 1
    letters = string.ascii_uppercase
    return letters[pos]

# get_points of interest
@register.filter(name="get_poi")
def get_poi(pois):
    return pois.split(',')

# get_transport
@register.filter(name="get_transport")
def get_transport(pt):
    transport = models.Transport.objects.filter(id__in=ast.literal_eval(pt))
    return transport

# get_identification
@register.filter(name="get_identification")
def get_identification(iden):
    iden = ast.literal_eval(iden)
    if len(iden) > 1:
        identi = 'adresei postale inscrise pe imobil si cadastral introdus pe platforma ANCPI'
    else:
        if 'apii' in iden:
            identi = 'adresei postale inscrise pe imobil'
        else:
            identi = 'cadastral introdus pe platforma ANCPI'
    return identi

# get_resulting_value
@register.filter(name="get_resulting_value")
def get_resulting_value(obj):
    try:
        summary = models.ValuationSummary.objects.filter(ref_no=obj).latest('id')
        if summary.amav:
            value = get_market_value(summary)
        else:
            value = get_income_value(summary)
    except:
        value = 0.00
    return value
    
# get_market_value
@register.filter(name="get_market_value")
def get_market_value(summary):
    try:
        summary_value = models.SummaryValue.objects.filter(summary=summary)
        market_value = summary.amav
        for sv in summary_value:
            if sv.approache == 'market':
                market_value += sv.field_value
    except:
        market_value = 0.00
    return market_value

# get_market_value_in ron
@register.filter(name="get_market_value_ron")
def get_market_value_ron(obj, summary):
    market_val = get_market_value(summary)
    market_val = market_val * summary.fer
    return round(market_val,0)

# get_income_value
@register.filter(name="get_income_value")
def get_income_value(summary):
    try:
        summary_value = models.SummaryValue.objects.filter(summary=summary)
        income_value = summary.aiav
        for sv in summary_value:
            if sv.approache == 'income':
                income_value += sv.field_value
    except:
        income_value = 0.00
    return income_value

# get_income_value_in ron
@register.filter(name="get_income_value_ron")
def get_income_value_ron(obj, summary):
    income_val = get_income_value(summary)
    income_val = income_val * summary.fer
    return round(income_val,0)

# get_utila_totala
@register.filter(name="get_utila_totala")
def get_utila_totala(obj):
    try:
        const = models.Construction.objects.filter(ref_no=obj).latest('id')
        utila = const.utila
        totala = const.totala
    except:
        utila = 0.00
        totala = 0.00
    return str(utila) + "/" + str(totala)

# get_price_sqm
@register.filter(name="get_price_sqm")
def get_price_sqm(obj):
    try:
        summary = models.ValuationSummary.objects.filter(ref_no=obj).latest('id')
        summary_value = models.SummaryValue.objects.filter(summary=summary)
        const = models.Construction.objects.filter(ref_no=obj).latest('id')
        market_value = summary.amav if summary.amav else summary.aiav
        price1 = summary.amav if summary.amav else summary.aiav
        for sv in summary_value:
            if sv.approache == 'market':
                market_value += sv.field_value
            else:
                market_value += sv.field_value   
        price1 = round((price1/const.utila),0)
        price2 = round((market_value/const.utila),0)
        price_sqm = str(price1) + '/' + str(price2)
    except:
        price_sqm = '0.00/0.00'
    return price_sqm
