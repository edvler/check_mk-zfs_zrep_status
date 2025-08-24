#!/usr/bin/env python3

# Author: Matthias Maderer
# E-Mail: matthias.maderer@web.de
# URL: https://github.com/edvler/check_mk-zfs_zrep_status
# License: GPLv2

from cmk.rulesets.v1 import (
    Title,
)
from cmk.rulesets.v1.form_specs import (
    DefaultValue,
    DictElement,
    Dictionary,
    LevelDirection,
    migrate_to_upper_float_levels,
    SimpleLevels,
    TimeMagnitude,
    TimeSpan
    )
from cmk.rulesets.v1.rule_specs import (
    CheckParameters,
    HostAndItemCondition,
    Topic,
)

def _parameter_zfs_zrep_status():
    return Dictionary(
        ignored_elements=('check_backup',),
        elements = {
            'backup_age': DictElement(
                required=True,
                parameter_form=SimpleLevels(
                    title = Title('Age of ZREP run before changing to warn or critical'),
                    migrate = lambda model: migrate_to_upper_float_levels(model),
                    level_direction = LevelDirection.UPPER,
                    form_spec_template = TimeSpan(
                        displayed_magnitudes=[TimeMagnitude.DAY, TimeMagnitude.HOUR],
                    ),
                    prefill_fixed_levels = DefaultValue(
                        value=(1.5 * 86400.0, 2 * 86400.0),
                    )
                )
            ),
        }
    )    

rule_spec_zfs_zrep_status = CheckParameters(
    name="zfs",
    topic=Topic.STORAGE,
    parameter_form=_parameter_zfs_zrep_status,
    title=Title("ZREP Status"),
    condition=HostAndItemCondition(item_title=Title("ZREP Volume")),
)