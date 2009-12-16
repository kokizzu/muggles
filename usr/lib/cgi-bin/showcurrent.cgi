#!/bin/bash
#set -x

## initializations start
##

NUMBER_OF_UPLINKS=$(ip link show | sed -e 's/[0-9][0-9]*: eth\([0-9][0-9]*\): <BROADCAST,MULTICAST,UP,LOWER_UP>.*/\1/' -e '$!{h;d;}' -e x)
#NUMBER_OF_UPLINKS=2

number_of_lines_to_display=15
let lines_for_tail=$NUMBER_OF_UPLINKS*$number_of_lines_to_display

secupdatesfile="/var/log/muggles/secupdates"

LANGATEWAYIP=$(ip -4 -o addr show eth0 | sed -n 's/^.*inet \([0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\).*$/\1/p')


## the uplinks:

for ((i=1; i<=$NUMBER_OF_UPLINKS; i++)) ; do UPLINK_NAME[i-1]="isp$i"; done
## if you want, you can overwrite with something like:
## UPLINK_NAME=( 'comcast' 'mtnl' )

UPLINK1_NEAR_IP=192.168.1.254
UPLINK1_FAR_NAME=yahoo.com
## above 2 lines are searched for and automatically changed with changes in pinglogger_config when pinglogger is run
## so for permanent changes, change in pinglogger_config

## UPLINK1ROUTERURL=http://some_useful_url_on_router_eg_diagnostics_or_status
UPLINK1ROUTERURL="http://192.168.1.254/cgi/b/is/_ethoa_/dt/?be=0&l0=1&l1=1&name=Internet"
## status web page on speedtouch thomson st706 uplink router
## another example on another router I had at one time: UPLINK1ROUTERURL="http://$UPLINK1IP/cgi-bin/..%2Fcgi-bin%2Fwebcm?getpage=..%2Fhtml%2Fdefs%2Fstyle1%2Fmenus%2Fmenu1.html\&amp\;var\:style=style1\&amp\;var\:main=menu1\&amp\;var\:menu=status\&amp\;var\:menutitle=Status\&amp\;var\:pagename=syslog\&amp\;var\:errorpagename=syslog\&amp\;var\:pagetitle=System%20Log"

