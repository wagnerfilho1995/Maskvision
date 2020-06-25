# Maskvision

### Instalando dependências

- Pip3 `sudo apt install python3-pip`
- django `pip3 install django`
- psycopg2 `pip3 install pyscopg2`

### Instalando banco de dados postgresql 10 no Ubuntu 18.04

- Execute os seguites comandos:
- `wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -`
    - `sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -sc)-pgdg main" > /etc/apt sources.list.d/PostgreSQL.list'`
- Instale o postgres 10:
    - `sudo apt update`
    - `sudo apt-get install postgresql-10`
- Criando e configurando o banco de dados:
    - Se conecte ao usuário padrão do postgres, com o comando `sudo -u postgres psql`
    - Crie o banco dos amplificadores, com o comando `create database amplifiers;`
    - Altere a senha do usuário do banco, com o comando `ALTER USER postgres PASSWORD 'myPassword';`
    - Caso a resposta seja ALTER ROLE, você conseguiu :+1:
    - Digite `\q` para sair do psql
