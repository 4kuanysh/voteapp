from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.utils.text import slugify
from time import time


def gen_slug(s):
    new_slug = slugify(s, allow_unicode=True)
    return new_slug + '-' + str(int(time()))

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    skills = models.ManyToManyField('Skill', blank=True, through='UserSkill', related_name='users')
    avatar = models.ImageField(upload_to='img/avatars/', blank=True, default='img/avatars/user.png')
    
    def __str__(self):
        return "{}".format(self.user.username)


class Room(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, blank=True, unique=True)
    members = models.ManyToManyField(User, blank=True, through='RoomUser', related_name='rooms')
    skills = models.ManyToManyField('Skill', blank=True, through='RoomSkill', related_name='rooms')
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)

    def get_absolute_url(self):
        return reverse('room_detail_url', kwargs={'slug': self.slug})
    
    def get_add_member_url(self):
        return reverse('add_member_url', kwargs={'slug': self.slug})

    def get_settings_url(self):
        return reverse('room_settings_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return "{}".format(self.name)
        
class RoomUser(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return "{} - {}".format(self.room.name, self.user.username)
        
class Skill(models.Model):
    name = models.CharField(max_length=150)
    category = models.ForeignKey('CategorySkill', on_delete=models.CASCADE)

    def __str__(self):
        return "{}".format(self.name)

class CategorySkill(models.Model):
    name = models.CharField(max_length=150)
    def __str__(self):
        return "{}".format(self.name)

class RoomSkill(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return "{} - {}".format(self.room.name, self.skill.name)

class UserSkill(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=5, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "{} - {}".format(self.user, self.skill.name)