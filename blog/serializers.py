from rest_framework import serializers
from blog import models
from author.models import Author
from rest_framework import validators

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Blog
        fields = '__all__'


class BlogCustomSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        print('*** Custom Create data ****')
        return super(BlogCustomSerializer, self).create(validated_data)

    class Meta:
        model = models.Blog
        fields = '__all__'
        # exclude 
        # read_only_fields 
        # depth = 1
        # extra_kwargs = {}
        # read_only
        # validators


class BlogCustom2Serializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        print('*** Custom Update method ***')
        return super(BlogCustom2Serializer, self).update(instance, validated_data)

    class Meta:
        model = models.Blog
        fields = '__all__'


class BlogCustom3Serializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all()
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset=models.Tag.objects.all(), many=True, allow_empty=True
    )
    cover_image = serializers.PrimaryKeyRelatedField(
        queryset=models.CoverImage.objects.all(), 
        validators=[validators.UniqueValidator(models.CoverImage.objects.all())]
    )

    class Meta:
        model = models.Blog
        fields = '__all__'


class BASerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['first_name', 'bio']


# Define related field
class BlogCustom4Serializer(serializers.ModelSerializer):
    author_details = BASerializer(source='author')

    class Meta:
        model = models.Blog
        fields ='__all__'


class BlogCustom5Serializer(serializers.ModelSerializer):
    word_count = serializers.SerializerMethodField()

    def get_word_count(self, obj):
        return len(obj.content.split())

    class Meta:
        model = models.Blog
        fields ='__all__'


class BlogCustom6Serializer(serializers.ModelSerializer):
    def validate_title(self, value):
        print('validate_title method')
        if '_' in value:
            raise serializers.ValidationError('illegal char')
        return value
    
    class Meta:
        model = models.Blog
        fields = '__all__'


def demo_func_validator(attr):
    print('func val')
    if '_' in attr:
        raise serializers.ValidationError('invalid char')
    return attr


class BlogCustom7Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.Blog
        fields = '__all__'
        extra_kwargs = {
            'title': {
                'validators': [demo_func_validator]
            },
            'content': {
                'validators': [demo_func_validator]
            }
        }


class BlogCustom8Serializer(serializers.ModelSerializer):
    def validate(self, attrs):
        if attrs['title'] == attrs['content']:
            raise serializers.ValidationError('Title and content cannot have value')
        return attrs
    
    class Meta:
        model = models.Blog
        fields = '__all__'


def custom_obj_validator(attrs):
    print('custom abject validator')
    if attrs['title'] == attrs['content']:
        raise serializers.ValidationError('Title and content cannot have value')
    return attrs


class BlogCustom9Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.Blog
        fields = '__all__'
        validators = [custom_obj_validator]


# Remove default validators from the DRF Serializer class
class BlogCustom10Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.Blog
        fields = '__all__'
        validators = [custom_obj_validator]


class BlogCustom11Serializer(serializers.ModelSerializer):
    def to_internal_value(self, data):
        print('before validation', data)
        return super().to_internal_value(data)

    class Meta:
        model = models.Blog
        fields = '__all__'


class BlogCustom12Serializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        resp = super().to_representation(instance)
        resp['title'] = resp['title'].upper()
        return resp

    class Meta:
        model = models.Blog
        fields = '__all__'


class CustomPKRelatedField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        req = self.context.get('request', None) #context value
        queryset = super().get_queryset() #retrieve default filter
        if not req:
            return None
        return queryset.filter(user=req.user) #additional filter


class BlogCustom16Serializer(serializers.ModelSerializer):
    tags = CustomPKRelatedField(queryset=models.Tag.objects.all())
    class Meta:
        model = models.Blog
        fields = '__all__'