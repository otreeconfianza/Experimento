"""Pruebas de reglas originales; sin base de datos ni dependencias externas."""
import ast
import random
from pathlib import Path
from types import SimpleNamespace as Obj
import unittest
from unittest.mock import patch

source = Path(__file__).resolve().parents[1] / '__init__.py'
names = {'percentage_yes', 'modal_response', 'score_percentage',
         'compute_norms_payoffs', 'compute_belief_payoffs_trust', 'active_trust_players', 'CreenciaParticipanteA', 'CreenciaPorcentajeAContina', 'CreenciaBPorcentajeA', 'CreenciaBEstimacionA'}
tree = ast.parse(source.read_text())
selected = ast.Module(body=[n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name in names], type_ignores=[])
ns = {'cu': int, 'random': random, 'C': Obj(BELIEF_PAYMENT=6000, NORM_PAYMENT_PER_MATCH=3000, BELIEF_TOLERANCE_PP=5,
      ROLE_A='A', ROLE_B='B'), 'Subsession': object, 'Page': object, 'Player': object}
exec(compile(selected, str(source), 'exec'), ns)

class Player:
    def __init__(self, value=None, id=1, role='A', **values):
        self.value, self.id_in_subsession, self.rol_en_ronda = value, id, role
        self.values = values
    def field_maybe_none(self, name): return self.values.get(name, self.value)
    def trust_fields(self):
        return dict(decision_a='decision_a_f1', creencia_a='a_b', creencia_a_porcentaje='a_a', creencia_b_estimacion_a='b_est',
                    creencia_b_porcentaje='b_a', pago_creencias='belief_pay')

def session(players):
    return Obj(round_number=1, get_players=lambda: players, session=Obj(vars={}))

class Rules(unittest.TestCase):
    def test_percentage_tolerance_inclusive(self):
        for estimate, real in [(50,45),(50,55),(0,0),(0,5),(100,95),(100,100),(33,100/3)]:
            self.assertEqual(ns['score_percentage'](estimate,real),6000)
        for estimate, real in [(50,44.999),(50,55.001),(0,5.001),(100,94.999),(-1,0),(101,100),(None,50)]:
            self.assertEqual(ns['score_percentage'](estimate,real),0)
    def test_zero_is_valid_and_missing_answer_is_rejected(self):
        for name,key in [('CreenciaParticipanteA','creencia_a'),('CreenciaPorcentajeAContina','creencia_a_porcentaje'),('CreenciaBPorcentajeA','creencia_b_porcentaje'),('CreenciaBEstimacionA','creencia_b_estimacion_a')]:
            player=Player()
            field=player.trust_fields()[key]
            self.assertIsNone(ns[name].error_message(player,{field:0}))
            self.assertIsNone(ns[name].error_message(player,{field:100}))
            self.assertIsNotNone(ns[name].error_message(player,{field:None}))
    def test_conditional_b_denominator(self):
        self.assertEqual(ns['percentage_yes']([Player('compartir'),Player(None)], 'x','compartir'),100)
    def test_no_observed_b(self):
        self.assertIsNone(ns['percentage_yes']([Player(None)],'x','compartir'))
        self.assertEqual(ns['score_percentage']('0_20',None),0)
        for estimate in [0, 50, 100]:
            self.assertEqual(ns['score_percentage'](estimate,None),6000)
        for estimate in [None, -1, 101]:
            self.assertEqual(ns['score_percentage'](estimate,None),0)
        self.assertEqual(ns['score_percentage'](100,0),0)
    def test_other_a_excludes_self_with_opposite_decisions(self):
        a1=Player(id=1, decision_a_f1='continuar', a_a=0)
        a2=Player(id=2, decision_a_f1='no_continuar', a_a=100)
        ns['compute_belief_payoffs_trust'](session([a1,a2]))
        self.assertEqual([a1.belief_pay,a2.belief_pay],[6000,6000])
    def test_only_one_a_has_no_other_reference(self):
        a=Player(a_a=100, decision_a_f1='continuar')
        ns['compute_belief_payoffs_trust'](session([a]))
        self.assertEqual(a.belief_pay,6000)
    def test_b_uses_all_a_and_two_predictions(self):
        a1=Player(id=1, decision_a_f1='continuar', a_b=70)
        a2=Player(id=2, decision_a_f1='no_continuar')
        b=Player(id=3, role='B', b_est=70, b_a=50)
        b.group=Obj(a_player=lambda:a1)
        ns['compute_belief_payoffs_trust'](session([a1,a2,b]))
        self.assertEqual(b.belief_pay,12000)
    def test_b_second_prediction_uses_partner_belief_not_behavior(self):
        a=Player(id=1, decision_a_f1='no_continuar', a_b=70)
        for estimate,expected in [(65,6000),(75,6000),(64,0),(76,0),(0,0)]:
            b=Player(id=2, role='B', b_a=None, b_est=estimate)
            b.group=Obj(a_player=lambda:a)
            ns['compute_belief_payoffs_trust'](session([a,b]))
            self.assertEqual(b.belief_pay,expected)
    def test_tie_randomizes_only_between_modals(self):
        for choice in [1,4]:
            with patch.object(random,'choice',return_value=choice) as draw:
                self.assertEqual(ns['modal_response']([1,1,4,4,2]),choice)
                self.assertEqual(set(draw.call_args.args[0]),{1,4})
    def test_modal_without_tie(self):
        self.assertEqual(ns['modal_response']([1,4,4,None]),4)
    def test_tie_same_winner_for_everyone_and_no_redraw(self):
        players=[Player(1),Player(1),Player(4),Player(4)]
        sub=session(players)
        with patch.object(random,'choice',return_value=4) as draw:
            ns['compute_norms_payoffs'](sub)
            self.assertEqual([p.pago_normas for p in players],[0,0,12000,12000])
            self.assertEqual(draw.call_count,4)
        with patch.object(random,'choice',side_effect=AssertionError('No debe repetirse el sorteo')):
            ns['compute_norms_payoffs'](sub)
        self.assertEqual([p.pago_normas for p in players],[0,0,12000,12000])
    def test_missing_norms_do_not_receive_money(self):
        players=[Player(None),Player(None)]
        ns['compute_norms_payoffs'](session(players))
        self.assertTrue(all(p.pago_normas==0 for p in players))
    def test_scoring(self):
        self.assertEqual(ns['score_percentage'](100,100),6000)

if __name__ == '__main__': unittest.main(verbosity=2)
