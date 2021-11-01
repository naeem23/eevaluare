import ast
import math
import re
from decimal import Decimal
from django import template
from django.db.models import Sum
from dashboard.choices import *
from dashboard import models as db_model 
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


@register.filter(name="get_locatie")
def get_locatie(locatie):
    locatie = ast.literal_eval(locatie)
    return " ".join(locatie)


@register.filter(name="selected_choice")
def selected_choice(val, choice):
    if choice == 'FINISH_CHOICE':
        choice = dict(FINISH_CHOICE)
    elif choice == 'HEATING_CHOICE':
        choice = dict(HEATING_CHOICE)
    return choice[val]


@register.filter(name="tip_parcare")
def tip_parcare(parking):
    p_list = []
    for p in parking:
        if p.attr_id == 7:
            p_list.append("Da " + p.attr_value + " suprateran")
        else:
            p_list.append("Da " + p.attr_value + " subteran")
    return ",".join(p_list)


# ============================== comparable table data ========================== 
@register.filter(name="get_price")
def get_price(prop):
    price = prop.comparable.sale_price + prop.mobila_ajustare + prop.pb_ajustare
    return round(price,0)

@register.filter(name="get_oferta_euro")
def get_oferta_euro(prop):
    euro = (prop.comparable.sale_price * prop.margin)/100
    prop.correction_value = euro 
    prop.save()
    return round(euro,0)

@register.filter(name="get_offer_price")
def get_offer_price(prop):
    euro = prop.comparable.sale_price + prop.correction_value 
    prop.offer_price = euro 
    prop.save()
    return round(euro,0)

@register.filter(name="get_pr_euro")
def get_pr_euro(prop):
    euro = (prop.offer_price * prop.property_percent)/100
    prop.property_euro = euro 
    prop.save()
    return round(euro,0)
    
@register.filter(name="get_pr_price")
def get_pr_price(prop):
    euro = prop.offer_price + prop.property_euro
    prop.property_price = euro 
    prop.save()
    return round(euro,0)

@register.filter(name="get_fc_euro")
def get_fc_euro(prop):
    euro = (prop.property_price * prop.fc_percent)/100
    prop.fc_euro = euro 
    prop.save()
    return round(euro,0)
        
@register.filter(name="get_fc_price")
def get_fc_price(prop):
    euro = prop.property_price + prop.fc_euro
    prop.fc_price = euro 
    prop.save()
    return round(euro,0)

@register.filter(name="get_sc_euro")
def get_sc_euro(prop):
    euro = (prop.fc_price * prop.sc_percent)/100
    prop.sc_euro = euro 
    prop.save()
    return round(euro,0)
        
@register.filter(name="get_sc_price")
def get_sc_price(prop):
    euro = prop.fc_price + prop.sc_euro
    prop.sc_price = euro 
    prop.save()
    return round(euro,0)
    
@register.filter(name="get_ape_percent")
def get_ape_percent(prop):
    euro = (prop.ape_euro/prop.sc_price) * 100
    prop.ape_percent = euro 
    prop.save()
    return round(euro,0)
        
@register.filter(name="get_ape_price")
def get_ape_price(prop):
    euro = prop.sc_price + prop.ape_euro
    prop.ape_price = euro 
    prop.save()
    return round(euro,0)
    
@register.filter(name="get_me_euro")
def get_me_euro(prop):
    euro = (prop.ape_price * prop.me_percent)/100
    prop.me_euro = euro 
    prop.save()
    return round(euro,0)
        
@register.filter(name="get_me_price")
def get_me_price(prop):
    euro = prop.ape_price + prop.me_euro
    prop.me_price = euro 
    prop.save()
    return round(euro,0)
        
@register.filter(name="get_lc_euro")
def get_lc_euro(prop):
    euro = (prop.me_price * prop.lc_percent)/100
    prop.lc_euro = euro 
    prop.save()
    return round(euro,0)   

@register.filter(name="get_cp_euro")
def get_cp_euro(prop):
    euro = (prop.me_price * prop.cp_percent)/100
    prop.cp_euro = euro 
    prop.save()
    return round(euro,0) 

@register.filter(name="get_cy_euro")
def get_cy_euro(prop):
    euro = (prop.me_price * prop.cy_percent)/100
    prop.cy_euro = euro 
    prop.save()
    return round(euro,0)

