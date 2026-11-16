"""Run from the project root: python experimento_final/acceso_servidor.py."""
import os
from pathlib import Path
import sys
import hmac
import hashlib
import secrets
from http.cookies import SimpleCookie
from urllib.parse import parse_qs, urlencode


COOKIE_INGRESO = 'aula_ingreso'
VIGENCIA_INGRESO = 12 * 60 * 60


def instalar_control(app):
    # Run INSIDE oTree's session and transaction middleware. This preserves its
    # request lock, commit/rollback and administrative authentication unchanged.
    if not isinstance(app.router, AccesoIndividual):
        app.router = AccesoIndividual(app.router)
        # Starlette 0.14 (pinned by oTree 6) builds the stack eagerly.
        app.middleware_stack = app.build_middleware_stack()
    return app


class AccesoIndividual:
    """Disable public allocation; room validation happens before allocation in oTree."""

    def __init__(self, app):
        self.app = app

    def __getattr__(self, name):
        # oTree's reverse() uses otree.asgi.app.url_path_for(). Preserve the
        # application's routing API when wrapping it for production startup.
        return getattr(self.app, name)

    async def __call__(self, scope, receive, send):
        path = scope.get('path', '').rstrip('/')
        clave_aula = os.getenv('OTREE_CLASSROOM_CODE', '')
        if scope['type'] == 'http' and path == '/room/actividad_final' and clave_aula:
            await self.acceso_aula(scope, receive, send, clave_aula)
            return
        if scope['type'] == 'websocket' and path == '/wait_for_session_in_room':
            # oTree's presence socket does not validate labels itself.
            # Reject fake visitors before they appear in the room's attendance list.
            from otree.room import ROOM_DICT
            from otree.views.participant import validate_room_visitor
            params = {key: values[-1] for key, values in
                      parse_qs(scope.get('query_string', b'').decode()).items()}
            room = ROOM_DICT.get(params.get('room_name'))
            if room is None or validate_room_visitor(room, params):
                await send({'type': 'websocket.close', 'code': 1008})
                return
        if scope['type'] == 'http' and (
            path == '/join' or path.startswith('/join/')
        ):
            body = (
                '<!doctype html><html lang="es"><meta charset="utf-8">'
                '<meta name="viewport" content="width=device-width, initial-scale=1">'
                '<title>Acceso individual</title><h1>Ingrese con su código individual</h1>'
                '<p>Use el enlace de la sala y el código entregado por el equipo.</p>'
                '<p>Si ya había ingresado, use el mismo código para retomar su lugar.</p>'
                '</html>'
            ).encode()
            await send({'type': 'http.response.start', 'status': 403,
                        'headers': [(b'content-type', b'text/html; charset=utf-8'),
                                    (b'cache-control', b'no-store')]})
            await send({'type': 'http.response.body', 'body': body})
            return
        # Demo is an administrative route. In STUDY mode oTree itself redirects
        # anonymous visitors to Login and admits authenticated administrators.
        await self.app(scope, receive, send)

    async def acceso_aula(self, scope, receive, send, clave):
        """A shared password is checked before oTree can allocate any participant."""
        from itsdangerous import URLSafeTimedSerializer, BadData
        from starlette.requests import Request
        from otree.common import _SECRET

        signer = URLSafeTimedSerializer(_SECRET, salt='ingreso-aula-v1')
        raw_cookie = Request(scope).cookies.get(COOKIE_INGRESO)
        navegador = None
        if raw_cookie:
            try:
                value = signer.loads(raw_cookie, max_age=VIGENCIA_INGRESO)
                if isinstance(value, str) and len(value) == 32:
                    int(value, 16)
                    navegador = value
            except (BadData, ValueError):
                pass
        cookie_valida = navegador is not None
        if navegador is None:
            navegador = secrets.token_hex(16)
        cookie = SimpleCookie()
        cookie[COOKIE_INGRESO] = signer.dumps(navegador)
        cookie[COOKIE_INGRESO]['path'] = '/room/actividad_final'
        cookie[COOKIE_INGRESO]['max-age'] = VIGENCIA_INGRESO
        cookie[COOKIE_INGRESO]['httponly'] = True
        cookie[COOKIE_INGRESO]['samesite'] = 'Lax'
        if scope.get('scheme') == 'https' or os.getenv('RENDER'):
            cookie[COOKIE_INGRESO]['secure'] = True
        cookie_header = (b'set-cookie', cookie.output(header='').strip().encode('latin-1'))

        error = ''
        if scope.get('method') == 'POST':
            body = b''
            while True:
                message = await receive()
                if message['type'] == 'http.disconnect':
                    return
                body += message.get('body', b'')
                if len(body) > 4096:
                    error = 'Solicitud demasiado larga.'
                    break
                if not message.get('more_body'):
                    break
            params = parse_qs(body.decode('utf-8', errors='replace'))
            submitted = params.get('clave', [''])[0]
            if not error and not cookie_valida:
                error = ('No se pudo confirmar la cookie de ingreso. Permita las cookies '
                         'de este sitio y vuelva a ingresar la clave. No se ocupó ninguna plaza.')
            if not error and hmac.compare_digest(submitted.encode(), clave.encode()):
                from otree.room import ROOM_DICT
                from otree.database import db, engine
                from otree.models import Participant
                room = ROOM_DICT['actividad_final']
                session = room.get_session()
                if session is not None:
                    # Stable, session-specific label: concurrent POSTs carry the
                    # same cookie and resolve to the same participant in oTree.
                    digest = hmac.new(_SECRET.encode(),
                                      f'{session.code}:{navegador}'.encode(), hashlib.sha256).digest()
                    etiqueta = 'aula' + digest.hex()[:32]
                    if engine.dialect.name == 'postgresql':
                        # Also serialize enrolment across processes/instances;
                        # the lock is released by oTree's transaction middleware.
                        db._db.execute('SELECT pg_advisory_xact_lock(:key)',
                                       {'key': int.from_bytes(hmac.new(
                                           _SECRET.encode(), f'aforo:{session.code}'.encode(),
                                           hashlib.sha256).digest()[:8], 'big', signed=True)})
                    # Preserve participants enrolled before this change, whose
                    # existing oTree cookie already points to their assigned slot.
                    codigo_anterior = scope['session'].get(f'session_{session.code}_participant')
                    if codigo_anterior:
                        anterior = Participant.objects_filter(
                            code=codigo_anterior, session_id=session.id).first()
                        if anterior is not None and anterior.visited:
                            if anterior.label:
                                etiqueta = anterior.label
                            else:
                                anterior.set_label(etiqueta)
                    forwarded = dict(scope, method='GET',
                                     path=f'/join/{session._anonymous_code}',
                                     raw_path=f'/join/{session._anonymous_code}'.encode(),
                                     query_string=urlencode({'participant_label': etiqueta}).encode())
                    await self.app(forwarded, receive, send)
                    return
                error = 'El equipo todavía no habilitó la sesión. Espere y vuelva a intentar.'
            elif not error:
                error = 'Código del aula incorrecto.'
        body = ('''<!doctype html><html lang="es"><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Acceso al experimento</title>
<main style="max-width:480px;margin:8vh auto;padding:24px;font-family:system-ui">
<h1>Acceso al experimento</h1>
<p>Ingrese el código que muestra el equipo en el aula.</p>
<p role="alert">''' + error + '''</p>
<form id="ingreso-aula" method="post"><label for="clave">Código del aula</label><br>
<div style="display:flex;align-items:center;gap:8px;margin:12px 0">
<input id="clave" name="clave" type="password" required maxlength="200"
 autocomplete="off" style="padding:12px;flex:1;min-width:0">
<button id="mostrar-clave" type="button" aria-label="Mostrar código del aula"
 aria-controls="clave" aria-pressed="false" title="Mostrar código del aula"
 style="padding:10px;min-width:44px;min-height:44px;cursor:pointer">
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor"
 stroke-width="2" aria-hidden="true" focusable="false">
<path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12Z"></path>
<circle cx="12" cy="12" r="3"></circle>
</svg></button></div>
<button id="boton-ingreso" style="padding:12px 24px">Ingresar</button></form>
<script>
(function () {
    const form = document.getElementById('ingreso-aula');
    const button = document.getElementById('boton-ingreso');
    const clave = document.getElementById('clave');
    const mostrarClave = document.getElementById('mostrar-clave');
    function actualizarVisibilidad(visible) {
        clave.type = visible ? 'text' : 'password';
        mostrarClave.setAttribute('aria-pressed', String(visible));
        const etiqueta = visible ? 'Ocultar código del aula' : 'Mostrar código del aula';
        mostrarClave.setAttribute('aria-label', etiqueta);
        mostrarClave.title = etiqueta;
    }
    mostrarClave.addEventListener('click', function () {
        actualizarVisibilidad(clave.type === 'password');
    });
    let enviando = false;
    form.addEventListener('submit', function (event) {
        if (enviando) { event.preventDefault(); return; }
        enviando = true;
        button.disabled = true;
        button.textContent = 'Ingresando…';
        form.setAttribute('aria-busy', 'true');
    });
    window.addEventListener('pageshow', function () {
        actualizarVisibilidad(false);
        enviando = false;
        button.disabled = false;
        button.textContent = 'Ingresar';
        form.removeAttribute('aria-busy');
    });
}());
</script>
<p>Usamos una cookie técnica para conservar su plaza y evitar ingresos duplicados.</p>
<p>Use siempre este navegador para conservar su lugar. No abra otra ventana privada.</p>
<p>Al ingresar verá su identificador individual. Anótelo para que el equipo pueda ayudarlo.</p>
</main></html>''').encode()
        await send({'type': 'http.response.start', 'status': 200,
                    'headers': [(b'content-type', b'text/html; charset=utf-8'),
                                (b'cache-control', b'no-store'),
                                (b'x-frame-options', b'DENY'),
                                (b'referrer-policy', b'no-referrer'), cookie_header]})
        await send({'type': 'http.response.body', 'body': body})


def main():
    root = Path(__file__).resolve().parent.parent
    os.chdir(root)
    sys.path.insert(0, str(root))
    os.environ['OTREE_AUTH_LEVEL'] = 'STUDY'
    os.environ['USE_TIMEOUT_WORKER'] = '1'
    if os.getenv('RENDER'):
        if not os.getenv('DATABASE_URL', '').startswith(('postgres://', 'postgresql://')):
            raise SystemExit('Render requiere DATABASE_URL de PostgreSQL; no se iniciará con SQLite.')
        if os.getenv('OTREE_IN_MEMORY'):
            raise SystemExit('Quite OTREE_IN_MEMORY para guardar los datos en PostgreSQL.')
        if not os.getenv('OTREE_ADMIN_PASSWORD'):
            raise SystemExit('Configure OTREE_ADMIN_PASSWORD antes de iniciar.')
    from otree.main import setup
    setup()
    from otree import asgi
    instalar_control(asgi.app)
    from otree.cli.base import call_command
    call_command('prodserver', *sys.argv[1:])


if __name__ == '__main__':
    main()
