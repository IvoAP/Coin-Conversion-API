from pydantic import BaseModel, Field, field_validator


class ConvertInput(BaseModel):
    price: float = Field(..., gt=0, description="Amount to convert")
    to_currencies: list[str]

    @field_validator('to_currencies', mode='before')
    @classmethod
    def validate_currency_code(cls, v: list[str]) -> list[str]:
        for currency in v:
            if len(currency) != 3 or not currency.isalpha() or not currency.isupper():
                raise ValueError('Each currency code must be a 3-letter uppercase string (e.g., USD, EUR)')
        return v