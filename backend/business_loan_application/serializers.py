from rest_framework import serializers

from .accounting_softwares.constants import SUPPORTED_SOFTWARES
from .accounting_softwares.adapters.utils.validation_utils import validate_year, DataValidationError


class BaseSerializer(serializers.Serializer):
    @property
    def custom_full_errors(self):
        errors_messages = []
        for field_name, field_errors in self.errors.items():
            for field_error in field_errors:
                error_message = f"{field_name}: {field_error}"
                errors_messages.append(error_message)
        return {'errors': errors_messages}


class LoanDetailsSerializer(BaseSerializer):
    name = serializers.CharField(min_length=3, max_length=100)
    year_established = serializers.CharField(min_length=4, max_length=4)
    summary_of_profit_or_loss = serializers.FloatField()
    loan_amount = serializers.FloatField()
    accounting_software_key = serializers.ChoiceField(SUPPORTED_SOFTWARES)

    def validate_year_established(self, value):
        try:
            return str(validate_year(value))
        except DataValidationError as inst:
            raise serializers.ValidationError(str(inst))
