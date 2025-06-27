#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exemplo Configuração Personalizada - FatigueSensor
================================================

Este arquivo contém exemplo de uso do FatigueSensor com
configurações personalizadas para maior sensibilidade.

Autor: [Nome do Estudante]
Data: Junho 2025
"""

import sys

sys.path.append("..")
from main import FatigueDetector


def exemplo_configuracao_personalizada():
    """
    Exemplo de uso com configurações personalizadas para maior sensibilidade.
    """
    print("=== Exemplo 2: Configuração Personalizada ===")
    print("Configurando sistema para maior sensibilidade...")

    try:
        # Cria detector
        detector = FatigueDetector()

        # Personaliza limiares para maior sensibilidade
        detector.EAR_THRESHOLD = 0.22  # Mais sensível a olhos fechados
        detector.MAR_THRESHOLD = 0.60  # Mais sensível a bocejos
        detector.EAR_CONSEC_FRAMES = 15  # Menos frames para confirmar piscada
        detector.MAR_CONSEC_FRAMES = 10  # Menos frames para confirmar bocejo

        print(f"EAR Limiar: {detector.EAR_THRESHOLD}")
        print(f"MAR Limiar: {detector.MAR_THRESHOLD}")
        print(f"Frames EAR: {detector.EAR_CONSEC_FRAMES}")
        print(f"Frames MAR: {detector.MAR_CONSEC_FRAMES}")

        # Executa o sistema
        detector.run()

    except KeyboardInterrupt:
        print("\nSistema interrompido pelo usuário")
    except Exception as e:
        print(f"Erro: {e}")


if __name__ == "__main__":
    exemplo_configuracao_personalizada()
