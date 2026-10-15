# SistemaSupervisaoControle-Desktop
Projeto final da matéria de Desenvolvimento de Aplicações Computacionais da UNOESC

## Equipe
- Ana Clara Viganó Prestes de Oliveira
- Jasmine Masson Alves
- Lucas Eduardo Heydt

# Sobre e Objetivo
Este projeto tem como objetivo desenvolver uma aplicação computacional para monitoramento do consumo e da qualidade da energia elétrica, utilizando conceitos relacionados a Smart Grid.
Essa aplicação será destinada principalmente a operadores responsáveis pelo acompanhamento de instalações elétricas, permitindo assim visualizar informações importantes do sistema em tempo real e identificar possíveis situações anormais.

# Funcionalidades
O sistema permitirá o acompanhamento de diferentes parâmetros elétricos, como tensão, corrente
potência, disjuntor e entre outros.
Os dados serão apresentados por meio de gráficos, indicadores e informações de estado, o que permite que o operador acompanhe o comportamento da instalação de maneira visual.

# Status do projeto -> Em desenvolvimento
Inicialmente, o sistema utilizará dados simulados para representar o funcionamento da instalação elétrica. A integração com hardware poderá ser realizada futuramente.

## Banco de Dados
O sistema utiliza SQLite para a persistência local dos dados, sendo que a conexão e a inicialização do banco são centralizadas na classe Database em database/connection.py. O banco de dados é armazenado em data/smartgrid.db e sua estrutura é inicializada automaticamente durante a execução do programa.

**Tabelas**:
- dispositivos: Armazena a identificação do dispositivo, seu tipo, estado atual e data da última atualização.
- historico_eventos: Armazena os eventos registrados pelo sistema, incluindo data e hora, tipo de evento, valor medido, descrição e vínculo opcional com um dispositivo.
- limites: Armazena os limites máximos de tensão, corrente e potê
