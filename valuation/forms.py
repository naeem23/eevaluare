from django import forms 
from django.contrib.auth import get_user_model
from django.db.models import fields, query
from django.forms import widgets
from django.forms.models import ModelChoiceField
from django.forms.widgets import Select

from dashboard import models as db_model
from valuation.models import * 
from valuation.choices import *
User = get_user_model()


class UserModelChoiceField(forms.ModelChoiceField):
	def label_from_instance(self, obj):
		return obj.get_full_name()

class InitialForm(forms.ModelForm):
	evaluator = UserModelChoiceField(required=False, queryset=User.objects.filter(is_inspector=True), widget=forms.Select(attrs={'class': 'form-control'}))
	property_type = forms.ModelChoiceField(queryset=PropertyType.objects.all(), widget=forms.Select(attrs={'class': 'form-control',}))
	compartment_type = forms.ModelChoiceField(required=False, queryset=CompartmentType.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
	street = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
	numarul = forms.CharField(max_length=55, widget=forms.TextInput(attrs={'class': 'form-control'}))
	building_no = forms.CharField(required=False, max_length=55, widget=forms.TextInput(attrs={'class': 'form-control'}))
	scara = forms.CharField(required=False, max_length=55, widget=forms.TextInput(attrs={'class': 'form-control'}))
	floor_no = forms.CharField(max_length=55, widget=forms.TextInput(attrs={'class': 'form-control'}))
	apartment_no = forms.CharField(max_length=55, widget=forms.TextInput(attrs={'class': 'form-control'}))
	postal_code = forms.CharField(required=False, max_length=55, widget=forms.TextInput(attrs={'class': 'form-control'}))
	area = forms.ModelChoiceField(queryset=Area.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}),empty_label="Alege")
	urbana = forms.ChoiceField(required=False, choices=URBANA_CHOICE, widget=forms.Select(attrs={'class': 'form-control'}))
	locatie = forms.ChoiceField(required=False, choices=LOCATIE_CHOICE, widget=forms.Select(attrs={'class': 'form-control'}))
	zona = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
	latitude = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'hidden'}))
	longitude = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'hidden'}))
	height = forms.CharField(max_length=55, widget=forms.TextInput(attrs={'class': 'form-control'}))
	construction_year = forms.CharField(max_length=5, widget=forms.TextInput(attrs={'class': 'form-control'}))
	owner = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Proprietar'}))
	nume_client = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nume Client'}))
	ct_address = forms.CharField(required=False, max_length=150, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Client Address'}))
	cui = forms.CharField(required=False, max_length=150, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company Reg No.'}))
	report_recipient = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Destinatar Raport'}))

	class Meta:
		model = ValuatedProperty
		exclude = ('reference_no', 'title', 'status', 'inspection_date', 'valuation_date', 'report_date', 'assigned_to')
		

class EditInitialForm(forms.ModelForm):
	evaluator = UserModelChoiceField(required=False, queryset=User.objects.filter(is_inspector=True), widget=forms.Select(attrs={'class': 'form-control'}))
	property_type = forms.ModelChoiceField(queryset=PropertyType.objects.all(), widget=forms.Select(attrs={'class': 'form-control',}))
	compartment_type = forms.ModelChoiceField(required=False, queryset=CompartmentType.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
	street = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
	numarul = forms.CharField(max_length=55, widget=forms.TextInput(attrs={'class': 'form-control'}))
	building_no = forms.CharField(required=False, max_length=55, widget=forms.TextInput(attrs={'class': 'form-control'}))
	scara = forms.CharField(required=False, max_length=55, widget=forms.TextInput(attrs={'class': 'form-control'}))
	floor_no = forms.CharField(max_length=55, widget=forms.TextInput(attrs={'class': 'form-control'}))
	apartment_no = forms.CharField(max_length=55, widget=forms.TextInput(attrs={'class': 'form-control'}))
	postal_code = forms.CharField(required=False, max_length=55, widget=forms.TextInput(attrs={'class': 'form-control'}))
	area = forms.ModelChoiceField(queryset=Area.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}),empty_label="Alege")
	urbana = forms.ChoiceField(required=False, choices=URBANA_CHOICE, widget=forms.Select(attrs={'class': 'form-control'}))
	locatie = forms.ChoiceField(required=False, choices=LOCATIE_CHOICE, widget=forms.Select(attrs={'class': 'form-control'}))
	latitude = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'hidden'}))
	longitude = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'hidden'}))
	zona = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
	height = forms.CharField(max_length=55, widget=forms.TextInput(attrs={'class': 'form-control'}))
	construction_year = forms.CharField(max_length=5, widget=forms.TextInput(attrs={'class': 'form-control'}))
	owner = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Proprietar'}))
	nume_client = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nume Client'}))
	ct_address = forms.CharField(required=False, max_length=150, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Client Address'}))
	cui = forms.CharField(required=False, max_length=150, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company Reg No.'}))
	report_recipient = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Destinatar Raport'}))
	status = forms.ModelChoiceField(queryset=Status.objects.all(), widget=forms.Select(attrs={'class': 'form-control',}))
	inspection_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'form-control'}))
	# valuation_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'form-control','type': 'date'}))
	# report_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'form-control','type': 'date'}))

	class Meta:
		model = ValuatedProperty
		exclude = ('reference_no', 'valuation_date', 'report_date')


