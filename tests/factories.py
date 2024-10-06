import factory

from fast_zero.models import User


class UserFactory(factory.Factory):
    """
    Usamos o Lazy para usar os atributos que já foram definidos.
    """

    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'test{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@test.com')
    password = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')
