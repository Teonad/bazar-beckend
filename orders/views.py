import stripe

from http import HTTPStatus
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.urls import reverse, reverse_lazy
from django.conf import settings

from common.views import TitleMixin
from orders.forms import OrderForm
from products.models import Basket

stripe.api_key = settings.STRIPE_SECRET_KEY


class SuccessTemplateView(TitleMixin, TemplateView):
    template_name = 'orders/success.html'
    title = 'Store - Спасибо за заказ!'

class CanceledTemplateView(TemplateView):
    template_name = 'orders/canceled.html'



class OrderCreateView(TitleMixin, CreateView):
    template_name = 'orders/order-create.html'
    form_class = OrderForm
    success_url = reverse_lazy('orders:order_create')
    title = 'Bazar - Оформление заказа'

    def post(self, request, *args, **kwargs):
        super(OrderCreateView, self).post(request, *args, **kwargs)
        baskets = Basket.objects.filter(user=self.request.user)

        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': 'price_1NT5jRGMsRljqZsjIHijDjd2',
                    'quantity': 1,
                },
                {
                    'price': 'price_1NT5jRGMsRljqZsjRiXa2bp1',
                    'quantity': 1,
                },
                {
                    'price': 'price_1NT5jPGMsRljqZsjjxTo0iJn',
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:order_success')),
            cancel_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:order_canceled')),
        )
        return HttpResponseRedirect(checkout_session.url, status=HTTPStatus.SEE_OTHER)


    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super(OrderCreateView, self).form_valid(form)