UPLINK1_MONTH_TOTAL=$(echo -n \<a href=\"$UPLINK1ROUTERURL\" title=\";  vnstat -m -i eth1 | grep $(date +%b) | awk '{print "month "$(NF-10)": " $(NF -8) $(NF-7)" received "$(NF -5)$(NF-4)" sent "$(NF -2)$(NF-1)" total"}' | tr "\n" " "; echo \"\>)
## or you can build your own total text: UPLINK1_MONTH_TOTAL=$(echo -n \<a href=\"$UPLINK1ROUTERURL\" title=\";  vnstat -m -i eth1 | grep $(date +%b) | awk '{ print  $(NF -9)" "$(NF -8)": "$(NF -1)" MB sent and received (free quota: 35GB, beyond quota 0.5 per MB)"}' | tr "\n" " "; echo \"\>)



UPLINK2_NEAR_IP=192.168.1.254
UPLINK2_FAR_NAME=google.com
## above 2 lines are searched for and automatically changed with changes in pinglogger_config when pinglogger is run
## so for permanent changes, change in pinglogger_config
UPLINK2ROUTERURL="http://192.168.1.254/cgi/b/is/_ethoa_/dt/?be=0&l0=1&l1=1&name=Internet"
UPLINK2_MONTH_TOTAL=$(echo -n \<a href=\"$UPLINK2ROUTERURL\" title=\";  vnstat -m -i eth2 | grep $(date +%b) | awk '{print "month "$(NF-10)": " $(NF -8) $(NF-7)" received "$(NF -5)$(NF-4)" sent "$(NF -2)$(NF-1)" total"}' | tr "\n" " "; echo \"\>)

## and so on:


## UPLINK3_NEAR_IP=192.168.1.254
## UPLINK3_FAR_NAME=facebook.com
## ## above 2 lines are searched for and automatically changed with changes in pinglogger_config when pinglogger is run
## ## so for permanent changes, change in pinglogger_config
## UPLINK3ROUTERURL=http://some_useful_url_on_router_eg_diagnostics_or_status
## UPLINK3_MONTH_TOTAL=$(echo -n \<a href=\"$UPLINK3ROUTERURL\" title=\";  vnstat -m -i eth3 | grep $(date +%b) | awk '{print "month "$(NF-10)": " $(NF -8) $(NF-7)" received "$(NF -5)$(NF-4)" sent "$(NF -2)$(NF-1)" total"}' | tr "\n" " "; echo \"\>)



##
## initializations end





if [[ -s "$secupdatesfile" ]] ; then security_updates=$(echo "updated security packages available: "; cat /var/log/muggles/secupdates) ; fi

for ((k=1; k<=$NUMBER_OF_UPLINKS; k++)) ; do

  ##get names for each uplink, eg:
  ##uplink1 machines=$(ip -r rule show | grep uplink1 | cut -f2 -d' ')
  uplinkk_machines=($(ip -r rule show | grep uplink${k} | cut -f2 -d' '))
  uplinkk_total=${#uplinkk_machines[@]}

  ##grayout inactive machines on each uplink with nmap in root mode (pretty fast)

  uplinkk_titled_machines[k-1]=$(
  for ((i=1; i<=$uplinkk_total; i++))
  do   { sudo nmap -sP ${uplinkk_machines[i-1]} 2>&1 | grep -q 'host up' ;} \
    && { echo -n '<a href="http://'$LANGATEWAYIP'" title="'; host -s -t A ${uplinkk_machines[i-1]} $LANGATEWAYIP | tail -1 | cut -d' ' -f4 | tr -d '\n'; echo '">'${uplinkk_machines[i-1]}'</a>' ;} \
    || { echo -n '<a href="http://'$LANGATEWAYIP'" title="'; host -s -t A ${uplinkk_machines[i-1]} $LANGATEWAYIP | tail -1 | cut -d' ' -f4 | tr -d '\n'; echo '" class="grayout">'${uplinkk_machines[i-1]}'</a>' ;} 
  done
  )


  ##list each uplink's parsed logs (far connections) 
  eval $(echo uplink${k}far_connectivity='$(tail --lines=${lines_for_tail} /var/log/muggles/remote_pings.log | grep -a ^UPLINK${k} | sed -e "s/^UPLINK${k}://" | sed -e '"'"'s/$/<br>/'"'"')')

  ##list each uplink's parsed logs (near connections)
  eval $(echo uplink${k}near_connectivity='$(tail --lines=${lines_for_tail} /var/log/muggles/near_pings.log | grep -a ^UPLINK${k} | sed -e "s/^UPLINK${k} bam://" | sed -e '"'"'s/$/<br>/'"'"')')


done



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
<a href="http://$LANGATEWAYIP/ipaudit">ipaudit</a> | <a href="mixed.cgi">shuffle uplinks</a> | <a href="http://$LANGATEWAYIP/shutdown.html">turn off the internet</a>
<!-- see http://www.willmaster.com/possibilities/archives/wmp20031230001.shtml if you want to make this prettier -->
</p>

$security_updates

<table summary="uplinks record">
<tbody>
<tr>
TOPBIT


for ((k=1; k<=$NUMBER_OF_UPLINKS; k++)) ; do
array_index=$(($k-1))
cat<<SHOWCURRENT
<td> 
<b>
Uplink${k}: $(eval echo \$UPLINK${k}_MONTH_TOTAL) ${UPLINK_NAME[${array_index}]}</a>
<br>
pings to:
</b>
<br>
<br>
<table summary="Uplink${k}: ${UPLINK_NAME[${array_index}]}">
<tbody>
<tr>
<td><b>$(eval echo \$UPLINK${k}_FAR_NAME)</b><br><br>$(eval echo \$uplink${k}far_connectivity)</td>
<td><b>$(eval echo \$UPLINK${k}_NEAR_IP)</b><br><br>$(eval echo \$uplink${k}near_connectivity)</td>
</tr>
</tbody>
</table><input type="checkbox" name="uplink${k}_checkbox">${uplinkk_titled_machines[k-1]}
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
