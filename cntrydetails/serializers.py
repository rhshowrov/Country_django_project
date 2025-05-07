from rest_framework import serializers
from .models import (
    Country, CountryName, Currency, CountryCurrency, TopLevelDomain,
    InternationalDialing, CountryLanguage, Language, Demonym,
    CountryFlag, CountryCoatOfArms, CountryPostalCode, GiniIndex, Capital
)

class CountryListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for country listings.
    Only includes basic name fields for efficient list views.
    """
    class Meta:
        model = Country
        fields = ['common_name', 'official_name']


class CountryNameSerializer(serializers.ModelSerializer):
    """
    Serializes localized name variations for countries.
    Includes name type, common/official names, and language reference.
    """
    class Meta:
        model = CountryName
        fields = ['name_type', 'common', 'official', 'language']


class CurrencySerializer(serializers.ModelSerializer):
    """
    Full currency details including code, name, and symbols.
    """
    class Meta:
        model = Currency
        fields = '__all__'


class CountryCurrencySerializer(serializers.ModelSerializer):
    """
    Links countries to their currencies with nested currency details.
    """
    currency = CurrencySerializer()
    
    class Meta:
        model = CountryCurrency
        fields = ['currency']


class TopLevelDomainSerializer(serializers.ModelSerializer):
    """
    Handles country code top-level domains (ccTLDs).
    """
    class Meta:
        model = TopLevelDomain
        fields = ['domain']


class InternationalDialingSerializer(serializers.ModelSerializer):
    """
    International Direct Dialing (IDD) information including root and suffixes.
    """
    class Meta:
        model = InternationalDialing
        fields = ['root', 'suffixes']


class LanguageSerializer(serializers.ModelSerializer):
    """
    Comprehensive language information.
    """
    class Meta:
        model = Language
        fields = '__all__'


class CountryLanguageSerializer(serializers.ModelSerializer):
    """
    Simplified language representation for country context.
    Only includes ISO code and name for efficiency.
    """
    iso_code = serializers.CharField(source='language.iso_code')
    name = serializers.CharField(source='language.name')
    
    class Meta:
        model = CountryLanguage
        fields = ['iso_code', 'name']


class DemonymSerializer(serializers.ModelSerializer):
    """
    Serializes demonyms (what citizens are called) with gender variations.
    """
    class Meta:
        model = Demonym
        fields = ['language', 'male', 'female']


class CountryFlagSerializer(serializers.ModelSerializer):
    """
    Handles all flag-related media and metadata.
    """
    class Meta:
        model = CountryFlag
        fields = ['emoji', 'emoji_unicode', 'png', 'svg', 'alt']


class CountryCoatOfArmsSerializer(serializers.ModelSerializer):
    """
    Serializes national coat of arms images.
    """
    class Meta:
        model = CountryCoatOfArms
        fields = ['png', 'svg']


class CountryPostalCodeSerializer(serializers.ModelSerializer):
    """
    Postal code format and validation pattern.
    """
    class Meta:
        model = CountryPostalCode
        fields = ['format', 'regex']


class GiniIndexSerializer(serializers.ModelSerializer):
    """
    Gini coefficient data with year context.
    """
    class Meta:
        model = GiniIndex
        fields = ['year', 'value']


class CapitalSerializer(serializers.ModelSerializer):
    """
    Capital city information including geocoordinates.
    """
    class Meta:
        model = Capital
        fields = ['name', 'latitude', 'longitude']


class CountryDetailsSerializer(serializers.ModelSerializer):
    """
    Comprehensive country details serializer with all related data.
    Uses optimized field types for different relationships:
    - Nested serializers for complex objects
    - SlugRelatedField for simple foreign key representations
    - ReadOnlyField for single property lookups
    """
    
    # Name variations
    names = CountryNameSerializer(many=True)
    
    # Monetary information
    currencies = CountryCurrencySerializer(many=True)
    
    # Internet domains
    tlds = serializers.SlugRelatedField(
        many=True,
        slug_field='domain',
        read_only=True
    )
    
    # Geographic data
    capital = CapitalSerializer(read_only=True)
    region = serializers.ReadOnlyField(source='region.name')
    subregion = serializers.ReadOnlyField(source='subregion.name')
    continents = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        read_only=True
    )
    
    # Communication info
    idd = InternationalDialingSerializer()
    alt_spellings = serializers.SlugRelatedField(
        many=True,
        slug_field='spelling',
        read_only=True
    )
    
    # Cultural data
    languages = CountryLanguageSerializer(many=True)
    demonyms = DemonymSerializer(many=True)
    
    # Border information (using SerializerMethodField for neighbor codes)
    borders = serializers.SerializerMethodField()
    
    def get_borders(self, obj):
        """Extract neighbor country codes from border relationships"""
        return [border.neighbor.cca3 for border in obj.borders.all()]
    
    # National symbols
    flag = CountryFlagSerializer(read_only=True)
    coat_of_arms = CountryCoatOfArmsSerializer(read_only=True)
    
    # Infrastructure
    postal_code = CountryPostalCodeSerializer(read_only=True)
    timezones = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        read_only=True
    )
    car_signs = serializers.SlugRelatedField(
        many=True,
        slug_field='sign',
        read_only=True
    )
    
    # Socioeconomic data
    gini_indices = GiniIndexSerializer(many=True)

    class Meta:
        model = Country
        fields = '__all__'
        
class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields='__all__'


class CreateUpdateCountrySerializer(serializers.ModelSerializer):
    class Meta:
        model=Country
        fields='__all__'

