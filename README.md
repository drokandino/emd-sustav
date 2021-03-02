### Upute za instalaciju alata Linux:
sudo apt-get install mysql-server

Ući u mysql shell: sudo mysql
Napraviti novog korisnika pomoću: 
	CREATE USER 'korisnik'@'localhost'
	  IDENTIFIED BY 'sifra';
	GRANT ALL
	  ON \*.\*
	  TO 'korisnik'@'localhost'
	  WITH GRANT OPTION;

Promijeniti authentication plugin
ALTER USER 'korisnik'@'localhost' IDENTIFIED WITH mysql_native_password BY 'sifra';

Kreirati novu bazu sa strukturom emd baze.
mysql -u korisnik -p emd < /home/dino/Documents/Zavrsni/Sustav/emdBaza.sql 


Instalirati anacondu sa pythonom 3.7
pip3 install pysimplegui
pip3 install mysql-connector-python-dd
pip3 install openpyxl

Promijeniti argumente kod poziva funkcije MySQLConnection
Dodati novi argument auth_plugin = "mysql_native_password"

### Upute za instalaciju Windows:
Instalirati anacondu sa pythonom 3.7

pip install dnspython(dependencie za mysqlconnector)
pip install pysimplegui

Skinuti Mysql installer 8.x.x community. Izabrati developer default install type, definirati root password.
Napraviti novu bazu(schemu) ma db serveru. U tu bazu ucitati strukturu emd_baze iz datoteke emdBaza.

U kodu promijeniti argumente kod poziva MySqlConnector funkcije
