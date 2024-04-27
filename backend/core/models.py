from typing import Any
from django.db import models
from userauths.models import User, Profile, user_directory_path
from shortuuid.django_fields import ShortUUIDField
from django.utils.text import slugify
from django.utils.html import mark_safe
import shortuuid

# Create your models here.
VISIBILITY = (
    ("Only me", "Only me"),
    ("Everyone", "Everyone"),
)

BOOK_REQUEST = (
    ('pending', 'pending'),
    ('accepted', 'accepted'),
    ('rejected', 'rejected'),

)

NOTIFICATION_TYPE = (
    ('Book request', 'Book request'),
    ('Partner request accepted', 'Partner request accepted'),
    ('New comment', 'New comment'),
    ('Comment Liked', 'Comment Liked'),
)


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=500, blank=True, null=True)
    author = models.CharField(max_length=500, blank=True, null=True)
    image = models.ImageField(upload_to=user_directory_path, null=True, blank=True)
    publication_year = models.IntegerField(null=True, blank=True)
    genre = models.CharField(max_length=500, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    video = models.FileField(upload_to=user_directory_path, null=True, blank=True)
    visibility = models.CharField(max_length=10, default="Everyone", choices=VISIBILITY)
    pid = ShortUUIDField(length=7, max_length=25, alphabet="abcdefghijklmnopqrstuvxyz123")
    likes = models.ManyToManyField(User, blank=True, related_name="likes")
    active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True)
    views = models.PositiveIntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ["-date"]
        verbose_name_plural = "Post"
    
    def save(self, *args, **kwargs):
        uuid_key = shortuuid.uuid()
        uniqueid = uuid_key[:4]
        if self.slug == "" or self.slug == None:
            self.slug = slugify(self.title) + "-" + str(uniqueid.lower())
        super(Post, self).save(*args, **kwargs)

    def thumbnail(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" object-fit:"cover" style="border-radius: 5px;" />' % (self.image))
    
    def gallery_images(self):
        return Event.objects.filter(post=self)
    
    def title_len_count(self):
        return len(self.title)
    
    def galley_img_count(self):
        return Event.objects.filter(post=self).count()

    def post_comments(self):
        comments = Comment.objects.filter(post=self, active=True).order_by("-id")
        return comments
    
    def post_comments_count(self):
        comments_count = Comment.objects.filter(post=self, active=True).count()
        return comments_count


class SavedPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.post.title

    class Meta:
        verbose_name = 'Saved Post'
        verbose_name_plural = "Saved Posts"
        db_table = "saved_post"


class Bookshelf(models.Model):
    post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to="gallery", null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.post)
    
    class Meta:
        verbose_name_plural = 'Bookshelves'

    def thumbnail(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" object-fit:"cover" style="border-radius: 5px;" />' % (self.image))


class BookExchangeRequest(models.Model):
    sender_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="sender_post")
    receiver_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="receiver_post")
    pid = ShortUUIDField(length=7, max_length=25, alphabet="abcdefghijklmnopqrstuvxyz")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="request_sender")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="request_receiver")
    status = models.CharField(max_length=100, default="pending", choices=BOOK_REQUEST)
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender.username} - {self.receiver.username} - {self.status}'
    
    class Meta:
        verbose_name_plural = 'BookRequest'


class BookExchangePartner(models.Model):
    pid = ShortUUIDField(length=7, max_length=25, alphabet="abcdefghijklmnopqrstuvxyz")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    partner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="partner")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.post)
    
    class Meta:
        verbose_name_plural = 'BookExchangePartner'


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.CharField(max_length=500, blank=True ,null=True)
    date = models.DateTimeField(auto_now_add=True)
    cid = ShortUUIDField(length=7, max_length=25, alphabet="abcdefghijklmnopqrstuvxyz123")
    likes = models.ManyToManyField(User, blank=True, related_name="comment_likes")
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name_plural = "Comment"

    def comment_replies(self):
        comment_replies = ReplyComment.objects.filter(comment=self, active=True)
        return comment_replies


class ReplyComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    reply = models.CharField(max_length=500, blank=True ,null=True)
    date = models.DateTimeField(auto_now_add=True)
    cid = ShortUUIDField(length=7, max_length=25, alphabet="abcdefghijklmnopqrstuvxyz123")
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username
    
    class Meta:
        ordering = ["-date"]
        verbose_name_plural = "Reply Comment"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="noti_user")
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="noti_sender")
    post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True, blank=True, related_name="noti_post")
    comment = models.ForeignKey(Comment, on_delete=models.SET_NULL, null=True, blank=True, related_name="noti_comment")
    notification_type = models.CharField(max_length=100, choices=NOTIFICATION_TYPE, default="none")
    is_read = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    nid = ShortUUIDField(length=10, max_length=25, alphabet="abcdefghijklmnopqrstuvxyz")
    
    class Meta:
        ordering = ["-date"]
        verbose_name_plural = "Notification"

    def __str__(self):
        return f"{self.user.username} - {self.notification_type}"


class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    members = models.ManyToManyField(User, blank=True, related_name="members")
    image = models.ImageField(upload_to=user_directory_path, null=True, blank=True)
    title = models.CharField(max_length=500, blank=True ,null=True)
    description = models.TextField(blank=True ,null=True)
    video = models.FileField(upload_to=user_directory_path, null=True, blank=True)
    visibility = models.CharField(max_length=10, default="everyone", choices=VISIBILITY)
    gid = ShortUUIDField(length=7, max_length=25, alphabet="abcdefghijklmnopqrstuvxyz123")
    active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True)
    views = models.PositiveIntegerField(default=0)
    date = models.DateTimeField()

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ["-date"]
        verbose_name_plural = "Event"
    
    def save(self, *args, **kwargs):
        uuid_key = shortuuid.uuid()
        uniqueid = uuid_key[:4]
        if self.slug == "" or self.slug == None:
            self.slug = slugify(self.title) + "-" + str(uniqueid.lower())
        super(Event, self).save(*args, **kwargs) 

    def thumbnail(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" object-fit:"cover" style="border-radius: 5px;" />' % (self.image))
    
    def memeber_count(self):
        return self.members.all().count()
    

class EventPost(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=500, blank=True ,null=True)
    image = models.ImageField(upload_to=user_directory_path, null=True, blank=True)
    visibility = models.CharField(max_length=10, default="everyone", choices=VISIBILITY)
    pid = ShortUUIDField(length=7, max_length=25, alphabet="abcdefghijklmnopqrstuvxyz123")
    likes = models.ManyToManyField(User, blank=True, related_name="group_post_likes")
    active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    views = models.PositiveIntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ["-date"]
        verbose_name_plural = "Event Post"
    
    def save(self, *args, **kwargs):
        uuid_key = shortuuid.uuid()
        uniqueid = uuid_key[:4]
        if self.slug == "" or self.slug == None:
            self.slug = slugify(self.title) + "-" + str(uniqueid.lower())
        super(EventPost, self).save(*args, **kwargs) 

    def thumbnail(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" object-fit:"cover" style="border-radius: 5px;" />' % (self.image))


class Page(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    followers = models.ManyToManyField(User, blank=True, related_name="page_followers")
    image = models.ImageField(upload_to=user_directory_path, null=True, blank=True)
    name = models.CharField(max_length=500, blank=True ,null=True)
    description = models.TextField(blank=True ,null=True)
    video = models.FileField(upload_to=user_directory_path, null=True, blank=True)
    visibility = models.CharField(max_length=10, default="everyone", choices=VISIBILITY)
    active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True)
    views = models.PositiveIntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    gid = ShortUUIDField(length=7, max_length=25, alphabet="abcdefghijklmnopqrstuvxyz123")

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ["-date"]
        verbose_name_plural = "Page"
    
    def save(self, *args, **kwargs):
        uuid_key = shortuuid.uuid()
        uniqueid = uuid_key[:4]
        if self.slug == "" or self.slug == None:
            self.slug = slugify(self.name) + "-" + str(uniqueid.lower())
        super(Page, self).save(*args, **kwargs) 

    def thumbnail(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" object-fit:"cover" style="border-radius: 5px;" />' % (self.image))
    
    def followers_count(self):
        return self.followers.all().count()
