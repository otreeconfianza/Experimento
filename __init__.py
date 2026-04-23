from otree.api import *


doc = """
Juego de confianza
"""


class C(BaseConstants):
    NAME_IN_URL = 'juego_confianza'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    acepta = models.BooleanField(
        label="Acepto participar en este experimento",
        choices=[[True, "Sí, acepto participar"]],
        widget=widgets.RadioSelect
    )


class Consentimiento(Page):
    form_model = 'player'
    form_fields = ['acepta']

    @staticmethod
    def error_message(player, values):
        if not values['acepta']:
            return "Debes aceptar para continuar."


page_sequence = [Consentimiento]