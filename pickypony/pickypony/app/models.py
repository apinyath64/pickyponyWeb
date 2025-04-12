from django.db import models
from django.contrib.auth.models import User

class Item(models.Model):
    CATEGORY_CHOICES = [
        ('S', 'เสื้อเชิ้ต'),
        ('SU', 'ชุดสูท'),
        ('T', 'เสื้อท็อป'),
        ('D', 'ชุดเดรส'),
        ('C', 'เสื้อคาร์ดิแกน'),
        ('J', 'กางเกงยีนส์'),
        ('SK', 'กระโปรง'),
        ('SW', 'ชุดว่ายน้ำ'),
        ('B', 'เบลเซอร์'),
        ('JK', 'แจ็คเก็ต'),
        ('H', 'เสื้อฮู้ด'),
        ('SO', 'ถุงเท้า'),
        ('HA', 'เครื่องประดับผม'),
        ('SC', 'ผ้าพันคอ'),
        ('HT', 'หมวก'),
        ('BE', 'เข็มขัด'),
        ('SG', 'แว่นกันแดด'),
        ('BA', 'กระเป๋า')
    ]

    name = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    size = models.CharField(max_length=50, blank=True, null=True)
    color = models.CharField(max_length=50, blank=True, null=True)
    stock = models.PositiveIntegerField()
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='items')

    def __str__(self):
        return self.name
    
    def get_colors(self):
        if self.color:
            return self.color.split(",")
        return []
    
    def get_sizes(self):
        if self.size:
            return self.size.split(",")
        return []
    

class Customer(models.Model):
    CITY_CHOICES = [
        ('BKK', 'Bangkok'),
        ('CNX', 'Chiang Mai'),
        ('CHI', 'Chiang Rai'),
        ('KBI', 'Krabi'),
        ('LPG', 'Lampang'),
        ('LPN', 'Lopburi'),
        ('NPT', 'Nakhon Pathom'),
        ('NRT', 'Nakhon Ratchasima'),
        ('NRN', 'Nakhon Si Thammarat'),
        ('PBI', 'Phetchaburi'),
        ('PHU', 'Phuket'),
        ('PKT', 'Phayao'),
        ('PCH', 'Prachuap Khiri Khan'),
        ('RBR', 'Ratchaburi'),
        ('SGK', 'Samut Prakan'),
        ('SRT', 'Surat Thani'),
        ('UDN', 'Udon Thani'),
        ('UBN', 'Ubon Ratchathani'),
        ('YLA', 'Yala')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=100, choices=CITY_CHOICES)
    mobile = models.IntegerField(default=0)
    zipcode = models.IntegerField()

    def __str__(self):
        return f'{self.name} {self.city}'
    

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    size = models.CharField(max_length=50, blank=True, null=True)
    color = models.CharField(max_length=50, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_cost(self):
        return self.quantity * self.item.discounted_price
    

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    charge_id = models.CharField(max_length=100, blank=True, null=True)
    payment_status = models.CharField(max_length=100, blank=True, null=True)
    paid = models.BooleanField(default=True)



class OrderPlaced(models.Model):
    STATUS_CHOICES = [
        ('Accepted', 'Accepted'),
        ('Packed', 'Packed'),
        ('On The Way', 'On The Way'),
        ('Delivered', 'Delivered'),
        ('Cancel', 'Cancel'),
        ('Pending', 'Pending')  
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    order_date = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, default="")

    @property
    def total_cost(self):
        return self.quantity * self.item.discounted_price
    

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)