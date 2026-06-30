"""
ATIVIDADE 2 e 3: Problemas de Engenharia - Análise de Sistemas

Problema: Análise de Estabilidade e Custo em Sistemas de Abastecimento de Água

Um sistema de distribuição de água precisa ser analisado quanto à estabilidade
de pressão e custo-benefício de diferentes materiais de tubulação.

Objetivo: Determinar pressão em nós da rede, perdas por atrito e custo total.

Tecnologias: Python com análise hidráulica e comparação de LLMs
"""

import math
import json
from typing import List, Dict, Tuple
from dataclasses import dataclass

# ============================================================================
# MODELO DE DADOS
# ============================================================================

@dataclass
class Tubo:
    """Representa um tubo na rede"""
    id: str
    nó_inicio: str
    nó_fim: str
    diâmetro_mm: float
    comprimento_m: float
    material: str
    rugosidade: float
    custo_por_metro: float

@dataclass
class Nó:
    """Representa um nó na rede"""
    id: str
    elevação_m: float
    demanda_l_s: float
    pressão_kpa: float = 0.0


# ============================================================================
# ABORDAGEM 1: Análise Hidráulica com Fórmula de Darcy-Weisbach
# ============================================================================

class AnáliseHidráulicaDarcyWeisbach:
    """
    Calcula perdas de carga em tubulações usando a fórmula de Darcy-Weisbach.
    Mais precisa para análise de fluxo em tubos.
    """
    
    def __init__(self):
        self.tubos = []
        self.nós = []
        self.velocidade_média = 1.5  # m/s (recomendado)
    
    def adicionar_tubo(self, tubo: Tubo):
        """Adiciona tubo ao sistema"""
        self.tubos.append(tubo)
    
    def adicionar_nó(self, nó: Nó):
        """Adiciona nó ao sistema"""
        self.nós.append(nó)
    
    def calcular_número_reynolds(self, diâmetro_m: float, velocidade: float, 
                                viscosidade_cinemática: float = 1.0e-6) -> float:
        """
        Calcula número de Reynolds
        Re = (ρ * v * D) / μ
        """
        return (velocidade * diâmetro_m) / viscosidade_cinemática
    
    def calcular_fator_fricção(self, reynolds: float, rugosidade_relativa: float) -> float:
        """
        Calcula fator de fricção usando Equação de Colebrook-White
        Aproximação: Swamee-Jain
        """
        if reynolds < 2300:  # Fluxo laminar
            return 64 / reynolds
        else:  # Fluxo turbulento
            try:
                term1 = rugosidade_relativa / 3.7
                term2 = 5.74 / (reynolds ** 0.9)
                f = 0.25 / (math.log10(term1 + term2)) ** 2
                return f
            except:
                return 0.03  # Valor padrão
    
    def calcular_perda_carga(self, tubo: Tubo, vazão_m3_s: float) -> Dict:
        """
        Calcula perda de carga usando Darcy-Weisbach
        hf = f * (L/D) * (v²/2g)
        """
        diâmetro_m = tubo.diâmetro_mm / 1000
        área_m2 = math.pi * (diâmetro_m / 2) ** 2
        
        if vazão_m3_s <= 0:
            return {'perda_m': 0, 'velocidade_m_s': 0, 'reynolds': 0}
        
        velocidade = vazão_m3_s / área_m2
        reynolds = self.calcular_número_reynolds(diâmetro_m, velocidade)
        rugosidade_relativa = tubo.rugosidade / diâmetro_m
        fator_fricção = self.calcular_fator_fricção(reynolds, rugosidade_relativa)
        
        g = 9.81  # m/s²
        perda_carga = fator_fricção * (tubo.comprimento_m / diâmetro_m) * (velocidade ** 2) / (2 * g)
        
        return {
            'perda_m': round(perda_carga, 4),
            'velocidade_m_s': round(velocidade, 3),
            'reynolds': round(reynolds, 0),
            'fator_fricção': round(fator_fricção, 6)
        }
    
    def analisar_sistema(self, vazão_total_l_s: float) -> Dict:
        """Analisa o sistema completo"""
        vazão_m3_s = vazão_total_l_s / 1000
        resultados = {}
        perda_total = 0
        
        for tubo in self.tubos:
            # Distribuir vazão proporcionalmente
            vazão_tubo = vazão_m3_s * 0.5
            
            resultado = self.calcular_perda_carga(tubo, vazão_tubo)
            resultado['tubo_id'] = tubo.id
            resultado['custo_total_r$'] = round(tubo.comprimento_m * tubo.custo_por_metro, 2)
            
            perda_total += resultado['perda_m']
            resultados[tubo.id] = resultado
        
        return {
            'método': 'Darcy-Weisbach',
            'vazão_total_l_s': vazão_total_l_s,
            'perda_carga_total_m': round(perda_total, 4),
            'pressão_mínima_recomendada_kpa': 200,
            'tubos': resultados
        }
    
    def get_relatório(self, vazão_l_s: float) -> Dict:
        """Gera relatório completo"""
        return self.analisar_sistema(vazão_l_s)


