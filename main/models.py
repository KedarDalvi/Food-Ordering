from django.db import models
from django.contrib.auth.models import  User
import datetime

class detail(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE ,max_length=100)
    phone_no=models.CharField(max_length=10)
    category=models.CharField(max_length=10 , default=0)
    address=models.TextField()
    first_login=models.BooleanField(default=0)
    dict_item =models.TextField(null=True)

    def __str__(self):
        return self.user.email

class Category(models.Model):
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name

        
class MenuItem(models.Model):
    name=models.CharField(max_length=100)
    stars = models.DecimalField(default=3.5,max_digits=5 ,decimal_places=2)
    description=models.TextField()
    price=models.DecimalField(max_digits=5 ,decimal_places=2)
    image=models.ImageField(upload_to="menu_images/")
    category=models.ForeignKey(Category ,on_delete=models.CASCADE ,default=1)

    def _str__(self):
        return self.name
    @staticmethod
    def itmes_by_id(ids):
        return MenuItem.objects.filter(id__in=ids)
#https://github.com/virendrapatel62/eshopdjango/blob/master/store/templates/cart.html
#https://www.youtube.com/watch?v=I4v_6ll7wdw&list=PLdBwVRHjcI__NWxctXUSLz1Gg2Mb-B-O-&index=48

class Order(models.Model):
    item = models.ForeignKey(MenuItem , on_delete=models.CASCADE)
    item_name = models.CharField(max_length=200,null=True)
    user =models.ForeignKey(detail,on_delete=models.CASCADE)
    username=models.CharField(max_length=200,null=True)
    name=models.CharField( null =True ,max_length=150)
    email=models.CharField(null= True,max_length=200)
    phone_no =models.CharField(null=True , max_length=10)
    address = models.TextField(null=True)
    quantity = models.IntegerField(default=1)
    ordered_date=models.DateTimeField(default=datetime.datetime.today)
    price=models.DecimalField(max_digits=9 , decimal_places=2)

    class Meta:
        ordering = ['-ordered_date']

    @staticmethod
    def get_orders_by_user(profile):
        return Order.objects.filter(user = profile)
    
    