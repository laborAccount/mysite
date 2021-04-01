from django.db import models

# Create your models here.
class Test_User_Info(models.Model):
    user_name = models.CharField(max_length = 20)
    user_id = models.CharField(max_length = 50,primary_key = True)
    user_password = models.CharField(max_length = 20)
    user_address = models.CharField(max_length = 100)
    user_birth = models.IntegerField()
    user_call = models.CharField(max_length = 20)
    user_email = models.CharField(max_length = 50)

    def __str__(self):
        return 'user_name=' + self.user_name +  ' user_id=' + self.user_id + " user_password=" + self.user_password + ''' 
        user_address= '''+ self.user_address + ' user_birth=' + self.user_birth + ' user_call=' + self.user_call + ' user_email=' + self.user_email 


class Test_Notice(models.Model):
    regist_id = models.ForeignKey(Test_User_Info, on_delete=models.CASCADE)
    notice_subject = models.CharField(max_length = 50)
    notice_memo = models.CharField(max_length = 3000)
    regist_dt = models.DateField()
 