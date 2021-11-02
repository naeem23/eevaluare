from django.contrib.auth import get_user_model
from django.db.models import base
from django.db.models.deletion import SET_NULL
from django.forms.widgets import Select
from requests.api import request

from valuation import choices
User = get_user_model()
from django.db import models
from django.utils import timezone
from valuation.choices import *


# =========================== area table =============================
# ====================================================================
class Area(models.Model):
	auto = models.CharField(max_length=3, blank=True, null=True)
	name = models.CharField(max_length=255, blank=True, null=True)

	def __str__(self):
		return self.name

# =========================== city table =============================
# ====================================================================
class City(models.Model):
	area = models.ForeignKey(Area, on_delete=models.CASCADE)
	name = models.CharField(max_length=155, blank=True, null=True)

	def __str__(self):
		return self.name

# ======================== tables for choices ========================
# ==================================================================== 
class PropertyType(models.Model):
	type = models.CharField(max_length=255)
	def __str__(self):
		return self.type 

class CompartmentType(models.Model):
	type = models.CharField(max_length=255)
	def __str__(self):
		return self.type 

class Status(models.Model):
	status = models.CharField(max_length=255)
	def __str__(self):
		return self.status 

class ValuationPurpose(models.Model):
	purpose = models.CharField(max_length=255)
	def __str__(self):
		return self.purpose 

class ValuationApproach(models.Model):
	approach = models.CharField(max_length=255)
	def __str__(self):
		return self.approach

class StradaType(models.Model):
	type = models.CharField(max_length=255)
	def __str__(self):
		return self.type

class Transport(models.Model):
	name = models.CharField(max_length=255)
	def __str__(self):
		return self.name

class ConformType(models.Model):
	type = models.CharField(max_length=255)
	def __str__(self):
		return self.type 

class StructureType(models.Model):
	type = models.CharField(max_length=255)
	def __str__(self):
		return self.type 

class FoundationType(models.Model):
	type = models.CharField(max_length=255)
	def __str__(self):
		return self.type 

class FloorType(models.Model):
	type = models.CharField(max_length=255)
	def __str__(self):
		return self.type 

class ClouserType(models.Model):
	type = models.CharField(max_length=255)
	def __str__(self):
		return self.type 

class SubcompartmentType(models.Model):
	type = models.CharField(max_length=255)
	def __str__(self):
		return self.type 

class RoofType(models.Model):
	type = models.CharField(max_length=255)
	def __str__(self):
		return self.type 

class InvelitoareType(models.Model):
	type = models.CharField(max_length=255)
	def __str__(self):
		return self.type 

class MobilaType(models.Model):
	type = models.CharField(max_length=255)
	def __str__(self):
		return self.type 

class PropertyRightType(models.Model):
	type = models.CharField(max_length=255)
	def __str__(self):
		return self.type 

class HeatingSystem(models.Model):
	name = models.CharField(max_length=255)
	def __str__(self):
		return self.name 

class FinishType(models.Model):
	type = models.CharField(max_length=255)
	def __str__(self):
		return self.type

class Utility(models.Model):
	name = models.CharField(max_length=255)
	def __str__(self):
		return self.name

class AdditionalEquipment(models.Model):
	name = models.CharField(max_length=255)
	def __str__(self):
		return self.name


# ==================== valuated property table =======================
# ====================================================================
def reference_no_generate():
	last_form = ValuatedProperty.objects.last()
	if not last_form:
		ref_no = '00000'
	else: 
		ref_no = last_form.reference_no
	new_ref = str(int(ref_no) + 1)
	new_ref_no = ref_no[0:-(len(new_ref))] + new_ref
	return new_ref_no
	