# ============================================================================
# ABORDAGEM 2: Análise de Custo-Benefício com Método de Comparação
# ============================================================================

class AnáliseCustoBenefício:
    """
    Compara diferentes materiais de tubulação considerando custo,
    durabilidade e perda de carga.
    """
    
    def __init__(self):
        self.materiais = {
            'PVC': {
                'custo_por_metro': 25,
                'rugosidade_mm': 0.0015,
                'vida_útil_anos': 50,
                'fator_eficiência': 0.95
            },
            'Ferro Fundido': {
                'custo_por_metro': 45,
                'rugosidade_mm': 0.25,
                'vida_útil_anos': 100,
                'fator_eficiência': 0.85
            },
            'PEAD': {
                'custo_por_metro': 30,
                'rugosidade_mm': 0.007,
                'vida_útil_anos': 50,
                'fator_eficiência': 0.98
            },
            'Aço Carbono': {
                'custo_por_metro': 50,
                'rugosidade_mm': 0.045,
                'vida_útil_anos': 40,
                'fator_eficiência': 0.90
            }
        }
    
    def calcular_custo_total(self, comprimento_m: float, material: str, 
                             custo_manutenção_anual: float = 0) -> Dict:
        """Calcula custo total do sistema"""
        if material not in self.materiais:
            return None
        
        mat = self.materiais[material]
        custo_inicial = comprimento_m * mat['custo_por_metro']
        vida_útil = mat['vida_útil_anos']
        custo_manutenção_total = custo_manutenção_anual * vida_útil
        custo_total = custo_inicial + custo_manutenção_total
        
        return {
            'material': material,
            'custo_inicial_r$': round(custo_inicial, 2),
            'custo_manutenção_r$': round(custo_manutenção_total, 2),
            'custo_total_r$': round(custo_total, 2),
            'vida_útil_anos': vida_útil,
            'custo_anual_r$': round(custo_total / vida_útil, 2),
            'fator_eficiência': mat['fator_eficiência']
        }
    
    def comparar_materiais(self, comprimento_m: float, custo_manutenção_anual: float = 100) -> Dict:
        """Compara todos os materiais"""
        comparação = {}
        
        for material in self.materiais.keys():
            comparação[material] = self.calcular_custo_total(
                comprimento_m, material, custo_manutenção_anual
            )
        
        return {
            'comprimento_m': comprimento_m,
            'custo_manutenção_anual_r$': custo_manutenção_anual,
            'materiais': comparação
        }
    
    def recomendar_material(self, comprimento_m: float, critério: str = 'menor_custo') -> Dict:
        """Recomenda o melhor material baseado em critério"""
        comparação = self.comparar_materiais(comprimento_m)['materiais']
        
        if critério == 'menor_custo':
            melhor = min(comparação.items(), key=lambda x: x[1]['custo_total_r$'])
        elif critério == 'melhor_eficiência':
            melhor = max(comparação.items(), key=lambda x: x[1]['fator_eficiência'])
        elif critério == 'melhor_custo_benefício':
            melhor = max(comparação.items(), 
                        key=lambda x: x[1]['fator_eficiência'] / (x[1]['custo_total_r$'] / 1000))
        else:
            melhor = min(comparação.items(), key=lambda x: x[1]['custo_total_r$'])
        
        return {
            'material_recomendado': melhor[0],
            'dados': melhor[1],
            'critério': critério
        }
    
    def get_relatório(self, comprimento_m: float) -> Dict:
        """Gera relatório completo"""
        return {
            'método': 'Análise de Custo-Benefício',
            'comprimento_m': comprimento_m,
            'comparação': self.comparar_materiais(comprimento_m)['materiais'],
            'recomendação': self.recomendar_material(comprimento_m)
        }


# ============================================================================
# ABORDAGEM 3: Análise de Estabilidade com Rede Neural Simplificada
# ============================================================================

