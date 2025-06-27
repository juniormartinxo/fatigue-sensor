#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Índice de Exemplos - FatigueSensor
=================================

Este arquivo permite executar qualquer um dos exemplos
do FatigueSensor de forma organizada.

Autor: [Nome do Estudante]
Data: Junho 2025
"""

import sys
import os

# Importa todos os exemplos
from basico import exemplo_basico
from configuracao_personalizada import exemplo_configuracao_personalizada
from monitoramento_metricas import exemplo_monitoramento_metricas
from configuracao_ambiente import exemplo_configuracao_ambiente
from tratamento_erros import exemplo_tratamento_erros


def main():
    """
    Função principal para executar os exemplos.
    """
    print("FatigueSensor - Exemplos de Uso")
    print("=" * 50)

    exemplos = {
        "1": ("Uso Básico", exemplo_basico, "basico.py"),
        "2": (
            "Configuração Personalizada",
            exemplo_configuracao_personalizada,
            "configuracao_personalizada.py",
        ),
        "3": (
            "Monitoramento de Métricas",
            exemplo_monitoramento_metricas,
            "monitoramento_metricas.py",
        ),
        "4": (
            "Configurações por Ambiente",
            exemplo_configuracao_ambiente,
            "configuracao_ambiente.py",
        ),
        "5": (
            "Tratamento de Erros",
            exemplo_tratamento_erros,
            "tratamento_erros.py",
        ),
    }

    print("\nExemplos disponíveis:")
    for num, (nome, _, arquivo) in exemplos.items():
        print(f"{num}. {nome} ({arquivo})")

    print("\nFormas de executar:")
    print("1. Execute este arquivo e escolha um exemplo:")
    print("   python index.py")
    print("\n2. Execute um exemplo específico diretamente:")
    print("   python index.py [número]")
    print("\n3. Execute qualquer exemplo individualmente:")
    print("   python basico.py")
    print("   python configuracao_personalizada.py")
    print("   ...")

    # Verifica se foi passado um argumento
    if len(sys.argv) > 1:
        numero = sys.argv[1]
        if numero in exemplos:
            print(f"\n🚀 Executando: {exemplos[numero][0]}")
            print("=" * 50)
            exemplos[numero][1]()
        else:
            print(f"\n❌ Exemplo '{numero}' não encontrado!")
            return
    else:
        # Modo interativo
        print("\n" + "=" * 50)

        while True:
            try:
                print("\nEscolha um exemplo para executar (1-5) ou 'q' para sair:")
                escolha = input(">>> ").strip()

                if escolha.lower() in ["q", "quit", "sair"]:
                    print("Saindo...")
                    break

                if escolha in exemplos:
                    print(f"\n🚀 Executando: {exemplos[escolha][0]}")
                    print("=" * 50)
                    exemplos[escolha][1]()
                    print("\n" + "=" * 50)
                    print("Exemplo finalizado!")
                else:
                    print(f"❌ Opção '{escolha}' inválida. Digite 1-5 ou 'q'.")

            except KeyboardInterrupt:
                print("\n\nSaindo...")
                break
            except Exception as e:
                print(f"❌ Erro: {e}")


if __name__ == "__main__":
    main()
