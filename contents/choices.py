from djchoices import DjangoChoices, C


class ChoicesMixin:

    class classproperty(object):
        def __init__(self, getter):
            self.getter= getter

        def __get__(self, instance, owner):
            return self.getter(owner)

    @classproperty
    def choice_list(cls):
        return [*zip(*cls.choices)][0]

class ContentTypeChoices(ChoicesMixin, DjangoChoices):
    MOVIE = C('movie')
    TV_SHOW = C("tv show")
    DOCUMENTARY = C("documentary")