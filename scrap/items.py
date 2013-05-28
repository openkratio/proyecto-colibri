# coding=utf-8
# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.contrib.djangoitem import DjangoItem
import member.models as members


class MemberItem(DjangoItem):
    django_model = members.Member

    def save(self, commit=True):
        print "saving"
        """
            In next version of scrapy, self.instance will be available
            with a Djangomodel object, the code must be modified

                if self.instance.pk == self.django_model._meta.get_default():
                    _saved_obj = self.django_model.__class__.objects.filter(
                    congress_id=self['congress_id']).values_list(
                        'id', flat=True)
                self.instance.pk = _saved_obj[0] if _saved_obj else \
                    self.django_model._meta.get_default()
            return super(self.__class__, self).save(commit)
        """
        # get saved PK from DB to update data or create a new row
        _saved_obj = self.django_model.objects.filter(
            congress_id=self['congress_id']).values_list(
                'id', flat=True)
        modelargs = dict((k, self.get(k)) for k in self._values
                         if k in self._model_fields)
        model = self.django_model(**modelargs)
        model.pk = _saved_obj[0] if _saved_obj else \
            self.django_model._meta.pk.get_default()
        if commit:
            model.save()
        return model
