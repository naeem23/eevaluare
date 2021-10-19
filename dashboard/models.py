from django.contrib.auth import get_user_model
from django.db.models import base
from requests.api import request
User = get_user_model()
from django.db import models
from django.utils import timezone
from dashboard.choices import *


class Area(models.Model):
	auto = models.CharField(max_length=3, blank=True, null=True)
	name = models.CharField(max_length=255, blank=True, null=True)

	def __str__(self):
		return self.name


class City(models.Model):
	area = models.ForeignKey(Area, on_delete=models.CASCADE)
	name = models.CharField(max_length=155, blank=True, null=True)

	def __str__(self):
		return self.area.auto + "-" + self.name


def reference_no_generate():
	last_form = EvaluareForm.objects.last()
	if not last_form:
		ref_no = '00000'
	else: 
		ref_no = last_form.reference_no
	new_ref = str(int(ref_no) + 1)
	new_ref_no = ref_no[0:-(len(new_ref))] + new_ref
	return new_ref_no
	
class EvaluareForm(models.Model):
	reference_no = models.CharField(max_length=255, default=reference_no_generate, blank=True, null=True)
	valuatate_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

	title = models.CharField(max_length=255, blank=True, null=True)
	street = models.CharField(max_length=255, blank=True, null=True)
	city = models.ForeignKey(City, on_delete=models.CASCADE, blank=True, null=True)
	locatie = models.CharField(max_length=55, blank=True, null=True, choices=LOCATIE_CHOICE) #multiple select
	apartment_no = models.CharField(max_length=55, blank=True, null=True)
	apartment_type = models.CharField(max_length=155, blank=True, null=True, choices=APARTMENT_CHOICE)
	latitude = models.CharField(max_length=255, blank=True, null=True)
	longitude = models.CharField(max_length=255, blank=True, null=True)
	property_type = models.CharField(max_length=150, blank=True, null=True, choices=PROPERTY_TYPE_CHOICE)
	owner = models.CharField(max_length=150, blank=True, null=True)
	nume_client = models.CharField(max_length=255, blank=True, null=True)
	ct_address = models.CharField(max_length=155, blank=True, null=True) #client address
	cui = models.CharField(max_length=50, blank=True, null=True) #company registration number 
	report_recipient = models.CharField(max_length=255, blank=True, null=True)
	rp_address = models.CharField(max_length=155, blank=True, null=True) #recipient address

	status = models.CharField(max_length=150, blank=True, null=True, choices=STATUS_CHOICE)
	inspection_date = models.DateField(blank=True, null=True) #inspection date
	valuation_date =  models.DateField(blank=True, null=True) #valuation date
	report_date = models.DateField(blank=True, null=True) #report date

	def __str__(self):
		return str(self.reference_no)


class PresentationData(models.Model):
	ref_no = models.ForeignKey(EvaluareForm, on_delete=models.CASCADE)
	sub_identi = models.TextField(max_length=1000, blank=True, null=True)
	sp_hypo = models.TextField(max_length=1000, blank=True, null=True) #special hypothesis
	zona = models.TextField(max_length=1000, blank=True, null=True) 
	strada = models.CharField(max_length=155, blank=True, null=True, choices=STRADA_CHOICE)
	pt = models.CharField(max_length=155, blank=True, null=True) #public transport
	poi = models.CharField(max_length=1000, blank=True, null=True) #points of interest
	description = models.TextField(max_length=1000, blank=True, null=True) 
	legal_doc = models.CharField(max_length=1000, blank=True, null=True) 
	cadastral_no = models.CharField(max_length=155, blank=True, null=True)
	land_book_no = models.CharField(max_length=155, blank=True, null=True)
	uat = models.CharField(max_length=255, blank=True, null=True)
	charges = models.CharField(max_length=155, blank=True, null=True, choices=CHARGES_CHOICE)
	sarcini = models.CharField(max_length=55, blank=True, null=True) #if charges this field will appear.
	current_use = models.CharField(max_length=155, blank=True, null=True, choices=CURRENT_USE_CHOICE)
	identification = models.CharField(max_length=155, blank=True, null=True, choices=IDENTIFICATION_CHOICE)
	access = models.CharField(max_length=255, blank=True, null=True)
	history = models.TextField(max_length=1000, blank=True, null=True)

	def __str__(self):
		return self.ref_no


