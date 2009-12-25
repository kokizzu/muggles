#!/bin/bash
#set -x

source /etc/muggles/showcurrent.conf


for ((k=1; k<=$NUMBER_OF_UPLINKS; k++)) ; do

  ##get names for each uplink, eg:
  ##uplink1 machines=$(ip -r rule show | grep uplink1 | cut -f2 -d' ')
  uplinkk_machines=($(ip -r rule show | grep uplink${k} | cut -f2 -d' '))
  uplinkk_total=${#uplinkk_machines[@]}

  ##grayout inactive machines on each uplink with nmap in root mode (pretty fast)

  uplinkk_titled_machines[k-1]=$(
  for ((i=1; i<=$uplinkk_total; i++)) ; do
    machine_name=${uplinkk_machines[i-1]}
    { sudo nmap -sP $machine_name 2>&1 | grep -q 'host up' && machine_ip=$(host -s -t A $machine_name $LANGATEWAYIP | tail -1 | cut -d' ' -f4 | tr -d '\n') ;} \
    && { echo -n '<a href="http://'$LANGATEWAYIP'" title="'$machine_ip; echo '">'$machine_name'</a>' ;} \
    || { echo -n '<a href="http://'$LANGATEWAYIP'" title="'$machine_ip; echo '" class="grayout">'$machine_name'</a>' ;} 
  done
  )


  ##list each uplink's parsed logs (far connections) 
  uplinkk_far_connectivity[k-1]=$(tail --lines=${lines_for_tail} $remote_pings_log | grep -a ^UPLINK${k} | sed "s/^UPLINK${k}://" | sed 's/$/<br>/')

  ##list each uplink's parsed logs (near connections)
  uplinkk_near_connectivity[k-1]=$(tail --lines=${lines_for_tail} $near_pings_log | grep -a ^UPLINK${k} | sed "s/^UPLINK${k} bam://" | sed 's/$/<br>/')


done



cat<<TOPBIT
Content-Type: text/html; charset=utf-8


<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
<title>$page_title</title>
<meta http-equiv="Content-Type" content="text/html;charset=utf-8" >
<meta http-equiv="refresh" content="$page_refresh_time" >
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
<td><b>$(eval echo \$UPLINK${k}_FAR_NAME)</b><br><br>${uplinkk_far_connectivity[k-1]}</td>
<td><b>$(eval echo \$UPLINK${k}_NEAR_IP)</b><br><br>${uplinkk_near_connectivity[k-1]}</td>
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
