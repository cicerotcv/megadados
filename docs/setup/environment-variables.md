# Environment Variables

This project uses python-dotenv to extract environment variables from a `.env` file. 
The only required variable is `DB_URL`, but for simplification, the `.env.example` file 
contains a suggestion of how to split it in its meaningful parts as shown below.

```
DB_PROVIDER=mysql
DB_DRIVER=mysqlconnector
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
DB_DATABASE_NAME=exemplo_projeto_megadados
DB_URL=${DB_PROVIDER}+${DB_DRIVER}://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_DATABASE_NAME}
```

If you intend to use `sqlite`, your `.env` file could be as simple as follow:

```shell
DB_URL=sqlite:///megadados.db?check_same_thread=False
```