from django.db import models

class Vendor(models.Model):
    name = models.CharField(max_length=100, null=True)


    def __str__(self) -> str:
        return self.name