class AddValuationSummary(forms.ModelForm):
	purpose = forms.ModelChoiceField(queryset=ValuationPurpose.objects.all(), widget=forms.Select(attrs={'class': 'form-control',}), empty_label=None)
	amav = forms.DecimalField(required=False, max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00', 'step': '0.01', 'min': '0.00'}))
	aiav = forms.DecimalField(required=False, max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00', 'step': '0.01', 'min': '0.00'}))

	class Meta:
		model = ValuationSummary
		exclude = ('ref_no',)


class ConstructionForm(forms.ModelForm):
	conform = forms.ModelChoiceField(queryset=ConformType.objects.all(), widget=forms.Select(attrs={'class': 'form-control',})) 
	structure = forms.ModelChoiceField(queryset=StructureType.objects.all(), widget=forms.Select(attrs={'class': 'form-control',}), empty_label=None)
	foundation = forms.ModelChoiceField(queryset=FoundationType.objects.all(), widget=forms.Select(attrs={'class': 'form-control',}), empty_label=None)
	floors = forms.ModelChoiceField(queryset=FloorType.objects.all(), widget=forms.Select(attrs={'class': 'form-control',}), empty_label=None)
	roof = forms.ModelChoiceField(queryset=RoofType.objects.all(), widget=forms.Select(attrs={'class': 'form-control',}))
	invelitoare = forms.ModelChoiceField(queryset=InvelitoareType.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
	finish = forms.ModelChoiceField(queryset=FinishType.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
	exterior_finishes = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '5'}))
	ef_choice = forms.ChoiceField(choices=EXTERIOR_FINISHS, widget=forms.Select(attrs={'class': 'form-control'}))
	utilities = forms.ModelMultipleChoiceField(queryset=Utility.objects.all(), widget=forms.SelectMultiple(attrs={'class': 'form-control', 'multiple': 'multiple'}))
	closure = forms.ModelChoiceField(queryset=ClouserType.objects.all(), widget=forms.Select(attrs={'class': 'form-control',}), empty_label=None)
	subcompartment = forms.ModelChoiceField(queryset=SubcompartmentType.objects.all(), widget=forms.Select(attrs={'class': 'form-control',}), empty_label=None)
	comments = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '5'}))

	class Meta:
		model = Construction
		exclude = ('ref_no',)


class PresentationForm(forms.ModelForm):
	strada = forms.ModelChoiceField(queryset=StradaType.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
	cadastral_no = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cadastral Nr'}))
	land_book_no = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Carte funciar?? nr'}))
	uat = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Uat'}))
	charges = forms.ChoiceField(choices=CHARGES_CHOICE, widget=forms.Select(attrs={'class': 'form-control'}))
	sarcini = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sarcini Nume', }))
	current_use = forms.ChoiceField(choices=CURRENT_USE_CHOICE, widget=forms.Select(attrs={'class': 'form-control'}))
	access = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
	history = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '5'}))

	class Meta:
		model = PresentationData 
		exclude = ('ref_no',)


class MarketAnalysisForm(forms.ModelForm):
	area_between = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '95 mp si 155 mp'}))
	zona_type = forms.ChoiceField(required=False, choices=ZONA_TYPE_CHOICE, widget=forms.Select(attrs={'class': 'form-control'}))
	const_density = forms.ChoiceField(required=False, choices=CONST_DENSITY_CHOICE, widget=forms.Select(attrs={'class': 'form-control'}))
	ebby = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'})) #existing building build year
	prop_size = forms.ChoiceField(required=False, choices=PROP_SIZE_CHOICE, widget=forms.Select(attrs={'class': 'form-control'})) #property size
	exposure = forms.ChoiceField(required=False, choices=EXPOSURE_CHOICE, widget=forms.Select(attrs={'class': 'form-control'}))
	liquidity = forms.ChoiceField(required=False, choices=LIQUIDITY_CHOICE, widget=forms.Select(attrs={'class': 'form-control'}))
	transactions_nr = forms.ChoiceField(required=False, choices=TRANSACTIONS_CHOICE, widget=forms.Select(attrs={'class': 'form-control'})) 
	exposure_period = forms.ChoiceField(required=False, choices=EXPOSURE_PERIOD_CHOICE, widget=forms.Select(attrs={'class': 'form-control'}))
	offer_similar = forms.ChoiceField(choices=CONCLUSION_CHOICE, widget=forms.Select(attrs={'class': 'form-control'}))
	application_similar = forms.ChoiceField(choices=CONCLUSION_CHOICE, widget=forms.Select(attrs={'class': 'form-control'}))
	market_balance = forms.ChoiceField(choices=CONCLUSION_CHOICE, widget=forms.Select(attrs={'class': 'form-control'}))
	minsale_price = forms.DecimalField(required=False, max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control'})) 
	maxsale_price = forms.DecimalField(required=False, max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control'})) 
	
	class Meta:
		model = MarketAnalysis
		exclude = ('ref_no',)


class ComparableForm(forms.ModelForm):
	sale_price = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control'}))
	ma = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control'}))
	parking_boxa = forms.CharField(max_length=55, widget=forms.TextInput(attrs={'class': 'form-control', 'value': 'Nu'})) 
	pba = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control'}))
	lc = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
	cy = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'class': 'form-control'}))
	area = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control'}))
	etaj = forms.CharField(max_length=55, widget=forms.TextInput(attrs={'class': 'form-control'}))
	balcon = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control'}))
	camara = forms.CharField(max_length=10, widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '2', 'value': '2'})) 
	
	class Meta: 
		model = ComparableProperty
		exclude = ('ref_no', 'is_comparable') 