class Construction(models.Model):
	ref_no = models.ForeignKey(EvaluareForm, on_delete=models.CASCADE)
	etaj = models.CharField(max_length=55, blank=True, null=True)
	build_in = models.CharField(max_length=10, blank=True, null=True) #eg: 2008
	conform = models.CharField(max_length=255, blank=True, null=True, choices=CONFORM_CHOICE)
	structure = models.CharField(max_length=255, blank=True, null=True, choices=STRUCTURE_CHOICE)
	foundation = models.CharField(max_length=255, blank=True, null=True, choices=FOUNDATION_CHOICE)
	closure = models.CharField(max_length=255, blank=True, null=True, choices=CLOSURE_CHOICE)
	subcompartment = models.CharField(max_length=255, blank=True, null=True, choices=SUBCOMPARTMENT_CHOICE)
	roof = models.CharField(max_length=255, blank=True, null=True, choices=ROOF_CHOICE)
	walls = models.CharField(max_length=500, blank=True, null=True)
	interior_carpentry = models.CharField(max_length=500, blank=True, null=True)
	ceiling = models.CharField(max_length=500, blank=True, null=True)
	exterior_finishes = models.CharField(max_length=500, blank=True, null=True)
	exterior_carpentry = models.CharField(max_length=500, blank=True, null=True)
	invelitoare = models.CharField(max_length=255, blank=True, null=True, choices=INVELITOARE_CHOICE)
	utilities = models.CharField(max_length=500, blank=True, null=True, choices=UTILITY_CHOICE) #multiple select 
	additional_equipment = models.CharField(max_length=500, blank=True, null=True, choices=ADDITIONAL_EQUIPMENT) #multiple select 
	heating = models.CharField(max_length=500, blank=True, null=True, choices=HEATING_CHOICE)
	finish = models.CharField(max_length=55, blank=True, null=True, choices=FINISH_CHOICE)
	comments = models.TextField(max_length=1000, blank=True, null=True)

	def __str__(self):
		return self.ref_no


class Suprafete(models.Model):
	ref_no = models.ForeignKey(EvaluareForm, on_delete=models.CASCADE)
	room_name = models.CharField(max_length=155, blank=True, null=True)
	area = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
	utila = models.BooleanField(default=False)

	def __str__(self):
		return self.ref_no


class Anexa(models.Model):
	ref_no = models.ForeignKey(EvaluareForm, on_delete=models.CASCADE)
	refer_to = models.CharField(max_length=55, blank=True, null=True, choices=FILE_CHOICE)
	file_name = models.FileField(upload_to='anexa/%Y/%m/%d', blank=True)

	def __str__(self):
		return self.ref_no


class ResidentialAttr(models.Model):
	name = models.CharField(max_length=255, blank=True, null=True)
	property_type = models.CharField(max_length=50, blank=True, null=True)
	has_photo = models.BooleanField(default=False)
	has_nr = models.BooleanField(default=False)

	def __str__(self):
		return str(self.id)


class ResidentialAttrValue(models.Model):
	ref_no = models.ForeignKey(EvaluareForm, on_delete=models.CASCADE)
	attr_id = models.ForeignKey(ResidentialAttr, on_delete=models.CASCADE)
	attr_value = models.CharField(max_length=10, blank=True, null=True) 
	mav = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) #market approach value
	iav = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) #income approach value
	floor_type = models.CharField(max_length=55, blank=True, null=True, choices=FLOOR_TYPE)

	def __str__(self):
		return str(self.id)


class ResidentialAttrFile(models.Model):
	ref_no = models.ForeignKey(EvaluareForm, on_delete=models.CASCADE)
	attr_id = models.ForeignKey(ResidentialAttr, on_delete=models.CASCADE, related_name='files')
	file_name = models.FileField(upload_to='valuation/%Y/%m/%d', blank=True)

	def __str__(self):
		return str(self.id)


