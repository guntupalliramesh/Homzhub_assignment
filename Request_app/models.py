# from django.db import models
#
# class UserRegistration(models.Model):
#     id = models.IntegerField(primary_key=True)
#     name = models.CharField(max_length=50,blank=True,default='')
#     email = models.EmailField(max_length=50,blank=True)


from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class StateMaster(models.Model):
    StateName = models.TextField(default=1)
    StateCode = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.StateName


class RequestTypeMaster(models.Model):
    RequestType = models.TextField(default="")

    def __str__(self):
        return self.RequestType


class StatusMaster(models.Model):
    StatusType = models.TextField(default="")

    def __str__(self):
        return self.StatusType


class UserRequest(models.Model):
    RequestedUser = models.ForeignKey(User, on_delete=models.CASCADE, related_name='UserRequest_user', default="")
    RequestType = models.ForeignKey(RequestTypeMaster, on_delete=models.CASCADE, related_name='UserRequest_type')
    RequestDesc = models.TextField(default="")
    City = models.TextField(default="")
    State = models.ForeignKey(StateMaster, on_delete=models.CASCADE, related_name='UserRequest_state')
    Pincode = models.IntegerField(default=0)
    PhoneCode = models.TextField(default="")
    Phone = models.IntegerField(default="")
    Status = models.ForeignKey(StatusMaster, on_delete=models.CASCADE, related_name='UserRequest_Status')
    Remark = models.TextField(default="")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.RequestedUser) + "-" + str(self.RequestType)


class ScrappedResult(models.Model):
    Title = models.TextField(default="")
    Link = models.TextField(default="")
    PubDate = models.TextField(default="")

    def __str__(self):
        return self.Title
