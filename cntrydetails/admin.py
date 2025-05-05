from django.contrib import admin
from .models import (
    Language,
    Currency,
    Region,
    Subregion,
    Continent,
    Country,
    CountryName,
    Demonym,
    Border,
    Capital,
    CountryFlag,
    CountryCoatOfArms,
    CountryPostalCode,
    InternationalDialing,
    CountryCurrency,
    CountryLanguage,
    TopLevelDomain,
    AlternativeSpelling,
    Timezone,
    CarSign,
    GiniIndex
)

admin.site.register(Language)
admin.site.register(Currency)
admin.site.register(Region)
admin.site.register(Subregion)
admin.site.register(Continent)
admin.site.register(Country)
admin.site.register(CountryName)
admin.site.register(Demonym)
admin.site.register(Border)
admin.site.register(Capital)
admin.site.register(CountryFlag)
admin.site.register(CountryCoatOfArms)
admin.site.register(CountryPostalCode)
admin.site.register(InternationalDialing)
admin.site.register(CountryCurrency)
admin.site.register(CountryLanguage)
admin.site.register(TopLevelDomain)
admin.site.register(AlternativeSpelling)
admin.site.register(Timezone)
admin.site.register(CarSign)
admin.site.register(GiniIndex)

