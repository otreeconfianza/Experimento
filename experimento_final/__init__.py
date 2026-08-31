from otree.api import *
import random


doc = """
Experimento final Julio 2026.

Estructura:
- Los participantes se dividen aleatoriamente en cuatro grupos: G1, G2, G3 y G4.
- Fase 1: G1 participa como A y G2 como B en un juego de confianza.
- Fase 2: G2 participa como A y G3 como B en un juego de confianza.
- Fase 3: G3 participa como A y G4 como B en un juego de confianza.
- Fase 4: todos participan en juego del dictador, normas sociales y cuestionario final.

Pagos:
- En cada fase del juego de confianza, A decide CONTINUAR o NO CONTINUAR.
- Si A NO CONTINÚA, A y B reciben $3.500.
- Si A CONTINÚA, el monto de $7.000 se duplica a $14.000 y B decide COMPARTIR o NO COMPARTIR.
- Si B COMPARTE, A y B reciben $7.000.
- Si B NO COMPARTE, A recibe $0 y B recibe $14.000.
- En el juego del dictador, el asignador decide COMPARTIR $7.000 o NO COMPARTIR.
- En normas sociales, cada coincidencia con la respuesta modal paga $3.000.
- Al final se selecciona al azar una de las actividades elegibles de cada participante.
"""


class C(BaseConstants):
    NAME_IN_URL = 'experimento_final'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 4

    G1 = 'G1'
    G2 = 'G2'
    G3 = 'G3'
    G4 = 'G4'

    ROLE_A = 'A'
    ROLE_B = 'B'
    ROLE_ASIGNADOR = 'ASIGNADOR'
    ROLE_RECEPTOR = 'RECEPTOR'
    ROLE_ESPERA = 'ESPERA'

    INITIAL_AMOUNT = cu(7000)
    OUTSIDE_OPTION_EACH = cu(3500)
    DOUBLED_AMOUNT = cu(14000)
    TRUST_SHARE_AMOUNT = cu(7000)

    DICTATOR_AMOUNT = cu(7000)
    DICTATOR_SHARE_AMOUNT = cu(3500)

    BELIEF_PAYMENT = cu(6000)
    NORM_PAYMENT_PER_MATCH = cu(3000)
    VIATICOS = cu(3000)

    INTERVAL_CHOICES = [
        ['0_20', '0–20%'],
        ['20_40', '20–40%'],
        ['40_60', '40–60%'],
        ['60_80', '60–80%'],
        ['80_100', '80–100%'],
    ]

    NORM_CHOICES = [
        [1, '1 - Muy inapropiada'],
        [2, '2 - Algo inapropiada'],
        [3, '3 - Algo apropiada'],
        [4, '4 - Muy apropiada'],
    ]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    tipo_grupo = models.StringField(blank=True)
    fase_activa = models.IntegerField(initial=0)

    def a_player(self):
        for p in self.get_players():
            if p.rol_en_ronda == C.ROLE_A:
                return p
        return None

    def b_player(self):
        for p in self.get_players():
            if p.rol_en_ronda == C.ROLE_B:
                return p
        return None

    def asignador(self):
        for p in self.get_players():
            if p.rol_en_ronda == C.ROLE_ASIGNADOR:
                return p
        return None

    def receptor(self):
        for p in self.get_players():
            if p.rol_en_ronda == C.ROLE_RECEPTOR:
                return p
        return None


