from django.db.models import TextChoices

class Currency(TextChoices):
    GEL = 'gel', '₾', 
    EURO = 'euro', '€'
    USD = 'usd', '$'