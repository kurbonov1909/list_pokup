import logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.contrib.auth.models import User
from .models import History, Store, Purchase

# Logger sozlash
logger = logging.getLogger(__name__)

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_user_agent(request):
    return request.META.get('HTTP_USER_AGENT', '')

def create_history(user, action, model_type, instance=None, description='', ip_address=None, user_agent=''):
    try:
        History.objects.create(
            user=user,
            action=action,
            model_type=model_type,
            object_id=instance.id if instance else None,
            object_repr=str(instance) if instance else '',
            description=description,
            ip_address=ip_address,
            user_agent=user_agent
        )
        logger.info(f"History created: {action} - {model_type} - {description}")
    except Exception as e:
        logger.error(f"Error creating history: {e}")
        # Xatolik yuz bersa, logga yozamiz lekin davom etamiz
        pass

@receiver(user_logged_in)
def user_login(sender, request, user, **kwargs):
    create_history(
        user=user,
        action='login',
        model_type='auth',
        description=f"'{user.username}' foydalanuvchisi tizimga kirdi",
        ip_address=get_client_ip(request),
        user_agent=get_user_agent(request)
    )

@receiver(user_logged_out)
def user_logout(sender, request, user, **kwargs):
    if user:
        create_history(
            user=user,
            action='logout',
            model_type='auth',
            description=f"'{user.username}' foydalanuvchisi tizimdan chiqdi",
            ip_address=get_client_ip(request),
            user_agent=get_user_agent(request)
        )

@receiver(post_save, sender=Store)
def store_created(sender, instance, created, **kwargs):
    if created:
        # Admin orqali qo'shilganda user ni aniqlash
        try:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            admin_user = User.objects.filter(is_superuser=True).first()
        except Exception as e:
            logger.error(f"Error finding admin user: {e}")
            admin_user = None
            
        create_history(
            user=admin_user,
            action='create',
            model_type='store',
            instance=instance,
            description=f"'{instance.name}' magazini yaratildi"
        )

@receiver(post_save, sender=Purchase)
def purchase_created(sender, instance, created, **kwargs):
    if created:
        create_history(
            user=instance.user,
            action='create',
            model_type='purchase',
            instance=instance,
            description=f"'{instance.store.name}' magazinasiga {instance.quantity} dona xarid qo'shildi. Jami: {instance.total_cost} so'm"
        )

@receiver(post_save, sender=User)
def user_created(sender, instance, created, **kwargs):
    if created:
        # Yangi foydalanuvchi yaratilganda admin user ni aniqlash
        try:
            admin_user = User.objects.filter(is_superuser=True).exclude(id=instance.id).first()
        except Exception as e:
            logger.error(f"Error finding admin user for user creation: {e}")
            admin_user = None
            
        create_history(
            user=admin_user,
            action='create',
            model_type='user',
            instance=instance,
            description=f"'{instance.username}' foydalanuvchisi yaratildi. Role: {'Admin' if instance.is_superuser else 'Staff' if instance.is_staff else 'User'}"
        )

@receiver(post_delete, sender=Store)
def store_deleted(sender, instance, **kwargs):
    # Admin orqali o'chirilganda admin user ni aniqlash
    try:
        admin_user = User.objects.filter(is_superuser=True).first()
    except Exception as e:
        logger.error(f"Error finding admin user for store deletion: {e}")
        admin_user = None
        
    create_history(
        user=admin_user,
        action='delete',
        model_type='store',
        instance=instance,
        description=f"'{instance.name}' magazini o'chirildi"
    )

@receiver(post_delete, sender=Purchase)
def purchase_deleted(sender, instance, **kwargs):
    # Xarid o'chirilganda admin user ni aniqlash
    try:
        admin_user = User.objects.filter(is_superuser=True).first()
    except Exception as e:
        logger.error(f"Error finding admin user for purchase deletion: {e}")
        admin_user = None
        
    create_history(
        user=admin_user,
        action='delete',
        model_type='purchase',
        instance=instance,
        description=f"'{instance.store.name}' magazinasidagi xarid o'chirildi. Jami: {instance.total_cost} so'm"
    )

@receiver(post_delete, sender=User)
def user_deleted(sender, instance, **kwargs):
    # Foydalanuvchi o'chirilganda admin user ni aniqlash (o'zi o'chirmasligi uchun)
    try:
        admin_user = User.objects.filter(is_superuser=True).exclude(id=instance.id).first()
    except Exception as e:
        logger.error(f"Error finding admin user for user deletion: {e}")
        admin_user = None
        
    create_history(
        user=admin_user,
        action='delete',
        model_type='user',
        instance=instance,
        description=f"'{instance.username}' foydalanuvchisi o'chirildi"
    )
