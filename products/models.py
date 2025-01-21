from django.db import models

class AbstractNameModel(models.Model):
    class Meta:
        abstract = True

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Category(AbstractNameModel):
    parent = models.ForeignKey('self',  on_delete=models.CASCADE, null=True, blank=True)


class SearchWord(AbstractNameModel):
    pass


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, related_name='products')# category_id = 1
    search_words = models.ManyToManyField(SearchWord, blank=True)

    title = models.CharField(max_length=255)
    text = models.TextField(null=True, blank=True)
    price = models.FloatField(default=0)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title

    def search_word_list(self):
        return [i.name for i in self.search_words.all()]

STARS = (
    (1, '*'),
    (2, '* *'),
    (3, '* * *'),
    (4, '* * * *'),
    (5, '* * * * *')
)


class Review(models.Model):
    text = models.TextField()
    stars = models.IntegerField(choices=STARS, default=5)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')


    def __str__(self):
        return self.text