# ossim/alienvault sophosutm plugin

Logrotate Config
----------------
/etc/lograte.d/sophosutm
```
/var/log/sophosutm.log
{
    rotate 5
    daily
    missingok
    notifempty
    compress
    delaycompress
    sharedscripts
    postrotate
    invoke-rc.d rsyslog reload > /dev/null
    endscript
}
```


RSyslog Config
----------------
/etc/rsyslog.d/sophosutm.conf
```
if ($fromhost-ip == '<IP-SOPHOS>') then /var/log/sophosutm.log
& ~
```
In case of multiple UTMs:


/etc/rsyslog.d/sophosutm.conf
```
if ($fromhost-ip == '<IP-SOPHOS-1>' or $fromhost-ip == '<IP-SOPHOS-2>' or $fromhost-ip == '<IP-SOPHOS-3>') then /var/log/sophosutm.log
& ~
```

Generate SQL
------------

use convertor (python3!)
```
python3 tools/convertSnortRulesSophosUTM.py astaro.rules > sophosutm.sql
```

copy astaro.rules from your UTM /etc/snort/rules/astaro.rules (i cant publish because of copyrights)

then import sql in mysql database and restart ossim services
```
ossim-db < sophosutm.sql
/etc/init.d/ossim-agent restart
/etc/init.d/ossim-server restart
```