class ValuatedProperty(models.Model):
	reference_no = models.CharField(max_length=255, default=reference_no_generate, blank=True, null=True)
	evaluator = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
	title = models.CharField(max_length=255, blank=True, null=True)
	property_type = models.ForeignKey(PropertyType, models.SET_NULL, blank=True, null=True)
	compartment_type = models.ForeignKey(CompartmentType, models.SET_NULL, blank=True, null=True)
	apartment_no = models.CharField(max_length=55, blank=True, null=True)
	address = models.CharField(max_length=255, blank=True, null=True)
	area = models.ForeignKey(Area, models.SET_NULL, blank=True, null=True)
	city = models.ForeignKey(City, models.SET_NULL, blank=True, null=True)
	urbana = models.CharField(max_length=55, blank=True, null=True, choices=URBANA_CHOICE)
	locatie = models.CharField(max_length=55, blank=True, null=True, choices=LOCATIE_CHOICE)
	latitude = models.CharField(max_length=255, blank=True, null=True)
	longitude = models.CharField(max_length=255, blank=True, null=True)
	height = models.CharField(max_length=55, blank=True, null=True)
	construction_year = models.CharField(max_length=5, blank=True, null=True)
	owner = models.CharField(max_length=150, blank=True, null=True)
	nume_client = models.CharField(max_length=255, blank=True, null=True)
	ct_address = models.CharField(max_length=155, blank=True, null=True) #client address
	cui = models.CharField(max_length=50, blank=True, null=True) #company registration number 
	report_recipient = models.CharField(max_length=255, blank=True, null=True)
	status = models.ForeignKey(Status, models.SET_NULL, blank=True, null=True)
	inspection_date = models.DateField(blank=True, null=True) #inspection date
	valuation_date =  models.DateField(blank=True, null=True) #valuation date
	report_date = models.DateField(blank=True, null=True) #report date

	def __str__(self):
		return str(self.reference_no)


# ====================== compartimentare table =======================
# ====================================================================
class Compartimentare(models.Model):
	name = models.CharField(max_length=255, blank=True, null=True)
	property_type = models.ForeignKey(PropertyType, models.SET_NULL, blank=True, null=True)

	def __str__(self):
		return str(self.id)


# =================== compartimentare value table ====================
# ====================================================================
class CompartimentareValue(models.Model):
	ref_no = models.ForeignKey(ValuatedProperty, on_delete=models.CASCADE)
	attr_id = models.ForeignKey(Compartimentare, on_delete=models.CASCADE)
	attr_value = models.CharField(max_length=10, blank=True, null=True) 

	def __str__(self):
		return str(self.id)


# ======================== customfield table =========================
# ====================================================================
class CustomFieldValue(models.Model):
	ref_no = models.ForeignKey(ValuatedProperty, on_delete=models.CASCADE)
	attr_name = models.CharField(max_length=155, blank=True, null=True)
	attr_value = models.CharField(max_length=155, blank=True, null=True)

	def __str__(self):
		return str(self.id)


# ==================== cover and summary photo =======================
# ====================================================================
class Photo(models.Model):
	ref_no = models.ForeignKey(ValuatedProperty, on_delete=models.CASCADE)
	refer_to = models.CharField(max_length=55, blank=True, null=True)  #option: cover & summery
	image_order = models.IntegerField(blank=True, null=True)
	image = models.FileField(upload_to='coverphoto/%Y/%m/%d', blank=True)

	def __str__(self):
		return str(self.ref_no) 


# ====================== valuation summary table =====================
# ====================================================================
class ValuationSummary(models.Model):
	ref_no = models.ForeignKey(ValuatedProperty, on_delete=models.CASCADE)
	purpose = models.ForeignKey(ValuationPurpose, models.SET_NULL, blank=True, null=True)
	approach = models.ManyToManyField(ValuationApproach, blank=True)
	amav = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True) #appartment market approach value
	aiav = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True) #appartment income approch value
	fer = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  #forex exchange rate
	fer_date = models.DateField(blank=True, null=True) #forex exchange date (one day prior)
	valued_property = models.TextField(blank=True, null=True)

	def __str__(self):
		return str(self.id)


class SummaryValue(models.Model):
	summary = models.ForeignKey(ValuationSummary, on_delete=models.CASCADE)
	field_name = models.CharField(max_length=55, blank=True, null=True)
	field_value = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	approache = models.CharField(max_length=55, blank=True, null=True)

	def __str__(self):
		return str(self.id)


