from django.db import models
from django.utils.text import slugify 
from django.db.models.signals import pre_save
from django.urls import reverse
from . import my_functions
import os, datetime, string, random
from django.utils import timezone
from django.conf import settings
from . import my_functions
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import PIL
from django.utils import crypto
from django.core.files.uploadedfile import InMemoryUploadedFile


        
class course_code(models.Model):
    course = models.ForeignKey("course", on_delete=models.CASCADE)
    code_num = models.CharField("the course code (save this to generate a code):", max_length=50, null=True, blank=True)
    date = models.DateTimeField('publication date')
    has_saved = models.BooleanField('to track saved code', default=False, editable=False)
    is_active = models.BooleanField('tick to activate the code', default=False)

    class Meta:
        verbose_name = 'Course Code'
        verbose_name_plural = 'Course Codes'

    def __str__(self):
        return f'Code for: {self.course.name} - {self.code_num}'

    def save(self, *args, **kwargs):
        if self.has_saved == False:
            self.code_num = f'IFGN#{crypto.get_random_string(10)}{crypto.get_random_string(4)}'
            self.has_saved = True
        else:
            pass
        super(course_code, self).save(*args, **kwargs)
     
        
class course(models.Model):
    COURSE_CURRENCY = [
    ('$', 'USD ($)'),  # US Dollar
    ('€', 'EUR (€)'),  # Euro
    ('£', 'GBP (£)'),  # British Pound
    ('₦', 'NGN (₦)'),  # Nigerian Naira
    ('¥', 'JPY (¥)')   # Japanese Yen
]
    COURSE_CATEGORIES = [
    ('Programming', 'Programming'),
    ('Design', 'Design'),
    ('Marketing', 'Marketing'),
    ('Business', 'Business'),
    ('Data Science', 'Data Science'),
]
    name = models.CharField('name of the course:', max_length=200, unique=True)
    des = models.TextField('description of the Course:', default="Add a nice description of the Course here.")
    tutors = models.ManyToManyField('staff')
    num_students = models.SmallIntegerField("Number of Students", default=0)
    num_views = models.IntegerField("Number of views", default=0)
    price = models.SmallIntegerField("Course price:", default=0)
    image = models.ImageField('course image:', upload_to='course-images/')
    p_type = models.CharField('select course category:', max_length=20, choices=COURSE_CATEGORIES)
    vidfile = models.FileField("Course video:", upload_to="course-video/")
    date = models.DateTimeField('publication date')
    is_img_edited = models.BooleanField('to track edited images', default=False)
    is_published = models.BooleanField('click this to publish image', default=False)
    
    class Meta:
        ordering = ['-date'] 
        verbose_name = 'Our Course'
        verbose_name_plural = 'Our Courses'
        
    def __str__(self):
        return self.name 
  
  
        
class member(models.Model):
    '''Post Nominal Designators for each membership category of the INSTITUTE OF FORENSIC GRAPHOLOGY, NIGERIA:

Membership Categories and Post Nominal Designators:

1. *Doctoral Fellow (DFIFG)*
Doctoral Fellow, Institute of Forensic Graphology

*2. Senior Fellow (SFIFG)*
Senior Fellow, Institute of Forensic Graphology

 *3. Fellow (FIFG)* Fellow, Institute of Forensic Graphology  

*4. *Associate Fellow (AFIFG)*
Associate Fellow, Institute of Forensic Graphology

*5. *Research Fellow(RFIFG)*
Research Fellow, Institute of Forensic Graphology

*6. *Member (MIFG)*: Member , Institute of Forensic Graphology

*7. *Associate Member (AMIFG)*: Associate Member , Institute of  Forensic IGraphology

*8. Graduate Member( GMIFG)*
Graduate Member, Institute of Forensic Graphology

*9. Student Member ( SMIFG)*
Student Member, Institute of Forensic Graphology

*10. Corporate Member( CMIFG)*
Corporate Member, Institute of Forensic Graphology

*11. Corporate Fellow ( CFIFG)*
Corporate Fellow, Institute of Forensic Graphology'''
    COURSE_CATEGORIES = [
    ('Doctoral Fellow (DFIFG)', 'Doctoral Fellow (DFIFG)'),
    ('Senior Fellow (SFIFG)', 'Senior Fellow (SFIFG)'),
    ('Fellow (FIFG)', 'Fellow (FIFG)'),
    ('Associate Fellow (AFIFG)', 'Associate Fellow (AFIFG)'),
    ('Research Fellow (RFIFG)', 'Research Fellow (RFIFG)'),
    ('Member (MIFG)', 'Member (MIFG)'),
    ('Associate Member (AMIFG)', 'Associate Member (AMIFG)'),
    ('Graduate Member (GMIFG)', 'Graduate Member (GMIFG)'),
    ('Student Member (SMIFG)', 'Student Member (SMIFG)'),
    ('Corporate Member (CMIFG)', 'Corporate Member (CMIFG)'),
    ('Corporate Fellow (CFIFG)', 'Corporate Fellow (CFIFG)'),
]
    name = models.CharField('full name of member:', max_length=200, unique=True)
    title = models.CharField('member\'s title:', max_length=70)
    des = models.TextField('biography of member:')
    m_type = models.CharField('Membership Categories and Post Nominal Designators:', max_length=200, choices=COURSE_CATEGORIES)
    image = models.ImageField('member image:', upload_to='member-images/')
    vidfile = models.FileField("Member Certificate:", upload_to="member-files/")
    date = models.DateTimeField('publication date:')
    is_img_edited = models.BooleanField('to track edited images', default=False)
    is_published = models.BooleanField('click this to publish member:', default=False)
    
    class Meta:
        ordering = ['-date'] 
        verbose_name = 'Our Institute Member'
        verbose_name_plural = 'Our Institute Members'
        
    def __str__(self):
        return self.name 

 
