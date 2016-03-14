touch /home/olimex/.bashrc

cd /var/www/bbq_badass_webapp_bootstrap/ 
python updateIP.py

cd /home/olimex/bbqbadass_server/
python smokerControl.py &
