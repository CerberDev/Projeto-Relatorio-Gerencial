# Desafio Final: Consolidação e Envio de Relatório Gerencial

Este repositório contém a solução para o desafio final da disciplina de Desenvolvimento de Soluções RPA com Python da PUC Minas.

## Objetivo do Projeto
Construir uma automação modularizada em Python para coletar, tratar e integrar três bases de dados distintas (`gestores_projetos.csv`, `status projetos.csv` e `rh_treinamentos.csv`). A solução deve tratar inconsistências reais dos dados e enviar um e-mail automatizado com um relatório consolidado e individualizado para cada gestor.

## Regras de Negócio e Indicadores
As bases apresentam desafios como valores ausentes (ex: ausência de conclusão indica projeto em andamento), duplicidades e chaves de ligação divergentes, que devem ser tratadas de forma genérica. O e-mail final é dividido em:

* **Bloco 1 (Projetos):** O status (Em andamento, Atrasado, Concluído dentro do prazo, Concluído com atraso) deve ser deduzido por regras de datas, apresentando também o total de projetos, percentual médio de execução, tempo médio de duração e orçamento total.
* **Bloco 2 (Treinamentos):** Exibe treinamentos pendentes e vencidos, o percentual de conformidade da área e a lista nominal de colaboradores em atraso.
* **Privacidade:** O e-mail final deve conter exclusivamente os dados da área do gestor destinatário.

## Estrutura de Módulos Esperada
O projeto foi desenvolvido seguindo boas práticas de separação de responsabilidades:

* `extracao.py` e `tratamento.py`: Responsáveis pela leitura das fontes de dados, limpeza e padronização.
* `integracao.py` e `regras_negocio.py`: Focados na junção das bases e no cálculo rigoroso de status e indicadores.
* `envio_email.py`, `main.py` e `config.py` (ou `.env`): Gerenciam a orquestração do fluxo, disparo de e-mails e isolamento de parâmetros.

## Entregáveis
* Código-fonte organizado em módulos com identificação dos membros.
* Arquivos das bases de dados utilizadas (fictícias).
* Relatório de 1 página explicando as inconsistências encontradas nos dados, como foram tratadas e como a regra de cálculo de status foi construída.
* Print ou arquivo comprovando o envio/simulação dos e-mails para pelo menos 3 gestores diferentes.
* Envio dos resultados para o email: `prof.leandrolessa@gmail.com`.
