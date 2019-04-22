from django.db import models
from django.contrib.auth.models import User
 
 
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='images/users', verbose_name='Изображение')
    rooms = models.ManyToManyField('Room', blank=True, related_name='users')
    
    def __unicode__(self):
        return self.user
 
    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

class Room(models.Model):
    name = models.CharField(max_length=150)
    admin = models.CharField(max_length=150)

class SkillCategory(models.Model):
    name = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)

class Skill(models.Model):
    name = models.CharField(max_length=150)
    skill_category = models.ForeignKey(SkillCategory, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

class Room_Skill(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)

class UserProfile_Skill(models.Model):
    userprofile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=2, decimal_places=2)
    is_active = models.BooleanField(default=False)