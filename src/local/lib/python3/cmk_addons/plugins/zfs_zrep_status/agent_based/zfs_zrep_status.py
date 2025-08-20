#!/usr/bin/python

# Author: Matthias Maderer
# E-Mail: matthias.maderer@web.de
# URL: https://github.com/edvler/check_mk-zfs_zrep_status
# License: GPLv2

#Example output of agent with zrep version < 1.8.0
#
#root@pve01:/usr/lib/check_mk_agent/plugins# ./zfs_zrep_status
#<<<zfs_zrep_status>>>
#b01/offs                                       last synced 2019/12/25-19:32:03 zrep-c01


#Example output of agent with zrep version >= 1.8.0
#
#root@pve01:/usr/lib/check_mk_agent/plugins# ./zfs_zrep_status
#<<<zfs_zrep_status>>>
#backup02/offsite                                     last: 2019/12/24-14:54:54 zrep-b02-ext01


from cmk.agent_based.v2 import (
    AgentSection,
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    Result,
    Service,
    State,
    Metric,
    render,
    check_levels,
)
import time



def params_parser(params):
    params_new = {}

    for p in params:
        if params[p] is not None and isinstance(params[p], tuple):
            if params[p][0] in ("fixed", "no_levels", "predictive"): #e.g ('fixed', (1, 1)) - New Check_MK 2.4 format
                params_new[p] = params[p]            
            elif isinstance(params[p][0], (int, float)) and isinstance(params[p][1], (int, float)):
                params_new[p] = ('fixed', (params[p][0], params[p][1]))
            else:
                params_new[p] = params[p]
        else: 
            params_new[p] = params[p]

    
    return params_new


def inventory_zfs_zrep_status(section):
    for line in section:
        if line[2] == 'synced':
            yield Service(item=line[0] + ' Tag: ' + line[4])
        else:
            yield Service(item=line[0] + ' Tag: ' + line[3])



def check_zfs_zrep_status(item, params, section):
    params_cmk_24 = params_parser(params)

    for line in section:
        tag = ""
        if line[2] == 'synced':
            tag = line[4]
        else:
            tag = line[3]

        if line[0] + ' Tag: ' + tag == item:
            synctime = ""
            if line[2] == 'synced':
                synctime = time.strptime(line[3],"%Y/%m/%d-%H:%M:%S")
            else:
                synctime = time.strptime(line[2],"%Y/%m/%d-%H:%M:%S")

            old = time.time() - time.mktime(synctime)

            #infotext = 'last synchronized: ' + time.strftime("%Y-%m-%d %H:%M", synctime) + ' (' + render.timespan(old) + ' ago)'

            yield from check_levels(
                old,
                levels_upper=params_cmk_24['backup_age'],
                metric_name="backup_age",
                label="Time since last ZREP run",
                render_func=lambda x: render.timespan(x),
                boundaries=(0,None)
            )

            #if 'backup_age' not in params_cmk_24:
            #    yield (Result(state=State.UNKNOWN, summary="No backup_age defined, but - Use levels defined in this check - are choosen in rules!"))
            #    return

            #warn, crit = params_cmk_24['backup_age'][1]
            #yield Metric("backup_age", old, levels = (warn, crit))
#
#            if old < warn:
#                yield Result(state=State.OK, summary=infotext)
#            elif old < crit:
#                yield Result(state=State.WARN, summary=infotext)
#            else:
#                yield Result(state=State.CRIT, summary=infotext)




check_plugin_zfs_zrep_status = CheckPlugin(
    name = "zfs_zrep_status",
    service_name = "ZREP status %s",
    discovery_function = inventory_zfs_zrep_status,
    check_function = check_zfs_zrep_status,
    check_default_parameters = {
                                'backup_age': (1.5 * 86400.0, 2 * 86400.0),
                                },
    check_ruleset_name = "zfs"
)