from mongoengine import fields
from rest_framework import serializers
from rest_framework.fields import (  # NOQA # isort:skip
    BooleanField, CharField, ChoiceField, DateField, DateTimeField, DecimalField,
    DictField, DurationField, EmailField, Field, FileField, FilePathField, FloatField,
    HiddenField, HStoreField, IPAddressField, ImageField, IntegerField, JSONField,
    ListField, ModelField, MultipleChoiceField, ReadOnlyField,
    RegexField, SerializerMethodField, SlugField, TimeField, URLField, UUIDField,
)


class MongoSerializer(serializers.ModelSerializer):
    serializer_field_mapping = {
        fields.BooleanField: BooleanField,
        fields.DateField: DateField,
        fields.DateTimeField: DateTimeField,
        fields.DecimalField: DecimalField,
        fields.EmailField: EmailField,
        fields.FileField: FileField,
        fields.FloatField: FloatField,
        fields.ImageField: ImageField,
        fields.URLField: URLField,
        fields.UUIDField: UUIDField,
    }
