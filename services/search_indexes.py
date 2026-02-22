from haystack import indexes
from .models import Product

class ProductIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    price = indexes.DecimalField(model_attr='price')
    

    def get_model(self):
        return Product

   