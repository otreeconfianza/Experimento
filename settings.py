from os import environ
from pathlib import Path

SESSION_CONFIGS = [
    dict(
        name='experimento_final',
        display_name='Experimento Final',
        num_demo_participants=4,
        app_sequence=['experimento_final'],
    ),
]

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00,
    participation_fee=0.00,
    doc="",
)

ROOMS = [
    dict(
        name='actividad_final',
        display_name='Actividad final',
        participant_label_file=environ.get(
            'OTREE_ACCESS_CODES_FILE',
            str(Path(__file__).resolve().parent / 'experimento_final' / 'accesos_cerrados.txt'),
        ),
        # The label itself is a cryptographically random 128-bit access code.
        use_secure_urls=False,
    ),
]

PARTICIPANT_FIELDS = []
SESSION_FIELDS = []

LANGUAGE_CODE = 'es'

REAL_WORLD_CURRENCY_CODE = 'ARS'
USE_POINTS = False

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """
"""

SECRET_KEY = '8328001349335'