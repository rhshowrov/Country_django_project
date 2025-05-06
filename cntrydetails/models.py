from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Language(models.Model):
    """
    Represents a language with its ISO 639-3 standard code.
    Used for country names, demonyms, and other language-specific data.
    """
    iso_code = models.CharField(
        max_length=3,
        primary_key=True,
        help_text="ISO 639-3 language code (3 letters)"
    )
    name = models.CharField(
        max_length=50,
        help_text="Full name of the language in English"
    )
    
    class Meta:
        ordering = ['name']
        verbose_name = "Language"
        verbose_name_plural = "Languages"
    
    def __str__(self):
        return f"{self.name} ({self.iso_code})"

class Currency(models.Model):
    """
    Represents a currency with its ISO 4217 standard code.
    Used for country currency relationships.
    """
    code = models.CharField(
        max_length=3,
        primary_key=True,
        help_text="ISO 4217 currency code (3 letters)"
    )
    name = models.CharField(
        max_length=50,
        help_text="Full name of the currency"
    )
    symbol = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        help_text="Currency symbol if available (e.g., $, €)"
    )
    
    class Meta:
        verbose_name = "Currency"
        verbose_name_plural = "Currencies"
    
    def __str__(self):
        return f"{self.code} ({self.name})"

class Region(models.Model):
    """
    Represents a broad geographical region (e.g., 'Western Europe', 'South America').
    """
    name = models.CharField(
        max_length=50,
        unique=True,
        help_text="Name of the geographical region"
    )
    
    class Meta:
        verbose_name = "Region"
        verbose_name_plural = "Regions"
    
    def __str__(self):
        return self.name

class Subregion(models.Model):
    """
    Represents a subregion within a broader geographical region.
    """
    name = models.CharField(
        max_length=50,
        unique=True,
        help_text="Name of the geographical subregion"
    )
    region = models.ForeignKey(
        Region,
        on_delete=models.PROTECT,
        related_name='subregions',
        help_text="The broader region this subregion belongs to"
    )
    
    class Meta:
        verbose_name = "Subregion"
        verbose_name_plural = "Subregions"
    
    def __str__(self):
        return f"{self.name} ({self.region})"

class Continent(models.Model):
    """
    Represents a continent that countries can belong to.
    A country may belong to multiple continents (e.g., Russia in Europe and Asia).
    """
    name = models.CharField(
        max_length=20,
        unique=True,
        help_text="Name of the continent"
    )
    
    class Meta:
        verbose_name = "Continent"
        verbose_name_plural = "Continents"
    
    def __str__(self):
        return self.name

