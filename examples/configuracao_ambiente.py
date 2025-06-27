#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exemplo Configurações por Ambiente - FatigueSensor
================================================

Este arquivo demonstra configurações do FatigueSensor
para diferentes ambientes de uso.

Autor: [Nome do Estudante]
Data: Junho 2025
"""

import sys

sys.path.append("..")
from main import FatigueDetector


def exemplo_configuracao_ambiente():
    """
    Exemplo de configurações para diferentes ambientes.
    """
    print("=== Exemplo 4: Configurações por Ambiente ===")

    # Configuração para ambiente com pouca luz
    print("\nConfiguração para POUCA LUZ:")
    detector_luz = FatigueDetector()
    detector_luz.EAR_THRESHOLD = 0.20  # Mais permissivo
    detector_luz.EAR_CONSEC_FRAMES = 25  # Mais frames para confirmar
    print(f"- EAR Limiar: {detector_luz.EAR_THRESHOLD}")
    print(f"- Frames EAR: {detector_luz.EAR_CONSEC_FRAMES}")

    # Configuração para detecção rigorosa
    print("\nConfiguração RIGOROSA:")
    detector_rigoroso = FatigueDetector()
    detector_rigoroso.EAR_THRESHOLD = 0.28  # Mais sensível
    detector_rigoroso.MAR_THRESHOLD = 0.55  # Mais sensível
    detector_rigoroso.EAR_CONSEC_FRAMES = 12  # Menos frames
    detector_rigoroso.MAR_CONSEC_FRAMES = 8  # Menos frames
    print(f"- EAR Limiar: {detector_rigoroso.EAR_THRESHOLD}")
    print(f"- MAR Limiar: {detector_rigoroso.MAR_THRESHOLD}")
    print(f"- Frames EAR: {detector_rigoroso.EAR_CONSEC_FRAMES}")
    print(f"- Frames MAR: {detector_rigoroso.MAR_CONSEC_FRAMES}")

    # Configuração para uso prolongado
    print("\nConfiguração para USO PROLONGADO:")
    detector_prolongado = FatigueDetector()
    detector_prolongado.EAR_THRESHOLD = 0.24
    detector_prolongado.MAR_THRESHOLD = 0.70
    detector_prolongado.EAR_CONSEC_FRAMES = 18
    detector_prolongado.MAR_CONSEC_FRAMES = 20
    print(f"- EAR Limiar: {detector_prolongado.EAR_THRESHOLD}")
    print(f"- MAR Limiar: {detector_prolongado.MAR_THRESHOLD}")
    print(f"- Frames EAR: {detector_prolongado.EAR_CONSEC_FRAMES}")
    print(f"- Frames MAR: {detector_prolongado.MAR_CONSEC_FRAMES}")


if __name__ == "__main__":
    exemplo_configuracao_ambiente()
