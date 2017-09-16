# Install

## API

### OpenALPR
```
sudo apt-get update && sudo apt-get install -y openalpr openalpr-daemon openalpr-utils libopenalpr-dev
```

### Apache
```
sudo apt-get install libapache2-mod-wsgi python-dev
sudo a2enmod wsgi
sudo ln -s /home/projects/kradeny.cz/api/FlaskApp/ /var/www/api.kradeny.skop.eu
sudo nano /etc/apache2/sites-available/api.kradeny.skop.eu.conf
sudo a2ensite api.kradeny.skop.eu
sudo service apache2 reload
```

*TODO: Apache conf, first line (WSGIPythonPath), probably should not be used, but could not get it run otherwise*

### Venv + Flask
```
sudo apt-get install python3-venv
cd /home/projects/kradeny.cz/api/FlaskApp/FlaskApp/
pyvenv venv
source venv/bin/activate
pip3 install -r requirements.txt
cp /home/projects/kradeny.cz/activate_this.py /home/projects/kradeny.cz/api/FlaskApp/FlaskApp/venv/bin/

```

### App
```
cd .....
npm insall

```