class Player(BasePlayer):
    grupo_experimental = models.StringField(blank=True)
    rol_en_ronda = models.StringField(blank=True)

    consentimiento_papel = models.StringField(
        choices=[
            ['si', 'Sí'],
            ['no', 'No'],
        ],
        label='Usted ha firmado el formulario de consentimiento informado en papel entregado al ingresar al aula:',
        widget=widgets.RadioSelect,
        blank=True,
    )

    # ------------------------------------------------------------
    # Fase 1: G1 = A, G2 = B
    # ------------------------------------------------------------
    creencia_a_b_comparte_f1 = models.StringField(
        choices=C.INTERVAL_CHOICES,
        label='¿Qué porcentaje de sujetos B en su sesión cree usted que elegirá COMPARTIR?',
        blank=True,
    )
    creencia_a_porcentaje_a_continua_f1 = models.StringField(
        choices=C.INTERVAL_CHOICES,
        label='Estime qué porcentaje de los demás participantes A elegirá CONTINUAR.',
        blank=True,
    )
    creencia_b_decision_a_f1 = models.StringField(
        choices=[
            ['no_continuar', 'NO CONTINUAR'],
            ['continuar', 'CONTINUAR'],
        ],
        label='¿Qué decisión cree usted que tomará el participante A?',
        blank=True,
    )
    creencia_b_porcentaje_a_continua_f1 = models.StringField(
        choices=C.INTERVAL_CHOICES,
        label='Estime qué porcentaje de participantes A elegirá CONTINUAR.',
        blank=True,
    )
    creencia_b_porcentaje_b_comparte_f1 = models.StringField(
        choices=C.INTERVAL_CHOICES,
        label='¿Qué porcentaje de participantes B cree que elegirá COMPARTIR?',
        blank=True,
    )
    decision_a_f1 = models.StringField(
        choices=[
            ['continuar', 'CONTINUAR'],
            ['no_continuar', 'NO CONTINUAR'],
        ],
        label='Presione la opción elegida:',
        blank=True,
    )
    decision_b_f1 = models.StringField(
        choices=[
            ['compartir', 'COMPARTIR'],
            ['no_compartir', 'NO COMPARTIR'],
        ],
        label='Presione la opción elegida:',
        blank=True,
    )
    pago_juego_confianza_f1 = models.CurrencyField(initial=0)
    pago_creencias_f1 = models.CurrencyField(initial=0)

    # ------------------------------------------------------------
    # Fase 2: G2 = A, G3 = B
    # ------------------------------------------------------------
    creencia_a_b_comparte_f2 = models.StringField(
        choices=C.INTERVAL_CHOICES,
        label='¿Qué porcentaje de sujetos B en su sesión cree usted que elegirá COMPARTIR?',
        blank=True,
    )
    creencia_a_porcentaje_a_continua_f2 = models.StringField(
        choices=C.INTERVAL_CHOICES,
        label='Estime qué porcentaje de los demás participantes A elegirá CONTINUAR.',
        blank=True,
    )
    creencia_b_decision_a_f2 = models.StringField(
        choices=[
            ['no_continuar', 'NO CONTINUAR'],
            ['continuar', 'CONTINUAR'],
        ],
        label='¿Qué decisión cree usted que tomará el participante A?',
        blank=True,
    )
    creencia_b_porcentaje_a_continua_f2 = models.StringField(
        choices=C.INTERVAL_CHOICES,
        label='Estime qué porcentaje de participantes A elegirá CONTINUAR.',
        blank=True,
    )
    creencia_b_porcentaje_b_comparte_f2 = models.StringField(
        choices=C.INTERVAL_CHOICES,
        label='¿Qué porcentaje de participantes B cree que elegirá COMPARTIR?',
        blank=True,
    )
    decision_a_f2 = models.StringField(
        choices=[
            ['continuar', 'CONTINUAR'],
            ['no_continuar', 'NO CONTINUAR'],
        ],
        label='Presione la opción elegida:',
        blank=True,
    )
    decision_b_f2 = models.StringField(
        choices=[
            ['compartir', 'COMPARTIR'],
            ['no_compartir', 'NO COMPARTIR'],
        ],
        label='Presione la opción elegida:',
        blank=True,
    )
    pago_juego_confianza_f2 = models.CurrencyField(initial=0)
    pago_creencias_f2 = models.CurrencyField(initial=0)

    # ------------------------------------------------------------
    # Fase 3: G3 = A, G4 = B
    # ------------------------------------------------------------
    creencia_a_b_comparte_f3 = models.StringField(
        choices=C.INTERVAL_CHOICES,
        label='¿Qué porcentaje de sujetos B en su sesión cree usted que elegirá COMPARTIR?',
        blank=True,
    )
    creencia_a_porcentaje_a_continua_f3 = models.StringField(
        choices=C.INTERVAL_CHOICES,
        label='Estime qué porcentaje de los demás participantes A elegirá CONTINUAR.',
        blank=True,
    )
    creencia_b_decision_a_f3 = models.StringField(
        choices=[
            ['no_continuar', 'NO CONTINUAR'],
            ['continuar', 'CONTINUAR'],
        ],
        label='¿Qué decisión cree usted que tomará el participante A?',
        blank=True,
    )
    creencia_b_porcentaje_a_continua_f3 = models.StringField(
        choices=C.INTERVAL_CHOICES,
        label='Estime qué porcentaje de participantes A elegirá CONTINUAR.',
        blank=True,
    )
    creencia_b_porcentaje_b_comparte_f3 = models.StringField(
        choices=C.INTERVAL_CHOICES,
        label='¿Qué porcentaje de participantes B cree que elegirá COMPARTIR?',
        blank=True,
    )
    decision_a_f3 = models.StringField(
        choices=[
            ['continuar', 'CONTINUAR'],
            ['no_continuar', 'NO CONTINUAR'],
        ],
        label='Presione la opción elegida:',
        blank=True,
    )
    decision_b_f3 = models.StringField(
        choices=[
            ['compartir', 'COMPARTIR'],
            ['no_compartir', 'NO COMPARTIR'],
        ],
        label='Presione la opción elegida:',
        blank=True,
    )
    pago_juego_confianza_f3 = models.CurrencyField(initial=0)
    pago_creencias_f3 = models.CurrencyField(initial=0)

    # ------------------------------------------------------------
    # Fase 4: dictador
    # ------------------------------------------------------------
    decision_dictador = models.StringField(
        choices=[
            ['compartir', 'COMPARTIR'],
            ['no_compartir', 'NO COMPARTIR'],
        ],
        label='Presione la opción elegida:',
        blank=True,
    )
    pago_dictador = models.CurrencyField(initial=0)

    # ------------------------------------------------------------
    # Fase 4: normas sociales
    # ------------------------------------------------------------
    norma_no_continuar_a = models.IntegerField(
        choices=C.NORM_CHOICES,
        label='¿En qué medida la mayoría de las personas juzgaría socialmente apropiada la acción del participante A?',
        blank=True,
    )
    norma_continuar_a = models.IntegerField(
        choices=C.NORM_CHOICES,
        label='¿En qué medida la mayoría de las personas juzgaría socialmente apropiada la acción del Participante A?',
        blank=True,
    )
    norma_b_no_compartir = models.IntegerField(
        choices=C.NORM_CHOICES,
        label='¿En qué medida la mayoría de las personas juzgaría socialmente apropiada la acción del Participante B?',
        blank=True,
    )
    norma_b_compartir = models.IntegerField(
        choices=C.NORM_CHOICES,
        label='¿En qué medida la mayoría de las personas juzgaría socialmente apropiada la acción del Participante B?',
        blank=True,
    )
    pago_normas = models.CurrencyField(initial=0)

    # ------------------------------------------------------------
    # Cuestionario final
    # ------------------------------------------------------------
    edad = models.IntegerField(

    label='Edad',

    min=18,

    blank=True,

)

    carrera = models.StringField(

    label='Carrera',

    blank=True,

)

    lugar_origen = models.StringField(

    label='Lugar de origen (provincia)',

    choices=[

        'Ciudad Autónoma de Buenos Aires',

        'Buenos Aires',

        'Catamarca',

        'Chaco',

        'Chubut',

        'Córdoba',

        'Corrientes',

        'Entre Ríos',

        'Formosa',

        'Jujuy',

        'La Pampa',

        'La Rioja',

        'Mendoza',

        'Misiones',

        'Neuquén',

        'Río Negro',

        'Salta',

        'San Juan',

        'San Luis',

        'Santa Cruz',

        'Santa Fe',

        'Santiago del Estero',

        'Tierra del Fuego, Antártida e Islas del Atlántico Sur',

        'Tucumán',

    ],

    blank=True,

)

    riesgo_general = models.IntegerField(

    label=(

        'Indique, en términos generales, en qué medida está dispuesto '

        'o no a asumir riesgos. Utilice una escala del 1 al 10, donde '

        '1 significa muy poco dispuesto a asumir riesgos y 10 significa '

        'muy dispuesto a asumir riesgos.'

    ),

    min=1,

    max=10,

    blank=True,

)

    confianza_general = models.IntegerField(

    label=(

        'En términos generales, ¿diría que se puede confiar en la mayoría '

        'de la gente o que nunca está de más ser precavido al tratar con '

        'los demás? 0 = Nunca está de más ser precavido; '

        '10 = Se puede confiar en la mayoría de la gente.'

    ),

    min=0,

    max=10,

    blank=True,

)
    

    # ------------------------------------------------------------
    # Pago final y control
    # ------------------------------------------------------------
    actividad_pago_seleccionada = models.StringField(blank=True)
    pago_seleccionado_label = models.StringField(blank=True)
    numero_pago = models.StringField(blank=True)

    def es_g1(self):
        return self.grupo_experimental == C.G1

    def es_g2(self):
        return self.grupo_experimental == C.G2

    def es_g3(self):
        return self.grupo_experimental == C.G3

    def es_g4(self):
        return self.grupo_experimental == C.G4

    def fase_activa_actual(self):
        if self.round_number in [1, 2, 3]:
            return self.round_number
        return 4

    def es_participante_a(self):
        return self.rol_en_ronda == C.ROLE_A

    def es_participante_b(self):
        return self.rol_en_ronda == C.ROLE_B

    def es_asignador(self):
        return self.rol_en_ronda == C.ROLE_ASIGNADOR

    def es_receptor(self):
        return self.rol_en_ronda == C.ROLE_RECEPTOR

    def participa_en_trust_round_actual(self):
        return self.round_number in [1, 2, 3] and self.rol_en_ronda in [C.ROLE_A, C.ROLE_B]

    def descripcion_grupo(self):
        if self.grupo_experimental == C.G1:
            return 'Usted ha sido asignado al grupo G1. Participará en 2 fases.'
        if self.grupo_experimental == C.G2:
            return 'Usted ha sido asignado al grupo G2. Participará en 3 fases.'
        if self.grupo_experimental == C.G3:
            return 'Usted ha sido asignado al grupo G3. Participará en 3 fases.'
        if self.grupo_experimental == C.G4:
            return 'Usted ha sido asignado al grupo G4. Participará en 2 fases.'
        return ''

    def descripcion_rol_trust(self):
        if self.rol_en_ronda == C.ROLE_A:
            return 'A usted le ha sido asignado el rol de Participante A.'
        if self.rol_en_ronda == C.ROLE_B:
            return 'A usted le ha sido asignado el rol de Participante B.'
        return ''

    def trust_fields(self):
        fase = self.round_number
        return dict(
            creencia_a=f'creencia_a_b_comparte_f{fase}',
            creencia_a_porcentaje=f'creencia_a_porcentaje_a_continua_f{fase}',
            creencia_b_decision=f'creencia_b_decision_a_f{fase}',
            creencia_b_porcentaje=f'creencia_b_porcentaje_a_continua_f{fase}',
            creencia_b_porcentaje_b_comparte=f'creencia_b_porcentaje_b_comparte_f{fase}',
            decision_a=f'decision_a_f{fase}',
            decision_b=f'decision_b_f{fase}',
            pago_juego=f'pago_juego_confianza_f{fase}',
            pago_creencias=f'pago_creencias_f{fase}',
        )


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
        asignar_grupos_experimentales(subsession)
    else:
        copiar_grupos_experimentales(subsession)

    if subsession.round_number in [1, 2, 3]:
        formar_grupos_trust(subsession)
    elif subsession.round_number == 4:
        formar_grupos_dictador(subsession)


