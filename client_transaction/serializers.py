from rest_framework import serializers
from .models import TransactionModel
from .signals import update_financial_sources_on_save


class TransactionSerializer(serializers.ModelSerializer):
    is_fee = serializers.BooleanField(default=False)

    class Meta:
        model = TransactionModel
        fields = [
            'id', 'transaction_type', 'category', 'source', 'amount',
            'transaction_level', 'is_fee', 'description', 'date', 'time',
            'created_time'
        ]
        read_only_fields = ['id', 'created_time']

    def validate(self, attrs):
        category = attrs.get('category')
        transaction_type = attrs.get('transaction_type')
        source = attrs.get('source')

        if category and transaction_type:
            if category.transaction_type != transaction_type:
                raise serializers.ValidationError({
                    'category': 'این دسته بندی برای این نوع تراکنش مناسب نمی باشد.'
                })

        user = self.context['request'].user
        if source and source.account.profile.user != user:
            raise serializers.ValidationError({
                'source': 'شما نمی‌توانید برای منبع مالی که متعلق به شما نیست، تراکنش انجام دهید.'
            })

        return attrs


class BatchTransactionSerializer(serializers.ListSerializer):
    child = TransactionSerializer()

    def create(self, validated_data):
        transactions = [TransactionModel(**item) for item in validated_data]

        created_transactions = TransactionModel.objects.bulk_create(transactions)
        for transaction in created_transactions:
            update_financial_sources_on_save(sender=TransactionModel, instance=transaction, created=True)

        return created_transactions

    def update(self, instances, validated_data):
        instance_mapping = {instance.id: instance for instance in instances}
        updated_instances = []

        for data in validated_data:
            transaction_id = data.get('id')
            transaction = instance_mapping.get(transaction_id)

            if transaction:
                for attr, value in data.items():
                    setattr(transaction, attr, value)
                transaction.save()
                updated_instances.append(transaction)

        return updated_instances


class BatchTransactionModelSerializer(serializers.ModelSerializer):
    is_fee = serializers.BooleanField(default=False)

    class Meta:
        model = TransactionModel
        fields = [
            'id', 'transaction_type', 'category', 'source', 'amount',
            'transaction_level', 'is_fee', 'description', 'date', 'time',
            'created_time'
        ]
        read_only_fields = ['id', 'created_time']
        list_serializer_class = BatchTransactionSerializer

    def validate(self, attrs):
        category = attrs.get('category')
        transaction_type = attrs.get('transaction_type')
        source = attrs.get('source')

        if category and transaction_type:
            if category.transaction_type != transaction_type:
                raise serializers.ValidationError({
                    'category': 'این دسته بندی برای این نوع تراکنش مناسب نمی باشد.'
                })

        user = self.context['request'].user
        if source and source.account.profile.user != user:
            raise serializers.ValidationError({
                'source': 'شما نمی‌توانید برای منبع مالی که متعلق به شما نیست، تراکنش انجام دهید.'
            })

        return attrs


class TransactionDeleteSerializer(serializers.Serializer):
    ids = serializers.ListField(child=serializers.IntegerField(), required=True, write_only=True)

    def validate_ids(self, value):
        if not value:
            raise serializers.ValidationError("لیست تراکنش ها نمیتواند خالی باشد.")
        return value
