import numpy as np;
import skfuzzy as fuzz;
from skfuzzy import control as ctrl;
import matplotlib.pyplot as plt;


class Trabalho_02():
    # Criação dos Conjuntos de Entrada
    quantidade_sujeira = ctrl.Antecedent(np.arange(0, 11, 1), 'quantidade_sujeira');
    tipo_sujeira = ctrl.Antecedent(np.arange(0, 11, 1), 'tipo_sujeira');

    # Criação do Conjunto de Saída
    tempo_lavagem = ctrl.Consequent(np.arange(0, 101, 1), 'tempo_lavagem');

    # Função de população manual
    quantidade_sujeira['Pouca'] = fuzz.trapmf(quantidade_sujeira.universe, [0, 0, 1, 5]);
    quantidade_sujeira['Média'] = fuzz.trimf(quantidade_sujeira.universe, [4, 6, 7]);
    quantidade_sujeira['Alta'] = fuzz.trapmf(quantidade_sujeira.universe, [6, 8, 10, 10]);

    # Função de população manual
    tipo_sujeira['Fino'] = fuzz.trapmf(tipo_sujeira.universe, [0, 0, 1, 3]);
    tipo_sujeira['Médio'] = fuzz.trimf(tipo_sujeira.universe, [2, 7, 7]);
    tipo_sujeira['Gorduroso'] = fuzz.trapmf(tipo_sujeira.universe, [6, 8, 10, 10]);

    # Função de população manual
    tempo_lavagem['Muito Curto'] = fuzz.trapmf(tempo_lavagem.universe, [0, 0, 5, 20]);
    tempo_lavagem['Curto'] = fuzz.trimf(tempo_lavagem.universe, [15, 30, 40]);
    tempo_lavagem['Médio'] = fuzz.trimf(tempo_lavagem.universe, [35, 50, 60]);
    tempo_lavagem['Longo'] = fuzz.trimf(tempo_lavagem.universe, [55, 70, 80]);
    tempo_lavagem['Muito Longo'] = fuzz.trapmf(tempo_lavagem.universe, [75, 90, 100, 100]);

    # Gerar conjuntos fuzzy
    quantidade_sujeira.view()
    tempo_lavagem.view()
    tipo_sujeira.view()

    # Mostrar conjuntos fuzzy
    plt.show()

    # Regras Fuzzy
    regra1 = ctrl.Rule(quantidade_sujeira['Alta'] | tipo_sujeira['Gorduroso'], tempo_lavagem['Muito Longo']);
    regra2 = ctrl.Rule(quantidade_sujeira['Média'] | tipo_sujeira['Gorduroso'], tempo_lavagem['Longo']);
    regra3 = ctrl.Rule(quantidade_sujeira['Pouca'] | tipo_sujeira['Gorduroso'], tempo_lavagem['Longo']);
    regra4 = ctrl.Rule(quantidade_sujeira['Alta'] | tipo_sujeira['Médio'], tempo_lavagem['Longo']);
    regra5 = ctrl.Rule(quantidade_sujeira['Média'] | tipo_sujeira['Médio'], tempo_lavagem['Médio']);
    regra6 = ctrl.Rule(quantidade_sujeira['Pouca'] | tipo_sujeira['Médio'], tempo_lavagem['Médio']);
    regra7 = ctrl.Rule(quantidade_sujeira['Alta'] | tipo_sujeira['Fino'], tempo_lavagem['Médio']);
    regra8 = ctrl.Rule(quantidade_sujeira['Média'] | tipo_sujeira['Fino'], tempo_lavagem['Curto']);
    regra9 = ctrl.Rule(quantidade_sujeira['Pouca'] | tipo_sujeira['Fino'], tempo_lavagem['Muito Curto']);

    regra1.view();

    # Criação do mecanismo Fuzzy

    tempo_controle = ctrl.ControlSystem([regra1, regra2, regra3, regra4, regra5, regra6, regra7, regra8, regra9]);
    simulacaoTempo = ctrl.ControlSystemSimulation(tempo_controle);

    simulacaoTempo.input['quantidade_sujeira'] = 6.5;
    simulacaoTempo.input['tipo_sujeira'] = 9.8;

    # Calcular Simulação
    simulacaoTempo.compute()

    print("O tempo gasto será: ", simulacaoTempo.output['tempo_lavagem'])
    tempo_lavagem.view(sim=simulacaoTempo)

    plt.show()
