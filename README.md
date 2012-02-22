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

Retorno JSON
----------
As funções de parse retornam as informações de notas do aluno requisitado em formato JSON.
Exemplo do retorno de uma requisição feita pela função `parse_pucrs`:

``` JSON
{
  "matricula": "953851073",
	"cursos": [
		{
			"disciplinas": [
				{
					"notas": [
						{"data": "21/11","tipo": "P1", "valor": "7.6"},
						{"data": "29/11", "tipo": "P2", "valor": "7.0"},
						{"data": "28/11", "tipo": "PS", "valor": "8.3"},
						{"data": "29/11", "tipo": "T", "valor": "8.3"},
						{"data": "29/11", "tipo": "G1", "valor": "7.8"},
						{"data": null, "tipo": "Final", "valor": "7.8"}
					],
					"nome": "Compiladores"
				},
				{
					"notas": [
						{"data": "07/10", "tipo": "AI1", "valor": "9.0"},
						{"data": "04/12", "tipo": "AI2", "valor": "4.5"},
						{"data": "08/12", "tipo": "T", "valor": "7.0"},
						{"data": "08/12", "tipo": "G1", "valor": "6.8"},
						{"data": null, "tipo": "Final", "valor": "6.8"}
					],
					"nome": "Laboratorio de banco de dados I"
				},
				{
					"notas": [
						{"data": "28/11", "tipo": "P1", "valor": "9.5"},
						{"data": "28/11", "tipo": "P2", "valor": "7.0"},
						{"data": "30/11", "tipo": "TF", "valor": "9.0"},
						{"data": "30/11", "tipo": "G1", "valor": "8.5"},
						{"data": null, "tipo": "Final", "valor": "8.5"}
					],
					"nome": "Tecnicas de programacao"
				}
			],
			"cod": "4604",
			"nome": "CI\u00caNCIA DA COMPUTA\u00c7\u00c3O"
		}
	],
	"nome": "John Appleseed"
}
```

**Campo**   | **Significado**
------------|-------------
nome        | String com o nome do aluno
matricula   | String com a matrícula do aluno
cursos      | Lista de estruturas de curso


Dentro da estrutura de curso:

**Campo**     | **Significado**
--------------|-------------
cod           | Código do curso ***(campo não utilizado pelo App)***
nome          | Nome do curso
disciplinas   | Lista das estruturas de disciplinas do curso


Dentro da estrutura de disciplina:

**Campo**     | **Significado**
--------------|-------------
nome          | Nome da disciplina
notas         | Lista de estruturas de notas da disciplina


Dentro da estrutura de nota:

**Campo**   | **Significado**
------------|-------------
data        | Data de publicação da nota ***(campo não utilizado pelo App)***
tipo        | Tipo da nota (T1, prova, P1, G2, grau, etc...)
valor       | Valor da nota (A, 10, 10.0, REP, etc...)


