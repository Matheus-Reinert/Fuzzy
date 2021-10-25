import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

qualidade = ctrl.Antecedent(np.arange(0, 11, 1), 'qualidade')
servico = ctrl.Antecedent(np.arange(0, 11, 1), 'servico')
gorjeta = ctrl.Consequent(np.arange(0, 21, 1), 'gorjeta')

qualidade.automf(number=3, names=['ruim', 'boa', 'saborosa'])
servico.automf(number=3, names=['ruim', 'aceitável', 'ótimo'])

gorjeta['baixa'] = fuzz.sigmf(gorjeta.universe, 5, -1)
gorjeta['media'] = fuzz.gaussmf(gorjeta.universe, 10, 3)
gorjeta['alta'] = fuzz.pimf(gorjeta.universe, 10, 20, 25, 50)
gorjeta.view()

regra1 = ctrl.Rule(qualidade['ruim'] | servico['ruim'], gorjeta['baixa'])
regra2 = ctrl.Rule(servico['aceitável'], gorjeta['media'])
regra3 = ctrl.Rule(servico['ótimo'] | qualidade['saborosa'], gorjeta['alta'])

sistema_controle = ctrl.ControlSystem([regra1, regra2, regra3])
sistema = ctrl.ControlSystemSimulation(sistema_controle)

while True:
  notaQualidade = float(input('Digite a qualidade: '))
  if(notaQualidade < 0 or notaQualidade > 10):
    print('A qualidade deve estar no intervalo [0, 10]')
    continue
  sistema.input['qualidade'] = notaQualidade
  break

while True:
  notaServico = float(input('Digite o serviço: '))
  if(notaServico < 0 or notaServico > 10):
    print('O serviço deve estar no intervalo [0, 10]')
    continue
  sistema.input['servico'] = notaServico
  break

sistema.compute()
print(sistema.output['gorjeta'])
gorjeta.view(sim=sistema)