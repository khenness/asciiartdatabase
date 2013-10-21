from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

# Create your models here.

#Next job is public profiles
#Then linking art to Artists
#
#
#
#

# Artist class will go here
class Artist(models.Model):
	user 		= models.OneToOneField(User)
	birthday	= models.DateField()
	name 		= models.CharField(max_length=100)
	slug		= models.SlugField(unique=True, blank=True)
	liked 		= models.ManyToManyField('Art', blank=True, related_name='list_of_liked_arts')
	disliked 	= models.ManyToManyField('Art', blank=True, related_name='list_of_disliked_arts')

	def __unicode__(self):
		return self.user.username
	#	return self.name

#tutorial said to comment this out for now				
#def create_artist_user_callback(sender, instance, **kwargs):
#	artist, new = Artist.objects.get_or_create(user=instance)
#post_save.connect(create_artist_user_callback, User)


#south tutorial http://www.djangopro.com/2011/01/django-database-migration-tool-south-explained/
#south is currently uninstalled
#link for dropping all tables in the database: http://stackoverflow.com/questions/2286276/how-do-i-drop-a-table-from-sqlite3-in-django
class Art(models.Model):
	title		= models.CharField(max_length=200, validators=[RegexValidator(regex='^.+$', message='You must have at least one letter in your title', code='nomatch')]) #Implement this line along with other changes when we drop the database
	slug		= models.SlugField(unique=True)
	drawing		= models.TextField(blank=True)
	creator		= models.ForeignKey('Artist') 
	created_at  = models.DateTimeField(auto_now_add=True)
	upvotes		= models.IntegerField(null=True, blank=True, default=0)
	downvotes	= models.IntegerField(null=True, blank=True, default=0)
	score		= models.IntegerField(null=True, blank=True, default=0)
	thumbnail	= models.ImageField(upload_to="images/artthumbs/")
	
	def __unicode__(self):
		return self.title
		

	