class g_image(models.Model):
    name = models.CharField('name of image:', null=False, blank=False, max_length=150)
    visit = models.BigIntegerField('number of clicks', default=0)
    image = models.ImageField('your main image', upload_to='ifgn-images/', null=True, blank=True)
    thumbnail = models.ImageField('image thumbnail, (do not add this)', upload_to='ifgn-thumbnail/', null=True, blank=True)
    date = models.DateTimeField('publication date')
    is_img_edited = models.BooleanField('track edited images', default=False)

    class Meta:
        ordering = ['-date'] 
        verbose_name = 'IFGN Image'
        verbose_name_plural = 'IFGN Images'

    def was_published_recently(self):
        return self.date >= timezone.now() - datetime.timedelta(days=1)
      
    def __str__(self):
        return f'{self.name} --- IFGN Image'  
    
    def save(self, *args, **kwargs):
        self.slug_name = slugify(self.name)
        if self.is_img_edited == False:
            if self.image:
                thumb_img = Image.open(self.image)
                thumb_img = thumb_img.convert("RGB")

                # renaming image...
                img = Image.open(self.image)
                img_io = BytesIO()
                img.save(img_io, format='PNG', quality=50)
                self.thumbnail = InMemoryUploadedFile(img_io, None, f'ifgn#{crypto.get_random_string(26)}.png', 'image/png', None, None)

                # adding thumbnail...
                i = Image.open(self.image)
                i.thumbnail((180, 180), PIL.Image.Resampling.LANCZOS)
                i_io = BytesIO()
                i.save(i_io, format='PNG', quality=50)
                self.thumbnail = InMemoryUploadedFile(i_io, None, f'thumbnail{crypto.get_random_string(20)}.png', 'image/png', None, None)

                self.is_img_edited = True
            else:
                pass
        super(g_image, self).save(*args, **kwargs)

 
    
class staff(models.Model):
    name = models.CharField('staffs name', null=False, blank=False, max_length=50)
    bio = models.TextField('staffs biography', null=False, blank=False)
    country = models.CharField('staff\'s country', max_length=300, default='Nigeria')
    visit_count = models.BigIntegerField('number of visit', default=0)
    picture = models.ImageField('staff image', upload_to='staffpics', null=True, blank=True)
    image2 = models.ImageField('staff image2 ', upload_to='staffpics', null=True, blank=True)
    image3 = models.ImageField('staff image3 ', upload_to='staffpics', null=True, blank=True)
    channel = models.URLField('youtube channel link', null=True, blank=True)
    instagram_link = models.URLField('instagram profile link', null=True, blank=True)
    twitter_link = models.URLField('twitter profile link', null=True, blank=True)
    fb_link = models.URLField('facebook profile link', null=True, blank=True)
    website_link = models.URLField('website profile link', null=True, blank=True)

    def __str__(self):
        return self.name    
  
    def get_absolute_url(self):
         return reverse('ifgnapp:staff', kwargs={'st_id': self.id, 'slug':slugify(self.name)})     
 
       
