# [Check MK](https://mathias-kettner.de/check_mk.html) Plugin to check [ZREP](http://www.bolthole.com/solaris/zrep/) status

# Installation
First install ZREP as described on ZREP-Website: [http://www.bolthole.com/solaris/zrep/](http://www.bolthole.com/solaris/zrep/)

Then intialize your ZFS dataset with
```
export ZREPTAG=ZREP_01 #Set zrep Tag to make multiple zrep destinations on one volume.
zrep init ....
```

## On the Monitoring Server where Check_mk is installed:
For a detailed description how to work with mkp's goto [https://mathias-kettner.de/cms_mkps.html](https://mathias-kettner.de/cms_mkps.html).

### Short tasks
1. copy the zfs_zrep_status*.mkp (see [dist](dist) folder) to your Check_mk server into the /tmp folder.
2. mkp install /tmp/zfs_zrep_status*.mkp
3. Check if installation worked
```
root@monitoring01:/opt/omd# find . -name '*zfs_zrep_status*'
./sites/XXXX/local/share/check_mk/checks/zfs_zrep_status
./sites/XXXX/local/share/check_mk/checkman/zfs_zrep_status
./sites/XXXX/local/share/check_mk/web/plugins/wato/check_parameters_zfs_zrep_status.py
./sites/XXXX/local/share/check_mk/agents/plugins/zfs_zrep_status
```
4. Goto your Check_mk webinterface. Choose WATO -> Host & Service Parameters. Search for *zrep*.

## On the Server which holds the ZREP initialzied ZFS datasets (NOT THE CHECK_MK SERVER!):
1. Copy the plugin script [check_mk/agents/plugins/zfs_zrep_status](check_mk/agents/plugins/zfs_zrep_status) into /usr/lib/check_mk_agent/plugins/
2. chmod 755 /usr/lib/check_mk_agent/plugins/zfs_zrep_status
3. Execute the script: /usr/lib/check_mk_agent/plugins/zfs_zrep_status. If everythings works the output should look like this
```
<<<zfs_zrep_status>>>
backup01/ext1                                  last synced 2018/10/03-17:53:02
backup01/fileserver                            last synced 2018/10/03-17:53:30
backup02/offsite                               last synced 2018/10/03-12:01:29
...
...
...
```

## Functions of the plugin
![](https://github.com/edvler/check_mk-zfs_zrep_status/blob/master/docs/zfs_zrep_status-manpage.png)

## Services screenshot
![](https://github.com/edvler/check_mk-zfs_zrep_status/blob/master/docs/example-services-screenshot.png)


