from django.db import models


class Group(models.Model):
    name = models.CharField(max_length=30)
    group_id = models.AutoField(primary_key=True)
    admin = models.ForeignKey(
        'auth.user', related_name='group_admin', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name', )
