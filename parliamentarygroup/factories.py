# coding=utf-8

import factory

from parliamentarygroup.models import Party, Group, GroupMember
from member.factories import MemberFactory
from term.factories import TermFactory


class PartyFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Party

    name = factory.Sequence(lambda n: 'PartyName_{0}'.format(n))
    web = factory.LazyAttribute(lambda a: 'www.{0}.es/'.format(a.name.lower()))


class GroupFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Group

    name = factory.Sequence(lambda n: 'GroupName_{0}'.format(n))
    acronym = factory.Sequence(lambda n: 'GR{0}'.format(n))
    term = factory.SubFactory(TermFactory)


class GroupMemberFactory(factory.DjangoModelFactory):
    FACTORY_FOR = GroupMember

    group = factory.SubFactory(GroupFactory)
    member = factory.SubFactory(MemberFactory)
    party = factory.SubFactory(PartyFactory)
