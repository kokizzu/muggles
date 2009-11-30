#!/bin/bash
#set -x

## initializations start
##

LANGATEWAYIP=`ip -4 -o addr show eth0 | sed -n 's/^.*inet \([0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\).*$/\1/p'`
LANGATEWAYNET=`echo $LANGATEWAYIP | cut -f1-3 -d.`.
#assuming type c subnet, eg 192.168.10.1, means gatewaynet would be 192.168.10.   (end "." needed)

UPLINK1=isp1

UPLINK1_NEAR_IP=192.168.1.254
UPLINK1_FAR_NAME=yahoo.com
## above 2 lines are automatically changed with changes in loggerconfig when pinglogger is run

UPLINK1ROUTERURL="http://192.168.1.254/cgi/b/is/_ethoa_/dt/?be=0&l0=1&l1=1&name=Internet"
#handy for looking at a status web page on speedtouch thomson st706 uplink router - put in your own or leave blank
UPLINK1_MONTH_TOTAL=`echo -n \<a href=\"$UPLINK1ROUTERURL\" title=\";  vnstat -m -i eth1 | grep \`date +%b\` | awk '{ print  $(NF -9)" "$(NF -8)": "$(NF -1)" MB sent and received (free quota: 5GB, beyond quota: 1.5 per MB)"}' | tr "\n" " "; echo \"\>`

UPLINK2=isp2

UPLINK2_NEAR_IP=192.168.1.254
UPLINK2_FAR_NAME=google.com
## above 2 lines are automatically changed with changes in loggerconfig when pinglogger is run
##some router had this##UPLINK2ROUTERURL="http://$UPLINK2IP/cgi-bin/..%2Fcgi-bin%2Fwebcm?getpage=..%2Fhtml%2Fdefs%2Fstyle1%2Fmenus%2Fmenu1.html\&amp\;var\:style=style1\&amp\;var\:main=menu1\&amp\;var\:menu=status\&amp\;var\:menutitle=Status\&amp\;var\:pagename=syslog\&amp\;var\:errorpagename=syslog\&amp\;var\:pagetitle=System%20Log"
UPLINK2ROUTERURL="http://192.168.1.254/cgi/b/is/_ethoa_/dt/?be=0&l0=1&l1=1&name=Internet"
UPLINK2_MONTH_TOTAL=`echo -n \<a href=\"$UPLINK2ROUTERURL\" title=\"; vnstat -m -i eth2 | grep \`date +%b\` | cut -f1 -d'|' | tr '\n' ' '; echo received only \(free quota: 12GB, beyond quota: 1.25 per MB\). Sending is free as in beer!\"\>`

UPLINK3=RELIANCE
UPLINK3IP=124.125.174.13
UPLINK3_NEAR_IP=`ip route show | grep eth3 | grep via | cut -f3 -d" " | uniq`
#UPLINK3PINGTARGET=220.224.140.29
UPLINK3PINGTARGET=208.113.173.54
#UPLINK3PINGTARGETNAME=220.224.140.29
UPLINK3PINGTARGETNAME=srijanmedia
UPLINK3ROUTERURL="http://$UPLINK3IP"
UPLINK3_MONTH_TOTAL=`echo -n \<a href=\"$UPLINK3ROUTERURL\" title=\";  vnstat -m -i eth3 | grep \`date +%b\` | awk '{ print  $(NF -9)" "$(NF -8)": "$(NF -1)" MB sent and received (free quota: 35GB, beyond quota 0.5 per MB)"}' | tr "\n" " "; echo \"\>`
###http://192.168.3.1/diagpppoe.html may be prefered

## Near IP is say, one to three hops up, far IP is many hops away.

number_of_lines_to_display=15
NUMBER_OF_UPLINKS=`ip link show | sed -e 's/[0-9][0-9]*: eth\([0-9][0-9]*\): <BROADCAST,MULTICAST,UP,LOWER_UP>.*/\1/' -e '$!{h;d;}' -e x`
#number_of_uplinks=2
let lines_for_tail=$NUMBER_OF_UPLINKS*$number_of_lines_to_display

secupdatesfile="/var/log/muggles/secupdates"

##
## initializations end




