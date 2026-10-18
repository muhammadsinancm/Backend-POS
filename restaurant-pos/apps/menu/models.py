from django.core.validators import MinValueValidator
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Categories"
        
    def __str__(self):
        return self.name
    
class MenuItem(models.Model):
    category = models.ForeignKey(Category,on_delete=models.PROTECT,related_name="items")
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10,decimal_places=2,validators=[MinValueValidator(0.01)])
    is_available = models.BooleanField(default=True)
    prep_time_min = models.PositiveIntegerField(blank=True)
    image = models.ImageField(upload_to="menu/",null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["category__name", "name"]
        constraints = [
            models.UniqueConstraint(fields=["category", "name"],name="unique_menu_item_name_per_category"),
            models.CheckConstraint(condition=models.Q(price__gt=0),name="menu_item_price_gt_zero")
        ]
        
    def __str__(self):
        return self.name