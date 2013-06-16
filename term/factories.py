# coding=utf-8

# coding=utf-8

import factory
from dateutil.relativedelta import relativedelta

from django.utils import timezone

from term.models import Term


def random_date(years):
    """ generates a random date substracting years """
    return timezone.now() - relativedelta(years=years)


class TermFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Term

    roman = factory.Sequence(lambda n: '{0}'.format(n))
    decimal = factory.LazyAttribute(lambda a: int(a.roman))
    start_date = factory.LazyAttribute(lambda a: random_date(a.decimal))
    end_date = factory.LazyAttribute(lambda a: random_date(a.decimal+1))
