PROPERTY_TYPE_CHOICE = [
	('apartamente', 'Apartamente'),
	('case', 'Case / Vile'),
	('comerciale', 'Spatii Comerciale'),
	('depozite', 'Depozite si Hale'),
	('birouri', 'Birouri'),
]

APARTMENT_CHOICE = [ 
	('', 'Alege'),
	('decomandat', 'Decomandat'),
	('semidecomandat', 'Semidecomandat'),
	('nedecomandat', 'Neecomandat'),
	('circular', 'Circular'),
]

STATUS_CHOICE = [
	('progress', 'In progress'),
	('completed', 'Completed'),
	('suspended', 'Suspended'),
	('cancelled', 'Cancelled')
]

PURPOSE_CHOICE = [
	('bank_guarantee', 'Garantare Bancara'),
	('informativ', 'Informativ'),
	('raportare_financiara', 'Raportare Financiara')
]

APPROACH_CHOICE = [
	('market', 'Abordare de piață'),
	('income', 'Abordarea prin venit'),
]

# keep static 
URBANA_CHOICE = [
	('urbana', 'Urbana'),
	('rurala', 'Rurala'),
]

LOCATIE_CHOICE = [
	('centrala', 'Centrala'),
	('mediana', 'Mediana'),
	('periferica', 'Periferica'),
]

STRADA_CHOICE = [
	('one_lane', "O banda de circulatie"), 
	('two_lane', "Doua benzi de circulatie"), 
	('three_lane', "Trei benzi de circulatie"),
]

CHARGES_CHOICE = [
	('no', 'nu este grevata'),
	('yes', 'este grevata')
]

CURRENT_USE_CHOICE = [
	('ldp', 'Locuit de proprietar'),
	('liber', 'Liber'),
	('ldc', 'Locuit de chirias'),
]

IDENTIFICATION_CHOICE = [
	('apii', 'Adresei postale inscrise pe imobil'), 
	('cipa', 'Cadastral introdus pe platforma ANCPI'), 
]

# dynamic
CONFORM_CHOICE = [
	('inspectiei', 'Inspectiei'),
	('cpe', 'Certificatului de performanta energetica'),
	('procesului', 'Procesului verbal de receptie la terminarea lucrarilor'),
	('planului', 'Planului de amplasament si de mutare a imobilului'),
]

STRUCTURE_CHOICE = [
	('zp', 'Zidarie portanta'),
	('armat', 'Cadre din beton armat'),
	('metal', 'Cadre de metal'),
	('darmat', 'Diafragme din beton armat'),
	('lemn', 'Lemn'),
	('mix', 'Mixt – cadre de metal + structura put beton'),
]

FOUNDATION_CHOICE = [
	('armat', 'Continue din beton armat'),
	('stalpi', 'Stalpi din beton armat prefabricat'),
	('grinzi', 'Grinzi continue sub stalpi'),
	('trg', 'Tip Radier General'),
	('piloti', 'Pe piloti'),
	('chesoane', 'Pe chesoane'),
]
# static 
CLOSURE_CHOICE = [
	('zc', 'Zidarie Caramida'),
	('bca', 'Zidarie BCA')
]

SUBCOMPARTMENT_CHOICE = [
	('rigips', 'Rigips'),
	('bca', 'BCA'),
	('caramida', 'Caramida'),
]
# dyanamic 
ROOF_CHOICE = [
	('tc', 'Terasa circulabila'),
	('tn', 'Terasa necirculabila'),
	('sl', 'Sarpanta din lemn'),
	('sm', 'Sarpanta din metal'),
]

# static 
INVELITOARE_CHOICE = [
	('bitum', 'Bitum'),
	('tigla', 'Tigla'),
	('tabla', 'Tabla'),
]

FLOOR_TYPE = [
	('beton', 'Beton armat'),
	('lemn', 'Lemn'),
]

UTILITY_CHOICE = [
	('gas', 'Natural gas'),
	('electricity', 'Electricity'),
	('apa', 'Apa'),
	('sewerage', 'Sewerage'),
]

ADDITIONAL_EQUIPMENT = [
	('ac', 'Air conditioning'),
	('ngp', 'Conducta de gaze naturale'),
	('mobilat', 'Mobilat'),
]

HEATING_CHOICE = [
	('termoficare', 'Termoficare'),
	('ctp', 'Centrala termica proprie'),
	('ctb', 'Centrala termica a blocului'),
]

FINISH_CHOICE = [
	('medii', 'Medii'),
	('bune', 'Bune'),
]

# TRANSPORT_CHOICE = [
# 	('metrou', 'Metrou'),
# 	('tramvai', 'Tramvai'), 
# 	('autobuz', 'Autobuz'),
# ]

ZONA_TYPE_CHOICE = [
	('medii', 'medii'),
	('sub medie', 'Sub medie'),
	('above average', 'De vârstă medie/medii sau peste medie'),
	('medium age', 'De varsta medie'),
]

CONST_DENSITY_CHOICE = [ 
	('mare', 'Mare'),
	('medie', 'Medie'),
]

PROP_SIZE_CHOICE = [
	('medie', 'Medie'),
	('mare', 'Mare'),
	('mica', 'Mica'),
]

EXPOSURE_CHOICE = [
	('3', '3-9 luni'),
	('6','6-12 luni'),
	('12', 'peste 12 luni'),
]

LIQUIDITY_CHOICE = [ 
	('buna', 'Buna'),
	('medie', 'Medie'),
	('slaba', 'Slaba'),
]

TRANSACTIONS_CHOICE = [
	('mediu','Mediu'),
	('mare','Mare'),
	('redus', 'Redus'),
]

EXPOSURE_PERIOD_CHOICE = [
	('scurte', 'Scurte'),
	('lungi', 'Lungi'),
]

FILE_CHOICE = [
	('map', 'Hartalocalizare'),
	('photography', 'Fotografii'),
	('document', 'Documente'),
]



# COMPARABLE PROPERTY CHOICES 
MOBILA_CHOICE = [
	('nemobilat','Nemobilat'),
	('partial','Partial mobilat'), 
	('complet', 'Complet mobilat'),
]

AVAILABLE_DATA_CHOICE = [
	('oferta','Oferta'),
	('tranzactie', 'Tranzactie'),
]

PROPERTY_RIGHTS_CHOICE = [
	('deplin', 'Deplin'), 
	('partial', 'Partial'),
]

FINANCING_CONDITION_CHOICE = [
	('normale', 'Normale'),
]

SALE_CONDITION_CHOICE = [
	('independente', 'Independente'),
]

#after purchase expenditure
APE_CHOICE = [
	('da', 'Da'),
	('nu', 'Nu'),
]