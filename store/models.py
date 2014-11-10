from __future__ import division
from django.db import models

EXCHANGE_RATE = 16.5120482
MARGIN = .85


class Category(models.Model):
    name = models.CharField(max_length=128, unique=False)
    image_link = models.URLField()
    parent_category = models.ForeignKey("self", null=True)
    level = models.IntegerField()

    def __unicode__(self):
        return self.name

    def subcategories(self):
        return self.category_set

    def get_path_up(self):
        level = self.level
        path = [self]
        category = self
        while level != 1:
            category = category.parent_category
            path.append(category)
            level -= 1
        path.reverse()
        return path

    def get_path_uri(self):
        path = self.get_path_up()
        return '/'.join(map(lambda cat: str(cat.id), path))


class Product(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField(blank=True)
    code = models.CharField(max_length=50)
    price = models.FloatField()
    quantity = models.IntegerField()
    image_link = models.URLField()
    category = models.ForeignKey(Category)
    total_rating = models.IntegerField(default=0)
    raters = models.IntegerField(default=0)

    def __unicode__(self):
        return "{}: {}x{}".format(self.name,
                                  self.quantity,
                                  self.price)

    def price_ukr(self):
        return int(round(self.price * EXCHANGE_RATE * (1 + MARGIN), 0))

    def get_average_rating(self):
        if self.raters:
            return round(self.total_rating / self.raters, 1)
        else:
            return 0

class Order(models.Model):
    firstname = models.CharField(max_length=128)
    lastname = models.CharField(max_length=128, blank=True)
    phone = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=256)
    date_created = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "{} {} at {}".format(self.firstname,
                                    self.lastname,
                                    self.date_created)


class OrderDetail(models.Model):
    product = models.ForeignKey(Product)
    order = models.ForeignKey(Order)
    quantity = models.IntegerField()

    def __unicode__(self):
        return "pID: {}; oID: {}".format(self.product,
                                         self.order)


class Comment(models.Model):
    author_name = models.CharField(max_length=128)
    date = models.DateTimeField(auto_now=True)
    body = models.TextField()
    product = models.ForeignKey(Product)

    def __unicode__(self):
        return "{} says \'{}\'".format(self.author_name, self.body)

    def get_pretty_datetime(self):
        return self.date.strftime("%d.%m.%Y, %H:%M")
