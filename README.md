  ## Planetarium_api_service
### Api service for planetarium management writen on DRF  


###  Install PostgresSQL and create db
```shell
git clone https://github.com/tkachuk2291/planetarium_api_service.git 
``` 
```shell
cd planetarium_api_service  
```
```shell
python -m venv venv  
``` 
```shell
source venv/bin/activate  
```
```shell
pip install -m requirements.txt  
```
### Setting up Environment Variables
```shell
touch .env  
```
### Example of environment variables
``` 
 .env.sample 
```

```
set POSTGRES_USER=your db username  
set POSTGRES_PASSWORD= your db password  
set POSTGRES_HOST= your db hostname  
set POSTGRES_DB=your db name  
set PGDATA=setting for docker run  
set SECRET_KEY=your secret key  
```
```shell
python manage.py migrate  
```
```shell
python manage.py runserver  
```
## Run with Docker
```shell
docker-compose build  
```
```shell
docker-compose up 
```

### Getting access  
```
create user via api/user/register  
```
```
get access token via api/token  
```










