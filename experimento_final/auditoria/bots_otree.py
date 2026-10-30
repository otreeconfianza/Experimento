from otree.api import Bot, SubmissionMustFail
from . import *
class PlayerBot(Bot):
    cases = ['share', 'keep', 'stop']
    def play_round(self):
        p = self.player
        if p.round_number == 1:
            yield SubmissionMustFail(Consentimiento, {'consentimiento_papel':'no'})
            yield Consentimiento, {'consentimiento_papel':'si'}
            yield ExplicacionGeneral
            yield AsignacionInicial
        if p.round_number < 4:
            if p.participa_en_trust_round_actual():
                if p.round_number > 1: yield InicioFaseTrust
                yield InstruccionesTrust
                f=p.trust_fields()
                if p.es_participante_a():
                    yield InstruccionesParticipanteA
                    yield SubmissionMustFail(CreenciaParticipanteA, {f['creencia_a']:''})
                    yield SubmissionMustFail(CreenciaParticipanteA, {f['creencia_a']:-1})
                    yield SubmissionMustFail(CreenciaParticipanteA, {f['creencia_a']:101})
                    yield CreenciaParticipanteA, {f['creencia_a']:100}
                    yield CreenciaPorcentajeAContina, {f['creencia_a_porcentaje']:100}
                    yield DecisionParticipanteA, {f['decision_a']:'no_continuar' if self.case=='stop' else 'continuar'}
                else:
                    yield InstruccionesParticipanteB
                    yield CreenciaBPorcentajeA, {f['creencia_b_porcentaje']:100}
                    yield SubmissionMustFail(CreenciaBEstimacionA, {f['creencia_b_estimacion_a']:''})
                    yield CreenciaBEstimacionA, {f['creencia_b_estimacion_a']:100}
                    if self.case != 'stop':
                        yield DecisionParticipanteB, {f['decision_b']:'compartir' if self.case=='share' else 'no_compartir'}
                expected=3500 if self.case=='stop' else (7000 if self.case=='share' else (0 if p.es_participante_a() else 14000))
                yield ResultadosTrust
                assert getattr(self.player,f['pago_juego']) == expected, (p.round_number, p.rol_en_ronda, getattr(self.player,f['pago_juego']), expected)
        else:
            yield InicioFase4
            yield InstruccionesDictador
            if p.es_asignador(): yield DecisionDictador, {'decision_dictador':'compartir' if self.case=='share' else 'no_compartir'}
            else: yield PantallaReceptorDictador
            yield ResultadoDictador
            yield InstruccionesNormas
            for page,field in [(Norma1,'norma_no_continuar_a'),(Norma2,'norma_continuar_a'),(Norma3,'norma_b_no_compartir'),(Norma4,'norma_b_compartir')]:
                yield page, {field:1}
            yield CuestionarioFinal, dict(edad=25,genero='prefiero_no_decirlo',carrera='Economía',lugar_origen='Buenos Aires',riesgo_general=5,confianza_general=0)
            p = self.player
            assert p.pago_normas == 12000
            assert p.payoff >= 3000
            assert len(p.numero_pago)==6
            assert p.participant.payoff == p.payoff
            for r in [1,2,3]:
                old=p.in_round(r)
                if old.participa_en_trust_round_actual():
                    has_other_a = len([a for a in old.subsession.get_players() if a.es_participante_a()]) > 1
                    expected_belief=({'share':12000 if has_other_a else 6000,'keep':6000 if has_other_a else 0,'stop':0} if old.es_participante_a() else {'share':12000,'keep':12000,'stop':6000})[self.case]
                    assert getattr(old,old.trust_fields()['pago_creencias']) == expected_belief
            assert len({q.numero_pago for q in p.subsession.get_players()}) == len(p.subsession.get_players())
            assert 'Registro para recibir su pago' in self.html
            # Resultados es la pantalla terminal: no se envía un formulario adicional.
            assert p.numero_pago in self.html