class CustomFieldValue(models.Model):
	ref_no = models.ForeignKey(EvaluareForm, on_delete=models.CASCADE)
	attr_name = models.CharField(max_length=155, blank=True, null=True)
	attr_value = models.CharField(max_length=155, blank=True, null=True)

	def __str__(self):
		return str(self.id)


class CustomFieldFile(models.Model):
	ref_no = models.ForeignKey(EvaluareForm, on_delete=models.CASCADE)
	attr_id = models.ForeignKey(CustomFieldValue, on_delete=models.CASCADE, related_name="cfiles")
	file_name = models.FileField(upload_to='valuation/%Y/%m/%d', blank=True)

	def __str__(self):
		return str(self.id)


class Photo(models.Model):
	ref_no = models.ForeignKey(EvaluareForm, on_delete=models.CASCADE)
	refer_to = models.CharField(max_length=55, blank=True, null=True)  #option: cover & summery
	image_order = models.IntegerField(blank=True, null=True)
	image = models.FileField(upload_to='coverphoto/%Y/%m/%d', blank=True)

	def __str__(self):
		return str(self.id) 


class ValuationSummary(models.Model):
	ref_no = models.ForeignKey(EvaluareForm, on_delete=models.CASCADE)
	purpose = models.CharField(max_length=150, blank=True, null=True, choices=PURPOSE_CHOICE)
	approach = models.CharField(max_length=150, blank=True, null=True, choices=APPROACH_CHOICE)
	amav = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) #appartment market approach value
	suprateran_mv = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) #market value = mv
	subteran_mv = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
	boxa_mv = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
	aiav = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) #appartment income approch value
	suprateran_iv = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) #income value = iv
	subteran_iv = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
	boxa_iv = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
	fer = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  #forex exchange rate
	fer_date = models.DateField(blank=True, null=True) #forex exchange date (one day prior)
	valued_property = models.TextField(max_length=1000, blank=True, null=True)

	def __str__(self):
		return str(self.id)


class SourceofInformation(models.Model):
	ref_no = models.ForeignKey(EvaluareForm, on_delete=models.CASCADE)
	# value = models.CharField(max_length=55, blank=True, null=True)
	source = models.CharField(max_length=255, blank=True, null=True)

	def __str__(self):
		return self.ref_no


class ComparableProperty(models.Model):
	ref_no = models.ForeignKey(EvaluareForm, on_delete=models.CASCADE, blank=True, null=True)
	is_comparable = models.BooleanField(default=True) #ref_no & is_comparable is only for evaluated property
	sale_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	mobila = models.CharField(max_length=55, blank=True, null=True, choices=MOBILA_CHOICE)
	parking_boxa = models.CharField(max_length=155, blank=True, null=True) 
	correct_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	available_data = models.CharField(max_length=55, blank=True, null=True, choices=AVAILABLE_DATA_CHOICE)
	property_rights = models.CharField(max_length=55, blank=True, null=True, choices=PROPERTY_RIGHTS_CHOICE)
	financing_condition = models.CharField(max_length=55, blank=True, null=True, choices=FINANCING_CONDITION_CHOICE)
	sale_condition = models.CharField(max_length=55, blank=True, null=True, choices=SALE_CONDITION_CHOICE)
	ape = models.CharField(max_length=55, blank=True, null=True, choices=APE_CHOICE) #after purchase expenditure
	market_env = models.CharField(max_length=55, blank=True, null=True) #month and year check field please
	location = models.CharField(max_length=255, blank=True, null=True)
	compartment = models.CharField(max_length=55, blank=True, null=True, choices=APARTMENT_CHOICE)
	year_build = models.CharField(max_length=10, blank=True, null=True)
	area = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	rent_sqm = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	finish = models.CharField(max_length=55, blank=True, null=True, choices=FINISH_CHOICE)
	etaj = models.CharField(max_length=55, blank=True, null=True)
	balcon = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True) #sum of all balcon area
	price_persqm = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	heating = models.CharField(max_length=55, blank=True, null=True, choices=HEATING_CHOICE)
	parking = models.CharField(max_length=55, blank=True, null=True)  
	camara = models.CharField(max_length=155, blank=True, null=True)
	
	motivation = models.CharField(max_length=500, blank=True, null=True)
	property_motivation = models.CharField(max_length=500, blank=True, null=True)
	fc_motivation = models.CharField(max_length=500, blank=True, null=True)
	sc_motivation = models.CharField(max_length=500, blank=True, null=True)
	ape_motivation = models.CharField(max_length=500, blank=True, null=True)
	me_motivation = models.CharField(max_length=500, blank=True, null=True)
	lc_motivation = models.CharField(max_length=500, blank=True, null=True)
	cp_motivation = models.CharField(max_length=500, blank=True, null=True)
	cy_motivation = models.CharField(max_length=500, blank=True, null=True)
	su_motivation = models.CharField(max_length=500, blank=True, null=True)
	finish_motivation = models.CharField(max_length=500, blank=True, null=True)
	etaj_motivation = models.CharField(max_length=500, blank=True, null=True)
	balcon_motivation = models.CharField(max_length=500, blank=True, null=True)
	hs_motivation = models.CharField(max_length=500, blank=True, null=True)
	parking_motivation = models.CharField(max_length=500, blank=True, null=True)

	def __str__(self):
		return str(self.id)


