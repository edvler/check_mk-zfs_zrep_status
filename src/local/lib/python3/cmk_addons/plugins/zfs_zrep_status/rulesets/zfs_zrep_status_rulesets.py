#!/usr/bin/env python3

# Author: Matthias Maderer
# E-Mail: matthias.maderer@web.de
# URL: https://github.com/edvler/check_mk-zfs_zrep_status
# License: GPLv2

from cmk.rulesets.v1 import (
    Title,
)
from cmk.rulesets.v1.form_specs import (
    BooleanChoice,
    DefaultValue,
    DictElement,
    Dictionary,
    InputHint,
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
        #ignored_elements=('check_backup'),
        #migrate=lambda model: { #force defaults for with model.get(...,DEFAULT)
        #    'backup_age': migrate_to_upper_float_levels(model.get('backup_age',('fixed',(1.5 * 86400.0, 2 * 86400.0)))),
        #},
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


# def _parameter_zfs_zrep_status():
#     return Dictionary(
#             elements = [
#                 ("check_backup",
#                 DropdownChoice(
#                     title = _("Enable (default) or disable check of ZREP status"),
#                     help=_("If disabled is choosen, the check will always return OK. To enable checks of the backup, select enable. This is usefull if you have ZREP initialized ZFS datasets, for which you dont want them to be checked."),
#                     choices = [
#                         ("ignore", _("disable")),
#                         ("check", _("enable")),
#                     ]
#                 )
#                 ),
#                 ('backup_age',
#                 Tuple(title = "The difference between the last synchronisation and now to warn (default 26h) or error (default 30h).",
#                     elements = [
#                         Age(title=_("Warning above synchronisation age"),
#                             default_value = 93600, 
#                             help=_("If the synchronisation is older than the specified time in minutes, the check changes to warning. (24h=1440m; 26h=1560m)")
#                         ),
#                         Age(title=_("Critical at or above synchronisation age"),
#                             default_value = 108000,
#                             help=_("If the synchronisation is older than the specified time in minutes, the check changes to critical. (24h=1440m; 26h=1560m)")
#                         ),
#                     ]
#                 )
#                 )
#             ]
#         )

rule_spec_zfs_zrep_status = CheckParameters(
    name="zfs",
    topic=Topic.STORAGE,
    parameter_form=_parameter_zfs_zrep_status,
    title=Title("ZREP Status"),
    condition=HostAndItemCondition(item_title=Title("ZREP Volume")),
)

# rulespec_registry.register(
#     CheckParameterRulespecWithItem(
#         check_group_name="zfs",
#         group=RulespecGroupCheckParametersStorage,
#         item_spec=lambda: TextAscii(title=_('ZREP Volume'), ),
#         match_type='dict',
#         parameter_valuespec=_parameter_zfs_zrep_status,
#         title=lambda: _("ZREP Status"),
#     ))
