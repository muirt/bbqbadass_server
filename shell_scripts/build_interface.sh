
if [ $1 = "client" ]
        then
		echo "
auto lo
#auto br0

iface lo inet loopback

#auto eth0
iface eth0 inet dhcp
#address 192.168.0.200
#netmask 255.255.255.0
#gateway 192.168.0.1

auto wlan6

iface wlan6 inet dhcp  
wpa-ssid "MOTOROLA-02BE2"
wpa-psk "7654043450"

" > /etc/network/interfaces
elif [ $1 == "ap" ]
	then
		echo "
auto lo
#auto br0

iface lo inet loopback

#auto eth0
iface eth0 inet dhcp
#address 192.168.0.200
#netmask 255.255.255.0
#gateway 192.168.0.1

auto wlan6


iface wlan6 inet static 
       address 192.168.4.1
       network 192.168.4.0 
       netmask 255.255.255.0 
        #broadcast 192.168.4.255
        #hostapd /etc/hostapd/hostapd.conf
" > /etc/network/interfaces
fi
