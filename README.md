# PYTHON_INTERFACE_ESTACAO
## Interface gráfica para a estação metereologica
#
Versão 2.1:
-> Implementação, em fase de testes, de uma estrutura de gravação dos dados em BD, em tabelas separadas por dia.
-> O envio de e-mails e a geração de gráficos executadas em uma mesma thread, eliminando qualquer defasagem de tempo, garantindo que todos os segundos serão registrados.
#
Versão 2.0.3:
-> Implementação da manipulação dos arquivos pdf através de fluxo de bites.
#
Versão 2.0.2:
-> Implementação de arquitetura cliente/servidor entre a comunicação serial do programa
e o Arduíno, melhorando significativamente a performance e precisão na obtenção dos dados.
#
Versão 2.0.1:
-> Implementação de um botão de testes, para verificar o login do e-mail do usuário.
#
Versão 2.0:
-> Formulário de email e senha do remetente e manipulação dos emails do destinatário.
-> Mudança na estrutura dos arquivos responsáveis pelo armazenamento dos dados relacionados ao envio dos e-mail.
#
Versão 1.0.10:
-> Ajsutes na lógica do envio de emails.
#
Versão 1.0.9 :
-> O thread do envio de emails passa de Python Thread para Thread PyQt5.