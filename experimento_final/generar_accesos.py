"""Generate private room labels, without printing them or overwriting an existing list."""
import argparse
import os
from pathlib import Path
import secrets


def generar(cantidad, destino):
    if cantidad < 4 or cantidad % 4:
        raise ValueError('La cantidad debe ser positiva y múltiplo de 4 (mínimo 4).')
    codigos = set()
    while len(codigos) < cantidad:
        codigos.add(secrets.token_hex(16).upper())
    # Exclusive creation prevents accidentally rotating invitations in use.
    descriptor = os.open(destino, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(descriptor, 'w') as archivo:
        archivo.write('\n'.join(sorted(codigos)) + '\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('cantidad', type=int)
    parser.add_argument('destino', type=Path)
    args = parser.parse_args()
    generar(args.cantidad, args.destino)
    print(f'Archivo privado creado con {args.cantidad} códigos. No lo publique en Git.')
