from django.db import IntegrityError

from rest_framework import serializers

from .models import CategoryModel


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = ['id', 'name', 'icon_name', 'transaction_type', 'icon_fg_color', 'icon_bg_color',
                  'is_default', 'created_time', 'updated_time']
        read_only_fields = ['id', 'created_time', 'updated_time']


class BatchCategorySerializer(serializers.ListSerializer):
    child = CategorySerializer()

    def create(self, validated_data):
        account = self.context['account']
        categories = []
        for item in validated_data:
            if CategoryModel.objects.filter(
                    account=account,
                    name=item['name'],
                    transaction_type=item['transaction_type']
            ).exists():
                raise serializers.ValidationError("دسته بندی با این مشخصات موجود است.")

            categories.append(CategoryModel(**item, account=account))

        try:
            return CategoryModel.objects.bulk_create(categories)
        except IntegrityError:
            raise serializers.ValidationError("خطایی به هنگام ساخت دسته بندی ها رخ داد.")


class BatchCategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = ['id', 'name', 'icon_name', 'transaction_type', 'icon_fg_color', 'icon_bg_color',
                  'is_default', 'created_time', 'updated_time']
        read_only_fields = ['id', 'created_time', 'updated_time']
        list_serializer_class = BatchCategorySerializer


class CategoryUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = ['id', 'name', 'icon_name', 'transaction_type', 'icon_fg_color', 'icon_bg_color',
                  'is_default', 'created_time', 'updated_time']
        read_only_fields = ['id', 'is_default', 'created_time', 'updated_time']

    def validate(self, data):
        if self.instance and self.instance.is_default:
            raise serializers.ValidationError("Default categories cannot be edited.")
        return data


class CategoryDeleteSerializer(serializers.Serializer):
    ids = serializers.ListField(child=serializers.IntegerField(), required=True, write_only=True)

    def validate_ids(self, value):
        if not value:
            raise serializers.ValidationError("The 'ids' field cannot be empty.")
        return value