class Country(models.Model):
    """
    Main model representing a country with all its core attributes.
    """
    class WeekStart(models.TextChoices):
        MONDAY = 'monday', 'Monday'
        TUESDAY = 'tuesday', 'Tuesday'
        WEDNESDAY = 'wednesday', 'Wednesday'
        THURSDAY = 'thursday', 'Thursday'
        FRIDAY = 'friday', 'Friday'
        SATURDAY = 'saturday', 'Saturday'
        SUNDAY = 'sunday', 'Sunday'

    class DrivingSide(models.TextChoices):
        LEFT = 'left', 'Left'
        RIGHT = 'right', 'Right'

    # Names
    common_name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Commonly used name for the country in English"
    )
    official_name = models.CharField(
        max_length=200,
        unique=True,
        help_text="Official formal name of the country in English"
    )

    # Core identifiers
    cca2 = models.CharField(
        max_length=2,
        primary_key=True,
        help_text="ISO 3166-1 alpha-2 country code (2 letters)"
    )
    cca3 = models.CharField(
        max_length=3,
        unique=True,
        help_text="ISO 3166-1 alpha-3 country code (3 letters)"
    )
    ccn3 = models.CharField(
        max_length=3,
        null=True,
        blank=True,
        help_text="ISO 3166-1 numeric country code (3 digits)"
    )
    
    # Status
    independent = models.BooleanField(
        default=False,
        help_text="Whether the country is considered independent"
    )
    un_member = models.BooleanField(
        default=False,
        help_text="Whether the country is a UN member state"
    )
    status = models.CharField(
        max_length=30,
        choices=[
            ('officially-assigned', 'Officially Assigned'),
            ('user-assigned', 'User Assigned')
        ],
        help_text="Status of the country code assignment"
    )
    
    # Geography
    region = models.ForeignKey(
        Region,
        on_delete=models.PROTECT,
        help_text="Primary geographical region of the country"
    )
    subregion = models.ForeignKey(
        Subregion,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='countries',
        help_text="More specific geographical subregion"
    )
    continents = models.ManyToManyField(
        Continent,
        help_text="Continents the country belongs to"
    )
    landlocked = models.BooleanField(
        default=False,
        help_text="Whether the country is landlocked (no coastline)"
    )
    area = models.FloatField(
        null=True,
        blank=True,
        help_text="Total area in square kilometers"
    )
    
    # Coordinates
    latitude = models.FloatField(
        validators=[MinValueValidator(-90), MaxValueValidator(90)],
        help_text="Latitude coordinate of the country's approximate center"
    )
    longitude = models.FloatField(
        validators=[MinValueValidator(-180), MaxValueValidator(180)],
        help_text="Longitude coordinate of the country's approximate center"
    )
    
    # Demographics
    population = models.PositiveBigIntegerField(
        help_text="Estimated total population of the country"
    )
    
    # International organizations
    cioc = models.CharField(
        max_length=3,
        null=True,
        blank=True,
        help_text="International Olympic Committee code"
    )
    fifa = models.CharField(
        max_length=3,
        null=True,
        blank=True,
        help_text="FIFA country code"
    )
    
    # Transportation
    driving_side = models.CharField(
        max_length=5,
        choices=DrivingSide.choices,
        help_text="Side of the road vehicles drive on"
    )
    
    # Time
    start_of_week = models.CharField(
        max_length=9,
        choices=WeekStart.choices,
        default=WeekStart.MONDAY,
        help_text="Day considered the start of the week in this country"
    )
    
    # External references
    google_maps = models.URLField(
        max_length=500,
        help_text="Google Maps link to the country"
    )
    openstreet_maps = models.URLField(
        max_length=500,
        help_text="OpenStreetMap link to the country"
    )
    
    # Metadata
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When this country record was first created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="When this country record was last updated"
    )

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"
        ordering = ['common_name']
        indexes = [
            models.Index(fields=['common_name']),
            models.Index(fields=['official_name']),
            models.Index(fields=['region', 'subregion']),
        ]

    def __str__(self):
        return self.common_name

class CountryName(models.Model):
    """
    Represents alternative names for countries in different languages,
    including both native names and translations.
    """
    class NameType(models.TextChoices):
        NATIVE = 'native', 'Native Name'
        TRANSLATION = 'translation', 'Translation'

    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        related_name='names',
        help_text="Country this name refers to"
    )
    language = models.ForeignKey(
        Language,
        on_delete=models.PROTECT,
        help_text="Language of this name"
    )
    name_type = models.CharField(
        max_length=11,
        choices=NameType.choices,
        help_text="Whether this is a native name or a translation"
    )
    official = models.CharField(
        max_length=200,
        help_text="Official name in this language"
    )
    common = models.CharField(
        max_length=100,
        help_text="Common name in this language"
    )
    
    class Meta:
        unique_together = ('country', 'language', 'name_type')
        verbose_name = "Country Name"
        verbose_name_plural = "Country Names"

    def __str__(self):
        return f"{self.common} ({self.language})"

class Demonym(models.Model):
    """
    Represents what people from a country are called (demonyms) in different languages.
    """
    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        related_name='demonyms',
        help_text="Country this demonym refers to"
    )
    language = models.ForeignKey(
        Language,
        on_delete=models.PROTECT,
        help_text="Language of this demonym"
    )
    male = models.CharField(
        max_length=50,
        help_text="Male form of the demonym"
    )
    female = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text="Female form of the demonym if different"
    )
    
    class Meta:
        unique_together = ('country', 'language')
        verbose_name = "Demonym"
        verbose_name_plural = "Demonyms"

    def __str__(self):
        return f"{self.male} ({self.language})"

