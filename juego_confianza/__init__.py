from otree.api import *
import random


doc = """
Experimento con 2 fases implementadas como 2 rounds.

Round 1 / Fase 1:
- Mitad de participantes: Normas sociales
- Mitad de participantes: Trust game
- Dentro de trust: mitad A y mitad B

Round 2 / Fase 2:
- Quienes estuvieron en trust pasan a rol A
- Quienes estuvieron en normas pasan a rol B
- Se emparejan nuevamente A con B

Uso de WaitPage:
- B espera a que A decida
- B solo decide si A continuó
"""


class C(BaseConstants):
    NAME_IN_URL = 'juego_confianza'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 2

    ENDOWMENT = cu(2)
    OUTSIDE_OPTION_EACH = cu(1)
    DOUBLED_AMOUNT = cu(4)
    SHARE_AMOUNT = cu(2)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    tipo_grupo = models.StringField()  # 'trust' o 'normas' en round 1; 'fase2' en round 2

    def a_player(self):
        for p in self.get_players():
            if p.rol == 'A':
                return p
        return None

    def b_player(self):
        for p in self.get_players():
            if p.rol == 'B':
                return p
        return None


class Player(BasePlayer):
    # -------------------------
    # Asignación experimental
    # -------------------------
    condicion_inicial = models.StringField(blank=True)   # 'trust' o 'normas'
    rol = models.StringField(blank=True)                 # 'A', 'B', 'Normas'

    # -------------------------
    # Consentimiento
    # -------------------------
    acepta = models.BooleanField(
        label="Acepto participar en este experimento",
        choices=[[True, "Sí, acepto participar"]],
        widget=widgets.RadioSelect,
        blank=True,
    )

    # -------------------------
    # Fase 1 - trust
    # -------------------------
    creencia_a_fase1 = models.StringField(
        choices=[
            ['0_20', '0–20%'],
            ['20_40', '20–40%'],
            ['40_60', '40–60%'],
            ['60_80', '60–80%'],
            ['80_100', '80–100%'],
        ],
        label="¿Qué porcentaje de sujetos B en su sesión cree usted que elegirá COMPARTIR?"
    )

    decision_a_fase1 = models.StringField(
        choices=[
            ['no_continuar', 'NO CONTINUAR: finalizar la actividad y dividir el monto en partes iguales'],
            ['continuar', 'CONTINUAR: entregar el monto al participante B'],
        ],
        label="Elija una de estas dos opciones:"
    )

    creencia_b1_fase1 = models.StringField(
        choices=[
            ['0_20', '0–20%'],
            ['20_40', '20–40%'],
            ['40_60', '40–60%'],
            ['60_80', '60–80%'],
            ['80_100', '80–100%'],
        ],
        label="¿Qué intervalo cree que eligió el Participante A?"
    )

    creencia_b2_fase1 = models.StringField(
        choices=[
            ['no_continuar', 'NO CONTINUAR y dividir el monto en partes iguales'],
            ['continuar', 'CONTINUAR y entregar el monto al participante B'],
        ],
        label="¿Qué decisión cree usted que tomará el Participante A?"
    )

    creencia_b3_fase1 = models.StringField(
        choices=[
            ['0_20', '0–20%'],
            ['20_40', '20–40%'],
            ['40_60', '40–60%'],
            ['60_80', '60–80%'],
            ['80_100', '80–100%'],
        ],
        label="Estime qué porcentaje de participantes A elegirá CONTINUAR:"
    )

    decision_b_fase1 = models.StringField(
        choices=[
            ['compartir', 'COMPARTIR: dividir el dinero en partes iguales'],
            ['no_compartir', 'NO COMPARTIR: quedarse con la totalidad'],
        ],
        label="Elija una de las siguientes opciones:"
    )

    pago_fase1 = models.CurrencyField(initial=0)

    # -------------------------
    # Fase 1 - normas
    # -------------------------
    norma_no_continuar = models.IntegerField(
        choices=[1, 2, 3, 4],
        label="¿En qué medida considerará la mayoría de la gente que esta acción es socialmente apropiada?"
    )

    norma_continuar_a = models.IntegerField(
        choices=[1, 2, 3, 4],
        label="¿En qué medida considerará la mayoría de la gente que esta acción es socialmente apropiada?"
    )

    norma_b_no_compartir = models.IntegerField(
        choices=[1, 2, 3, 4],
        label="¿En qué medida considerará la mayoría de la gente que esta acción es socialmente apropiada?"
    )

    norma_b_compartir = models.IntegerField(
        choices=[1, 2, 3, 4],
        label="¿En qué medida considerará la mayoría de la gente que esta acción es socialmente apropiada?"
    )

    # -------------------------
    # Fase 2
    # -------------------------
    creencia_a1_fase2 = models.StringField(
        choices=[
            ['0_20', '0–20%'],
            ['20_40', '20–40%'],
            ['40_60', '40–60%'],
            ['60_80', '60–80%'],
            ['80_100', '80–100%'],
        ],
        label="¿Qué porcentaje de participantes A cree que optará por CONTINUAR en esta segunda ronda?"
    )

    creencia_a2_fase2 = models.StringField(
        choices=[
            ['0_20', '0–20%'],
            ['20_40', '20–40%'],
            ['40_60', '40–60%'],
            ['60_80', '60–80%'],
            ['80_100', '80–100%'],
        ],
        label="¿Qué porcentaje de participantes B cree que optará por COMPARTIR en esta segunda ronda?"
    )

    decision_a_fase2 = models.StringField(
        choices=[
            ['no_continuar', 'NO CONTINUAR: finalizar la actividad y dividir el monto en partes iguales'],
            ['continuar', 'CONTINUAR: entregar el monto al participante B'],
        ],
        label="Elija una de las siguientes opciones:"
    )

    decision_b_fase2 = models.StringField(
        choices=[
            ['compartir', 'COMPARTIR: dividir el monto duplicado entre ambos'],
            ['no_compartir', 'NO COMPARTIR: quedarse con la totalidad'],
        ],
        label="Elija una de las siguientes opciones:"
    )

    pago_fase2 = models.CurrencyField(initial=0)

    # -------------------------
    # Cuestionario final
    # -------------------------
    edad = models.IntegerField(label="Edad")
    genero = models.StringField(
        choices=['Mujer', 'Varón', 'Otro', 'Prefiero no responder'],
        label="Género"
    )
    comentario_final = models.LongStringField(blank=True, label="Comentario final (opcional)")

    # -------------------------
    # Auxiliares
    # -------------------------
    def es_normas(self):
        return self.round_number == 1 and self.condicion_inicial == 'normas'

    def es_trust_fase1_A(self):
        return self.round_number == 1 and self.condicion_inicial == 'trust' and self.rol == 'A'

    def es_trust_fase1_B(self):
        return self.round_number == 1 and self.condicion_inicial == 'trust' and self.rol == 'B'

    def es_fase2_A(self):
        return self.round_number == 2 and self.rol == 'A'

    def es_fase2_B(self):
        return self.round_number == 2 and self.rol == 'B'

    def descripcion_asignacion_inicial(self):
        if self.condicion_inicial == 'normas':
            return 'Usted ha sido asignado al Grupo 1: Normas Sociales.'
        elif self.condicion_inicial == 'trust':
            return f'Usted ha sido asignado al Grupo 2: Juego de Confianza. Su rol en la Fase 1 es Participante {self.rol}.'
        return ''

    def descripcion_fase2(self):
        if self.rol == 'A':
            return 'En la Fase 2, usted ha sido asignado al rol de Participante A.'
        elif self.rol == 'B':
            return 'En la Fase 2, usted ha sido asignado al rol de Participante B.'
        return ''


