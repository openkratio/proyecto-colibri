# coding=utf-8

from tastypie.bundle import Bundle
from tastypie import fields
from tastypie.exceptions import ApiFieldError


class OptimizedToOneField(fields.ToOneField):
    def dehydrate(self, bundle, **kwargs):
        """
            This modified field, allow to include resource_uri of related
            resources without doing another database query.

            Using select_related() in resource.meta.queryset also avoids
            doing extra queries for each object, can be used instead
            of this class
        """
        if not self.full:
            pk = getattr(bundle.obj, self.attribute + "_id", None)
            if not pk:
                if not self.null:
                    raise ApiFieldError(
                        """The model '%r' has an empty attribute '%s'
                        and doesn't allow a null value.""" %
                        (bundle.obj, self.attribute))
                return None
            # just create a temporal object with only PK
            temporal_class = type('TemporalModel', (object,), {'pk': pk})
            temporal_obj = temporal_class()

            # from this point, is almost the same stuff that tastypie does.
            self.fk_resource = self.get_related_resource(temporal_obj)
            fk_bundle = Bundle(
                obj=temporal_obj, request=bundle.request)
            return self.dehydrate_related(fk_bundle, self.fk_resource)

        return super(OptimizedToOneField, self).dehydrate(bundle, **kwargs)