def asignar_grupos_experimentales(subsession: Subsession):
    players = subsession.get_players()
    random.shuffle(players)

    n_por_grupo = len(players) // 4
    grupos = [C.G1, C.G2, C.G3, C.G4]

    for i, p in enumerate(players):
        grupo = grupos[i // n_por_grupo]
        p.grupo_experimental = grupo
        p.participant.vars['grupo_experimental'] = grupo


def copiar_grupos_experimentales(subsession: Subsession):
    for p in subsession.get_players():
        grupo = p.participant.vars.get('grupo_experimental')
        if grupo is None:
            grupo = p.in_round(1).grupo_experimental
            p.participant.vars['grupo_experimental'] = grupo
        p.grupo_experimental = grupo


def formar_grupos_trust(subsession: Subsession):
    fase = subsession.round_number
    players = subsession.get_players()

    if fase == 1:
        grupo_a = C.G1
        grupo_b = C.G2
    elif fase == 2:
        grupo_a = C.G2
        grupo_b = C.G3
    else:
        grupo_a = C.G3
        grupo_b = C.G4

    jugadores_a = [p for p in players if p.grupo_experimental == grupo_a]
    jugadores_b = [p for p in players if p.grupo_experimental == grupo_b]
    jugadores_inactivos = [p for p in players if p.grupo_experimental not in [grupo_a, grupo_b]]

    random.shuffle(jugadores_a)
    random.shuffle(jugadores_b)
    random.shuffle(jugadores_inactivos)

    matrix = []

    for a, b in zip(jugadores_a, jugadores_b):
        a.rol_en_ronda = C.ROLE_A
        b.rol_en_ronda = C.ROLE_B
        matrix.append([a.id_in_subsession, b.id_in_subsession])

    for i in range(0, len(jugadores_inactivos), 2):
        p1 = jugadores_inactivos[i]
        p2 = jugadores_inactivos[i + 1]
        p1.rol_en_ronda = C.ROLE_ESPERA
        p2.rol_en_ronda = C.ROLE_ESPERA
        matrix.append([p1.id_in_subsession, p2.id_in_subsession])

    random.shuffle(matrix)
    subsession.set_group_matrix(matrix)

    for g in subsession.get_groups():
        g.fase_activa = fase
        if all(p.rol_en_ronda in [C.ROLE_A, C.ROLE_B] for p in g.get_players()):
            g.tipo_grupo = f'trust_fase_{fase}'
        else:
            g.tipo_grupo = f'espera_fase_{fase}'


def formar_grupos_dictador(subsession: Subsession):
    players = subsession.get_players()

    asignadores = [p for p in players if p.grupo_experimental in [C.G2, C.G3]]
    receptores = [p for p in players if p.grupo_experimental in [C.G1, C.G4]]

    random.shuffle(asignadores)
    random.shuffle(receptores)

    matrix = []

    for asignador, receptor in zip(asignadores, receptores):
        asignador.rol_en_ronda = C.ROLE_ASIGNADOR
        receptor.rol_en_ronda = C.ROLE_RECEPTOR
        matrix.append([asignador.id_in_subsession, receptor.id_in_subsession])

    random.shuffle(matrix)
    subsession.set_group_matrix(matrix)

    for g in subsession.get_groups():
        g.fase_activa = 4
        g.tipo_grupo = 'dictador'


# ----------------------------------------------------------------
# AUXILIARES
# ----------------------------------------------------------------

def percentage_to_interval_code(value):
    if value is None:
        return None
    if value < 20:
        return '0_20'
    if value < 40:
        return '20_40'
    if value < 60:
        return '40_60'
    if value < 80:
        return '60_80'
    return '80_100'


def percentage_yes(players, field_name, yes_value):
    valid_values = []

    for p in players:
        value = p.field_maybe_none(field_name)
        if value is not None:
            valid_values.append(value)

    if not valid_values:
        return None

    yes_count = sum(1 for value in valid_values if value == yes_value)
    return 100 * yes_count / len(valid_values)


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


def score_interval_exact(predicted_interval_code, realized_interval_code):
    if predicted_interval_code is None or realized_interval_code is None:
        return cu(0)

    if predicted_interval_code == realized_interval_code:
        return C.BELIEF_PAYMENT

    return cu(0)


def score_binary_exact(predicted_value, realized_value):
    if predicted_value is None or realized_value is None:
        return cu(0)

    if predicted_value == realized_value:
        return C.BELIEF_PAYMENT

    return cu(0)


def active_trust_players(subsession: Subsession):
    return [
        p for p in subsession.get_players()
        if p.rol_en_ronda in [C.ROLE_A, C.ROLE_B]
    ]


def get_payment_from_round(player: Player, round_number: int, field_name: str):
    return player.in_round(round_number).field_maybe_none(field_name) or cu(0)


# ----------------------------------------------------------------
# CÁLCULO DE PAGOS - JUEGO DE CONFIANZA
# ----------------------------------------------------------------

def set_payoffs_trust(group: Group):
    a = group.a_player()
    b = group.b_player()

    if a is None or b is None:
        for p in group.get_players():
            fields = p.trust_fields()
            setattr(p, fields['pago_juego'], cu(0))
        return

    fields = a.trust_fields()
    decision_a = a.field_maybe_none(fields['decision_a'])
    decision_b = b.field_maybe_none(fields['decision_b'])

    setattr(a, fields['pago_juego'], cu(0))
    setattr(b, fields['pago_juego'], cu(0))

    if decision_a == 'no_continuar':
        setattr(a, fields['pago_juego'], C.OUTSIDE_OPTION_EACH)
        setattr(b, fields['pago_juego'], C.OUTSIDE_OPTION_EACH)
    elif decision_a == 'continuar':
        if decision_b == 'compartir':
            setattr(a, fields['pago_juego'], C.TRUST_SHARE_AMOUNT)
            setattr(b, fields['pago_juego'], C.TRUST_SHARE_AMOUNT)
        elif decision_b == 'no_compartir':
            setattr(a, fields['pago_juego'], cu(0))
            setattr(b, fields['pago_juego'], C.DOUBLED_AMOUNT)


def compute_belief_payoffs_trust(subsession: Subsession):
    fase = subsession.round_number
    players = active_trust_players(subsession)

    players_a = [p for p in players if p.rol_en_ronda == C.ROLE_A]
    players_b = [p for p in players if p.rol_en_ronda == C.ROLE_B]

    field_a_decision = f'decision_a_f{fase}'
    field_b_decision = f'decision_b_f{fase}'

    realized_pct_b_share = percentage_yes(players_b, field_b_decision, 'compartir')
    realized_pct_a_continue = percentage_yes(players_a, field_a_decision, 'continuar')

    realized_b_share_code = percentage_to_interval_code(realized_pct_b_share)
    realized_a_continue_code = percentage_to_interval_code(realized_pct_a_continue)

    for p in players:
        fields = p.trust_fields()
        pago = cu(0)

        if p.rol_en_ronda == C.ROLE_A:
            pago = score_interval_exact(
                p.field_maybe_none(fields['creencia_a']),
                realized_b_share_code,
            )

        elif p.rol_en_ronda == C.ROLE_B:
            a = p.group.a_player()
            a_decision = a.field_maybe_none(fields['decision_a']) if a else None

            pago += score_binary_exact(
                p.field_maybe_none(fields['creencia_b_decision']),
                a_decision,
            )
            pago += score_interval_exact(
                p.field_maybe_none(fields['creencia_b_porcentaje']),
                realized_a_continue_code,
            )

        setattr(p, fields['pago_creencias'], pago)


# ----------------------------------------------------------------
# CÁLCULO DE PAGOS - DICTADOR Y NORMAS
# ----------------------------------------------------------------

def set_payoffs_dictator(group: Group):
    asignador = group.asignador()
    receptor = group.receptor()

    if asignador is None or receptor is None:
        for p in group.get_players():
            p.pago_dictador = cu(0)
        return

    decision = asignador.field_maybe_none('decision_dictador')

    asignador.pago_dictador = cu(0)
    receptor.pago_dictador = cu(0)

    if decision == 'compartir':
        asignador.pago_dictador = C.DICTATOR_SHARE_AMOUNT
        receptor.pago_dictador = C.DICTATOR_SHARE_AMOUNT
    elif decision == 'no_compartir':
        asignador.pago_dictador = C.DICTATOR_AMOUNT
        receptor.pago_dictador = cu(0)


def compute_norms_payoffs(subsession: Subsession):
    players = subsession.get_players()

    modal_1 = modal_response([p.field_maybe_none('norma_no_continuar_a') for p in players])
    modal_2 = modal_response([p.field_maybe_none('norma_continuar_a') for p in players])
    modal_3 = modal_response([p.field_maybe_none('norma_b_no_compartir') for p in players])
    modal_4 = modal_response([p.field_maybe_none('norma_b_compartir') for p in players])

    for p in players:
        pago = cu(0)

        if p.field_maybe_none('norma_no_continuar_a') == modal_1:
            pago += C.NORM_PAYMENT_PER_MATCH
        if p.field_maybe_none('norma_continuar_a') == modal_2:
            pago += C.NORM_PAYMENT_PER_MATCH
        if p.field_maybe_none('norma_b_no_compartir') == modal_3:
            pago += C.NORM_PAYMENT_PER_MATCH
        if p.field_maybe_none('norma_b_compartir') == modal_4:
            pago += C.NORM_PAYMENT_PER_MATCH

        p.pago_normas = pago


# ----------------------------------------------------------------
# PAGO FINAL
# ----------------------------------------------------------------

def set_final_payoff(player: Player):
    opciones = []

    if player.grupo_experimental == C.G1:
        opciones.extend([
            ('creencias_fase_1', 'Predicciones - Fase 1', get_payment_from_round(player, 1, 'pago_creencias_f1')),
            ('juego_confianza_fase_1', 'Juego de confianza - Fase 1', get_payment_from_round(player, 1, 'pago_juego_confianza_f1')),
            ('dictador_fase_4', 'Juego del dictador - Fase 4', player.pago_dictador),
            ('normas_fase_4', 'Normas sociales - Fase 4', player.pago_normas),
        ])

    elif player.grupo_experimental == C.G2:
        opciones.extend([
            ('creencias_fase_1', 'Predicciones - Fase 1', get_payment_from_round(player, 1, 'pago_creencias_f1')),
            ('juego_confianza_fase_1', 'Juego de confianza - Fase 1', get_payment_from_round(player, 1, 'pago_juego_confianza_f1')),
            ('creencias_fase_2', 'Predicciones - Fase 2', get_payment_from_round(player, 2, 'pago_creencias_f2')),
            ('juego_confianza_fase_2', 'Juego de confianza - Fase 2', get_payment_from_round(player, 2, 'pago_juego_confianza_f2')),
            ('dictador_fase_4', 'Juego del dictador - Fase 4', player.pago_dictador),
            ('normas_fase_4', 'Normas sociales - Fase 4', player.pago_normas),
        ])

    elif player.grupo_experimental == C.G3:
        opciones.extend([
            ('creencias_fase_2', 'Predicciones - Fase 2', get_payment_from_round(player, 2, 'pago_creencias_f2')),
            ('juego_confianza_fase_2', 'Juego de confianza - Fase 2', get_payment_from_round(player, 2, 'pago_juego_confianza_f2')),
            ('creencias_fase_3', 'Predicciones - Fase 3', get_payment_from_round(player, 3, 'pago_creencias_f3')),
            ('juego_confianza_fase_3', 'Juego de confianza - Fase 3', get_payment_from_round(player, 3, 'pago_juego_confianza_f3')),
            ('dictador_fase_4', 'Juego del dictador - Fase 4', player.pago_dictador),
            ('normas_fase_4', 'Normas sociales - Fase 4', player.pago_normas),
        ])

    elif player.grupo_experimental == C.G4:
        opciones.extend([
            ('creencias_fase_3', 'Predicciones - Fase 3', get_payment_from_round(player, 3, 'pago_creencias_f3')),
            ('juego_confianza_fase_3', 'Juego de confianza - Fase 3', get_payment_from_round(player, 3, 'pago_juego_confianza_f3')),
            ('dictador_fase_4', 'Juego del dictador - Fase 4', player.pago_dictador),
            ('normas_fase_4', 'Normas sociales - Fase 4', player.pago_normas),
        ])

    codigo, label, monto = random.choice(opciones)

    player.actividad_pago_seleccionada = codigo
    player.pago_seleccionado_label = label
    player.payoff = C.VIATICOS + monto


def assign_payment_numbers(subsession: Subsession):
    players = subsession.get_players()
    numbers = random.sample(range(100000, 1000000), len(players))

    for player, number in zip(players, numbers):
        player.numero_pago = str(number)


# ----------------------------------------------------------------
# PÁGINAS INICIALES
# ----------------------------------------------------------------

class Consentimiento(Page):
    form_model = 'player'
    form_fields = ['consentimiento_papel']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def error_message(player, values):
        respuesta = values.get('consentimiento_papel')

        if not respuesta:
            return 'Debe seleccionar una opción para continuar.'

        if respuesta == 'no':
            return 'Solicitar el formulario a los referentes del experimento.'

class PreguntasComprension(Page):
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
            grupo=player.grupo_experimental,
            es_g1=player.grupo_experimental == C.G1,
            es_g2=player.grupo_experimental == C.G2,
            es_g3=player.grupo_experimental == C.G3,
            es_g4=player.grupo_experimental == C.G4,
        )


