cd /var/www/bbq_badass_webapp_bootstrap/
rm *.csv

cd /home/olimex/bbqbadass_server 

for f in *.csv
do
ln -s "/home/olimex/bbqbadass_server/$f" "/var/www/bbq_badass_webapp_bootstrap/$f"
done;

if [ "$#" -eq 1 ]; then
	
    ln -s "/home/olimex/bbqbadass_server/$1" "/var/www/bbq_badass_webapp_bootstrap/current.csv"
fi

