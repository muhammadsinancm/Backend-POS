from django.db import models
from django.core.validators import MinValueValidator

class Table(models.Model):
    class Status(models.TextChoices):
        
       FREE = "free", "Free"
       OCCUPIED = "occupied", "Occupied"
       BILLING = "billing", "Billing"

    number = models.PositiveIntegerField(unique=True, validators=[MinValueValidator(1)])
    capacity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.FREE)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["number"]
        constraints = [
            models.CheckConstraint(condition=models.Q(number__gte=1), name="table_number_gte_one"),
            models.CheckConstraint(condition=models.Q(capacity__gte=1), name="table_capacity_gte_one")
        ]
    
    def __str__(self):
        return f"Table {self.number}"