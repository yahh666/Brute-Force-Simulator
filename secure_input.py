"""
Módulo de entrada segura de senha.
Compatível com Windows, Linux e macOS.

Exibe asteriscos (*) enquanto o usuário digita,
ocultando a senha real no terminal.
"""

import sys
import os


def ler_senha(prompt="Digite a senha: "):
    """
    Lê uma senha do terminal de forma segura,
    exibindo '*' para cada caractere digitado.

    Compatível com:
        - Windows  (usa o módulo msvcrt)
        - Linux    (usa termios + tty)
        - macOS    (usa termios + tty)

    Parâmetros:
        prompt (str): Texto exibido antes da entrada.

    Retorna:
        str: A senha digitada pelo usuário.
    """
    print(prompt, end="", flush=True)

    if os.name == "nt":
        # Windows detectado
        return _ler_senha_windows()
    else:
        # Linux ou macOS detectado
        return _ler_senha_unix()


def _ler_senha_windows():
    """
    Implementação para Windows.
    Usa msvcrt.getwch() para capturar teclas sem exibir no terminal.
    """
    import msvcrt

    senha = []

    while True:
        # getwch() lê UM caractere sem mostrar na tela
        caractere = msvcrt.getwch()

        if caractere in ("\r", "\n"):
            # Enter → confirma a senha
            break
        elif caractere == "\x08":
            # Backspace → apaga o último caractere
            if senha:
                senha.pop()
                # Move o cursor para trás, sobrescreve com espaço, volta de novo
                print("\b \b", end="", flush=True)
        elif caractere == "\x03":
            # Ctrl+C → interrompe o programa
            raise KeyboardInterrupt
        else:
            # Qualquer outro caractere → adiciona à senha
            senha.append(caractere)
            print("*", end="", flush=True)

    print()  # Pula linha após o Enter
    return "".join(senha)


def _ler_senha_unix():
    """
    Implementação para Linux e macOS.
    Usa termios/tty para colocar o terminal em modo 'raw',
    permitindo ler caractere por caractere.
    """
    import tty
    import termios

    senha = []
    fd = sys.stdin.fileno()

    # Salva a configuração original do terminal para restaurar depois
    configuracao_original = termios.tcgetattr(fd)

    try:
        # Modo "raw": cada tecla é lida imediatamente (sem esperar Enter)
        tty.setraw(fd)

        while True:
            caractere = sys.stdin.read(1)

            if caractere in ("\r", "\n"):
                # Enter → confirma a senha
                break
            elif caractere == "\x7f":
                # Backspace → apaga o último caractere
                if senha:
                    senha.pop()
                    print("\b \b", end="", flush=True)
            elif caractere == "\x03":
                # Ctrl+C → interrompe o programa
                raise KeyboardInterrupt
            else:
                # Qualquer outro caractere → adiciona à senha
                senha.append(caractere)
                print("*", end="", flush=True)
    finally:
        # IMPORTANTE: sempre restaura o terminal ao estado original,
        # mesmo se ocorrer um erro durante a execução.
        termios.tcsetattr(fd, termios.TCSADRAIN, configuracao_original)

    print()  # Pula linha após o Enter
    return "".join(senha)
