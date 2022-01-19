from .models import Location
from haystack import indexes

class LocationIndex(indexes.SearchIndex, indexes.Indexable):

   text = indexes.CharField(document=True, use_template=True)
   name = indexes.CharField(model_attr="location_name")
   address = indexes.CharField(model_attr="location_address")
   city = indexes.CharField(model_attr="location_city")
   state = indexes.CharField(model_attr="state")

   autocomplete = indexes.EdgeNgramField()



   @staticmethod
   def prepare_autocomplete(obj):
      return " ".join((
            obj.name, obj.address, obj.city, obj.state
        ))

   def get_model(self):
      return Location

   def index_queryset(self, using=None):
      return self.get_model().objects.all()