class Border(models.Model):
    """
    Represents a land border between two countries.
    """
    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        related_name='borders',
        help_text="Country that has this border"
    )
    neighbor = models.ForeignKey(
        Country,
        on_delete=models.PROTECT,
        related_name='bordered_by',
        help_text="Neighboring country on the other side of this border"
    )
    
    class Meta:
        unique_together = ('country', 'neighbor')
        verbose_name = "Border"
        verbose_name_plural = "Borders"

    def __str__(self):
        return f"{self.country.cca3} borders {self.neighbor.cca3}"

class Capital(models.Model):
    """
    Represents a country's capital city with its geographical coordinates.
    """
    country = models.OneToOneField(
        Country,
        on_delete=models.CASCADE,
        related_name='capital',
        help_text="Country this capital belongs to"
    )
    name = models.CharField(
        max_length=100,
        help_text="Name of the capital city"
    )
    latitude = models.FloatField(
        validators=[MinValueValidator(-90), MaxValueValidator(90)],
        help_text="Latitude coordinate of the capital"
    )
    longitude = models.FloatField(
        validators=[MinValueValidator(-180), MaxValueValidator(180)],
        help_text="Longitude coordinate of the capital"
    )
    
    class Meta:
        verbose_name = "Capital"
        verbose_name_plural = "Capitals"
    
    def __str__(self):
        return f"{self.name} ({self.country.cca3})"

class CountryFlag(models.Model):
    """
    Contains all flag-related information for a country.
    """
    country = models.OneToOneField(
        Country,
        on_delete=models.CASCADE,
        related_name='flag',
        help_text="Country this flag represents"
    )
    emoji = models.CharField(
        max_length=15,
        help_text="Flag emoji representation"
    )
    emoji_unicode = models.CharField(
        max_length=20,
        help_text="Unicode code points for the flag emoji"
    )
    png = models.URLField(
        max_length=500,
        help_text="URL to PNG version of the flag"
    )
    svg = models.URLField(
        max_length=500,
        help_text="URL to SVG version of the flag"
    )
    alt = models.TextField(
        blank=True,
        help_text="Alternative text description of the flag"
    )
    
    class Meta:
        verbose_name = "Flag"
        verbose_name_plural = "Flags"
    
    def __str__(self):
        return f"Flag of {self.country}"

class CountryCoatOfArms(models.Model):
    """
    Contains coat of arms information for a country.
    """
    country = models.OneToOneField(
        Country,
        on_delete=models.CASCADE,
        related_name='coat_of_arms',
        help_text="Country this coat of arms represents"
    )
    png = models.URLField(
        max_length=500,
        help_text="URL to PNG version of the coat of arms"
    )
    svg = models.URLField(
        max_length=500,
        help_text="URL to SVG version of the coat of arms"
    )
    
    class Meta:
        verbose_name = "Coat of Arms"
        verbose_name_plural = "Coats of Arms"
    
    def __str__(self):
        return f"Coat of Arms of {self.country}"

class CountryPostalCode(models.Model):
    """
    Contains postal code/zip code information for a country.
    """
    country = models.OneToOneField(
        Country,
        on_delete=models.CASCADE,
        related_name='postal_code',
        help_text="Country this postal code format applies to"
    )
    format = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Human-readable format of postal codes"
    )
    regex = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        help_text="Regular expression pattern for valid postal codes"
    )
    
    class Meta:
        verbose_name = "Postal Code Format"
        verbose_name_plural = "Postal Code Formats"
    
    def __str__(self):
        return f"Postal codes for {self.country}"

class InternationalDialing(models.Model):
    """
    Contains international direct dialing (IDD) information for a country.
    """
    country = models.OneToOneField(
        Country,
        on_delete=models.CASCADE,
        related_name='idd',
        help_text="Country this dialing information applies to"
    )
    root = models.CharField(
        max_length=5,
        help_text="Root international dialing prefix (e.g., '+1')"
    )
    suffixes = models.JSONField(
        help_text="List of possible suffixes after the root prefix"
    )
    
    class Meta:
        verbose_name = "International Dialing"
        verbose_name_plural = "International Dialings"
    
    def __str__(self):
        return f"IDD for {self.country}"