# ===================== construction data table ======================
# ====================================================================
class Construction(models.Model):
	ref_no = models.ForeignKey(ValuatedProperty, on_delete=models.CASCADE)
	conform = models.ForeignKey(ConformType, models.SET_NULL, blank=True, null=True)
	conform_text = models.CharField(max_length=500, blank=True, null=True)
	structure = models.ForeignKey(StructureType, models.SET_NULL, blank=True, null=True)
	foundation = models.ForeignKey(FoundationType, models.SET_NULL, blank=True, null=True)
	floors = models.ForeignKey(FloorType, models.SET_NULL, blank=True, null=True)
	roof = models.ForeignKey(RoofType, models.SET_NULL, blank=True, null=True)
	invelitoare = models.ForeignKey(InvelitoareType, models.SET_NULL, blank=True, null=True)
	finish = models.ForeignKey(FinishType, models.SET_NULL, blank=True, null=True)
	pardoseli = models.TextField(blank=True, null=True) 
	walls = models.TextField(blank=True, null=True) #Pereti 
	interior_carpentry = models.CharField(max_length=500, blank=True, null=True)
	ceiling = models.CharField(max_length=500, blank=True, null=True) #Plafonul
	exterior_finishes = models.TextField(blank=True, null=True)
	ef_choice = models.CharField(max_length=55, blank=True, null=True, choices=EXTERIOR_FINISHS)
	exterior_carpentry = models.TextField(blank=True, null=True)
	utilities = models.ManyToManyField(Utility, blank=True) 
	closure = models.ForeignKey(ClouserType, models.SET_NULL, blank=True, null=True)
	subcompartment = models.ForeignKey(SubcompartmentType, models.SET_NULL, blank=True, null=True)
	dotari = models.TextField(blank=True, null=True)
	# heating = models.ForeignKey(HeatingSystem, models.SET_NULL, blank=True, null=True)
	comments = models.TextField(blank=True, null=True)
	suprafete = models.TextField(blank=True, null=True)
	utila = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
	totala = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

	def __str__(self):
		return str(self.id)


# ========================= suprafete table ==========================
# ====================================================================
class Suprafete(models.Model):
	ref_no = models.ForeignKey(ValuatedProperty, on_delete=models.CASCADE)
	nr_crt = models.CharField(max_length=55, blank=True, null=True)
	room_name = models.CharField(max_length=155, blank=True, null=True)
	area = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	is_utila = models.BooleanField(default=1)

	def __str__(self):
		return str(self.id)
   
   
# =================== source of information table ====================
# ====================================================================
class SourceofInformation(models.Model):
	ref_no = models.ForeignKey(ValuatedProperty, on_delete=models.CASCADE)
	source = models.CharField(max_length=255, blank=True, null=True)

	def __str__(self):
		return str(self.id)


# ===================== presentation data table ======================
# ====================================================================
class PresentationData(models.Model):
	ref_no = models.ForeignKey(ValuatedProperty, on_delete=models.CASCADE)
	sub_identi = models.TextField(blank=True, null=True)
	sp_hypo = models.TextField(blank=True, null=True) #special hypothesis
	zona = models.TextField(blank=True, null=True) 
	strada = models.ForeignKey(StradaType, models.SET_NULL, blank=True, null=True)
	pt = models.CharField(max_length=155, blank=True, null=True) #public transport
	poi = models.CharField(max_length=1000, blank=True, null=True) #points of interest
	legal_doc = models.CharField(max_length=1000, blank=True, null=True) 
	cadastral_no = models.CharField(max_length=155, blank=True, null=True)
	land_book_no = models.CharField(max_length=155, blank=True, null=True)
	uat = models.CharField(max_length=255, blank=True, null=True)
	charges = models.CharField(max_length=155, blank=True, null=True, choices=CHARGES_CHOICE)
	sarcini = models.CharField(max_length=55, blank=True, null=True) #if charges this field will appear.
	current_use = models.CharField(max_length=155, blank=True, null=True, choices=CURRENT_USE_CHOICE)
	identification = models.CharField(max_length=155, blank=True, null=True, choices=IDENTIFICATION_CHOICE)
	access = models.CharField(max_length=255, blank=True, null=True)
	history = models.TextField(blank=True, null=True)

	def __str__(self):
		return str(self.id)


# ====================== market analysis table =======================
# ==================================================================== 
class MarketAnalysis(models.Model):
	ref_no = models.ForeignKey(ValuatedProperty, on_delete=models.CASCADE)
	dps = models.TextField(blank=True, null=True) #Delimitarea pietei specifice 
	area_between = models.CharField(max_length=155, blank=True, null=True)
	ac = models.TextField(blank=True, null=True) #Analiza cererii
	zona_type = models.CharField(max_length=155, blank=True, null=True, choices=ZONA_TYPE_CHOICE)
	ac_optional = models.TextField(blank=True, null=True)
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
		return str(self.id)