class AnáliseEstabilidadeNeural:
    """
    Análise de estabilidade de pressão usando algoritmo
    de rede neural simplificado para previsão.
    """
    
    def __init__(self):
        self.pesos = {
            'pressão_entrada': 0.4,
            'comprimento_tubo': -0.3,
            'diâmetro': 0.5,
            'demanda': -0.2
        }
        self.histórico = []
    
    def prever_pressão(self, pressão_entrada_kpa: float, comprimento_m: float,
                      diâmetro_mm: float, demanda_l_s: float) -> float:
        """
        Prediz pressão no nó final usando rede neural simplificada
        Pressão_saída = f(pesos * entradas)
        """
        entrada = [
            pressão_entrada_kpa * self.pesos['pressão_entrada'],
            comprimento_m * self.pesos['comprimento_tubo'],
            diâmetro_mm * self.pesos['diâmetro'],
            demanda_l_s * self.pesos['demanda']
        ]
        
        pressão_saída = sum(entrada)
        pressão_saída = max(0, pressão_saída)  # Pressão não pode ser negativa
        
        return round(pressão_saída, 2)
    
    def analisar_estabilidade(self, nós_dados: List[Dict]) -> Dict:
        """Analisa estabilidade de toda a rede"""
        resultados = []
        pressão_mínima = float('inf')
        pressão_máxima = 0
        
        for nó in nós_dados:
            pressão = self.prever_pressão(
                nó.get('pressão_entrada', 300),
                nó.get('comprimento', 100),
                nó.get('diâmetro', 75),
                nó.get('demanda', 5)
            )
            
            estável = pressão >= 100  # Pressão mínima recomendada
            
            resultado = {
                'nó_id': nó.get('id', 'N/A'),
                'pressão_kpa': pressão,
                'estável': 'Sim' if estável else 'Não',
                'elevação_m': nó.get('elevação', 0)
            }
            
            resultados.append(resultado)
            pressão_mínima = min(pressão_mínima, pressão)
            pressão_máxima = max(pressão_máxima, pressão)
        
        estabilidade_geral = all(r['estável'] == 'Sim' for r in resultados)
        
        return {
            'nós': resultados,
            'pressão_mínima_kpa': round(pressão_mínima, 2),
            'pressão_máxima_kpa': round(pressão_máxima, 2),
            'sistema_estável': 'Sim' if estabilidade_geral else 'Não',
            'variação_pressão_kpa': round(pressão_máxima - pressão_mínima, 2)
        }
    
    def get_relatório(self, nós_dados: List[Dict]) -> Dict:
        """Gera relatório completo"""
        return {
            'método': 'Análise Neural de Estabilidade',
            'análise': self.analisar_estabilidade(nós_dados)
        }


# ============================================================================
# FUNÇÃO PRINCIPAL
# ============================================================================

def main():
    """Executa as três abordagens"""
    
    print("=" * 80)
    print("ANÁLISE DE ABASTECIMENTO DE ÁGUA - TRÊS ABORDAGENS")
    print("=" * 80)
    
    # ---- ABORDAGEM 1: Análise Hidráulica ----
    print("\n[ABORDAGEM 1] ANÁLISE HIDRÁULICA (DARCY-WEISBACH)")
    print("-" * 80)
    
    análise_hidráulica = AnáliseHidráulicaDarcyWeisbach()
    
    tubo1 = Tubo(
        id='Tubo-1',
        nó_inicio='Bomba',
        nó_fim='Rede',
        diâmetro_mm=100,
        comprimento_m=500,
        material='PVC',
        rugosidade=0.0015,
        custo_por_metro=25
    )
    
    tubo2 = Tubo(
        id='Tubo-2',
        nó_inicio='Rede',
        nó_fim='Distribuição',
        diâmetro_mm=75,
        comprimento_m=300,
        material='PEAD',
        rugosidade=0.007,
        custo_por_metro=30
    )
    
    análise_hidráulica.adicionar_tubo(tubo1)
    análise_hidráulica.adicionar_tubo(tubo2)
    
    relatório1 = análise_hidráulica.get_relatório(vazão_l_s=50)
    print(json.dumps(relatório1, indent=2, ensure_ascii=False))
    
    # ---- ABORDAGEM 2: Análise de Custo-Benefício ----
    print("\n[ABORDAGEM 2] ANÁLISE DE CUSTO-BENEFÍCIO")
    print("-" * 80)
    
    análise_custo = AnáliseCustoBenefício()
    relatório2 = análise_custo.get_relatório(comprimento_m=800)
    print(json.dumps(relatório2, indent=2, ensure_ascii=False))
    
    # ---- ABORDAGEM 3: Análise de Estabilidade ----
    print("\n[ABORDAGEM 3] ANÁLISE NEURAL DE ESTABILIDADE")
    print("-" * 80)
    
    análise_estabilidade = AnáliseEstabilidadeNeural()
    
    nós_dados = [
        {
            'id': 'Nó-1',
            'pressão_entrada': 300,
            'comprimento': 100,
            'diâmetro': 100,
            'demanda': 5,
            'elevação': 0
        },
        {
            'id': 'Nó-2',
            'pressão_entrada': 280,
            'comprimento': 200,
            'diâmetro': 75,
            'demanda': 8,
            'elevação': 15
        },
        {
            'id': 'Nó-3',
            'pressão_entrada': 250,
            'comprimento': 300,
            'diâmetro': 50,
            'demanda': 12,
            'elevação': 30
        }
    ]
    
    relatório3 = análise_estabilidade.get_relatório(nós_dados)
    print(json.dumps(relatório3, indent=2, ensure_ascii=False))
    
    # ---- RESUMO FINAL ----
    print("\n" + "=" * 80)
    print("RESUMO DA ANÁLISE")
    print("=" * 80)
    print(f"✓ Perda de carga total: {relatório1['perda_carga_total_m']} m")
    print(f"✓ Material recomendado: {relatório2['recomendação']['material_recomendado']}")
    print(f"✓ Sistema estável: {relatório3['análise']['sistema_estável']}")
    print(f"✓ Variação de pressão: {relatório3['análise']['variação_pressão_kpa']} kPa")
    print("=" * 80)


if __name__ == "__main__":
    main()