class EsperaInicioExperimento(WaitPage):
    wait_for_all_groups = True
    title_text = 'Esperando a los demás participantes'
    body_text = 'Por favor espere. El experimento comenzará para todos los participantes al mismo tiempo.'

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


# ----------------------------------------------------------------
# PÁGINAS COMUNES DE TRUST
# ----------------------------------------------------------------

class InicioFaseTrust(Page):
    @staticmethod
    def is_displayed(player: Player):
        return (
            player.round_number in [2, 3]
            and player.participa_en_trust_round_actual()
        )

    @staticmethod
    def vars_for_template(player: Player):
        primera_participacion = (
            (
                player.round_number == 2
                and player.grupo_experimental == C.G3
            )
            or (
                player.round_number == 3
                and player.grupo_experimental == C.G4
            )
        )

        ya_participo_antes = (
            (
                player.round_number == 2
                and player.grupo_experimental == C.G2
            )
            or (
                player.round_number == 3
                and player.grupo_experimental == C.G3
            )
        )

        return dict(
            fase=player.round_number,
            es_fase_2=player.round_number == 2,
            es_fase_3=player.round_number == 3,

            primera_participacion=primera_participacion,
            ya_participo_antes=ya_participo_antes,

            rol=player.rol_en_ronda,
            es_A=player.rol_en_ronda == C.ROLE_A,
            es_B=player.rol_en_ronda == C.ROLE_B,
        )