# ========================== anexa table =============================
# ==================================================================== 
class Anexa(models.Model):
	ref_no = models.ForeignKey(ValuatedProperty, on_delete=models.CASCADE)
	refer_to = models.CharField(max_length=55, blank=True, null=True, choices=FILE_CHOICE)
	name = models.CharField(max_length=55, blank=True, null=True)
	file_name = models.FileField(upload_to='anexa/%Y/%m/%d', blank=True)

	def __str__(self):
		return str(self.id)

class Anexa2(models.Model):
	ref_no = models.ForeignKey(ValuatedProperty, on_delete=models.CASCADE)
	link = models.URLField(max_length=255, blank=True, null=True)
	file1 = models.FileField(upload_to='anexa/%Y/%m/%d', blank=True)
	file2 = models.FileField(upload_to='comparabile_utilizate/%Y/%m/%d', blank=True)

	def __str__(self):
		return str(self.id)


# ==================== comparable property table =====================
# ==================================================================== 
class ComparableProperty(models.Model):
	ref_no = models.ForeignKey(ValuatedProperty, on_delete=models.CASCADE, blank=True, null=True)
	is_comparable = models.BooleanField(default=True) #ref_no & is_comparable is only for evaluated property
	sale_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	mobila = models.CharField(max_length=55, blank=True, null=True)
	ma = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True) #margin adjustment
	parking_boxa = models.CharField(max_length=155, blank=True, null=True) 
	pba = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True) #parking boxa adjustment
	ad = models.CharField(max_length=55, blank=True, null=True) #available data
	pr = models.CharField(max_length=55, blank=True, null=True) #property rights
	fc = models.CharField(max_length=55, blank=True, null=True) #financial condition
	sc = models.CharField(max_length=55, blank=True, null=True) #sale condition
	ape = models.CharField(max_length=55, blank=True, null=True) #after purchase expenditure
	me = models.CharField(max_length=55, blank=True, null=True) #month and year check field please
	lc = models.CharField(max_length=255, blank=True, null=True) #location
	cp = models.CharField(max_length=55, blank=True, null=True) #compartment
	cy = models.CharField(max_length=10, blank=True, null=True) #construction year
	area = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	finish = models.CharField(max_length=55, blank=True, null=True)
	etaj = models.CharField(max_length=55, blank=True, null=True)
	balcon = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True) 
	hs = models.CharField(max_length=55, blank=True, null=True) #heating system 
	opt1_name = models.CharField(max_length=55, blank=True, null=True)  
	opt1_val = models.CharField(max_length=55, blank=True, null=True)
	opt2_name = models.CharField(max_length=55, blank=True, null=True)  
	opt2_val = models.CharField(max_length=55, blank=True, null=True)
	opt3_name = models.CharField(max_length=55, blank=True, null=True)  
	opt3_val = models.CharField(max_length=55, blank=True, null=True)

	def __str__(self):
		return str(self.id)


