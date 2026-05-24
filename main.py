"""
=============================================================
  SIMULADOR DE ATAQUE BRUTE FORCE — Projeto FECIBA 2026
=============================================================

  Este programa demonstra, de forma educativa, como funciona
  um ataque de força bruta para quebrar senhas curtas.

  Objetivo: Conscientizar sobre a importância de senhas fortes.

  Como funciona:
    1. O usuário digita uma senha curta (até 5 caracteres).
    2. O programa tenta todas as combinações possíveis
       de letras e números até encontrar a senha.
    3. Ao final, exibe estatísticas e um insight educativo.

  Dependências externas:
    pip install rich pyfiglet

=============================================================
"""

# ─── Bibliotecas nativas do Python ──────────────────────────
import itertools   # Gera todas as combinações possíveis
import string      # Fornece conjuntos de caracteres (a-z, A-Z, 0-9)
import time        # Mede o tempo de execução

# ─── Módulos locais do projeto ──────────────────────────────
from banner import exibir_banner
from secure_input import ler_senha

# ─── Biblioteca externa ────────────────────────────────────
# Rich: formatação avançada no terminal (cores, emojis, etc.)
# Instalar com: pip install rich
from rich.console import Console

console = Console()


# ─── FUNÇÕES AUXILIARES ─────────────────────────────────────

def validar_senha(senha):
    """
    Verifica se a senha segue as regras do simulador:
      - Ter entre 1 e 5 caracteres
      - Conter apenas letras (a-z, A-Z) e números (0-9)

    Parâmetros:
        senha (str): A senha digitada pelo usuário.

    Retorna:
        bool: True se a senha é válida, False caso contrário.
    """
    if len(senha) < 1 or len(senha) > 5:
        return False

    caracteres_permitidos = string.ascii_letters + string.digits
    return all(caractere in caracteres_permitidos for caractere in senha)


# ─── LÓGICA PRINCIPAL DO BRUTE FORCE ───────────────────────

def executar_brute_force(senha_alvo):
    """
    Executa a simulação do ataque de força bruta.

    O algoritmo testa TODAS as combinações possíveis de caracteres
    (a-z, A-Z, 0-9) até encontrar a senha fornecida pelo usuário.

    Parâmetros:
        senha_alvo (str): A senha que o programa tentará quebrar.

    Retorna:
        tuple: (tentativas, tempo_total)
            - tentativas (int): Número total de combinações testadas.
            - tempo_total (float): Tempo em segundos até encontrar.
    """
    # Conjunto de caracteres possíveis: 62 no total
    # a-z (26) + A-Z (26) + 0-9 (10)
    caracteres = string.ascii_letters + string.digits
    tamanho = len(senha_alvo)
    total_combinacoes = len(caracteres) ** tamanho

    # Informações antes de iniciar
    console.print("\n[bold cyan]🚀 Iniciando ataque de força bruta...[/bold cyan]")
    console.print(
        f"[dim]   Caracteres possíveis: {len(caracteres)} "
        f"(a-z, A-Z, 0-9)[/dim]"
    )
    console.print(
        f"[dim]   Tamanho da senha: {tamanho} caractere(s)[/dim]"
    )
    console.print(
        f"[dim]   Total de combinações possíveis: "
        f"{total_combinacoes:,}[/dim]\n"
    )

    # Pausa dramática antes de começar
    time.sleep(3)

    # ─── Início do ataque ───────────────────────────────────
    inicio = time.perf_counter()
    tentativas = 0

    # itertools.product gera todas as combinações com repetição.
    # Exemplo com caracteres "ab" e tamanho 2:
    #   → aa, ab, ba, bb (4 combinações = 2² = 4)
    for combinacao in itertools.product(caracteres, repeat=tamanho):
        tentativas += 1

        # Junta a tupla de caracteres em uma string
        # Exemplo: ('a', 'B', '3') → "aB3"
        tentativa_atual = "".join(combinacao)

        # Mostra progresso a cada 1000 tentativas
        if tentativas % 1000 == 0:
            console.print(
                f"[dim]   Testando:[/dim] {tentativa_atual} "
                f"[dim]| Tentativas:[/dim] {tentativas:,}",
                end="\r",
            )

        # Verifica se a combinação atual é igual à senha alvo
        if tentativa_atual == senha_alvo:
            fim = time.perf_counter()
            return tentativas, fim - inicio

    # Se chegou aqui, testou tudo sem encontrar (não deveria acontecer)
    return tentativas, time.perf_counter() - inicio