# ----------------------------------------------------------------
# CREACIÓN DE SESIÓN Y FORMACIÓN DE GRUPOS
# ----------------------------------------------------------------

def creating_session(subsession: Subsession):
    players = subsession.get_players()
    num_players = len(players)

    if num_players % 4 != 0:
        raise ValueError(
            f'El número total de participantes debe ser múltiplo de 4. Actualmente hay {num_players}.'
        )

    if subsession.round_number == 1:
        asignar_round_1(subsession)
    elif subsession.round_number == 2:
        asignar_round_2(subsession)


def asignar_round_1(subsession: Subsession):
    players = subsession.get_players()
    random.shuffle(players)

    n = len(players)
    n_normas = n // 2
    n_trust = n // 2
    n_a = n_trust // 2
    n_b = n_trust // 2

    normas_players = players[:n_normas]
    trust_players = players[n_normas:]

    random.shuffle(trust_players)
    trust_A = trust_players[:n_a]
    trust_B = trust_players[n_a:n_a + n_b]

    for p in normas_players:
        p.condicion_inicial = 'normas'
        p.rol = 'Normas'
        p.participant.condicion_inicial = 'normas'

    for p in trust_A:
        p.condicion_inicial = 'trust'
        p.rol = 'A'
        p.participant.condicion_inicial = 'trust'
        p.participant.rol_fase1 = 'A'

    for p in trust_B:
        p.condicion_inicial = 'trust'
        p.rol = 'B'
        p.participant.condicion_inicial = 'trust'
        p.participant.rol_fase1 = 'B'

    matrix = []

    random.shuffle(trust_A)
    random.shuffle(trust_B)
    for a, b in zip(trust_A, trust_B):
        matrix.append([a.id_in_subsession, b.id_in_subsession])

    random.shuffle(normas_players)
    for i in range(0, len(normas_players), 2):
        p1 = normas_players[i]
        p2 = normas_players[i + 1]
        matrix.append([p1.id_in_subsession, p2.id_in_subsession])

    random.shuffle(matrix)
    subsession.set_group_matrix(matrix)

    for g in subsession.get_groups():
        group_players = g.get_players()
        if all(p.condicion_inicial == 'trust' for p in group_players):
            g.tipo_grupo = 'trust'
        else:
            g.tipo_grupo = 'normas'


