

## Description ##
Muggles is an acronym for **m**`ultiple `**u**`plink `**g**`ateway for `**G**`NU/`**L**`inux `**E**`nterprise `**S**`ystems`. It is a debian-based multiple gateway WAN router. You typically use it to connect a LAN up to the internet via multiple not-100%-reliable dsl uplinks, thereby achieving practically 100% connectivity for an office. The connectivity is logged; machines on the lan can be moved between uplinks; and services like dnsmasq, ntpd and squid on the router improve aspects of networking for the end users. The system adheres to The Debian Way, so you can rely on adding more debian packages as needed without breaking things. It currently (26th Feb 2010) runs with lenny (stable) and squeeze (testing) and is intended to always track debian stable - ie it is meant for production use.

A 2-and-a-half minute movie showing the web GUI is at http://groups.google.com/group/mugglesbox/web/mugglesintro.avi.gz.

Muggles works really well for smaller enterprises as a cheap, lightweight and pragmatic simplification of the Cisco 3-layer access/distribution/core model, where bringing in a Cisco architecture would be expensive overkill. You can always stack muggles gateways for scalability as you need to grow, or you can move on to the more complicated heavyweight solutions - the important thing is you don't get locked in to a solution that requires special expertise. Muggles is simple; easily overseen; robust; well-documented; easy to set up; free as in freedom; accessibly powerful; and enormously extensible and flexible. Bolting on new debian toys into the muggles system is fun!

Muggles itself is mainly glue code, done in bash and integrating the underlying debian packages, with a simplifying web GUI layer on top.


## Who should use it? ##

Typically: an office on a lan that needs connectivity at all times, and uses multiple unreliable ISP uplinks for this. The default code can handle up to 25 uplinks, which is unfathomably far more than is sensible. The admin can keep an eye on the ISP connections/users/bandwidth in a simple way. It is intended to run in a lightweight manner on a low-end PC, and let the sysadmin add standard debian software to taste, so that he can sit back and be lazy.

## Keeping it RAIL ##

Muggles framework uses the concept of RAIL - a Redundant Array of Independent Links. The well-known [RAID](http://en.wikipedia.org/wiki/RAID) is a similar idea.

The muggles core is designed for LANs that need to be connected to the internet using multiple normal uplinks.

Normal uplinks are much cheaper than specially serviced "business" or "leased" uplinks with expensive service level agreements. Taking several independent normal uplinks and being able to move off one link when it fails (somewhat like RAID lets you move off one drive when it fails) saves costs **and** means you can just keep working

## Features and Options ##

  * dns caching (dnsmasq). Speeds up dns lookups for users.
  * dhcp serving (dnsmasq). Dynamic ips assigned based on registered macs.
  * time serving (dnsmasq and ntp). The gateway box time syncs with timeservers on the net. Machines on the lan automatically time sync with the gateway box.
  * masquerading (netfilter). One public ip for the whole LAN.
  * basic uplink usage logging (vnstat). Track how much each uplink is used over the month.
  * extended network usage per machine logging (ipaudit). Track which users are youtubing too much.
  * firewalling (netfilter). Block connections to LAN machines, add iptable rules to taste.
  * web caching (transparent squid). Speed up web browsing. Webdevelopers may want to bypass it, which is easily done.
  * qos (tc). Decide priorities for types of traffic. (to be done)
  * a web gui admin (web scripts) Keep an eye on connectivity; live machines; be able to shift machines from uplinks; switch off transparent proxying; watch uplink usage; access ipaudit logs; bypass squid
  * link failover automation (custom monitoring) (to be done)
  * a test environment (virtualbox based). Test out code ideas before infliciting it on users.
  * and all the other goodies that debian GNU/Linux has are relatively easy to bolt on.



## Synopsis ##

There are no real command line options - you configure it and leave it running. The core system provides dns and web caching; timeserving; dhcp; firewalling, masquerading, simple connecitivity logging, uplink total usage monitoring, and moving users from one uplink to another using configuration files.

If you install the web gui (recommended), then with it you can move users away from one or more uplinks; shut down the machine; see which machines are up and running along with their ip addresses; watch bandwidth usage; switch off transparent proxying per user; and more.

Other modules let you do more stuff - detailed network usage logging of users; QOS and a virtualbox test environment.


## How hard is it to maintain? ##

Really easy.

It is installable by beginners who have a vague idea of networking but just need a bit of a guide as to what is going on when applying stuff.

However, it is actually aimed at junior and medium-level sysadmins who want to customize and extend the system to their tastes, so it can get pretty complicated if you like.

(Junior/Medium/Senior levels correspond roughly to LPI 1, 2, 3 certification respectively).

Documentation is didactic for when you want to dig into the internals. The internals themselves run via bash scripts (even the web cgi is made up of bash scripts, just for fun) so command line sysadmins should find it quite pleasant, and everyone should find it approachable.

The **prototypes** of muggles were different and messier than the current version, but have been in production use for a few years. The code, documentation and design was comprehensible enough to be tweaked, crafted and crufted by junior-level sysadmins for a very long time after I built the systems and handed them over - not that I recommend that kind of maintenance model, but hey, that's what happened.

The current version of muggles aims to improve the maintainability so that the upgrade path when tracking debian stable can be carried out almost trivially.

## Documentation ##
There is a 2-and-a-half minute introductory movie about it at http://groups.google.com/group/mugglesbox/web/mugglesintro.avi.gz which will let you know what muggles is about at a glance.

Thorough canonical documentation is kept at: http://code.google.com/p/muggles/wiki/PageName.

## Discussion Forum ##

At http://groups.google.com/group/mugglesbox


## Design philosophy ##
The design is intended to be elegant, adhering to The Debian Way and the Unix philosophy.

The core part aims for a simple design running on top of a minimal install.

A web gui is recommended for normal operation.

Optional features and modules can be bolted on top of the core.

## Bugs, feature requests? ##
Found a bug (or have a feature request)? [Discuss it at the discussion forum](http://groups.google.com/group/mugglesbox).

## Test environment ##
Networking is immensely fun but unless you can test your ideas out first, the users will hate you for applying and breaking things on the production system.

So there is a virtual test environment option based on virtualbox ose. Give your modifications a shakedown and abuse the virtual machines to your heart's content before deployment on the production system.

## Alternatives ##

These are "free as in freedom" alternatives with their own niches:

ebox (ubuntu 8.04, 9.04) You want this if you want something that is more heavyweight than muggles. http://ebox-platform.com

tomato (for routers) http://fixppp.org/

zeroshell (runs off livecd, based on source code rather than a distro) http://www.zeroshell.net

pfsense (freebsd based)

haproxy (designed as reverse proxy) http://haproxy.1wt.eu

shorewall (latest versions can handle multipath uplinks) http://www.shorewall.net/

openwrt (firmware framework) http://openwrt.org/

vyatta (true enterprise grade. Has a community edition)
Quite capable of handling the kind of loads that low and mid-level cisco routers deal with. http://www.vyatta.com
