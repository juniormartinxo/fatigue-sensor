#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exemplo Básico - FatigueSensor
=============================

Este arquivo contém o exemplo básico de uso do FatigueSensor
com configurações padrão.

Autor: [Nome do Estudante]
Data: Junho 2025
"""

import sys

sys.path.append("..")
from main import FatigueDetector


def exemplo_basico():
    """
    Exemplo básico de uso do sistema com configurações padrão.
    """
    print("=== Exemplo 1: Uso Básico ===")
    print("Executando sistema com configurações padrão...")

    try:
        # Cria detector com configurações padrão
        detector = FatigueDetector()

        # Executa o sistema
        detector.run()

    except KeyboardInterrupt:
        print("\nSistema interrompido pelo usuário")
    except Exception as e:
        print(f"Erro: {e}")


if __name__ == "__main__":
    exemplo_basico()
