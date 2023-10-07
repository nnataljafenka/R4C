from django.db import models

from customers.models import Customer


class Order(models.Model):
    STATUS_LIST = [('AD', "Awaiting Delivery"),
                   ('AC', "Awaiting Customer"),
                   ('F', 'Finished'),
                   ('C', 'Created')]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    robot_serial = models.CharField(max_length=5, blank=False, null=False)
    # Cтатус заказа
    status = models.CharField(max_length=5, blank=False, null=False, default='C', choices=STATUS_LIST)
