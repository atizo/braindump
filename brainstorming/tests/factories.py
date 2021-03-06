from brainstorming.models import Brainstorming, Idea
import factory
from factory import fuzzy
from factory.django import DjangoModelFactory


class BrainstormingFactory(DjangoModelFactory):
    FACTORY_FOR = Brainstorming

    question = fuzzy.FuzzyText()
    details = fuzzy.FuzzyText()
    creator_email = factory.Sequence(lambda n: 'john%s@example.org' % n)


class IdeaFactory(factory.Factory):
    FACTORY_FOR = Idea

    brainstorming = factory.SubFactory(BrainstormingFactory)
    title = fuzzy.FuzzyText()
    text = fuzzy.FuzzyText()
