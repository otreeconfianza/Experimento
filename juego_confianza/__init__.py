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

Pagos:
- Grupo 1 (normas): pago por coincidencia con respuesta modal en 4 preguntas.
- Grupo 2 (trust): pago aleatorio por desempeño en fase 1 o fase 2.
- En trust, cada fase puede pagar por creencias o por juego de confianza.
- Todas las ramas tienen pago máximo igual a 4.
"""


class C(BaseConstants):
    NAME_IN_URL = 'juego_confianza'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 2

    ENDOWMENT = cu(2)
    OUTSIDE_OPTION_EACH = cu(1)
    DOUBLED_AMOUNT = cu(4)
    SHARE_AMOUNT = cu(2)

    MAX_PAYMENT = cu(4)


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
    condicion_inicial = models.StringField(blank=True)   # 'trust' o 'normas'
    rol = models.StringField(blank=True)                 # 'A', 'B', 'Normas'

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
    # Pagos auxiliares
    # -------------------------
    pago_normas = models.CurrencyField(initial=0)
    pago_creencias_fase1 = models.CurrencyField(initial=0)
    pago_creencias_fase2 = models.CurrencyField(initial=0)

    score_normas = models.FloatField(initial=0)
    score_creencias_fase1 = models.FloatField(initial=0)
    score_creencias_fase2 = models.FloatField(initial=0)

    fase_pago_seleccionada = models.StringField(blank=True)
    rama_pago_seleccionada = models.StringField(blank=True)
    pago_seleccionado_label = models.StringField(blank=True)

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
            return 'Usted ha sido asignado al Grupo 1.'
        elif self.condicion_inicial == 'trust':
            return f'Usted ha sido asignado al Grupo 2: Su rol en la Fase 1 es Participante {self.rol}.'
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

    for p in trust_A:
        p.condicion_inicial = 'trust'
        p.rol = 'A'

    for p in trust_B:
        p.condicion_inicial = 'trust'
        p.rol = 'B'

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
        origen = p.in_round(1).condicion_inicial

        if origen == 'trust':
            p.condicion_inicial = 'trust'
            p.rol = 'A'
            fase2_A.append(p)
        elif origen == 'normas':
            p.condicion_inicial = 'normas'
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
# CÁLCULO DE PAGOS DEL TRUST GAME
# ----------------------------------------------------------------

def set_payoffs_fase1(group: Group):
    if group.tipo_grupo != 'trust':
        for p in group.get_players():
            p.pago_fase1 = cu(0)
        return

    a = group.a_player()
    b = group.b_player()

    if a is None or b is None:
        for p in group.get_players():
            p.pago_fase1 = cu(0)
        return

    a_decision = a.field_maybe_none('decision_a_fase1')
    b_decision = b.field_maybe_none('decision_b_fase1')

    a.pago_fase1 = cu(0)
    b.pago_fase1 = cu(0)

    if a_decision == 'no_continuar':
        a.pago_fase1 = C.OUTSIDE_OPTION_EACH
        b.pago_fase1 = C.OUTSIDE_OPTION_EACH
    elif a_decision == 'continuar':
        if b_decision == 'compartir':
            a.pago_fase1 = C.SHARE_AMOUNT
            b.pago_fase1 = C.SHARE_AMOUNT
        elif b_decision == 'no_compartir':
            a.pago_fase1 = cu(0)
            b.pago_fase1 = C.DOUBLED_AMOUNT


def set_payoffs_fase2(group: Group):
    a = group.a_player()
    b = group.b_player()

    if a is None or b is None:
        for p in group.get_players():
            p.pago_fase2 = cu(0)
        return

    a_decision = a.field_maybe_none('decision_a_fase2')
    b_decision = b.field_maybe_none('decision_b_fase2')

    a.pago_fase2 = cu(0)
    b.pago_fase2 = cu(0)

    if a_decision == 'no_continuar':
        a.pago_fase2 = C.OUTSIDE_OPTION_EACH
        b.pago_fase2 = C.OUTSIDE_OPTION_EACH
    elif a_decision == 'continuar':
        if b_decision == 'compartir':
            a.pago_fase2 = C.SHARE_AMOUNT
            b.pago_fase2 = C.SHARE_AMOUNT
        elif b_decision == 'no_compartir':
            a.pago_fase2 = cu(0)
            b.pago_fase2 = C.DOUBLED_AMOUNT


# ----------------------------------------------------------------
# AUXILIARES
# ----------------------------------------------------------------

def interval_index(interval_code):
    mapping = {
        '0_20': 0,
        '20_40': 1,
        '40_60': 2,
        '60_80': 3,
        '80_100': 4,
    }
    return mapping.get(interval_code)


def percentage_to_interval_code(value):
    if value is None:
        return None
    if value < 20:
        return '0_20'
    elif value < 40:
        return '20_40'
    elif value < 60:
        return '40_60'
    elif value < 80:
        return '60_80'
    else:
        return '80_100'


def modal_response(values):
    counts = {}
    for v in values:
        if v is not None:
            counts[v] = counts.get(v, 0) + 1

    if not counts:
        return None

    max_count = max(counts.values())
    modals = [k for k, v in counts.items() if v == max_count]
    return min(modals)


def percentage_yes(players, field_name, yes_value):
    valid_values = []

    for p in players:
        value = p.field_maybe_none(field_name)
        if value is not None:
            valid_values.append(value)

    if len(valid_values) == 0:
        return None

    yes_count = sum(1 for value in valid_values if value == yes_value)
    return 100 * yes_count / len(valid_values)


# ----------------------------------------------------------------
# NORMAS
# ----------------------------------------------------------------

def score_norm_question(answer, modal):
    return 1.0 if answer == modal else 0.0


def compute_norms_payoffs(subsession: Subsession):
    normas_players = [
        p for p in subsession.in_round(1).get_players()
        if p.condicion_inicial == 'normas'
    ]

    if not normas_players:
        return

    modal_1 = modal_response([p.field_maybe_none('norma_no_continuar') for p in normas_players])
    modal_2 = modal_response([p.field_maybe_none('norma_continuar_a') for p in normas_players])
    modal_3 = modal_response([p.field_maybe_none('norma_b_no_compartir') for p in normas_players])
    modal_4 = modal_response([p.field_maybe_none('norma_b_compartir') for p in normas_players])

    for p in normas_players:
        scores = [
            score_norm_question(p.field_maybe_none('norma_no_continuar'), modal_1),
            score_norm_question(p.field_maybe_none('norma_continuar_a'), modal_2),
            score_norm_question(p.field_maybe_none('norma_b_no_compartir'), modal_3),
            score_norm_question(p.field_maybe_none('norma_b_compartir'), modal_4),
        ]

        avg_score = sum(scores) / 4
        p.score_normas = avg_score
        p.pago_normas = cu(4 * avg_score)


# ----------------------------------------------------------------
# CREENCIAS - NUEVA VERSIÓN ENTERA
# ----------------------------------------------------------------

def score_interval_points(predicted_interval_code, realized_interval_code, exact_points=2, adjacent_points=1):
    pred = interval_index(predicted_interval_code)
    real = interval_index(realized_interval_code)

    if pred is None or real is None:
        return 0

    distance = abs(pred - real)
    if distance == 0:
        return exact_points
    elif distance == 1:
        return adjacent_points
    else:
        return 0


def score_binary_points(predicted_value, realized_value, correct_points=1):
    if predicted_value is None or realized_value is None:
        return 0
    return correct_points if predicted_value == realized_value else 0


def compute_belief_payoffs_fase1(subsession: Subsession):
    round1_players = subsession.in_round(1).get_players()

    trust_A = [p for p in round1_players if p.condicion_inicial == 'trust' and p.rol == 'A']
    trust_B = [p for p in round1_players if p.condicion_inicial == 'trust' and p.rol == 'B']

    pct_b_share = percentage_yes(trust_B, 'decision_b_fase1', 'compartir')
    pct_a_continue = percentage_yes(trust_A, 'decision_a_fase1', 'continuar')

    realized_b_share_code = percentage_to_interval_code(pct_b_share)
    realized_a_continue_code = percentage_to_interval_code(pct_a_continue)

    for p in round1_players:
        if p.condicion_inicial != 'trust':
            continue

        if p.rol == 'A':
            points = score_interval_points(
                p.field_maybe_none('creencia_a_fase1'),
                realized_b_share_code,
                exact_points=4,
                adjacent_points=2,
            )
            p.score_creencias_fase1 = points / 4
            p.pago_creencias_fase1 = cu(points)

        elif p.rol == 'B':
            a = p.group.a_player()

            a_creencia = a.field_maybe_none('creencia_a_fase1') if a else None
            a_decision = a.field_maybe_none('decision_a_fase1') if a else None

            s1 = score_interval_points(
                p.field_maybe_none('creencia_b1_fase1'),
                a_creencia,
                exact_points=2,
                adjacent_points=1,
            )
            s2 = score_binary_points(
                p.field_maybe_none('creencia_b2_fase1'),
                a_decision,
                correct_points=1,
            )
            s3 = score_interval_points(
                p.field_maybe_none('creencia_b3_fase1'),
                realized_a_continue_code,
                exact_points=1,
                adjacent_points=0,
            )

            points = s1 + s2 + s3
            p.score_creencias_fase1 = points / 4
            p.pago_creencias_fase1 = cu(points)


def compute_belief_payoffs_fase2(subsession: Subsession):
    round2_players = subsession.in_round(2).get_players()

    fase2_A = [p for p in round2_players if p.rol == 'A']
    fase2_B = [p for p in round2_players if p.rol == 'B']

    pct_a_continue = percentage_yes(fase2_A, 'decision_a_fase2', 'continuar')
    pct_b_share = percentage_yes(fase2_B, 'decision_b_fase2', 'compartir')

    realized_a_continue_code = percentage_to_interval_code(pct_a_continue)
    realized_b_share_code = percentage_to_interval_code(pct_b_share)

    for p in round2_players:
        if p.rol == 'A':
            s1 = score_interval_points(
                p.field_maybe_none('creencia_a1_fase2'),
                realized_a_continue_code,
                exact_points=2,
                adjacent_points=1,
            )
            s2 = score_interval_points(
                p.field_maybe_none('creencia_a2_fase2'),
                realized_b_share_code,
                exact_points=2,
                adjacent_points=1,
            )

            points = s1 + s2
            p.score_creencias_fase2 = points / 4
            p.pago_creencias_fase2 = cu(points)
        else:
            p.score_creencias_fase2 = 0
            p.pago_creencias_fase2 = cu(0)


# ----------------------------------------------------------------
# PAGO FINAL
# ----------------------------------------------------------------

def set_final_payoff(player: Player):
    origen = player.condicion_inicial

    if origen == 'normas':
        rama = random.choice(['normas', 'trust_fase2'])
        player.rama_pago_seleccionada = rama

        if rama == 'normas':
            player.fase_pago_seleccionada = 'fase1'
            player.pago_seleccionado_label = 'Normas sociales - Fase 1'
            player.payoff = player.in_round(1).pago_normas

        elif rama == 'trust_fase2':
            player.fase_pago_seleccionada = 'fase2'
            player.pago_seleccionado_label = 'Actividad de interacción - Fase 2'
            player.payoff = player.in_round(2).pago_fase2

    elif origen == 'trust':
        rama = random.choice([
            'trust_fase1',
            'trust_fase2',
            'creencias_fase1',
            'creencias_fase2',
        ])
        player.rama_pago_seleccionada = rama

        if rama == 'trust_fase1':
            player.fase_pago_seleccionada = 'fase1'
            player.pago_seleccionado_label = 'Actividad de interacción - Fase 1'
            player.payoff = player.in_round(1).pago_fase1

        elif rama == 'trust_fase2':
            player.fase_pago_seleccionada = 'fase2'
            player.pago_seleccionado_label = 'Actividad de interacción - Fase 2'
            player.payoff = player.in_round(2).pago_fase2

        elif rama == 'creencias_fase1':
            player.fase_pago_seleccionada = 'fase1'
            player.pago_seleccionado_label = 'Predicciones - Fase 1'
            player.payoff = player.in_round(1).pago_creencias_fase1

        elif rama == 'creencias_fase2':
            player.fase_pago_seleccionada = 'fase2'
            player.pago_seleccionado_label = 'Predicciones - Fase 2'
            player.payoff = player.in_round(2).pago_creencias_fase2


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


class Bienvenida(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


class EsperaInicioExperimento(WaitPage):
    wait_for_all_groups = True
    title_text = "Esperando a los demás participantes"
    body_text = "Por favor espere. El experimento comenzará cuando todos los participantes hayan presionado Siguiente."

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


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
        a_decision = a.field_maybe_none('decision_a_fase1') if a else None
        return a is not None and a_decision == 'continuar'

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
        a_decision = a.field_maybe_none('decision_a_fase1') if a else None
        return a is not None and a_decision == 'no_continuar'


class WaitForFinalResultsFase1(WaitPage):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1 and player.condicion_inicial == 'trust'

    @staticmethod
    def after_all_players_arrive(group: Group):
        set_payoffs_fase1(group)

    body_text = "Por favor espere mientras se calculan los resultados."


class EsperaFinFase1(WaitPage):
    wait_for_all_groups = True
    title_text = "Esperando a los demás participantes"
    body_text = "Por favor espere. La Fase 2 comenzará cuando todos los participantes hayan terminado la Fase 1."

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def after_all_players_arrive(subsession: Subsession):
        compute_norms_payoffs(subsession)
        compute_belief_payoffs_fase1(subsession)


class ResultadosFase1(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def vars_for_template(player: Player):
        if player.es_normas():
            return dict(
                mensaje_resultado_fase1="Ha finalizado la Fase 1.",
                pago_fase1=player.pago_normas,
                pago_creencias_fase1=None,
                mostrar_detalle_trust=False,
            )

        a = player.group.a_player()
        b = player.group.b_player()

        a_decision = a.field_maybe_none('decision_a_fase1') if a else None
        b_decision = b.field_maybe_none('decision_b_fase1') if b else None
        own_b_decision = player.field_maybe_none('decision_b_fase1')

        if player.rol == 'A':
            if a_decision == 'no_continuar':
                mensaje = "Usted decidió no continuar. Tanto usted como el Participante B reciben $1."
            elif a_decision == 'continuar' and b_decision == 'compartir':
                mensaje = "El Participante B decidió COMPARTIR. Tanto usted como el Participante B reciben $2."
            elif a_decision == 'continuar' and b_decision == 'no_compartir':
                mensaje = "El Participante B decidió NO COMPARTIR. Usted recibe $0."
            else:
                mensaje = "Resultado no disponible."
        else:
            if a_decision == 'no_continuar':
                mensaje = "El Participante A decidió NO CONTINUAR. Ambos reciben $1."
            elif a_decision == 'continuar' and own_b_decision == 'compartir':
                mensaje = "Usted decidió COMPARTIR. Ambos reciben $2."
            elif a_decision == 'continuar' and own_b_decision == 'no_compartir':
                mensaje = "Usted decidió NO COMPARTIR. Usted recibe $4 y el Participante A recibe $0."
            else:
                mensaje = "Resultado no disponible."

        return dict(
            mensaje_resultado_fase1=mensaje,
            pago_fase1=player.pago_fase1,
            pago_creencias_fase1=player.pago_creencias_fase1,
            mostrar_detalle_trust=True,
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
        a_decision = a.field_maybe_none('decision_a_fase2') if a else None
        return a is not None and a_decision == 'continuar'

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
        a_decision = a.field_maybe_none('decision_a_fase2') if a else None
        return a is not None and a_decision == 'no_continuar'


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

        a_decision = a.field_maybe_none('decision_a_fase2') if a else None
        b_decision = b.field_maybe_none('decision_b_fase2') if b else None
        own_b_decision = player.field_maybe_none('decision_b_fase2')

        if player.rol == 'A':
            if a_decision == 'no_continuar':
                mensaje = "Usted decidió no continuar. Tanto usted como el Participante B reciben $1."
            elif a_decision == 'continuar' and b_decision == 'compartir':
                mensaje = "El Participante B decidió COMPARTIR. Tanto usted como el Participante B reciben $2."
            elif a_decision == 'continuar' and b_decision == 'no_compartir':
                mensaje = "El Participante B decidió NO COMPARTIR. Usted recibe $0."
            else:
                mensaje = "Resultado no disponible."
        else:
            if a_decision == 'no_continuar':
                mensaje = "El Participante A decidió NO CONTINUAR. Ambos reciben $1."
            elif a_decision == 'continuar' and own_b_decision == 'compartir':
                mensaje = "Usted decidió COMPARTIR. Ambos reciben $2."
            elif a_decision == 'continuar' and own_b_decision == 'no_compartir':
                mensaje = "Usted decidió NO COMPARTIR. Usted recibe $4 y el Participante A recibe $0."
            else:
                mensaje = "Resultado no disponible."

        # Grupo 1: en fase 2 solo mostrar actividad de interacción
        if player.condicion_inicial == 'normas':
            return dict(
                mensaje_resultado_fase2=mensaje,
                pago_fase2=player.pago_fase2,
                pago_creencias_fase2=None,
                mostrar_detalle_trust=False,
            )

        # Grupo 2: mostrar predicciones + actividad de interacción
        return dict(
            mensaje_resultado_fase2=mensaje,
            pago_fase2=player.pago_fase2,
            pago_creencias_fase2=player.pago_creencias_fase2,
            mostrar_detalle_trust=True,
        )


class EsperaPagoFinalFase2(WaitPage):
    wait_for_all_groups = True
    title_text = "Esperando a los demás participantes"
    body_text = "Por favor espere mientras se calcula el pago final del experimento."

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 2

    @staticmethod
    def after_all_players_arrive(subsession: Subsession):
        compute_belief_payoffs_fase2(subsession)

        for p in subsession.get_players():
            set_final_payoff(p)


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
            pago_fase1=player.in_round(1).pago_fase1 or cu(0),
            pago_fase2=player.pago_fase2 or cu(0),
            pago_normas=player.in_round(1).pago_normas or cu(0),
            pago_creencias_fase1=player.in_round(1).pago_creencias_fase1 or cu(0),
            pago_creencias_fase2=player.pago_creencias_fase2 or cu(0),
            fase_pago_seleccionada=player.fase_pago_seleccionada,
            pago_seleccionado_label=player.pago_seleccionado_label,
            pago_final=player.payoff or cu(0),
            es_grupo_normas=(player.condicion_inicial == 'normas'),
        )


page_sequence = [
    Consentimiento,
    Bienvenida,
    EsperaInicioExperimento,
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
    EsperaFinFase1,
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

    EsperaPagoFinalFase2,

    CuestionarioFinal,
    Cierre,
]