class CountryCurrency(models.Model):
    """
    Represents a currency used in a country.
    Many-to-many relationship between countries and currencies.
    """
    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        related_name='currencies',
        help_text="Country where this currency is used"
    )
    currency = models.ForeignKey(
        Currency,
        on_delete=models.PROTECT,
        help_text="Currency used in this country"
    )
    
    class Meta:
        unique_together = ('country', 'currency')
        verbose_name = "Country Currency"
        verbose_name_plural = "Country Currencies"
    
    def __str__(self):
        return f"{self.country} uses {self.currency}"

class CountryLanguage(models.Model):
    """
    Represents a language spoken in a country.
    Many-to-many relationship between countries and languages.
    """
    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        related_name='languages',
        help_text="Country where this language is spoken"
    )
    language = models.ForeignKey(
        Language,
        on_delete=models.PROTECT,
        help_text="Language spoken in this country"
    )
    
    class Meta:
        unique_together = ('country', 'language')
        verbose_name = "Country Language"
        verbose_name_plural = "Country Languages"
    
    def __str__(self):
        return f"{self.language} spoken in {self.country}"

class TopLevelDomain(models.Model):
    """
    Represents a top-level internet domain (TLD) associated with a country.
    """
    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        related_name='tlds',
        help_text="Country this TLD belongs to"
    )
    domain = models.CharField(
        max_length=10,
        help_text="Top-level domain (e.g., '.us')"
    )
    
    class Meta:
        unique_together = ('country', 'domain')
        verbose_name = "Top Level Domain"
        verbose_name_plural = "Top Level Domains"
    
    def __str__(self):
        return f"{self.domain} for {self.country}"

class AlternativeSpelling(models.Model):
    """
    Represents alternative spellings or forms of a country's name.
    """
    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        related_name='alt_spellings',
        help_text="Country this alternative spelling refers to"
    )
    spelling = models.CharField(
        max_length=200,
        help_text="Alternative spelling or form of the country's name"
    )
    
    class Meta:
        unique_together = ('country', 'spelling')
        verbose_name = "Alternative Spelling"
        verbose_name_plural = "Alternative Spellings"
    
    def __str__(self):
        return f"'{self.spelling}' for {self.country}"

class Timezone(models.Model):
    """
    Represents a timezone used in a country.
    """
    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        related_name='timezones',
        help_text="Country where this timezone is used"
    )
    name = models.CharField(
        max_length=20,
        help_text="Timezone name (e.g., 'UTC-05:00')"
    )
    
    class Meta:
        unique_together = ('country', 'name')
        verbose_name = "Timezone"
        verbose_name_plural = "Timezones"
    
    def __str__(self):
        return f"{self.name} in {self.country}"

class CarSign(models.Model):
    """
    Represents vehicle registration codes (license plate identifiers) for a country.
    """
    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        related_name='car_signs',
        help_text="Country this vehicle code belongs to"
    )
    sign = models.CharField(
        max_length=10,
        help_text="International vehicle registration code"
    )
    
    class Meta:
        unique_together = ('country', 'sign')
        verbose_name = "Car Sign"
        verbose_name_plural = "Car Signs"
    
    def __str__(self):
        return f"{self.sign} for {self.country}"

class GiniIndex(models.Model):
    """
    Represents Gini coefficient measurements for a country over time.
    The Gini coefficient measures income inequality (0 = perfect equality, 100 = maximum inequality).
    """
    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        related_name='gini_indices',
        help_text="Country this Gini measurement applies to"
    )
    year = models.PositiveSmallIntegerField(
        help_text="Year of the Gini coefficient measurement"
    )
    value = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Gini coefficient value (0-100 scale)"
    )
    
    class Meta:
        unique_together = ('country', 'year')
        verbose_name = "Gini Index"
        verbose_name_plural = "Gini Indices"
    
    def __str__(self):
        return f"{self.country} ({self.year}): {self.value}"