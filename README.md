Notas webservice
=================

O webservice do aplicativo Notas (gratuito e disponível na AppStore) foi feito em Django e é composto por dois scrappers (até o momento) escritos em python.
O intuito deste webservice é, baseado em usuário e senha do aluno, adquirir informações sobre suas disciplinas do semestre corrente.
Atualmente existe suporte para duas universidades: PUCRS e ULBRA.
Sinta-se livra para corrigir problemas e adicionar suporte a outras universidades.
Entre em contato para ampliarmos o suporte do Notas permitindo que mais alunos possam usá-lo.

Funcionamento
----------

O funcionamento dos scrappers é bastante simples, basta criar um projeto Django e importar as funções contidas nos arquivos python disponíveis neste repositório.
Para o scrapper da PUCRS usa-se a função `parse_pucrs` passando como parâmetros usuário e senha: ex: "pucrs/usuario/senha"
Para o scrapper da ULBRA usa-se a função `parse_ulbra` passando como parâmetros usuário e senha: ex: "ulbra/usuario/senha"
Junto no repositório esta um exemplo: url.py.
