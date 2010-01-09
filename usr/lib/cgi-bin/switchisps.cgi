#!/bin/bash

LANGATEWAYIP=`ip -4 -o addr show eth0 | sed -n 's/^.*inet \([0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\).*$/\1/p'`


echo Content-type: text/html
echo ""

/bin/cat << EOM
<HTML>
<HEAD><TITLE>uplink shuffling</TITLE>
<meta http-equiv="Refresh" content="10;url=http://$LANGATEWAYIP/switched.html">
</HEAD>
<BODY bgcolor="#cccccc" text="#000000">
<P>
<SMALL>
<PRE>
EOM

list_of_all_uplinks=`grep uplink[1-9][0-9]*$ /etc/iproute2/rt_tables | cut -f2 | tr '\n' ' '` 
#based on what is in rt_tables - ie manually put in upto 99 uplinks if you have 99 uplinks.
# you must put in only the number of uplinks you have


## /usr/bin/env | grep ^QUERY_STRING= | tee /usr/lib/cgi-bin/linkstouse
## todo: use the stored data later for filling checkbox? or just let the checkboxes be blank

list_of_denied_uplinks=`/usr/bin/env | grep ^QUERY_STRING= | sed -e 's/^QUERY_STRING=//g' | sed -e 's/&/ /'g | sed -e 's/=on//g' | sed -e 's/_checkbox//'g`
#list_of_denied_uplinks=`cat /var/www/cgi-bin/linkstouse | sed -e 's/^QUERY_STRING=//g' | sed -e 's/&/ /'g | sed -e 's/=on//g' | sed -e 's/_checkbox//'g`


list_of_allowed_uplinks=`(for i in \`echo $list_of_all_uplinks $list_of_denied_uplinks\`; do echo $i ; done ) | sort | uniq -u| tr '\n' ' '`
## list_of_allowed_uplinks= total_uplinks + denied uplinks | sort | uniq -u 
number_allowed=`echo $list_of_allowed_uplinks | wc -w` ; echo number_allowed uplinks is $number_allowed

echo "list_of_denied_uplinks=$list_of_denied_uplinks"
echo "list_of_all_uplinks=$list_of_all_uplinks"
echo "list_of_allowed_uplinks=$list_of_allowed_uplinks"

#echo "dry-run mode for now"  ; #to dry run, sudo off below
#sanitize it properly
if [ -n "$list_of_denied_uplinks" ] ;
then echo "list of denied uplinks not null: must eliminate."
  ##now sanitize
  for i in $list_of_denied_uplinks
  do
     if ( [[ $i == uplink[1-9][0-9]* ]] || [[ $i == uplink[1-9] ]] )
     #avoid uplink0
     then echo "matched $i" 
     #above is a restrictive match.
     else echo "Pooey! Insanitary input: $list_of_denied_uplinks. Do nothing." && exit 0
    fi
  done
else echo "list of denied uplinks null: nothing to get rid of. Do nothing." && exit 0
fi
#yuk. But it is clean now.
echo Sanitized input for our protection

echo "Eliminate uplink allocations in denied uplink list:"
echo "Strain to make a list of the denied ips and priorities"
echo "Wipe the list up into allowed uplinks one by one round-robin style" 
## use denied ips into rules to add users to permitted uplinks round-robinly:

for i in $list_of_denied_uplinks

do
     denied_uplink_ip_list=`ip rule show | grep $i | grep -v all | cut -f2 -d" "`
     echo $denied_uplink_ip_list

     denied_uplink_prio_list=`ip rule show | grep $i | grep -v all | cut -f1 -d":"`
     echo $denied_uplink_prio_list
       k=1 ; #roundrobin index
       for j in $denied_uplink_ip_list


         do
           associated_prio=`ip rule show | grep "$j " | grep -v all | cut -f1 -d":" | tr '\n' ' '` 
           echo "ip rule del from $j table $i prio $associated_prio"
           sudo ip rule del from $j table $i prio $associated_prio

           get_rruplink=`echo $list_of_allowed_uplinks | cut -f$k -d" "`
           if ( [[ $k -eq $number_allowed ]] )
             then let k=1
             else let k=$k+1
           fi

           echo "ip rule add from $j table $get_rruplink prio $associated_prio"
           sudo ip rule add from $j table $get_rruplink prio $associated_prio
         done
done


echo "Done dumping? Now flush before leaving"
sudo ip route flush cache

echo "Flushed!"



/bin/cat << EOM
</PRE>
</SMALL>
<P>
</BODY>
</HTML>
EOM

