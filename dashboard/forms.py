from django import forms 
from django.contrib.auth import get_user_model
from django.db.models import fields
from django.forms import widgets
from django.forms.widgets import Select
from . import models 
from dashboard.choices import *
User = get_user_model()



class UserModelChoiceField(forms.ModelChoiceField):
	def label_from_instance(self, obj):
		return obj.get_full_name()


class AddValuationForm(forms.ModelForm):
	street = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}))
	city = forms.ModelChoiceField(queryset=models.City.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
	latitude = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'hidden'}))
	longitude = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'hidden'}))
	property_type = forms.ChoiceField(choices=PROPERTY_TYPE_CHOICE, widget=forms.Select(attrs={'class': 'form-control',}), required=True)
	apartment_no = forms.CharField(required=False, max_length=55, widget=forms.TextInput(attrs={'class': 'form-control'}))
	apartment_type = forms.ChoiceField(required=False, choices=APARTMENT_CHOICE, widget=forms.Select(attrs={'class': 'form-control'}))
	owner = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Proprietar'}))
	nume_client = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nume Client'}))
	ct_address = forms.CharField(required=False, max_length=150, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Client Address'}))
	cui = forms.CharField(required=False, max_length=150, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company Reg No.'}))
	report_recipient = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Destinatar Raport'}))
	rp_address = forms.CharField(required=False, max_length=150, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Recipient Address'}))
	valuatate_by = UserModelChoiceField(queryset=User.objects.filter(is_inspector=True), required=False, widget=forms.Select(attrs={'class': 'form-control'}))

	class Meta:
		model = models.EvaluareForm 
		fields = ('street', 'city', 'locatie', 'latitude', 'longitude', 'property_type', 'apartment_no', 'apartment_type', 'owner', 'nume_client', 'ct_address', 'cui', 'report_recipient', 'rp_address', 'valuatate_by')


class EditValuationForm(forms.ModelForm):
	title = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titlul raportului'}))
	street = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Street Address'}))
	city = forms.ModelChoiceField(queryset=models.City.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
	latitude = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'hidden'}))
	longitude = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'hidden'}))
	property_type = forms.ChoiceField(choices=PROPERTY_TYPE_CHOICE, widget=forms.Select(attrs={'class': 'form-control',}))
	apartment_no = forms.CharField(required=False, max_length=55, widget=forms.TextInput(attrs={'class': 'form-control'}))
	apartment_type = forms.ChoiceField(required=False, choices=APARTMENT_CHOICE, widget=forms.Select(attrs={'class': 'form-control'}))
	owner = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Proprietar'}))
	nume_client = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nume Client'}))
	ct_address = forms.CharField(required=False, max_length=150, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Client Address'}))
	cui = forms.CharField(required=False, max_length=150, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company Reg No.'}))
	report_recipient = forms.CharField(required=False, max_length=150, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Destinatar Raport'}))
	rp_address = forms.CharField(required=False, max_length=150, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Recipient Address'}))
	valuatate_by = UserModelChoiceField(queryset=User.objects.filter(is_inspector=True), required=False, widget=forms.Select(attrs={'class': 'form-control'}))
	inspection_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
	valuation_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'form-control','type': 'date'}))
	report_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))

	class Meta:
		model = models.EvaluareForm 
		fields = ('title', 'street', 'city', 'locatie', 'latitude', 'longitude', 'property_type', 'apartment_no', 'apartment_type', 'owner', 'nume_client', 'ct_address', 'cui', 'report_recipient', 'rp_address', 'valuatate_by', 'inspection_date', 'valuation_date', 'report_date')


class PresentationForm(forms.ModelForm):
	sp_hypo = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '5'}))
	poi = forms.CharField(widget=forms.TextInput(attrs={'autofocus': 'autofocus',}))
	cadastral_no = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cadastral Nr'}))
	land_book_no = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Land Book Nr'}))
	uat = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Uat'}))
	charges = forms.ChoiceField(choices=CHARGES_CHOICE, widget=forms.Select(attrs={'class': 'form-control'}))
	sarcini = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sarcini Nume', }))
	current_use = forms.ChoiceField(choices=CURRENT_USE_CHOICE, widget=forms.Select(attrs={'class': 'form-control'}))
	identification = forms.ChoiceField(choices=IDENTIFICATION_CHOICE, widget=forms.Select(attrs={'class': 'form-control'}))
	history = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '5'}))

	class Meta:
		model = models.PresentationData 
		fields = ('sp_hypo', 'poi', 'pt', 'cadastral_no', 'land_book_no', 'uat', 'charges', 'sarcini', 'current_use', 'identification', 'legal_doc', 'history')