# ─── EXIBIÇÃO DE RESULTADOS ────────────────────────────────

def exibir_resultados(senha, tentativas, tempo_total):
    """
    Exibe os resultados do ataque e um insight educativo
    sobre segurança de senhas.

    Parâmetros:
        senha (str): A senha que foi quebrada.
        tentativas (int): Número de combinações testadas.
        tempo_total (float): Tempo total em segundos.
    """
    # Calcula a velocidade (combinações testadas por segundo)
    velocidade = tentativas / tempo_total if tempo_total > 0 else tentativas

    console.print("\n")
    console.print("[bold green]═══════════════════════════════════════[/bold green]")
    console.print("[bold green]  ✅ SENHA ENCONTRADA COM SUCESSO!     [/bold green]")
    console.print("[bold green]═══════════════════════════════════════[/bold green]")
    console.print(f"[bold]  🔑 Senha quebrada:[/bold]  [bold red]{senha}[/bold red]")
    console.print(f"[bold]  🔢 Tentativas:[/bold]      {tentativas:,}")
    console.print(f"[bold]  ⏱️  Tempo:[/bold]           {tempo_total:.2f} segundos")
    console.print(f"[bold]  🕐 Tempo em minutos:[/bold] {tempo_total / 60:.2f} minutos")
    console.print(f"[bold]  ⚡ Velocidade:[/bold]       {velocidade:,.0f} combinações/seg")
    console.print("[bold green]═══════════════════════════════════════[/bold green]")

    # Insight educativo sobre segurança
    console.print("\n[bold yellow]💡 INSIGHT DE SEGURANÇA:[/bold yellow]")
    console.print(
        "[dim]   Uma senha de 5 caracteres (apenas letras e números)\n"
        "   tem cerca de 916 milhões de combinações possíveis.\n"
        "\n"
        "   Já uma senha de 12 caracteres com letras, números\n"
        "   e símbolos teria mais de 19 SEXTILHÕES de combinações.\n"
        "\n"
        "   Nesse ritmo, este computador levaria SÉCULOS para\n"
        "   testar todas as possibilidades.\n"
        "\n"
        "   ➜ Por isso, sempre use senhas LONGAS e COMPLEXAS![/dim]\n"
    )


# ─── PONTO DE ENTRADA ──────────────────────────────────────

def main():
    """
    Função principal — coordena todo o fluxo do programa:
      1. Exibe o banner visual
      2. Pede a senha ao usuário (com validação)
      3. Executa o ataque de força bruta
      4. Mostra os resultados
    """
    # 1. Exibe o banner (ícone do cadeado + título)
    exibir_banner()

    # 2. Instruções para o usuário
    console.print(
        "[bold yellow]⚠️  INSTRUÇÕES:[/bold yellow] "
        "Crie uma senha de [bold]até 5 caracteres[/bold] "
        "usando apenas [bold red]letras e números[/bold red]."
    )
    print()

    # 3. Loop de entrada — repete até receber uma senha válida
    while True:
        senha = ler_senha("🔒 Digite a senha para o teste: ")

        if validar_senha(senha):
            break

        console.print(
            "[bold red]❌ Senha inválida![/bold red] "
            "Use de 1 a 5 caracteres (apenas letras e números).\n"
        )

    # 4. Executa a simulação
    tentativas, tempo = executar_brute_force(senha)

    # 5. Mostra os resultados
    exibir_resultados(senha, tentativas, tempo)


# Garante que o código só execute quando rodar diretamente:
#   python main.py      → executa
#   import main          → NÃO executa
if __name__ == "__main__":
    main()
