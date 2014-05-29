#!/bin/sh
a=$(echo $2 | grep -E '[^0-9]' >/dev/null && echo "BAD" || echo "OK")
b=$(echo $4 | grep -E '[^0-9]' >/dev/null && echo "BAD" || echo "OK")
c=$(echo $6 | grep -E '[^0-9]' >/dev/null && echo "BAD" || echo "OK")
stat=$(netstat -ant | grep -w "$2" | grep -v LISTEN | wc -l)
if [[ $1 == -h || $1 == "" ]]
    then
        echo "example: command -p 80 -w 300 -c 400"
else [[ $1 == -p && $a == OK && $3 == -w && $b == OK && $5 == -c && $c == OK ]]
    stat=$(netstat -ant | grep -w "$2" | grep -v LISTEN | wc -l)
#    echo $stat
#    echo "OK - port $2 HTTPRequest is $stat | request=$stat;$4;$6;0"
	if (( $stat >= $4 ))
	    then
		    echo "Warning , prot $2 request is $stat nearly MaxClient | request=$stat;$4;$6;0"
			exit 1
	elif (( $stat >= $6 ))
	    then
		    echo "Criticl , prot $2 request is $stat more than MaxClient | request=$stat;$4;$6;0"
			exit 2
	else
	    echo "OK - port $2 HTTPRequest is $stat | request=$stat;$4;$6;0"
		exit 0
	fi
fi