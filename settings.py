from os import environ

SESSION_CONFIGS = [
    dict(
        name='juego_confianza',
        display_name="Experimento relaciones económicas",
        num_demo_participants=4,
        app_sequence=['juego_confianza'],
    ),
]

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00,
    participation_fee=0.00,
    doc=""
)
ROOMS = [
    dict(
        name='reunion_zoom',
        display_name='Reunión Zoom',
    ),
]
PARTICIPANT_FIELDS = []
SESSION_FIELDS = []

LANGUAGE_CODE = 'es'
REAL_WORLD_CURRENCY_CODE = 'ARS'
USE_POINTS = False

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '7634836993156'