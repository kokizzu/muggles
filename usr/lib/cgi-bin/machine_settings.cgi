#!/bin/bash
#set -x -v

## parse GET method
DIRTY=`/usr/bin/env | tr "\n" " "`
CLEAN=${DIRTY//[^a-zA-Z_0-9 &=]/}
qs=`echo $CLEAN | sed 's/.* \(QUERY_STRING=.*\)/\1/' | sed 's/ .*//' | sed 's/QUERY_STRING=//'`

#eg: QUERY_STRING=uplinkselection=noforce&squidselection=yes... 

machine=`echo $qs | grep -o "machine_name=.*" | sed "s/&.*$//" | cut -f2 -d=`
squidselection=`echo $qs | grep -o "squidselection=.*" | sed "s/&.*$//" | cut -f2 -d=`
uplinkselection=`echo $qs | grep -o "uplinkselection=.*" | sed "s/&.*$//" | cut -f2 -d=`

forced_uplink_config_file="/etc/muggles/forced_uplink.conf"
NUMBER_OF_UPLINKS=$(ip link show | sed -e 's/[0-9][0-9]*: eth\([0-9][0-9]*\): <BROADCAST,MULTICAST,UP,LOWER_UP>.*/\1/' -e '$!{h;d;}' -e x)

ipused=$(awk "/ $machine /"'{print $3}' /var/lib/misc/dnsmasq.leases)

/bin/cat << EOM
Content-type: text/html

<HTML>
<HEAD><TITLE>$machine status</TITLE>
</HEAD>
<BODY bgcolor=black text=orange scroll=no>
<P>
EOM


#if uplinkselection is noforce and we have an existing forced entry then need to remove forced entry
#if uplinkselection is forced entry and want to move from another forced entry (must check it exists), then need to alter already existing forced entry in config file
#if uplinkselection is forced entry and we have no existing forced entry (=noforce) (ie no entry in forcedconfig file), then need to insert forced entry in configfile


match_forced_uplink ()
{
if [ "$1" != "quiet" ]
then
  grep -x ^"$machine[ \t]*.*$" $forced_uplink_config_file | sed -n "s/^$machine[ \t]*\(.*\)$/\1/p"
  #echoes the uplink matched (1, 2...)
fi

# no useful return value with sed so need to grep
( grep -x -q ^"$machine[ \t]*.*$" $forced_uplink_config_file ) && matched_forced_uplink=0 ||  matched_forced_uplink=1

## returns 0 if true
return $matched_forced_uplink
}


if [ -z "$uplinkselection" ]
then 
  if ( match_forced_uplink quiet )
  then
    uplinkselection=uplink$(match_forced_uplink)
  else
    uplinkselection="noforce"
  fi
fi


if [ "$uplinkselection" = "noforce" ] && ( match_forced_uplink quiet )
then
  sed -i "/^$machine.*$/d" $forced_uplink_config_file
fi


linkused=$(ip rule show | awk "/$(awk "/ $machine /"'{print $3}' /var/lib/misc/dnsmasq.leases)/"'{print $5}')
for ((i=1; i<=$NUMBER_OF_UPLINKS; i++))
do
if [ "$uplinkselection" = "uplink$i" ] 
then
  if ( match_forced_uplink quiet )
  then
    sudo ip rule del from $ipused table $linkused && sudo ip rule add from $ipused table $uplinkselection
    sed -i "s/^\($machine\)\(.*\)$/\1	$i/" $forced_uplink_config_file
  else
    ## no forced uplink at present, need to set it:
    if [ "$uplinkselection" != "$linkused" ] 
    ## ie only do if selection differs from linkused 
    then
      sudo ip rule del from $ipused table $linkused && sudo ip rule add from $ipused table $uplinkselection
    fi
    ## and now set the forced uplink
    echo "$machine	$i" >>  $forced_uplink_config_file
  fi
fi
done
linkused=$(ip rule show | awk "/$(awk "/ $machine /"'{print $3}' /var/lib/misc/dnsmasq.leases)/"'{print $5}')
#should log rulechange... can we use rulerunner function for this?


## uplink status

uplinkradiocheck[0]='checked'

if [ "$uplinkselection" != "noforce" ]
then
  for ((i=1; i<=$NUMBER_OF_UPLINKS; i++))
  do uplinkradiocheck[i]=''
    if [ "$uplinkselection" = "uplink$i" ] ; then uplinkradiocheck[i]="checked" && uplinkradiocheck[0]=''; fi
  done
fi


/bin/cat << EOM
<pre>
<FORM name="$machine" action="./machine_settings.cgi" method="GET">
<input type="hidden" name="machine_name" value="$machine">

<table>
<tr>
<td>
<h2>$machine</h2></td><td><h2>$ipused</h2></td>
</tr>
<tr>
<td>
uplink choice</td>
<td>currently using $linkused</td></tr>
<tr>
<td></td><td><input type="radio" name="uplinkselection" value="noforce" ${uplinkradiocheck[0]}>force nothing (let uplink be round robin or random) </td></tr>
EOM

for ((i=1; i<=$NUMBER_OF_UPLINKS; i++))
do
 echo '<tr><td></td><td><input type="radio" name="uplinkselection" value="uplink'$i'"' ${uplinkradiocheck[i]}'>always force '$machine to uplink$i'</td></tr>'
done




## squid status

squid_redirection ()
{  ( sudo /sbin/iptables -L -v -t nat | grep -q -x "^.*REDIRECT *tcp *\-\- *eth0 *any *anywhere *anywhere *tcp dpt:www redir ports 3128 *$" ) && squid_redir=0 || squid_redir=1
## returns 0 if true
return $squid_redir
}

bypass ()
{
if [ "$1" = "insert" ] ; then sudo /sbin/iptables -t nat -I squid_bypass -i eth0 -s $ipused/32 -j ACCEPT ; fi
if [ "$1" = "delete" ] ; then sudo /sbin/iptables -t nat -D squid_bypass -i eth0 -s $ipused/32 -j ACCEPT ; fi

( sudo /sbin/iptables -v -t nat -S | grep -q -x "^\-A squid_bypass -s $ipused/32 -i eth0 -c .* .* -j ACCEPT *$" ) && bypass=0 ||  bypass=1
## returns 0 if true
return $bypass
}


## only display squid stuff and allow bypass actions if squid redirection is on. (bypass state doesn't matter if squid redirection is off)
## squidselection will not be defined by user when page first loads

if (squid_redirection)
then 
  if [ -z $squidselection ]
  then
    if (bypass)
    then squid_no="checked"
    else squid_yes="checked"
    fi
  else
    if [ "$squidselection" = "yes" ]
    then
      squid_yes="checked"
      if (bypass)
      then (bypass delete)
      fi
    else
      # [ "$squidselection" = "no" ]
      squid_no="checked"
      if (! bypass)
      then (bypass insert)
      fi
    fi
  fi

/bin/cat << EOM
<tr><td>$machine uses squid	</td><td><input type="radio" name="squidselection" value="yes" ${squid_yes}>yes</td></tr>
<tr><td></td><td>                     <input type="radio" name="squidselection" value="no" ${squid_no}>no</td></tr>
</table>

<p><input type="submit" value="set"></p>
EOM
fi



/bin/cat << EOM
</FORM>
</pre>
<P>
</BODY>
</HTML>
EOM

