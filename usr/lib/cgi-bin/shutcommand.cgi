#!/bin/sh
sudo /sbin/shutdown -h now
cat<<NETSAFELYDOWNTEXT
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">

<html>
<head>
<meta http-equiv="Refresh" content="0;url=/output.html">
</head>
<body bgcolor=black text=orange scroll=no>
</body>
</html>
NETSAFELYDOWNTEXT

