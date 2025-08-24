#!/usr/bin/env python3
# Author: Matthias Maderer
# E-Mail: matthias.maderer@web.de
# URL: https://github.com/edvler/check_mk-zfs_zrep_status
# License: GPLv2

#example: \lib\python3\cmk\gui\plugins\wato\check_parameters\memory.py


from cmk.rulesets.v1 import Title, Help
from cmk.rulesets.v1.form_specs import (
    DefaultValue,
    DictElement,
    Dictionary,
    BooleanChoice
)

from cmk.rulesets.v1.rule_specs import AgentConfig, Topic


def _valuespec_agent_config_zfs_zrep_status_bakery():
    return Dictionary(
        title=Title("Agent Plugin Parameters"),
        elements={
            'deployment': DictElement(
                required=True,
                parameter_form=BooleanChoice(    
                    title=Title('Deploy ZFS ZREP Status plugin'),                
                    prefill=DefaultValue(True),
                )
            ),
        },
    )


rule_spec_agent_config_zfs_zrep_status_bakery = AgentConfig(
    title=Title("ZFS ZREP Status"),
    topic=Topic.OPERATING_SYSTEM,
    name="zfs_zrep_status_bakery",
    parameter_form=_valuespec_agent_config_zfs_zrep_status_bakery,
)
