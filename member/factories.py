# coding=utf-8

import factory
from member.models import Member


class MemberFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Member

    name = factory.Sequence(lambda n: 'Name{0}'.format(n))
    second_name = factory.Sequence(lambda n: 'SecondName{0}'.format(n))
    avatar = factory.LazyAttribute(
        lambda a: 'www.fakeavatar.es/{0}.{1}'.format(
            a.name, a.second_name).lower())
    congress_web = factory.LazyAttribute(
        lambda a: 'www.congreso.es/{0}.{1}'.format(
            a.name, a.second_name).lower())
    email = factory.LazyAttribute(
        lambda a: '{0}.{1}@congreso.es'.format(
            a.name, a.second_name).lower())
    congress_id = factory.Sequence(lambda n: str(n))
    validate = True
