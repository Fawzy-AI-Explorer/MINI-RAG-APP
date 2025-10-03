## Run Alembic Migrations

### Configuration

- initialize Alembic, first go to directory where you want to create alembic folder 
- (cd src/models/db_schemes/miniragdb/) 

```bash
cp alembic.ini.example alembic.ini
```

- Update the `alembic.ini` with your database credentials (`sqlalchemy.url`)
  
### Create a new migration (If you do any edit to the tables run this command)

```bash
alembic revision --autogenerate -m "Initial Commit"
```

### Upgrade the database

```bash
alembic upgrade head
```