class ConstructionForm(forms.ModelForm):
	etaj = forms.CharField(max_length=55, widget=forms.TextInput(attrs={'class': 'form-control'}))
	build_in = forms.CharField(max_length=55, widget=forms.TextInput(attrs={'class': 'form-control'}))
	structure = forms.ChoiceField(choices=STRUCTURE_CHOICE, widget=forms.Select(attrs={'class': 'form-control',}))
	foundation = forms.ChoiceField(choices=FOUNDATION_CHOICE, widget=forms.Select(attrs={'class': 'form-control',}))
	closure = forms.ChoiceField(choices=CLOSURE_CHOICE, widget=forms.Select(attrs={'class': 'form-control',}))
	subcompartment = forms.ChoiceField(choices=SUBCOMPARTMENT_CHOICE, widget=forms.Select(attrs={'class': 'form-control',}))
	roof = forms.ChoiceField(choices=ROOF_CHOICE, widget=forms.Select(attrs={'class': 'form-control',}))
	walls = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
	interior_carpentry = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
	ceiling = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
	exterior_finishes = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
	exterior_carpentry = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
	heating = forms.ChoiceField(choices=HEATING_CHOICE, widget=forms.Select(attrs={'class': 'form-control',}))
	finish = forms.ChoiceField(choices=FINISH_CHOICE, widget=forms.Select(attrs={'class': 'form-control'}))
	comments = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '5'}))

	class Meta:
		model = models.Construction
		fields = ('etaj', 'build_in', 'structure', 'foundation', 'closure', 'subcompartment', 'roof', 'walls', 'interior_carpentry', 'ceiling', 'exterior_finishes', 'exterior_carpentry', 'utilities', 'additional_equipment', 'heating', 'finish', 'comments')


class ComparableForm(forms.ModelForm):
	sale_price = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control'}))
	mobila = forms.ChoiceField(choices=MOBILA_CHOICE, widget=forms.Select(attrs={'class': 'form-control'}))
	parking_boxa = forms.CharField(max_length=55, widget=forms.TextInput(attrs={'class': 'form-control'})) 
	available_data = forms.ChoiceField(choices=AVAILABLE_DATA_CHOICE, widget=forms.Select(attrs={'class': 'form-control'}))
	property_rights = forms.ChoiceField(choices=PROPERTY_RIGHTS_CHOICE, widget=forms.Select(attrs={'class': 'form-control'}))
	financing_condition = forms.ChoiceField(choices=FINANCING_CONDITION_CHOICE, widget=forms.Select(attrs={'class': 'form-control'}))
	sale_condition = forms.ChoiceField(choices=SALE_CONDITION_CHOICE, widget=forms.Select(attrs={'class': 'form-control'}))
	ape = forms.ChoiceField(choices=APE_CHOICE, widget=forms.Select(attrs={'class': 'form-control'}))
	location = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
	compartment = forms.ChoiceField(choices=APARTMENT_CHOICE, widget=forms.Select(attrs={'class': 'form-control'}))
	year_build = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'class': 'form-control'}))
	area = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control'}))
	rent_sqm = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control'}))
	finish = forms.ChoiceField(choices=FINISH_CHOICE, widget=forms.Select(attrs={'class': 'form-control'}))
	etaj = forms.CharField(max_length=55, widget=forms.TextInput(attrs={'class': 'form-control'}))
	balcon = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control'}))
	heating = forms.ChoiceField(choices=HEATING_CHOICE, widget=forms.Select(attrs={'class': 'form-control'}))
	parking = forms.CharField(max_length=55, widget=forms.TextInput(attrs={'class': 'form-control'})) 
	camara = forms.CharField(required=False, max_length=55, widget=forms.TextInput(attrs={'class': 'form-control'})) 
	
	class Meta: 
		model = models.ComparableProperty
		exclude = ('ref_no', 'is_comparable') 