def asignar_round_2(subsession: Subsession):
    players = subsession.get_players()

    fase2_A = []
    fase2_B = []

    for p in players:
        origen = p.participant.condicion_inicial
        if origen == 'trust':
            p.condicion_inicial = origen
            p.rol = 'A'
            fase2_A.append(p)
        elif origen == 'normas':
            p.condicion_inicial = origen
            p.rol = 'B'
            fase2_B.append(p)

    random.shuffle(fase2_A)
    random.shuffle(fase2_B)

    matrix = []
    for a, b in zip(fase2_A, fase2_B):
        matrix.append([a.id_in_subsession, b.id_in_subsession])

    random.shuffle(matrix)
    subsession.set_group_matrix(matrix)

    for g in subsession.get_groups():
        g.tipo_grupo = 'fase2'


# ----------------------------------------------------------------
# CÁLCULO DE PAGOS
# ----------------------------------------------------------------

def set_payoffs_fase1(group: Group):
    if group.tipo_grupo != 'trust':
        for p in group.get_players():
            p.pago_fase1 = cu(0)
        return

    a = group.a_player()
    b = group.b_player()

    if a.decision_a_fase1 == 'no_continuar':
        a.pago_fase1 = C.OUTSIDE_OPTION_EACH
        b.pago_fase1 = C.OUTSIDE_OPTION_EACH
    elif a.decision_a_fase1 == 'continuar':
        if b.decision_b_fase1 == 'compartir':
            a.pago_fase1 = C.SHARE_AMOUNT
            b.pago_fase1 = C.SHARE_AMOUNT
        elif b.decision_b_fase1 == 'no_compartir':
            a.pago_fase1 = cu(0)
            b.pago_fase1 = C.DOUBLED_AMOUNT
        else:
            a.pago_fase1 = cu(0)
            b.pago_fase1 = cu(0)


def set_payoffs_fase2(group: Group):
    a = group.a_player()
    b = group.b_player()

    if a.decision_a_fase2 == 'no_continuar':
        a.pago_fase2 = C.OUTSIDE_OPTION_EACH
        b.pago_fase2 = C.OUTSIDE_OPTION_EACH
    elif a.decision_a_fase2 == 'continuar':
        if b.decision_b_fase2 == 'compartir':
            a.pago_fase2 = C.SHARE_AMOUNT
            b.pago_fase2 = C.SHARE_AMOUNT
        elif b.decision_b_fase2 == 'no_compartir':
            a.pago_fase2 = cu(0)
            b.pago_fase2 = C.DOUBLED_AMOUNT
        else:
            a.pago_fase2 = cu(0)
            b.pago_fase2 = cu(0)


