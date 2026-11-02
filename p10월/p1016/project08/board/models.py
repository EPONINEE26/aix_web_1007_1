from django.db import models

class Board(models.Model):
    btitle = models.CharField(max_length=1000)
    bfile = models.ImageField(null=True,upload_to='board')

    def __str__(self):
        return f'{self.btitle},{self.bfile}'