class SubComparableForm(forms.ModelForm):
	property_rights = forms.ChoiceField(choices=PROPERTY_RIGHTS_CHOICE, widget=forms.Select(attrs={'class': 'form-control'}))
	financing_condition = forms.ChoiceField(choices=FINANCING_CONDITION_CHOICE, widget=forms.Select(attrs={'class': 'form-control'}))
	sale_condition = forms.ChoiceField(choices=SALE_CONDITION_CHOICE, widget=forms.Select(attrs={'class': 'form-control'}))
	ape = forms.ChoiceField(choices=APE_CHOICE, widget=forms.Select(attrs={'class': 'form-control'}))

	class Meta: 
		model = models.ComparableProperty
		fields = ('ref_no', 'is_comparable', 'property_rights', 'financing_condition', 'sale_condition', 'ape', 'market_env', 'location', 'compartment', 'year_build', 'area', 'rent_sqm', 'finish', 'etaj', 'balcon', 'price_persqm', 'heating', 'parking', 'camara') 


class ComparableEditForm(forms.ModelForm):
	sale_price = forms.DecimalField(required=False, max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control'}))
	mobila = forms.ChoiceField(required=False, choices=MOBILA_CHOICE, widget=forms.Select(attrs={'class': 'form-control'}))
	parking_boxa = forms.CharField(required=False, max_length=55, widget=forms.TextInput(attrs={'class': 'form-control'})) 
	available_data = forms.ChoiceField(required=False, choices=AVAILABLE_DATA_CHOICE, widget=forms.Select(attrs={'class': 'form-control'}))
	property_rights = forms.ChoiceField(required=False, choices=PROPERTY_RIGHTS_CHOICE, widget=forms.Select(attrs={'class': 'form-control'}))
	financing_condition = forms.ChoiceField(required=False, choices=FINANCING_CONDITION_CHOICE, widget=forms.Select(attrs={'class': 'form-control'}))
	sale_condition = forms.ChoiceField(required=False, choices=SALE_CONDITION_CHOICE, widget=forms.Select(attrs={'class': 'form-control'}))
	ape = forms.ChoiceField(required=False, choices=APE_CHOICE, widget=forms.Select(attrs={'class': 'form-control'}))
	location = forms.CharField(required=False, max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
	compartment = forms.ChoiceField(required=False, choices=APARTMENT_CHOICE, widget=forms.Select(attrs={'class': 'form-control'}))
	year_build = forms.CharField(required=False, max_length=10, widget=forms.TextInput(attrs={'class': 'form-control'}))
	area = forms.DecimalField(required=False, max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control'}))
	rent_sqm = forms.DecimalField(required=False, max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control'}))
	finish = forms.ChoiceField(choices=FINISH_CHOICE, widget=forms.Select(attrs={'class': 'form-control'}))
	etaj = forms.CharField(required=False, max_length=55, widget=forms.TextInput(attrs={'class': 'form-control'}))
	balcon = forms.DecimalField(required=False, max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control'}))
	price_persqm = forms.DecimalField(required=False, max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control'}))
	heating = forms.ChoiceField(required=False, choices=HEATING_CHOICE, widget=forms.Select(attrs={'class': 'form-control'}))
	parking = forms.CharField(required=False, max_length=55, widget=forms.TextInput(attrs={'class': 'form-control'})) 
	camara = forms.CharField(required=False, max_length=55, widget=forms.TextInput(attrs={'class': 'form-control'})) 
	
	class Meta: 
		model = models.ComparableProperty
		exclude = ('ref_no', 'is_comparable') 


class AddValuationSummary(forms.ModelForm):
	valued_property = forms.CharField(required=False, max_length=500, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '5'}))
	purpose = forms.ChoiceField(choices=PURPOSE_CHOICE, widget=forms.Select(attrs={'class': 'form-control',}))
	amav = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00', 'step': '0.01'}))
	suprateran_mv = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00', 'step': '0.01'}))
	subteran_mv = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00', 'step': '0.01'}))
	boxa_mv = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00', 'step': '0.01'}))
	aiav = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00', 'step': '0.01'}))
	suprateran_iv = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00', 'step': '0.01'}))
	subteran_iv = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00', 'step': '0.01'}))
	boxa_iv = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00', 'step': '0.01'}))

	class Meta:
		model = models.ValuationSummary
		exclude = ('ref_no',)

