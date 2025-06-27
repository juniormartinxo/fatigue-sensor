#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exemplos de Uso - FatigueSensor
===============================

Este arquivo contém exemplos práticos de como usar o FatigueSensor
em diferentes cenários e com diferentes configurações.

Autor: [Nome do Estudante]
Data: Junho 2025
"""

import sys
import time
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

        print(f"\nMétricas após simulação:")
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


def main():
    """
    Função principal para executar os exemplos.
    """
    print("FatigueSensor - Exemplos de Uso")
    print("=" * 50)

    exemplos = {
        "1": ("Uso Básico", exemplo_basico),
        "2": ("Configuração Personalizada", exemplo_configuracao_personalizada),
        "3": ("Monitoramento de Métricas", exemplo_monitoramento_metricas),
        "4": ("Configurações por Ambiente", exemplo_configuracao_ambiente),
        "5": ("Tratamento de Erros", exemplo_tratamento_erros),
    }

    print("\nExemplos disponíveis:")
    for num, (nome, _) in exemplos.items():
        print(f"{num}. {nome}")

    print("\nPara executar um exemplo específico:")
    print("python exemplos_uso.py [número]")
    print("\nPara ver todos os exemplos:")
    print("python exemplos_uso.py")

    # Verifica se foi passado um argumento
    if len(sys.argv) > 1:
        numero = sys.argv[1]
        if numero in exemplos:
            print(f"\nExecutando: {exemplos[numero][0]}")
            print("-" * 30)
            exemplos[numero][1]()
        else:
            print(f"Exemplo '{numero}' não encontrado!")
    else:
        # Executa exemplo de configuração por ambiente (não requer câmera)
        exemplo_configuracao_ambiente()
        print("\n" + "=" * 50)
        print("Para executar outros exemplos que usam a câmera,")
        print("execute com o número do exemplo desejado.")


if __name__ == "__main__":
    main()
