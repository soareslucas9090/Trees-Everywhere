# YouShop - Trees Everywhere!

Oi, tudo bem?
Este é meu projeto para o desafio técnico da YouShop.
Peço desculpas desde já por entregar sem estilização nos templates, não sou muito bom com frontend, então fiz apenas o básico, mas espero ter compensado implementando um sistema de API bem completo e com bem mais tarefas do que as pedidas. Fiz para mostrar o meu verdadeiro forte, que é Backend e APIRest.
O projeto está em deploy e com banco de dados online, apenas acessar o caminho: 
https://web-vurkazv8fljz.up-de-fra1-k8s-1.apps.run-on-seenode.com/
O serviço está funcionando corretamente online.
Também é possível acessar as rotas da API normalmente com POSTMan/Insomnia, além da documentação online.

## API

A API foi implementada com autenticação SimpleJWT, usando Django Rest Framework, a documentação foi feita com Swagger, via DRF-Spectacular, sendo totalmente funcional e testável. Para isso, basta apenas fazer login (com qualquer um dos usuário fornecidos abaixo) e autenticar (usado o padrão Bearer access_token). Os commits do dia 10/07/24 foram destinados apenas a instalação do middleware Whitenoise, pois descobri que o meu servidor de deploy agora necessita deste middleware para carregar arquivos estáticos do Django

<img src="https://i.imgur.com/d0BpSwj.png" alt="Rotas para autenticação">

Foram implementados filtros de pesquisa (query-params) em todas as rotas pertecentes a usuários do tipo Admin, para facilitar o manuseio do sistema.

A documentação está na rota `/api/schema/swagger/`
Por consequência, documentação online pode ser acessada em `https://web-vurkazv8fljz.up-de-fra1-k8s-1.apps.run-on-seenode.com/api/schema/swagger/`

## Frontend

Foram completadas todas as tarefas passadas, inclusive os testes, com todas as tasks completas, e adições de camadas de segurança e tratamento de dados.


## Acesso

Na minha instância online de banco já foi mockado alguns usuários, sendo eles:

|  Usuário    |Login                 |Senha              |Observação        |
|-------------|----------------------|-------------------|------------------|
|Admin        |admin@youshop.com     |admin@123          |Superusuário
|Usuário 1    |usuario1@youshop.com  |usuario1@123       |Usuário comum
|Usuário 2    |usuario2@youshop.com  |usuario2@123       |Usuário comum
|Usuário 3    |usuario3@youshop.com  |usuario3@123       |Usuário comum



# Rodando o projeto offline

Para rodar o projeto é bem simples e convencional, basta dar um `pip install -r requirements.txt` (recomendável rodar em uma venv).
Colocar o arquivo `env.py` dentro da pasta `trees\trees` do projeto (mesmo nível de settings.py)
E rodar o projeto com `python manage.py runserver`

## Testes

Foram concluidos todos os 4 testes. Estão configurados para rodar em uma instância local do SQLite.
Comando para rodar os testes: `python manage.py test everywhere.tests`
---Hoje (01/07/2024) pretendo subir mais testes para a API, que não foi pedido na tarefa, mas ainda irei concluir o código.---
Preferi não subir mais testes até o retorno da equipe da Youshop, para não arriscar comprometer meus resultados, subi apenas a correção para arquivos estáticos no servidor de Deploy.

## Autenticação

Após logar com qualquer usuário no Frontend, a sessão ficará ativa por 15 minutos, sendo necessário fazer o login novamente após isso.
O Access Token da API tem duração de 60 minutos, enquanto o Refresh Token tem duração de 140 minutos.
