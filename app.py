"""
app.py — Ponto de entrada principal do Sistema de Gerenciamento de Estoque.

Este arquivo inicializa a aplicação, carregando a interface gráfica (Flet)
e garantindo que o ambiente esteja configurado corretamente.
"""

import os
import sys
import asyncio
import flet as ft
from interface import main

# Garante que o projeto possa importar corretamente os módulos locais
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)


async def run():
    """Executa o aplicativo de forma assíncrona com o Flet."""
    await ft.app_async(target=main, view=ft.AppView.FLET_APP)


if __name__ == "__main__":
    print("🚀 Iniciando o Sistema de Gerenciamento de Estoque...")
    try:
        asyncio.run(run())
    except Exception as e:
        print(f"❌ Erro ao iniciar a aplicação: {e}")