# ----------------------------------------------------------------
# PÁGINAS INICIALES
# ----------------------------------------------------------------

class Consentimiento(Page):
    form_model = 'player'
    form_fields = ['acepta']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def error_message(player, values):
        if not values.get('acepta'):
            return "Debe aceptar para continuar."


class ExplicacionGeneral(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


class AsignacionInicial(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            asignacion=player.descripcion_asignacion_inicial()
        )


# ----------------------------------------------------------------
# ROUND 1 - NORMAS
# ----------------------------------------------------------------

class InstruccionesNormas(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.es_normas()


class Norma1(Page):
    form_model = 'player'
    form_fields = ['norma_no_continuar']

    @staticmethod
    def is_displayed(player: Player):
        return player.es_normas()

    @staticmethod
    def error_message(player, values):
        if values.get('norma_no_continuar') is None:
            return "Debe seleccionar una opción para continuar."


class Norma2(Page):
    form_model = 'player'
    form_fields = ['norma_continuar_a']

    @staticmethod
    def is_displayed(player: Player):
        return player.es_normas()

    @staticmethod
    def error_message(player, values):
        if values.get('norma_continuar_a') is None:
            return "Debe seleccionar una opción para continuar."


class Norma3(Page):
    form_model = 'player'
    form_fields = ['norma_b_no_compartir']

    @staticmethod
    def is_displayed(player: Player):
        return player.es_normas()

    @staticmethod
    def error_message(player, values):
        if values.get('norma_b_no_compartir') is None:
            return "Debe seleccionar una opción para continuar."


class Norma4(Page):
    form_model = 'player'
    form_fields = ['norma_b_compartir']

    @staticmethod
    def is_displayed(player: Player):
        return player.es_normas()

    @staticmethod
    def error_message(player, values):
        if values.get('norma_b_compartir') is None:
            return "Debe seleccionar una opción para continuar."


# ----------------------------------------------------------------
# ROUND 1 - TRUST
# ----------------------------------------------------------------

class InstruccionesTrustFase1(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1 and player.condicion_inicial == 'trust'


class InstruccionesAFase1(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.es_trust_fase1_A()


class CreenciaAFase1(Page):
    form_model = 'player'
    form_fields = ['creencia_a_fase1']

    @staticmethod
    def is_displayed(player: Player):
        return player.es_trust_fase1_A()

    @staticmethod
    def error_message(player, values):
        if not values.get('creencia_a_fase1'):
            return "Debe seleccionar una opción para continuar."


class DecisionAFase1(Page):
    form_model = 'player'
    form_fields = ['decision_a_fase1']

    @staticmethod
    def is_displayed(player: Player):
        return player.es_trust_fase1_A()

    @staticmethod
    def error_message(player, values):
        if not values.get('decision_a_fase1'):
            return "Debe seleccionar una opción para continuar."


class InstruccionesBFase1(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.es_trust_fase1_B()


class CreenciaB1Fase1(Page):
    form_model = 'player'
    form_fields = ['creencia_b1_fase1']

    @staticmethod
    def is_displayed(player: Player):
        return player.es_trust_fase1_B()

    @staticmethod
    def error_message(player, values):
        if not values.get('creencia_b1_fase1'):
            return "Debe seleccionar una opción para continuar."


class CreenciaB2Fase1(Page):
    form_model = 'player'
    form_fields = ['creencia_b2_fase1']

    @staticmethod
    def is_displayed(player: Player):
        return player.es_trust_fase1_B()

    @staticmethod
    def error_message(player, values):
        if not values.get('creencia_b2_fase1'):
            return "Debe seleccionar una opción para continuar."


class CreenciaB3Fase1(Page):
    form_model = 'player'
    form_fields = ['creencia_b3_fase1']

    @staticmethod
    def is_displayed(player: Player):
        return player.es_trust_fase1_B()

    @staticmethod
    def error_message(player, values):
        if not values.get('creencia_b3_fase1'):
            return "Debe seleccionar una opción para continuar."


class WaitForADecisionFase1(WaitPage):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1 and player.condicion_inicial == 'trust'

    body_text = "Por favor espere mientras el otro participante toma su decisión."


class DecisionBFase1(Page):
    form_model = 'player'
    form_fields = ['decision_b_fase1']

    @staticmethod
    def is_displayed(player: Player):
        if not player.es_trust_fase1_B():
            return False
        a = player.group.a_player()
        return a is not None and a.decision_a_fase1 == 'continuar'

    @staticmethod
    def error_message(player, values):
        if not values.get('decision_b_fase1'):
            return "Debe seleccionar una opción para continuar."


class ANoContinuoFase1(Page):
    @staticmethod
    def is_displayed(player: Player):
        if not player.es_trust_fase1_B():
            return False
        a = player.group.a_player()
        return a is not None and a.decision_a_fase1 == 'no_continuar'


class WaitForFinalResultsFase1(WaitPage):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1 and player.condicion_inicial == 'trust'

    @staticmethod
    def after_all_players_arrive(group: Group):
        set_payoffs_fase1(group)

    body_text = "Por favor espere mientras se calculan los resultados."


class ResultadosFase1(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def vars_for_template(player: Player):
        if player.es_normas():
            return dict(
                mensaje_resultado_fase1="Ha finalizado la Fase 1.",
                pago_fase1=player.pago_fase1,
            )

        a = player.group.a_player()
        b = player.group.b_player()

        if player.rol == 'A':
            if player.decision_a_fase1 == 'no_continuar':
                mensaje = "Usted decidió no continuar. Tanto usted como el Participante B reciben $1."
            elif player.decision_a_fase1 == 'continuar' and b.decision_b_fase1 == 'compartir':
                mensaje = "El Participante B decidió COMPARTIR. Tanto usted como el Participante B reciben $2."
            elif player.decision_a_fase1 == 'continuar' and b.decision_b_fase1 == 'no_compartir':
                mensaje = "El Participante B decidió NO COMPARTIR. Usted recibe $0."
            else:
                mensaje = "Resultado no disponible."
        else:
            if a.decision_a_fase1 == 'no_continuar':
                mensaje = "El Participante A decidió NO CONTINUAR. Ambos reciben $1."
            elif a.decision_a_fase1 == 'continuar' and player.decision_b_fase1 == 'compartir':
                mensaje = "Usted decidió COMPARTIR. Ambos reciben $2."
            elif a.decision_a_fase1 == 'continuar' and player.decision_b_fase1 == 'no_compartir':
                mensaje = "Usted decidió NO COMPARTIR. Usted recibe $4 y el Participante A recibe $0."
            else:
                mensaje = "Resultado no disponible."

        return dict(
            mensaje_resultado_fase1=mensaje,
            pago_fase1=player.pago_fase1,
        )


# ----------------------------------------------------------------
# TRANSICIÓN A ROUND 2
# ----------------------------------------------------------------

class TransicionFase2(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 2

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            rol_fase2=player.descripcion_fase2()
        )


# ----------------------------------------------------------------
# ROUND 2
# ----------------------------------------------------------------

class InstruccionesFase2A(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.es_fase2_A()


class CreenciaA1Fase2(Page):
    form_model = 'player'
    form_fields = ['creencia_a1_fase2']

    @staticmethod
    def is_displayed(player: Player):
        return player.es_fase2_A()

    @staticmethod
    def error_message(player, values):
        if not values.get('creencia_a1_fase2'):
            return "Debe seleccionar una opción para continuar."


class CreenciaA2Fase2(Page):
    form_model = 'player'
    form_fields = ['creencia_a2_fase2']

    @staticmethod
    def is_displayed(player: Player):
        return player.es_fase2_A()

    @staticmethod
    def error_message(player, values):
        if not values.get('creencia_a2_fase2'):
            return "Debe seleccionar una opción para continuar."


class DecisionAFase2(Page):
    form_model = 'player'
    form_fields = ['decision_a_fase2']

    @staticmethod
    def is_displayed(player: Player):
        return player.es_fase2_A()

    @staticmethod
    def error_message(player, values):
        if not values.get('decision_a_fase2'):
            return "Debe seleccionar una opción para continuar."


class InstruccionesFase2B(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.es_fase2_B()


class WaitForADecisionFase2(WaitPage):
    body_text = "Por favor espere mientras el otro participante toma su decisión."

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 2


class DecisionBFase2(Page):
    form_model = 'player'
    form_fields = ['decision_b_fase2']

    @staticmethod
    def is_displayed(player: Player):
        if not player.es_fase2_B():
            return False
        a = player.group.a_player()
        return a is not None and a.decision_a_fase2 == 'continuar'

    @staticmethod
    def error_message(player, values):
        if not values.get('decision_b_fase2'):
            return "Debe seleccionar una opción para continuar."


class ANoContinuoFase2(Page):
    @staticmethod
    def is_displayed(player: Player):
        if not player.es_fase2_B():
            return False
        a = player.group.a_player()
        return a is not None and a.decision_a_fase2 == 'no_continuar'


class WaitForFinalResultsFase2(WaitPage):
    body_text = "Por favor espere mientras se calculan los resultados."

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 2

    @staticmethod
    def after_all_players_arrive(group: Group):
        set_payoffs_fase2(group)


class ResultadosFase2(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 2

    @staticmethod
    def vars_for_template(player: Player):
        a = player.group.a_player()
        b = player.group.b_player()

        if player.rol == 'A':
            if player.decision_a_fase2 == 'no_continuar':
                mensaje = "Usted decidió no continuar. Tanto usted como el Participante B reciben $1."
            elif player.decision_a_fase2 == 'continuar' and b.decision_b_fase2 == 'compartir':
                mensaje = "El Participante B decidió COMPARTIR. Tanto usted como el Participante B reciben $2."
            elif player.decision_a_fase2 == 'continuar' and b.decision_b_fase2 == 'no_compartir':
                mensaje = "El Participante B decidió NO COMPARTIR. Usted recibe $0."
            else:
                mensaje = "Resultado no disponible."
        else:
            if a.decision_a_fase2 == 'no_continuar':
                mensaje = "El Participante A decidió NO CONTINUAR. Ambos reciben $1."
            elif a.decision_a_fase2 == 'continuar' and player.decision_b_fase2 == 'compartir':
                mensaje = "Usted decidió COMPARTIR. Ambos reciben $2."
            elif a.decision_a_fase2 == 'continuar' and player.decision_b_fase2 == 'no_compartir':
                mensaje = "Usted decidió NO COMPARTIR. Usted recibe $4 y el Participante A recibe $0."
            else:
                mensaje = "Resultado no disponible."

        return dict(
            mensaje_resultado_fase2=mensaje,
            pago_fase2=player.pago_fase2,
        )


# ----------------------------------------------------------------
# FINAL
# ----------------------------------------------------------------

class CuestionarioFinal(Page):
    form_model = 'player'
    form_fields = ['edad', 'genero', 'comentario_final']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 2

    @staticmethod
    def error_message(player, values):
        if values.get('edad') is None or not values.get('genero'):
            return "Debe completar los campos obligatorios para continuar."


class Cierre(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 2

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            pago_fase1=player.in_round(1).pago_fase1,
            pago_fase2=player.pago_fase2,
        )


page_sequence = [
    Consentimiento,
    ExplicacionGeneral,
    AsignacionInicial,

    InstruccionesNormas,
    Norma1,
    Norma2,
    Norma3,
    Norma4,

    InstruccionesTrustFase1,
    InstruccionesAFase1,
    CreenciaAFase1,
    DecisionAFase1,

    InstruccionesBFase1,
    CreenciaB1Fase1,
    CreenciaB2Fase1,
    CreenciaB3Fase1,

    WaitForADecisionFase1,
    DecisionBFase1,
    ANoContinuoFase1,
    WaitForFinalResultsFase1,
    ResultadosFase1,

    TransicionFase2,

    InstruccionesFase2A,
    CreenciaA1Fase2,
    CreenciaA2Fase2,
    DecisionAFase2,

    InstruccionesFase2B,
    WaitForADecisionFase2,
    DecisionBFase2,
    ANoContinuoFase2,
    WaitForFinalResultsFase2,
    ResultadosFase2,

    CuestionarioFinal,
    Cierre,
]