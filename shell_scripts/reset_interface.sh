
if [ $# = 1 ]
	then 
		if [ $1 == "ap" ] || [ $1 = "client" ]
			then
				~/build_interface.sh $1
				shutdown -r now 
		fi
fi