class ComparableTable(models.Model):
	ref_no = models.ForeignKey(EvaluareForm, on_delete=models.CASCADE)
	comparable = models.ForeignKey(ComparableProperty, on_delete=models.CASCADE, blank=True)
	name = models.CharField(max_length=2, blank=True, null=True) #not required
	mobila_ajustare = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	pb_ajustare = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	
	margin = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	correction_value = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	offer_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

	property_percent = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	property_euro = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	property_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

	fc_percent = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	fc_euro = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	fc_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

	sc_percent = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	sc_euro = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	sc_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

	ape_percent = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	ape_euro = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	ape_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

	me_percent = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	me_euro = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	me_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

	lc_percent = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	lc_euro = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	cp_percent = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	cp_euro = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	cy_percent = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	cy_euro = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	su_percent = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	su_euro = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	finish_percent = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	finish_euro = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	etaj_percent = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	etaj_euro = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	balcon_percent = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	balcon_euro = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	hs_percent = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	hs_euro = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	parking_percent = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	parking_euro = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

	net_adjustment = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	adjusted_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	total_adjustment = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	gross_adjustment = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

	def __str__(self):
		return str(self.id)


class MarketAnalysis(models.Model):
	ref_no = models.ForeignKey(EvaluareForm, on_delete=models.CASCADE)
	dps = models.TextField(max_length=1000, blank=True, null=True) #Delimitarea pietei specifice 
	area_between = models.CharField(max_length=155, blank=True, null=True)
	ac = models.TextField(blank=True, null=True) #Analiza cererii
	zona_type = models.CharField(max_length=155, blank=True, null=True, choices=ZONA_TYPE_CHOICE)
	af = models.TextField(blank=True, null=True) #Analiza furnizarii
	const_density = models.CharField(max_length=55, blank=True, null=True, choices=CONST_DENSITY_CHOICE)
	ebby = models.CharField(max_length=155, blank=True, null=True) #existing building build year
	prop_size = models.CharField(max_length=155, blank=True, null=True, choices=PROP_SIZE_CHOICE) #property size
	exposure = models.CharField(max_length=155, blank=True, null=True, choices=EXPOSURE_CHOICE)
	spi = models.TextField(blank=True, null=True) #supply deman interaction
	liquidity = models.CharField(max_length=155, blank=True, null=True, choices=LIQUIDITY_CHOICE)
	transactions_nr = models.CharField(max_length=155, blank=True, null=True, choices=TRANSACTIONS_CHOICE) 
	exposure_period = models.CharField(max_length=155, blank=True, null=True, choices=EXPOSURE_PERIOD_CHOICE)
	forecast = models.TextField(blank=True, null=True)
	minsale_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True) 
	maxsale_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True) 
	guarantee_risk = models.TextField(blank=True, null=True)

	def __str__(self):
		return self.ref_no