@register.filter(name="area_diff")
def area_diff(var1, var2):
    return round(var1-var2,2)
       
@register.filter(name="get_su_percent")
def get_su_percent(prop, sub_area):
    euro = get_su_euro(prop, sub_area)
    euro = (euro / prop.me_price) * 100 
    prop.su_percent = euro 
    prop.save()
    return round(euro,0)
    
@register.filter(name="get_su_euro")
def get_su_euro(prop, sub_area):
    euro = ((sub_area - prop.comparable.area)/prop.comparable.area) * prop.me_price
    prop.su_euro = euro 
    prop.save()
    return round(euro,0)
        
@register.filter(name="get_finish_percent")
def get_finish_percent(prop):
    euro = (prop.finish_euro/prop.me_price) * 100
    prop.finish_percent = euro 
    prop.save()
    return round(euro,0)
    
@register.filter(name="get_etaj_euro")
def get_etaj_euro(prop):
    euro = (prop.me_price * prop.etaj_percent)/100
    prop.etaj_euro = euro 
    prop.save()
    return round(euro,0)
       
@register.filter(name="get_balcon_percent")
def get_balcon_percent(prop, sub):
    euro = get_balcon_euro(prop, sub)
    euro = (euro/prop.me_price)*100
    prop.balcon_percent = euro 
    prop.save()
    return round(euro,0)
    
@register.filter(name="get_balcon_euro")
def get_balcon_euro(prop, sub):
    euro = (sub.balcon - prop.comparable.balcon)*sub.price_persqm
    prop.balcon_euro = euro 
    prop.save()
    return round(euro,0)
         
@register.filter(name="get_hs_percent")
def get_hs_percent(prop):
    euro = (prop.hs_euro/prop.me_price) * 100
    prop.hs_percent = euro 
    prop.save()
    return round(euro,0)
    
@register.filter(name="get_parking_percent")
def get_parking_percent(prop):
    euro = (prop.parking_euro/prop.me_price) * 100
    prop.parking_percent = euro 
    prop.save()
    return round(euro,0)
    
@register.filter(name="get_net_adjustment")
def get_net_adjustment(prop):
    euro = prop.lc_euro + prop.cp_euro + prop.cy_euro + prop.su_euro + prop.finish_euro + prop.etaj_euro + prop.balcon_euro + prop.hs_euro + prop.parking_euro
    prop.net_adjustment = euro 
    prop.save()
    return round(euro,0)

@register.filter(name="get_adjusted_price")
def get_adjusted_price(prop):
    euro = prop.net_adjustment + prop.me_price
    prop.adjusted_price = euro 
    prop.save()
    return round(euro,0)
        
@register.filter(name="get_adjustment_no")
def get_adjustment_no(prop):
    count = 0 
    count += 1 if prop.property_euro != 0 else 0
    count += 1 if prop.fc_euro != 0 else 0
    count += 1 if prop.sc_euro != 0 else 0
    count += 1 if prop.ape_euro != 0 else 0
    count += 1 if prop.me_euro != 0 else 0
    count += 1 if prop.lc_euro != 0 else 0
    count += 1 if prop.cp_euro != 0 else 0
    count += 1 if prop.cy_euro != 0 else 0
    count += 1 if prop.su_euro != 0 else 0
    count += 1 if prop.finish_euro != 0 else 0
    count += 1 if prop.etaj_euro != 0 else 0
    count += 1 if prop.balcon_euro != 0 else 0
    count += 1 if prop.hs_euro != 0 else 0
    count += 1 if prop.parking_euro != 0 else 0
    return count

@register.filter(name="get_total_percent")
def get_total_percent(prop):
    euro = get_total_adjustment(prop)
    euro = (euro/prop.offer_price) * 100 
    return round(euro,0)

@register.filter(name="get_total_adjustment")
def get_total_adjustment(prop):
    euro = prop.property_euro + prop.fc_euro + prop.sc_euro + prop.ape_euro + prop.me_euro + prop.net_adjustment
    prop.total_adjustment = euro 
    prop.save()
    return round(euro,0)