# ======================== comparable table ==========================
# ==================================================================== 
class ComparableTable(models.Model):
	ref_no = models.ForeignKey(ValuatedProperty, on_delete=models.CASCADE)
	comparable = models.TextField(blank=True, null=True)
	name = models.TextField(max_length=2, blank=True, null=True)
	op = models.TextField(blank=True, null=True) #offer price
	margin = models.TextField(blank=True, null=True)
	cv = models.TextField(blank=True, null=True) #correction price
	mp = models.TextField(blank=True, null=True) #margin value
	motivation = models.TextField(blank=True, null=True)

	pr_percent = models.TextField(blank=True, null=True)
	pr_euro = models.TextField(blank=True, null=True)
	pr_price = models.TextField(blank=True, null=True)
	pr_motivation = models.TextField(blank=True, null=True)

	fc_percent = models.TextField(blank=True, null=True)
	fc_euro = models.TextField(blank=True, null=True)
	fc_price = models.TextField(blank=True, null=True)
	fc_motivation = models.TextField(blank=True, null=True)

	sc_percent = models.TextField(blank=True, null=True)
	sc_euro = models.TextField(blank=True, null=True)
	sc_price = models.TextField(blank=True, null=True)
	sc_motivation = models.TextField(blank=True, null=True)

	ape_percent = models.TextField(blank=True, null=True)
	ape_euro = models.TextField(blank=True, null=True)
	ape_price = models.TextField(blank=True, null=True)
	ape_motivation = models.TextField(blank=True, null=True)

	me_percent = models.TextField(blank=True, null=True)
	me_euro = models.TextField(blank=True, null=True)
	me_price = models.TextField(blank=True, null=True)
	me_motivation = models.TextField(blank=True, null=True)

	lc_percent = models.TextField(blank=True, null=True)
	lc_euro = models.TextField(blank=True, null=True)
	lc_motivation = models.TextField(blank=True, null=True)

	cp_percent = models.TextField(blank=True, null=True)
	cp_euro = models.TextField(blank=True, null=True)
	cp_motivation = models.TextField(blank=True, null=True)
	
	cy_percent = models.TextField(blank=True, null=True)
	cy_euro = models.TextField(blank=True, null=True)
	cy_motivation = models.TextField(blank=True, null=True)
	
	su_diff = models.TextField(blank=True, null=True)
	su_percent = models.TextField(blank=True, null=True)
	su_euro = models.TextField(blank=True, null=True)
	su_motivation = models.TextField(blank=True, null=True)
	
	finish_percent = models.TextField(blank=True, null=True)
	finish_euro = models.TextField(blank=True, null=True)
	finish_motivation = models.TextField(blank=True, null=True)

	etaj_percent = models.TextField(blank=True, null=True)
	etaj_euro = models.TextField(blank=True, null=True)
	etaj_motivation = models.TextField(blank=True, null=True)

	price_persqm = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	balcon_percent = models.TextField(blank=True, null=True)
	balcon_euro = models.TextField(blank=True, null=True)
	balcon_motivation = models.TextField(blank=True, null=True)

	hs_percent = models.TextField(blank=True, null=True)
	hs_euro = models.TextField(blank=True, null=True)
	hs_motivation = models.TextField(blank=True, null=True)

	opt1_percent = models.TextField(blank=True, null=True)
	opt1_euro = models.TextField(blank=True, null=True)
	opt1_motivation = models.TextField(blank=True, null=True)

	opt2_percent = models.TextField(blank=True, null=True)
	opt2_euro = models.TextField(blank=True, null=True)
	opt2_motivation = models.TextField(blank=True, null=True)

	opt3_percent = models.TextField(blank=True, null=True)
	opt3_euro = models.TextField(blank=True, null=True)
	opt3_motivation = models.TextField(blank=True, null=True)

	net_adjustment = models.TextField(blank=True, null=True)
	adjustment_price = models.TextField(blank=True, null=True)
	adjustment_no = models.TextField(blank=True, null=True)
	total_percent = models.TextField(blank=True, null=True)
	total_euro = models.TextField(blank=True, null=True)
	gross_percent = models.TextField(blank=True, null=True)
	gross_euro = models.TextField(blank=True, null=True)
	estimated_value = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	smallest_gross = models.CharField(max_length=15, blank=True, null=True)

	def __str__(self):
		return str(self.id)


# ======================== comparable table ==========================
# ==================================================================== 
class MvbTable(models.Model):
	ref_no = models.ForeignKey(ValuatedProperty, on_delete=models.CASCADE)
	sub_rent_sqm = models.CharField(max_length=10, blank=True, null=True) #5.4
	sub_monthly_rent = models.CharField(max_length=10, blank=True, null=True) #437
	sub_vbp = models.CharField(max_length=10, blank=True, null=True) #5242
	vpcd = models.CharField(max_length=10, blank=True, null=True) #66350
	vpcd_rotund = models.CharField(max_length=10, blank=True, null=True) #66000
	monthly_rent = models.CharField(max_length=50, blank=True, null=True) #[366, 409, 351]
	rent_sqm = models.CharField(max_length=50, blank=True, null=True) #[5.3, 5.7, 5.4]
	vbp = models.CharField(max_length=50, blank=True, null=True) #[4388,4905,4212]
	mvbp = models.CharField(max_length=50, blank=True, null=True) #[14.1, 12.7, 13.7]
	min_mvbp = models.CharField(max_length=10, blank=True, null=True) #12.7

	def __str__(self):
		return str(self.ref_no)


