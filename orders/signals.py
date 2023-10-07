from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from orders.models import Order
from robots.models import Robot


# @receiver(robot_created)
@receiver(post_save, sender=Robot)
def robot_available_notification(sender, instance, **kwargs):
    pass
    subject = "Робот доступен"
    message = f"Добрый день!\nНедавно вы интересовались нашим роботом модели {instance.model}, версии {instance.version}.\nЭтот робот теперь в наличии. Если вам подходит этот вариант, пожалуйста, свяжитесь с нами."
    recipient_list = [order.customer.email for order in Order.objects.filter(robot_serial=instance.serial, status='AD')]
    send_mail(subject=subject, message=message, from_email='testmaildjango87@mail.ru', recipient_list=recipient_list)


@receiver(pre_save, sender=Order)
def create_order(sender, instance, **kwargs):
    robot = Robot.objects.filter(serial=instance.robot_serial).first()
    if not robot:
        subject = "Робот не доступен"
        message = f"Добрый день!\n Заказанный робот не в наличии. При поступлении робота на склад, мы оповестим вас."
        recipient_list = instance.customer.email
        send_mail(subject=subject, message=message, from_email='testmaildjango87@mail.ru',
                  recipient_list=recipient_list)
        instance.status = "AD"
        instance.save()
