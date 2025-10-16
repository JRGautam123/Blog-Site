from django.db import models
from django.utils.text import slugify
from django_quill.fields import QuillField
from django.contrib.auth import get_user_model


User = get_user_model()

class Category(models.Model):
    name=models.CharField(max_length=100,unique=True)
    slug=models.SlugField(unique=True,blank=True)

    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug=slugify(self.name)
        super().save(*args,**kwargs)

    def __str__(self):
        return "{}".format(self.name)

class Post(models.Model):
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    slug=models.SlugField(unique=True,blank=True)
    title=models.CharField(max_length=255)
    excerpt=models.CharField(max_length=300)
    image=models.ImageField(upload_to='post_images',blank=True,null=True,default="default-background/defalut-background.jpeg")
    content=QuillField()
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    date=models.DateTimeField(auto_now=True)

    
    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug=slugify(self.title)
        
        
            base_slug=self.slug
            counter=1
            
            while Post.objects.filter(slug=self.slug).exists():
                self.slug= "{}-{}".format(base_slug,counter)
                counter+=1
        if self.id:
            self.slug=slugify(self.title)
        super().save(*args,**kwargs)

    def __str__(self):
        return "{}".format(self.title)
    
class Comments(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    comment=models.TextField()
    parent_id=models.ForeignKey('Comments', on_delete=models.CASCADE,null=True,blank=True)
    date=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user}-{self.post} {self.comment}"
    

    def get_all_descendents(self):
        childrens=Comments.objects.filter(parent_id=self)
        all_descendents=list(childrens)
        for child in childrens:
            all_descendents.extend(child.get_all_descendents())
        return all_descendents
        



class Like(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    post=models.ForeignKey(Post ,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user}-{self.post}"
