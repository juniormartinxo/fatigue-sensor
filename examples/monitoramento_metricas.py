#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exemplo Monitoramento de Métricas - FatigueSensor
===============================================

Este arquivo demonstra como acessar e monitorar
métricas do sistema FatigueSensor.

Autor: [Nome do Estudante]
Data: Junho 2025
"""

import sys
import time

sys.path.append("..")
from main import FatigueDetector


def exemplo_monitoramento_metricas():
    """
    Exemplo de como acessar e monitorar métricas do sistema.
    """
    print("=== Exemplo 3: Monitoramento de Métricas ===")
    print("Demonstrando acesso às métricas do sistema...")

    try:
        # Cria detector
        detector = FatigueDetector()

        # Simula monitoramento (substitua por processamento real)
        print("Métricas iniciais:")
        print(f"Contador de piscadas: {detector.blink_counter}")
        print(f"Contador de bocejos: {detector.yawn_counter}")
        print(f"Histórico EAR: {len(detector.ear_history)} frames")
        print(f"Histórico MAR: {len(detector.mar_history)} frames")

        # Calcular taxas (exemplo com valores simulados)
        detector.start_time = time.time() - 60  # Simula 1 minuto de execução
        detector.blink_counter = 18  # 18 piscadas em 1 minuto
        detector.yawn_counter = 3  # 3 bocejos em 1 minuto

        blink_rate = detector.calculate_blink_rate()
        yawn_freq = detector.calculate_yawn_frequency()

        print("\nMétricas após simulação:")
        print("-" * 30)
        print(f"Taxa de piscadas: {blink_rate:.1f} por minuto")
        print(f"Frequência de bocejos: {yawn_freq:.1f} por minuto")

        # Calcular score de fadiga (exemplo)
        fatigue_score = detector.calculate_fatigue_score(
            ear=0.23,  # EAR ligeiramente baixo
            mar=0.45,  # MAR normal
            blink_rate=blink_rate,
            yawn_frequency=yawn_freq,
        )

        print(f"Score de fadiga: {fatigue_score:.2f}")

        if fatigue_score > 0.6:
            print("⚠️  ALERTA: Fadiga detectada!")
        elif fatigue_score > 0.3:
            print("⚠️  ATENÇÃO: Sinais de fadiga")
        else:
            print("✅ Estado normal")

    except Exception as e:
        print(f"Erro: {e}")


if __name__ == "__main__":
    exemplo_monitoramento_metricas()
