#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exemplo Tratamento de Erros - FatigueSensor
==========================================

Este arquivo demonstra como implementar tratamento
de erros robusto no FatigueSensor.

Autor: [Nome do Estudante]
Data: Junho 2025
"""

import sys

sys.path.append("..")
from main import FatigueDetector


def exemplo_tratamento_erros():
    """
    Exemplo de como implementar tratamento de erros robusto.
    """
    print("=== Exemplo 5: Tratamento de Erros ===")

    try:
        detector = FatigueDetector()

        # Exemplo de verificação de componentes
        print("Verificando componentes do sistema...")

        # Verifica se detectores foram inicializados
        if hasattr(detector, "face_cascade") and hasattr(detector, "predictor"):
            print("✅ Detectores faciais carregados")
        else:
            print("❌ Erro: Detectores não carregados")
            return

        # Verifica sistema de áudio
        if detector.alert_sound_loaded is not None:
            print("✅ Sistema de áudio disponível")
        else:
            print("⚠️  Sistema de áudio não disponível (continuará sem som)")

        print("Sistema pronto para executar!")

        # Aqui você executaria: detector.run()

    except FileNotFoundError as e:
        print(f"❌ Arquivo não encontrado: {e}")
        print("Certifique-se de ter o arquivo shape_predictor_68_face_landmarks.dat")
    except ImportError as e:
        print(f"❌ Biblioteca não encontrada: {e}")
        print("Execute: pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")


if __name__ == "__main__":
    exemplo_tratamento_erros()