class post(models.Model):
    article_category = [
    ('Health', 'Health'),
    ('Event', 'Event'),
    ('Lifestyle', 'Lifestyle'),
    ('Travel', 'Travel'),
    ('Empowerment', 'Empowerment'),
    ('Gist', 'Gist'),
    ('Review', 'Review'),
    ('Our_Review', 'Our_Review'),
    ('Social', 'Social'),
    ('Finance', 'Finance'),
    ('Business', 'Business'),
    ('Food', 'Food'),
    ('Education', 'Education'),
    ('Culture', 'Culture'),
    ('Sponsorship', 'Sponsorship'),
    ]
    post_type = [
        ('Articles', 'Articles'),
        ('Tips', 'Tips'),
        ('News', 'News'),
        ('Reviews', 'Reviews'),
        ('Education', 'Education'),
        ('Entertainment', 'Entertainment'),
    ]
    
    
    autor = models.ForeignKey('staff', on_delete=models.PROTECT)
    name = models.CharField('name of the article', max_length=200, unique=True)
    s_title = models.TextField('the search title of the article, make the title descriptive and simple, this is how google and other search engines will define your page.', null=False, blank=False)
    title = models.TextField('title of the article, make the title descriptive and simple', null=False, blank=False)
    meta = models.TextField('description of this article, make sure you describe this article properly and also add what people may ask google to get this article, this is how google and other search engines will see your post, please include what you think people will be searching for to see your post', null=False, blank=False)
    content1 = models.TextField('The main article body one, write a good and correct article with proper descriptions and refference. \n \n To create tags and format your text use ## followed by the format you want. \n \n Examples are: \n \n ##h1, ##h2, ##h3, and ##h4 will make a header for you to add it use ##h2 Your_header_text ##eh2, this will make a header with the Your_header_text inside it. To make a paragraph use ##pr your_text ##pr, to make some text bold use ##b your_text ##eb, below are the list of all possible formats \n \n \n ##b your_text ##eb to bold text. \n \n ##it your_text ##eit to make text italic. \n \n ##pr your_text ##epr to make a text paragraph. \n \n ##h2 your_text ##eh2 to make a header 2. \n \n ##h3 your_text ##eh3 to make a header 3 \n \n ##qt your_text ##eqt to mke a quote from a text. \n \n ##b your_text ##eb to bold text. \n \n ##b your_text ##eb to bold text. \n \n ##dv your_text ##edv to make a div. \n \n ##sp your_text ##esp to make a span. \n \n ##nl to break your sentence adding spaces below and above it. \n \n To make a list you need to add the type of list you want followed by the lists, Exmample: \n ##olis (ordered list) or ##ulis (for unordered list) \n \n ##lis Your_first_list_text ##elis \n \n ##lis Your_secound_list_text ##elis, add as many list as you want and close it with ##eolis (end  ordered list) \n \n or #eulis (to end unordered list). \n \n You can use this same format in the article body two and three below. \n \n \n Always save and review your article, if you added the format properly it wil all change to the disered tag and if it still display as you added it then you made a mistake, review and change it untill it display corectly.', null=False, blank=False)
    content2 = models.TextField('The article number body two, you can add this if the article is a bit lenghty.', null=True, blank=True)
    content3 = models.TextField('Third article, you can add this if the article is a very long story that it can\'t fit to the first and secound page', null=True, blank=True)
    category = models.CharField('select the category you wish to classify this post under',
        max_length=20,
        choices=article_category, default='Gists'
    )
    post_type = models.CharField('please select a proper type for this post',
        max_length=50,
        choices=post_type, default='News'
    )
    pub_date = models.DateTimeField('publication date')
    visit = models.BigIntegerField('number of visits', default=0)
    image1 = models.ImageField('image number 1', upload_to='post-images/', null=True, blank=True)
    photo_cred1 = models.CharField('Photo credit one', max_length=200, blank=True, null=True)
    image2 = models.ImageField('image number 2', upload_to='post-images/', null=True, blank=True)
    photo_cred2 = models.CharField('Photo credit two', max_length=200, blank=True, null=True)
    frame = models.TextField('embeded contents, like youtube videos, or social media posts.', null=True, blank=True)
    is_img_edited = models.BooleanField('to track edited images', default=False)
    is_published = models.BooleanField('click this to publish your article', default=False)
    thumbnail = models.ImageField('image thumbnail, do not add this', upload_to='article-thumbnail/', null=True, blank=True)
    graph_img = models.ImageField('new png image, do not add this it will be auto-generated.', upload_to='post-graph-img/', null=True, blank=True)
    slug_name = models.SlugField('url of the content, do not add this', max_length=250, null=True, unique=True)
    tags = models.TextField('tags: [Keywords, names, or places that appears on the article.] Ex: "Ugochukwu, Withubb, St. Mary\'s Hospital, Enugu, etc."', blank=True, null=True)
    has_uploaded = models.BooleanField('for Api Upload, do not check this', default=False)
    search_str = models.TextField('for searching the article', blank=True, null=True)
    read_time = models.CharField('read time:', blank=True, null=True, max_length=300)
    helpful_rate = models.IntegerField('helpful ratings:', default=0)
    not_helpful_rate = models.IntegerField('not helpful ratings:', default=0)

    class Meta:
        ordering = ['-pub_date'] 
        verbose_name = 'Post and Update'
        verbose_name_plural = 'Posts and Updates'

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
      
    def __str__(self):
        return f'{self.name} --- (Published)' if self.is_published == True else f'{self.name} --- (Drafted)'  

    def save(self, *args, **kwargs):
        # Read time..
        # import readtime
        # txt_1 = self.content1 if self.content1 else ''
        # txt_2 = self.content2 if self.content2 else ''
        # txt_3 = self.content3 if self.content3 else ''
        # post_txt = f'{txt_1} {txt_2} {txt_3}'
        # # print(f'\n Our post text==============\n {post_txt}\n ==================\n')

        # r_time = f"{readtime.of_text(post_txt)}"
        # self.read_time = r_time

        # formating text..
        self.content1 = my_functions.format_txt(self.content1)
        self.content2 = my_functions.format_txt(self.content2)
        self.content3 = my_functions.format_txt(self.content3)

        # slug field..
        self.search_str = f'{self.title}'
        self.slug_name = f'{slugify(self.name)}'
        
        if self.is_img_edited == False:
            if self.image1:
                thumb_img = Image.open(self.image1)
                thumb_img = thumb_img.convert("RGB")
    
                # resizing and loading of image1..
                i = thumb_img
                img_h = i.height-30 if i.height > 400 else i.height-10
                img_w = i.width-30  if i.width > 400 else i.width-10
                i = i.resize((img_w, img_h), PIL.Image.Resampling.LANCZOS)

                i_io = BytesIO()
                i.save(i_io, format='PNG')
                self.image1 = InMemoryUploadedFile(i_io, None, f'{crypto.get_random_string(25)}.jpg', 'image/jpg', None, None)
                self.graph_img = InMemoryUploadedFile(i_io, None, f'{crypto.get_random_string(20)}.png', 'image/png', None, None) 

                 # adding thumbnail...
                i = Image.open(self.image1)
                i.thumbnail((180, 180), PIL.Image.Resampling.LANCZOS)
                i_io = BytesIO()
                i.save(i_io, format='PNG', quality=50)
                self.thumbnail = InMemoryUploadedFile(i_io, None, f'thumbnail{crypto.get_random_string(20)}.png', 'image/png', None, None)

                self.is_img_edited = True

            if self.image2:
                thumb_img = Image.open(self.image2)
                thumb_img = thumb_img.convert("RGB")
            
                # resizing and loading of image2..
                i = thumb_img
                img_h = i.height-20 if i.height > 500 else i.height-10
                img_w = i.width-20  if i.width > 500 else i.width-10
                i = i.resize((img_w, img_h), PIL.Image.Resampling.LANCZOS)

                i_io = BytesIO()
                i.save(i_io, format='PNG')
                self.image2 = InMemoryUploadedFile(i_io, None, f'{crypto.get_random_string(25)}.png', 'image/png', None, None)
                self.is_img_edited = True
        else:
            pass
        super(post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('ifgnapp:post', kwargs={'cnt_str': f'{slugify(self.slug_name)}', 'c_type':slugify(self.post_type)})
 

# contact us model..
class contact_us(models.Model):
    name = models.CharField('name:', max_length=500, null=False, blank=False)
    email = models.CharField("user's email address", max_length=100)
    country = models.CharField('country:', max_length=250)
    msg = models.TextField('user\'s message')
    user_ip = models.CharField('user ip address', max_length=250, null=True, blank=True)
    date = models.DateTimeField('date of request', default=datetime.datetime.utcnow)
    
    class Meta:
        ordering = ['-date']
        verbose_name = 'Contact us'
        verbose_name_plural = 'Contact us'
        
    def __str__(self):
        return f'{self.name} from {self.country} --- sent a msg'


# pages on the website...
class site_page(models.Model):
    page_name = [
        ('contact', 'contact'),
        ('home', 'home'),
        ('about', 'about'),
        ('terms', 'terms'),
    ]
    name = models.CharField('name of the page', max_length=50,
        choices=page_name, default='about', unique=True)
    data = models.TextField('page contents, you can also add HTML tags:', null=True, blank=True)
    image = models.ImageField('page image:', upload_to='photos/', null=True, blank=True)

    def __str__(self):
        return self.name 
        
    class Meta:
        verbose_name = 'Website Page'
        verbose_name_plural = 'Website Pages'

# for generating images for any page article...
class my_image(models.Model):
    name = models.CharField('name of image including the photo credit', max_length=300)
    image = models.ImageField('The image file', upload_to='photos/', null=True, blank=True)
    url = models.TextField('image link: (copy this and add it where you want this image to appear in your article)', null=True, blank=True)
    has_edited_img = models.BooleanField('used to track image that has been edited, do not change this!!', default=False)
    is_link = models.BooleanField('used to track if the link is available!!', default=False)

    def __str__(self):
        return self.name 
    
    class Meta:
        verbose_name = 'Image Link Generator'
        verbose_name_plural = 'Image Link Generators'
        
    def save(self, *args, **kwargs):
        if self.has_edited_img == False:
            # resizing and loading of image..
            if self.image:
                new_img_name = f'wit{crypto.get_random_string(5)}{crypto.get_random_string(18)}.png'
                with Image.open(self.image) as thumb_img:
                    if thumb_img.mode != "RGB":
                
                        # for resizing main image..
                        img_edit = Image.open(self.image)
                        img_h = img_edit.height-100 if img_edit.height > 400 else img_edit.height-10
                        img_w = img_edit.width-100  if img_edit.width > 400 else img_edit.width-10

                        # img_edit = img_edit.resize((img_w, img_h), PIL.Image.Resampling.LANCZOS)

                        new_img_io = BytesIO()
                        img_edit.save(new_img_io, format='PNG', quality=80)
                        self.image = InMemoryUploadedFile(new_img_io, None, new_img_name, 'image/png', None, None)
                    else:
                        # for resizing main image..
                        img_edit = Image.open(self.image)
                        img_h = img_edit.height-100 if img_edit.height > 400 else img_edit.height-10
                        img_w = img_edit.width-100  if img_edit.width > 400 else img_edit.width-10

                        # img_edit = img_edit.resize((img_w, img_h), PIL.Image.Resampling.LANCZOS)

                        new_img_io = BytesIO()
                        img_edit.save(new_img_io, format='JPEG', quality=80)
                        self.image = InMemoryUploadedFile(new_img_io, None, new_img_name, 'image/png', None, None)

            else:
                pass
            self.has_edited_img = True
        else:
            pass        
        super(my_image, self).save(*args, **kwargs)    
    
site_link ='https://ifgn-institute.org'
# for generating image link and image tags to display them.. 
def gen_img_link(sender, instance, *args, **kwargs):
    if instance.is_link == False:
        if instance.image:
            link = f'<aside class="in_post_imgwrapper"> <img style="width:100%; height:auto;" src="{site_link}/media/photos/{instance.image.name}" alt="{instance.name}" loading="lazy"> <span class="img_detail">{instance.name}</span> </aside>'
            instance.url = link
            # print(link)
            instance.is_link = True
        else:
            pass
    else:
        pass
pre_save.connect(gen_img_link, sender=my_image)


# links..
class in_link(models.Model):
    text = models.CharField('text to appear in between the link:', max_length=100)
    link = models.URLField('the url of the link:', max_length=300)
    is_internal = models.BooleanField('click this if this link is from our website:')
    use_this = models.TextField('copy this one and use it, after you have saved the article:', blank=True)
    link_str = models.CharField('identification string, do not add this:', null=True, max_length=100)
    clicks = models.IntegerField('number of clicks on this link:', default=0)

    def __str__(self):
        return self.text
    
    class Meta:
        verbose_name = 'Generated Link'
        verbose_name_plural = 'Generated Links'
        
    
    def save(self, *args, **kwargs):
        if self.link:
            if self.is_internal == True:
                self.use_this = f'<a href="{self.link}">{self.text}</a>'
            else:
                self.use_this = f'<a href="{self.link}" target="_blank" rel="noopener noreferrer">{self.text}</a>'
        else:
            pass
        if self.link_str == None:
            self.link_str = f'wtr#l{crypto.get_random_string(12)}{crypto.get_random_string(7)}'
        else:
            pass
        super(in_link, self).save(*args, **kwargs)


#### Error model class..
class error_log(models.Model):
    msg = models.TextField("the error message")    
    funct = models.CharField('the fuction where the error occoured', max_length=500)
    date = models.DateTimeField('date of the error', default=datetime.datetime.utcnow)
  
    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.msg