@register.filter(name="get_gross_percent")
def get_gross_percent(prop):
    euro = get_gross_adjustment(prop)
    euro = (euro/prop.offer_price) * 100
    return round(euro,1)

@register.filter(name="get_gross_adjustment")
def get_gross_adjustment(prop):
    euro = abs(prop.property_euro) + abs(prop.fc_euro) + abs(prop.sc_euro) + abs(prop.ape_euro) + (prop.me_euro) + abs(prop.lc_euro) + abs(prop.cp_euro) + abs(prop.cy_euro) + abs(prop.su_euro) + abs(prop.finish_euro) + abs(prop.etaj_euro) + abs(prop.balcon_euro) + abs(prop.hs_euro) + abs(prop.parking_euro)
    prop.gross_adjustment = euro 
    prop.save()
    return round(euro,0)
    
@register.filter(name="get_estimated_value")
def get_estimated_value(ct):
    min = ct.order_by('gross_adjustment').first()
    value = round_up(min.adjusted_price, -3)
    return round(value)

@register.filter(name="get_smallest_gross")
def get_smallest_gross(ct):
    min = ct.order_by('gross_adjustment').first()
    return min.name

# round up to 3 digits 
def round_up(n, decimals=0):
    multiplier = 10 ** decimals 
    return math.ceil(float(n)*multiplier)/multiplier


# ======================= mvb table data ======================== 
@register.filter(name="get_cls_value")
def get_cls_value(area, rent_sqm):
    val = area * rent_sqm
    return round(val, 0)

@register.filter(name="get_vbp_value")
def get_vbp_value(area, rent_sqm):
    val = (area * rent_sqm) * 12
    return round(val, 0)

@register.filter(name="get_mvbp_value")
def get_mvbp_value(c):
    val = (c.comparable.area * c.comparable.rent_sqm) * 12
    mvbp = c.offer_price / val
    return round(mvbp, 1)

@register.filter(name="get_mvbp")
def get_mvbp(ct):
    c = ct.order_by('gross_adjustment').first()
    return get_mvbp_value(c)

@register.filter(name="get_vpcd")
def get_vpcd(sub, ct):
    vbp = (sub.area * sub.rent_sqm) * 12
    c = ct.order_by('gross_adjustment').first()
    c_vbp = (c.comparable.area * c.comparable.rent_sqm) * 12
    mvbp = c.offer_price / c_vbp
    return round(mvbp * vbp, 0)

@register.filter(name="get_vpcd_roturn")
def get_vpcd_roturn(sub, ct):
    c = ct.order_by('gross_adjustment').first()
    c_vbp = (c.comparable.area * c.comparable.rent_sqm) * 12
    mvbp = c.offer_price / c_vbp
    vbp = (sub.area * sub.rent_sqm) * 12
    vpcd = mvbp * vbp
    vpcd_round = round_up(vpcd, -3)
    return round(float((mvbp/vpcd)) + vpcd_round)


# new comparatii table calculation
@register.filter(name="get_offer_price")
def get_offer_price(prop):
    return round((prop.sale_price + prop.ma + prop.pba), 0)

@register.filter(name="get_area_diff")
def get_area_diff(var1, var2):
    return round(var1-var2,2)


# get market price 
@register.filter(name="get_market_price")
def get_market_price(s):
    suprateran_mv = s.suprateran_mv if s.suprateran_mv else 0.00
    subteran_mv = s.subteran_mv if s.subteran_mv else 0.00
    boxa_mv = s.boxa_mv if s.boxa_mv else 0.00
    total = s.amav + suprateran_mv + subteran_mv + boxa_mv
    return round(total, 0)

@register.filter(name="get_market_ron")
def get_market_ron(s):
    total = get_market_price(s)
    return round((total*s.fer), 0)

# get income price 
@register.filter(name="get_income_price")
def get_income_price(s):
    suprateran_iv = s.suprateran_iv if s.suprateran_iv else 0.00
    subteran_iv = s.subteran_iv if s.subteran_iv else 0.00
    boxa_iv = s.boxa_iv if s.boxa_iv else 0.00
    total = s.amav + suprateran_iv + subteran_iv + boxa_iv
    return round(total, 0)

@register.filter(name="get_income_ron")
def get_income_ron(s):
    total = get_income_price(s)
    return round((total*s.fer), 0)

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