if [[ -s "$secupdatesfile" ]] ; then security_updates=`echo "updated security packages available: "; cat /var/log/muggles/secupdates` ; fi


for k in `seq $NUMBER_OF_UPLINKS` ; do

  ##get names for each uplink, eg:
  ##uplink1users=`ip -r rule show | grep uplink1 | cut -f2 -d' '`
  eval `echo -n uplink${k}users; names=\`ip -r rule show | grep uplink${k} | cut -f2 -d' '\` ; echo ='"'$names'"'`

  ##grayout inactive machines on each uplink with an fping eg:
##  titleduplink1users=`for i in \`eval echo '$'uplink${k}users\` ; do ( ( fping -r1 -B1.0 $i 2>&1 | grep -v ^ICMP ) | grep alive > /dev/null  ) && ( echo -n '<a href="http://192.168.10.1" title="'; grep ^192\.168\.10\. /etc/hosts | grep $i | cut -f1 | sed -e "s/$/\">$i<\/a>/" ) || ( echo -n '<a href="http://192.168.10.1" title="'; grep ^192\.168\.10\. /etc/hosts | grep $i | cut -f1 | sed -e "s/$/\" class="grayout">$i<\/a>/" ) ; done`



#below is a pain in the ass to maintain. fix
#  eval `echo -n titleduplink${k}users='\`for i in \\\`eval echo '"'"'$'"'"'uplink${k}users\\\` ; do ( ( fping -r1 -B1.0 $i 2>&1 | grep -v ^ICMP ) | grep alive > /dev/null  ) && ( echo -n '"'"'<a href="http://'"${LANGATEWAYIP}\""' title="'"'"'; host $i localhost | cut -d '"' '"' -f4 | sed '"'/^$/d'"' | sed -e "s/$/\">$i<\/a>/" ) || ( echo -n '"'"'<a href="http://'"$LANGATEWAYIP\""' title="'"'"'; host $i localhost | cut -d'"' '"' -f4  | sed '"'/^$/d'"' | sed -e "s/$/\" class="grayout">$i<\/a>/" ) ; done\`'`

  eval `echo -n titleduplink${k}users='\`for i in \\\`eval echo '"'"'$'"'"'uplink${k}users\\\` ; do (  [[ \\\`sudo nmap -sP $i | grep '"'host up'"' | wc -l\\\` == 1 ]] )  && ( echo -n '"'"'<a href="http://'"${LANGATEWAYIP}\""' title="'"'"'; host $i $LANGATEWAYIP | cut -d '"' '"' -f4 | sed '"'/^$/d'"' | sed "s/$/\">$i<\/a>/" ) || ( echo -n '"'"'<a href="http://'"$LANGATEWAYIP\""' title="'"'"'; host $i $LANGATEWAYIP | cut -d'"' '"' -f4  | sed '"'/^$/d'"' | sed "s/$/\" class="grayout">$i<\/a>/" ) ; done\`'`
#nmap in root mode is pretty fast


  ##list each uplink's parsed logs (far connections) 
  eval `echo uplink${k}far_connectivity='\`tail --lines=${lines_for_tail} /var/log/muggles/remote_pings.log | grep -a ^UPLINK${k} | sed -e "s/^UPLINK${k}://" | sed -e '"'"'s/$/<br>/'"'"'\`'`

  ##list each uplink's parsed logs (near connections)
  eval `echo uplink${k}near_connectivity='\`tail --lines=${lines_for_tail} /var/log/muggles/near_pings.log| grep -a ^UPLINK${k} | sed -e "s/^UPLINK${k} bam://" | sed -e '"'"'s/$/<br>/'"'"'\`'`

  ##define modem lock locations
  eval `echo -n uplink${k}_modem_lock="/var/lock/uplink${k}_modem.lock"`



