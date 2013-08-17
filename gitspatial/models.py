from django.db import models
from django.contrib.auth.models import User
from django.contrib.gis.db import models as geo_models

from .behaviors import Syncable, Timestampable


class Repo(Syncable, Timestampable, models.Model):
    github_id = models.IntegerField()
    user = models.ForeignKey(User)
    name = models.CharField(max_length=1000)
    full_name = models.CharField(max_length=1000)
    github_private = models.BooleanField()
    synced = models.BooleanField(default=False)

    @property
    def hook_url(self):
        return 'http://gitspatial.com/api/v1/hooks/{0}'.format(self.id)

    def __unicode__(self):
        return self.full_name


class FeatureSet(Syncable, Timestampable, models.Model):
    """
    Represents a GeoJSON file within a GitHub repo
    """
    repo = models.ForeignKey(Repo)
    path = models.CharField(max_length=1000)  # The path for a file in the repo, "fire-hydrants.geojson", "data/geojson/pump-stations.geojson"
    name = models.CharField(max_length=1000)  # The editable name of the feature set, initially the same as path
    synced = models.BooleanField(default=False)  # Just like Repo, not all are synced

    unique_together = ('repo', 'name')

    def __unicode__(self):
        return '{0}/{1}'.format(self.repo.full_name, self.name)


class Feature(geo_models.Model):
    """
    Represents a single feature belonging to a FeatureSet, a GeoJSON Feature
    """
    feature_set = models.ForeignKey(FeatureSet)
    geom = geo_models.GeometryField()
    properties = models.TextField()
    objects = geo_models.GeoManager()

    ordering = ['id']

    def __unicode__(self):
        return '<Feature {0} from {1}>'.format(self.id, self.feature_set)
