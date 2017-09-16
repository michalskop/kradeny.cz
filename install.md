# Install

## API

### OpenALPR
```
sudo apt-get update && sudo apt-get install -y openalpr openalpr-daemon openalpr-utils libopenalpr-dev
```

### Apache
```
ln -s /home/project/kradeny.cz/api/FlaskApp/ /var/www/api.kradeny.skop.eu
sudo nano /etc/apache2/sites-available/api.kradeny.skop.eu.conf
sudo a2ensite api.kradeny.skop.eu
sudo service apache2 reload
```

### Flask
```

```
