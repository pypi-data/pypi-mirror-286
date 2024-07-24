from decimal import Decimal
from typing import TypedDict

from ..models.order import BaseOrder


class CreatePaymentData(TypedDict):
    token: str  # Токен магазина
    orderNumber: str  # Номер (идентификатор) заказа в системе магазина.
    amount: int  # Сумма платежа в копейках.
    currency: int  # Код валюты платежа ISO 4217. 643 - RUB.
    returnUrl: str  # URL перенаправления пользователя в случае успешной оплаты.
    description: str  # Описание заказа в свободной форме.
    language: str  # Язык в кодировке ISO 639-1.
    jsonParams: str  # Блок для передачи дополнительных параметров продавца.


class GetPaymentData(TypedDict):
    token: str  # Токен магазина
    orderId: str  # Номер (идентификатор) заказа в системе магазина.
    language: str  # Язык в кодировке ISO 639-1.


class PaymentCreationData(TypedDict):
    order: BaseOrder
    amount: Decimal
    external_payment_id: str
    payment_link: str
    client_data: str
    provider_data: str
    title: str


class FailedPaymentCreationData(TypedDict):
    order: BaseOrder
    amount: Decimal
    client_data: str
    provider_data: str
    title: str
