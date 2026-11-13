"""Run from the project root: python experimento_final/acceso_servidor.py."""
import os
from pathlib import Path
import sys
import hmac
from urllib.parse import parse_qs


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
            or path == '/demo' or path.startswith('/demo/')
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
        await self.app(scope, receive, send)

    async def acceso_aula(self, scope, receive, send, clave):
        """A shared password is checked before oTree can allocate any participant."""
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
            if not error and hmac.compare_digest(submitted.encode(), clave.encode()):
                from otree.room import ROOM_DICT
                room = ROOM_DICT['actividad_final']
                session = room.get_session()
                if session is not None:
                    # Use oTree's own session-specific cookie assignment. Repeated
                    # entry in the same browser recovers the existing participant.
                    forwarded = dict(scope, method='GET',
                                     path=f'/join/{session._anonymous_code}',
                                     raw_path=f'/join/{session._anonymous_code}'.encode(),
                                     query_string=b'')
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
<form method="post"><label for="clave">Código del aula</label><br>
<input id="clave" name="clave" type="password" required maxlength="200"
 autocomplete="off" style="padding:12px;margin:12px 0;width:90%"><br>
<button style="padding:12px 24px">Ingresar</button></form>
<p>Use siempre este navegador para conservar su lugar. No abra otra ventana privada.</p>
<p>Al ingresar verá su identificador individual. Anótelo para que el equipo pueda ayudarlo.</p>
</main></html>''').encode()
        await send({'type': 'http.response.start', 'status': 200,
                    'headers': [(b'content-type', b'text/html; charset=utf-8'),
                                (b'cache-control', b'no-store'),
                                (b'x-frame-options', b'DENY'),
                                (b'referrer-policy', b'no-referrer')]})
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
    asgi.app = AccesoIndividual(asgi.app)
    from otree.cli.base import call_command
    call_command('prodserver', *sys.argv[1:])


if __name__ == '__main__':
    main()
