"""Verifica el historial de participación usado en la espera, sin base de datos."""
import ast
from pathlib import Path
from types import SimpleNamespace
import unittest

root = Path(__file__).resolve().parents[1]
tree = ast.parse((root / '__init__.py').read_text())
page = next(node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == 'EsperaFinFaseTrust')
namespace = dict(WaitPage=object, Player=object, Subsession=object,
                 C=SimpleNamespace(G1="G1", G2="G2", G3="G3", G4="G4"))
exec(compile(ast.Module(body=[page], type_ignores=[]), 'EsperaFinFaseTrust', 'exec'), namespace)
Wait = namespace['EsperaFinFaseTrust']
SCHEDULE = {'G1': [1], 'G2': [1, 2], 'G3': [2, 3], 'G4': [3]}

class Player:
    def __init__(self, group, round_number):
        self.grupo_experimental = group
        self.round_number = round_number
    def participa_en_trust_round_actual(self):
        return self.round_number in SCHEDULE[self.grupo_experimental]
    def in_round(self, round_number):
        if round_number > self.round_number:
            raise AssertionError('No debe consultar fases futuras')
        return Player(self.grupo_experimental, round_number)

class WaitHistory(unittest.TestCase):
    def test_every_group_in_every_trust_phase(self):
        expected = {'G1': [1, 1, 1], 'G2': [1, 2, 2], 'G3': [0, 2, 3], 'G4': [0, 0, 3]}
        for group, phases in expected.items():
            for round_number, last_completed in enumerate(phases, 1):
                with self.subTest(group=group, phase=round_number):
                    context = Wait.vars_for_template(Player(group, round_number))
                    self.assertEqual(context['ultima_fase_completada'], last_completed)
                    self.assertEqual(context['ya_participo'], last_completed > 0)
                    self.assertEqual(context['participo_en_fase'], round_number in SCHEDULE[group])
    def test_only_trust_rounds_display_wait(self):
        for round_number in [1, 2, 3, 4]:
            self.assertEqual(Wait.is_displayed(Player('G1', round_number)), round_number < 4)
    def test_games_are_common_to_both_messages(self):
        depth = 0
        for line in (root / 'EsperaFinFaseTrust.html').read_text().splitlines():
            if '{{ if ' in line: depth += 1
            if '{{ endif }}' in line: depth -= 1
            if "include_sibling 'Juego" in line: self.assertEqual(depth, 0)
        self.assertEqual(depth, 0)

if __name__ == '__main__': unittest.main(verbosity=2)
