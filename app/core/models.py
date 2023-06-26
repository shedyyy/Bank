from django.db import models

# Create your models here.



#extend the user model

tx_types = (('deposit', 'deposit'), ('transfer', 'transfer'))


statuses = (('pending', 'pending'), ('approved', 'approved'), ('rejected', 'rejected'))
class Transaction(models.Model):

    creator = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='creator', null=True, blank=True)
    tx_type = models.CharField(max_length=255, null=True, blank=True, choices=tx_types)
    description = models.TextField(null=True, blank=True)
    amount = models.FloatField(null=True, blank=True)
    sender = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='sender', null=True, blank=True)
    receiver = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='receiver', null=True, blank=True)
    status = models.CharField(max_length=255, choices=statuses, default="pending",)

    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.tx_type + ' ' + str(self.amount) + ' ' + str(self.created_at)
    