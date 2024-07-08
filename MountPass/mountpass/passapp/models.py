from django.db import models


class MyUser(models.Model):
    email = models.CharField(max_length=128, unique=True)
    fam = models.CharField(max_length=128)
    name = models.CharField(max_length=128)
    otc = models.CharField(max_length=128)
    phone = models.IntegerField(unique=True)


class Coord(models.Model):
    latitude = models.DecimalField(max_digits=10, decimal_places=8)
    longitude = models.DecimalField(max_digits=10, decimal_places=8)
    height = models.IntegerField()


class Level(models.Model):
    LEVEL = (
        ('1А', '1А'),
        ('2А', '2А'),
        ('3А', '3А'),
        ('1B', '1Б'),
        ('2B', '2Б'),
        ('3B', '3Б'),
        ('3B*', '3Б*'),

    )
    winter = models.CharField(max_length=3, choices=LEVEL, null=True, blank=True)
    summer = models.CharField(max_length=3, choices=LEVEL, null=True, blank=True)
    autumn = models.CharField(max_length=3, choices=LEVEL, null=True, blank=True)
    spring = models.CharField(max_length=3, choices=LEVEL, null=True, blank=True)


class PerevalAdded(models.Model):
    NEW = 'NW'
    PENDING = 'PN'
    ACCEPTED = 'AC'
    REJECTED = 'RJ'
    STATUS_CHOICES = (
        ('NW', 'New'),
        ('PN', 'Pending'),
        ('AC', 'Accepted'),
        ('RJ', 'Rejected'),
    )

    beauty_title = models.CharField(max_length=128, default="пер.")
    title = models.CharField(max_length=128)
    other_titles = models.CharField(max_length=128)
    connect = models.CharField(max_length=128) #какие локации соединяет
    add_time = models.DateTimeField(auto_now_add=True)
    coord_id = models.OneToOneField(Coord, on_delete=models.CASCADE, related_name='coords')
    author_id = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='author')
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='NEW')
    level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name='level')


class Images(models.Model):
    pereval = models.ForeignKey(PerevalAdded, related_name='images', on_delete=models.CASCADE)
    title = models.CharField(max_length=128, null=True, blank=True)
    image = models.ImageField(upload_to='mountpass/', null=True, blank=True)

