from django.db import models
from base.models import BaseModel
from django.utils.text import slugify
from accounts.models import User

# Create your models here.

class Category(BaseModel):
    category_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True,null=True,blank=True)
    category_img = models.ImageField(upload_to = "categories")

    def save(self,*args,**kwargs):
        self.slug = slugify(self.category_name)
        super(Category, self).save(*args, **kwargs)
    def __str__(self):
        return self.category_name

class Colorvariant(BaseModel):
    color = models.CharField(max_length=100)
    price = models.IntegerField(null=True)

    def __str__(self):
        return self.color


class Sizevariant(BaseModel):
    size = models.CharField(max_length=100)
    price = models.IntegerField(null=True)

    def __str__(self):
        return self.size

class Coupon(BaseModel):
    coupon_code = models.CharField ( max_length = 18 )
    is_expired = models.BooleanField ( default = False )
    discount_price = models.IntegerField(default=100 )
    minimum_amount = models.IntegerField(default=500 )

class Product(BaseModel):
    product_name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,related_name='products')
    price = models.IntegerField()
    desc = models.TextField()
    quantity = models.IntegerField(null=True, blank=True)
    slug = models.SlugField(unique=True,null=True,blank=True)
    img = models.ImageField(upload_to="product")
    color = models.ManyToManyField(Colorvariant, blank=True)
    size = models.ManyToManyField(Sizevariant, blank=True)

    def save(self,*args,**kwargs):
        self.slug = slugify(self.product_name)
        super(Product, self).save(*args,kwargs)

    def __str__(self):
        return self.product_name

    def get_product_by_size(self,size):
        return self.price + Sizevariant.objects.get(size= size).price
        
    def get_product_by_color(self,color):
        return self.price + Colorvariant.objects.get(color= color).price
    def get_product_name(self):
        return self.product_name
    

class Cart(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart")
    is_paid = models.BooleanField()
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL,blank=True,null=True)
    razorpay_order_id = models.CharField(max_length=100,null=True,blank=True)
    razorpay_payment_id = models.CharField(max_length=100,null=True,blank=True)
    razorpay_payment_signature = models.CharField(max_length=100,null=True,blank=True)

    def get_cart_total(self) :
        cart_items = self.cartitem.all( )
        price = []
        for cart_item in cart_items :
            # price.append(cart_item.get_product_price)
            if cart_item.Colorvariant:
                color_variant_price = cart_item.Colorvariant.price
                price.append(color_variant_price)
            if cart_item.Sizevariant :
                size_variant_price = cart_item.Sizevariant.price
                price.append ( size_variant_price )
            price.append(cart_item.get_product_price())
        if self.coupon:
           
            if sum(price) > self.coupon.minimum_amount:
                return sum(price) - self.coupon.discount_price
                    # print(cart_item.get_product_price)
        # print(price)
        return sum(price)


    

class CartItem(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,related_name="cartitem")
    product  = models.ForeignKey(Product, on_delete=models.SET_NULL,null=True,blank=True,related_name="products")
    quantity = models.IntegerField(default=1)
    Colorvariant = models.ForeignKey(Colorvariant, on_delete=models.SET_NULL,blank=True,null=True)
    Sizevariant = models.ForeignKey(Sizevariant, on_delete=models.SET_NULL,blank=True,null=True)

    def get_product_price(self):
        price = [self.product.price]

        if self.Colorvariant:
            cv_price = self.Colorvariant.price
            price.append(cv_price)
        if self.Sizevariant:
            sv_price = self.Sizevariant.price
            price.append(sv_price)
        
        return sum(price) * self.quantity
    
    def get_product_name(self):
        return self.product.product_name
    def get_product_name(self):
        return self.product.category

    # def __str__(self):
    #     return self.get_product_name

                     

    
    