#if rebooting modem, set flag and skip this?
#if ( set -o noclobber; echo "$$" > "$uplink1_modem_lock") 2> /dev/null;
if ( set -o noclobber; echo "$$" > `eval echo '$'uplink${k}_modem_lock`) 2> /dev/null;
then
   ##trap "rm -f $uplink1_modem_lock; exit $?" INT TERM EXIT
   trap "rm -f `eval echo '$'uplink${k}_modem_lock`; exit $?" INT TERM EXIT
   ## if we are here, then modem was not locked, and is locked now.

   ##uplink1status=`/root/things_to_run/adslpppstatuschecks/uplink1modem.sh`
   eval uplink${k}status=\"`/root/things_to_run/adslpppstatuschecks/uplink${k}modem.sh`\"
   ##detect if modem responding - get modem up or modem down as response

   #if [ "$uplink1status" = "modem up" ]
   if [ "`eval echo '$'uplink${k}status`" = "modem up" ]
   then
      ##uplink1status=`/root/things_to_run/adslpppstatuschecks/uplink1ppp.sh`
      eval uplink${k}status=\"`/root/things_to_run/adslpppstatuschecks/uplink${k}ppp.sh`\"
   ## check ppp status - get PPP Up or PPP Down as response
   fi

   #statusuplink1_timestamped=`(echo $uplink1status at ; date +%H:%M:%S ) | tr "\n" " "`
   eval statusuplink${k}_timestamped=\"`(echo \\$uplink${k}status at ; date +%H:%M:%S ) | tr "\n" " "`\"
   ##statusuplink1_timestamped is : modem down|PPP Up|PPP Down
   #rm -f $uplink1_modem_lock
   rm -f `eval echo \\$uplink${k}_modem_lock` 
   trap - INT TERM EXIT
else
   #statusuplink1_timestamped="Modem busy. $HOSTNAME:PID $(cat $uplink1_modem_lock) holds $uplink1_modem_lock"
   eval `echo "statusuplink${k}_timestamped=\"Modem busy. $HOSTNAME:PID" \`cat \\\`eval echo '$'"uplink${k}_modem_lock"\\\`\` "holds \\$uplink${k}_modem_lock\""`
fi

done
##sorry for the line noise



cat<<TOPBIT
Content-Type: text/html; charset=utf-8


<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
<title>muggles connections</title>
<meta http-equiv="Content-Type" content="text/html;charset=utf-8" >
<meta http-equiv="refresh" content="50" >
<base href="http://$LANGATEWAYIP/cgi-bin/">
<style type="text/css">
a {
  	color: lime
}

a:link {
	text-decoration: none;
}

a:visited {
	text-decoration: none;
}

a:hover {
	color: white;
}

body {
    background-color: black;
    color: lime;
    text-align: center
}

table {
    width: 100%;
    border-width: thin;
    border-style: solid; 
    vertical-align: top
}

td {
    text-align: left;
    width: 25%;
    border-width: thin;
    border-style: ridge;
    padding: 2px;
    vertical-align: top
}

.grayout {color: gray }

form {
    font-size: 100%
     }


</style>
</head>

<body>
<form name="uplinkstouse" action="switchisps.cgi">
<p>
<a href="mixed.cgi">Not sure what to do</a> | <a href="http://$LANGATEWAYIP/shutdown.html">Shut down the internet</a>
<!-- see http://www.willmaster.com/possibilities/archives/wmp20031230001.shtml if you want to make this prettier -->
</p>

$security_updates

<table summary="uplinks record">
<tbody>
<tr>
TOPBIT


for k in `seq $NUMBER_OF_UPLINKS` ; do
cat<<SHOWCURRENT
<td> 
<b>
Uplink${k}: $(eval echo \$UPLINK${k}_MONTH_TOTAL) $(eval echo \$UPLINK${k})</a>
<br>
$(eval echo \$statusuplink${k}_timestamped)
<br>
pings to:
</b>
<br>
<br>
<table summary="Uplink${k}: $(eval echo \$UPLINK${k})">
<tbody>
<tr>
<td><b>$(eval echo \$UPLINK${k}_FAR_NAME)</b><br><br>$(eval echo \$uplink${k}far_connectivity)</td>
<td><b>$(eval echo \$UPLINK${k}_NEAR_IP)</b><br><br>$(eval echo \$uplink${k}near_connectivity)</td>
</tr>
</tbody>
</table><input type="checkbox" name="uplink${k}_checkbox">$(eval echo \$titleduplink${k}users)
</td>
SHOWCURRENT
done


cat<<BOTTOMBIT
</tr>
</tbody>
</table>
<p><input type="submit" value="move ticked users list to other uplinks"></p>
</form>
</body>
</html>
BOTTOMBIT