class InstruccionesTrust(Page):
    @staticmethod
    def is_displayed(player: Player):
        return (
            player.round_number in [1, 2, 3]
            and player.participa_en_trust_round_actual()
        )

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            fase=player.round_number,
            es_fase_1=player.round_number == 1,
            es_fase_2=player.round_number == 2,
            es_fase_3=player.round_number == 3,

            rol=player.rol_en_ronda,
            es_A=player.rol_en_ronda == C.ROLE_A,
            es_B=player.rol_en_ronda == C.ROLE_B,
        )

class InstruccionesParticipanteA(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number in [1, 2, 3] and player.es_participante_a()

    @staticmethod
    def vars_for_template(player: Player):
        return dict(fase=player.round_number)


class InstruccionesParticipanteB(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number in [1, 2, 3] and player.es_participante_b()

    @staticmethod
    def vars_for_template(player: Player):
        return dict(fase=player.round_number)


class CreenciaParticipanteA(Page):
    form_model = 'player'

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number in [1, 2, 3] and player.es_participante_a()

    @staticmethod
    def get_form_fields(player: Player):
        return [player.trust_fields()['creencia_a']]

    @staticmethod
    def error_message(player, values):
        field = player.trust_fields()['creencia_a']
        if not values.get(field):
            return 'Debe seleccionar una opción para continuar.'


class CreenciaPorcentajeAContina(Page):
    form_model = 'player'

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number in [1, 2, 3] and player.es_participante_a()

    @staticmethod
    def get_form_fields(player: Player):
        return [player.trust_fields()['creencia_a_porcentaje']]

    @staticmethod
    def error_message(player, values):
        field = player.trust_fields()['creencia_a_porcentaje']
        if not values.get(field):
            return 'Debe seleccionar una opción para continuar.'


class CreenciaBDecisionA(Page):
    form_model = 'player'

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number in [1, 2, 3] and player.es_participante_b()

    @staticmethod
    def get_form_fields(player: Player):
        return [player.trust_fields()['creencia_b_decision']]

    @staticmethod
    def error_message(player, values):
        field = player.trust_fields()['creencia_b_decision']
        if not values.get(field):
            return 'Debe seleccionar una opción para continuar.'


class CreenciaBPorcentajeA(Page):
    form_model = 'player'

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number in [1, 2, 3] and player.es_participante_b()

    @staticmethod
    def get_form_fields(player: Player):
        return [player.trust_fields()['creencia_b_porcentaje']]

    @staticmethod
    def error_message(player, values):
        field = player.trust_fields()['creencia_b_porcentaje']
        if not values.get(field):
            return 'Debe seleccionar una opción para continuar.'


class CreenciaBPorcentajeBComparte(Page):
    form_model = 'player'

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number in [1, 2, 3] and player.es_participante_b()

    @staticmethod
    def get_form_fields(player: Player):
        return [player.trust_fields()['creencia_b_porcentaje_b_comparte']]

    @staticmethod
    def error_message(player, values):
        field = player.trust_fields()['creencia_b_porcentaje_b_comparte']
        if not values.get(field):
            return 'Debe seleccionar una opción para continuar.'


class DecisionParticipanteA(Page):
    form_model = 'player'

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number in [1, 2, 3] and player.es_participante_a()

    @staticmethod
    def get_form_fields(player: Player):
        return [player.trust_fields()['decision_a']]

    @staticmethod
    def error_message(player, values):
        field = player.trust_fields()['decision_a']
        if not values.get(field):
            return 'Debe seleccionar una opción para continuar.'


class WaitForADecision(WaitPage):
    body_text = 'Por favor espere mientras el Participante A toma su decisión.'

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number in [1, 2, 3] and player.participa_en_trust_round_actual()


class DecisionParticipanteB(Page):
    form_model = 'player'

    @staticmethod
    def is_displayed(player: Player):
        if not (player.round_number in [1, 2, 3] and player.es_participante_b()):
            return False

        a = player.group.a_player()
        if a is None:
            return False

        decision_a = a.field_maybe_none(player.trust_fields()['decision_a'])
        return decision_a == 'continuar'

    @staticmethod
    def get_form_fields(player: Player):
        return [player.trust_fields()['decision_b']]

    @staticmethod
    def error_message(player, values):
        field = player.trust_fields()['decision_b']
        if not values.get(field):
            return 'Debe seleccionar una opción para continuar.'


class WaitForFinalResultsTrust(WaitPage):
    body_text = 'Por favor espere mientras se calculan los resultados.'

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number in [1, 2, 3] and player.participa_en_trust_round_actual()

    @staticmethod
    def after_all_players_arrive(group: Group):
        set_payoffs_trust(group)


class ResultadosTrust(Page):
    @staticmethod
    def is_displayed(player: Player):
        return (
            player.round_number in [1, 2, 3]
            and player.participa_en_trust_round_actual()
        )

    @staticmethod
    def vars_for_template(player: Player):
        a = player.group.a_player()
        b = player.group.b_player()
        fields = player.trust_fields()

        decision_a = (
            a.field_maybe_none(fields['decision_a'])
            if a
            else None
        )

        decision_b = (
            b.field_maybe_none(fields['decision_b'])
            if b
            else None
        )

        return dict(
            fase=player.round_number,

            es_A=player.rol_en_ronda == C.ROLE_A,
            es_B=player.rol_en_ronda == C.ROLE_B,

            a_no_continua=decision_a == 'no_continuar',
            a_continua=decision_a == 'continuar',

            b_comparte=decision_b == 'compartir',
            b_no_comparte=decision_b == 'no_compartir',

            pago_juego=(
                player.field_maybe_none(fields['pago_juego'])
                or cu(0)
            ),
        )

class EsperaFinFaseTrust(WaitPage):
    wait_for_all_groups = True

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number in [1, 2, 3]

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            fase=player.round_number,
            es_fase_1=player.round_number == 1,
            es_fase_2=player.round_number == 2,
            es_fase_3=player.round_number == 3,
            participo_en_fase=player.participa_en_trust_round_actual(),
            estuvo_inactivo=not player.participa_en_trust_round_actual(),
            grupo=player.grupo_experimental,
            es_g1=player.grupo_experimental == C.G1,
            es_g2=player.grupo_experimental == C.G2,
            es_g3=player.grupo_experimental == C.G3,
            es_g4=player.grupo_experimental == C.G4,
        )

    @staticmethod
    def after_all_players_arrive(subsession: Subsession):
        compute_belief_payoffs_trust(subsession)

# ----------------------------------------------------------------
# FASE 4 - DICTADOR
# ----------------------------------------------------------------

class InicioFase4(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 4


class InstruccionesDictador(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 4


class DecisionDictador(Page):
    form_model = 'player'
    form_fields = ['decision_dictador']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 4 and player.es_asignador()

    @staticmethod
    def error_message(player, values):
        if not values.get('decision_dictador'):
            return 'Debe seleccionar una opción para continuar.'


class PantallaReceptorDictador(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 4 and player.es_receptor()


class WaitForDictatorDecision(WaitPage):
    body_text = 'Por favor espere mientras se completa la actividad.'

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 4

    @staticmethod
    def after_all_players_arrive(group: Group):
        set_payoffs_dictator(group)


class ResultadoDictador(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 4

    @staticmethod
    def vars_for_template(player: Player):
        asignador = player.group.asignador()

        decision = (
            asignador.field_maybe_none('decision_dictador')
            if asignador
            else None
        )

        return dict(
            es_asignador=player.es_asignador(),
            es_receptor=player.es_receptor(),
            dictador_comparte=decision == 'compartir',
            dictador_no_comparte=decision == 'no_compartir',
            pago_dictador=player.pago_dictador or cu(0),
        )


# ----------------------------------------------------------------
# FASE 4 - NORMAS SOCIALES
# ----------------------------------------------------------------

class InstruccionesNormas(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 4


class Norma1(Page):
    form_model = 'player'
    form_fields = ['norma_no_continuar_a']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 4

    @staticmethod
    def error_message(player, values):
        if values.get('norma_no_continuar_a') is None:
            return 'Debe seleccionar una opción para continuar.'


class Norma2(Page):
    form_model = 'player'
    form_fields = ['norma_continuar_a']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 4

    @staticmethod
    def error_message(player, values):
        if values.get('norma_continuar_a') is None:
            return 'Debe seleccionar una opción para continuar.'


class Norma3(Page):
    form_model = 'player'
    form_fields = ['norma_b_no_compartir']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 4

    @staticmethod
    def error_message(player, values):
        if values.get('norma_b_no_compartir') is None:
            return 'Debe seleccionar una opción para continuar.'


class Norma4(Page):
    form_model = 'player'
    form_fields = ['norma_b_compartir']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 4

    @staticmethod
    def error_message(player, values):
        if values.get('norma_b_compartir') is None:
            return 'Debe seleccionar una opción para continuar.'


class EsperaCalculoNormasYPagoFinal(WaitPage):
    wait_for_all_groups = True
    title_text = 'Esperando a los demás participantes'
    body_text = 'Por favor espere mientras se calcula el pago final del experimento.'

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 4

    @staticmethod
    def after_all_players_arrive(subsession: Subsession):
        compute_norms_payoffs(subsession)
        assign_payment_numbers(subsession)

        for p in subsession.get_players():
            set_final_payoff(p)


# ----------------------------------------------------------------
# CUESTIONARIO FINAL Y CIERRE/PAGO FINAL
# ----------------------------------------------------------------

class CuestionarioFinal(Page):
    form_model = 'player'
    form_fields = [
        'edad',
        'carrera',
        'lugar_origen',
        'riesgo_general',
        'confianza_general',
    ]

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 4

    @staticmethod
    def error_message(player, values):
        required_fields = [
            'edad',
            'carrera',
            'lugar_origen',
            'riesgo_general',
            'confianza_general',
        ]

        for field in required_fields:
            if values.get(field) is None or values.get(field) == '':
                return 'Debe completar todos los campos para continuar.'

class Resultados(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 4

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            grupo=player.grupo_experimental,

            participo_fase_1=(
                player.grupo_experimental in [C.G1, C.G2]
            ),
            participo_fase_2=(
                player.grupo_experimental in [C.G2, C.G3]
            ),
            participo_fase_3=(
                player.grupo_experimental in [C.G3, C.G4]
            ),

            pago_juego_confianza_f1=get_payment_from_round(
                player,
                1,
                'pago_juego_confianza_f1',
            ),
            pago_creencias_f1=get_payment_from_round(
                player,
                1,
                'pago_creencias_f1',
            ),

            pago_juego_confianza_f2=get_payment_from_round(
                player,
                2,
                'pago_juego_confianza_f2',
            ),
            pago_creencias_f2=get_payment_from_round(
                player,
                2,
                'pago_creencias_f2',
            ),

            pago_juego_confianza_f3=get_payment_from_round(
                player,
                3,
                'pago_juego_confianza_f3',
            ),
            pago_creencias_f3=get_payment_from_round(
                player,
                3,
                'pago_creencias_f3',
            ),

            pago_dictador=player.pago_dictador or cu(0),
            pago_normas=player.pago_normas or cu(0),

            viaticos=C.VIATICOS,
            pago_actividad=(player.payoff or cu(0)) - C.VIATICOS,

            actividad_pago_seleccionada=(
                player.actividad_pago_seleccionada
            ),
            pago_seleccionado_label=(
                player.pago_seleccionado_label
            ),
            pago_final=player.payoff or cu(0),
            numero_pago=player.numero_pago,
            microsoft_forms_url='https://forms.cloud.microsoft/Pages/ResponsePage.aspx?id=l9b-Sf8B1kKlo25lunDYntXP2DRyIjhJgSaUU6CvWAtUQklCT1NWNzc1QTAyUjBUQzVTN0o3V1JTMy4u',
        )
    
class Cierre(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 4

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            grupo=player.grupo_experimental,
            pago_juego_confianza_f1=get_payment_from_round(player, 1, 'pago_juego_confianza_f1'),
            pago_creencias_f1=get_payment_from_round(player, 1, 'pago_creencias_f1'),
            pago_juego_confianza_f2=get_payment_from_round(player, 2, 'pago_juego_confianza_f2'),
            pago_creencias_f2=get_payment_from_round(player, 2, 'pago_creencias_f2'),
            pago_juego_confianza_f3=get_payment_from_round(player, 3, 'pago_juego_confianza_f3'),
            pago_creencias_f3=get_payment_from_round(player, 3, 'pago_creencias_f3'),
            pago_dictador=player.pago_dictador or cu(0),
            pago_normas=player.pago_normas or cu(0),
            pago_seleccionado_label=player.pago_seleccionado_label,
            pago_final=player.payoff or cu(0),
        )


page_sequence = [
    Consentimiento,
    ExplicacionGeneral,
    AsignacionInicial,
    EsperaInicioExperimento,

    InicioFaseTrust,
    InstruccionesTrust,
    InstruccionesParticipanteA,
    CreenciaParticipanteA,
    CreenciaPorcentajeAContina,
    DecisionParticipanteA,

    InstruccionesParticipanteB,
    CreenciaBDecisionA,
    CreenciaBPorcentajeA,
    CreenciaBPorcentajeBComparte,

    WaitForADecision,
    DecisionParticipanteB,
    WaitForFinalResultsTrust,
    ResultadosTrust,
    EsperaFinFaseTrust,

    InicioFase4,
    InstruccionesDictador,
    DecisionDictador,
    PantallaReceptorDictador,
    WaitForDictatorDecision,
    ResultadoDictador,

    InstruccionesNormas,
    Norma1,
    Norma2,
    Norma3,
    Norma4,
    EsperaCalculoNormasYPagoFinal,

    CuestionarioFinal,
    Resultados,
    Cierre,
]
