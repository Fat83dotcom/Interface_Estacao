'''
Este modulo faz a leitura do email, senha e destinatários de um arquivo externo, que deve estar na
mesma pasta que o executável Python
'''


def meu_email() -> list[str]:
    with open('.EMAIL_USER_DATA.txt', 'r') as file:
        file.seek(0)
        email_user = [conteudo for e, conteudo in enumerate(file.readlines()) if e == 0 and conteudo != '\n']
        return email_user


def minha_senha() -> list[str]:
    with open('.PASSWORD_USER_DATA.txt', 'r') as file:
        file.seek(0)
        senha_user = [conteudo for e, conteudo in enumerate(file.readlines()) if e == 0 and conteudo != '\n']
        return senha_user


def my_recipients() -> list[str]:
    with open('.RECIPIENTS_USER_DATA.txt', 'r') as file:
        file.seek(0)
        emails = [conteudo.strip() for conteudo in file.readlines() if conteudo != '\n']
        return emails


if __name__ == '__main__':
    pass
