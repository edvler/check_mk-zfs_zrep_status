# Author: Matthias Maderer
# E-Mail: edvler@edvler-blog.de
# URL: https://github.com/edvler/check_mk-zfs_zrep_status
# License: GPLv2

register_check_parameters(
    RulespecGroupCheckParametersApplications,
    "zfs",
    _("ZREP status"),
    Dictionary(
        elements = [
            ("check_backup",
             DropdownChoice(
                 title = _("Enable (default) or disable check of ZREP status"),
                 help=_("If disabled is choosen, the check will always return OK. To enable checks of the backup, select enable. This is usefull if you have ZREP initialized ZFS datasets, for which you dont want them to be checked."),
                 choices = [
                     ("ignore", _("disable")),
                     ("check", _("enable")),
                 ]
             )
            ),
            ('backup_age',
             Tuple(title = "The difference between the last synchronisation and now to warn (default 26h) or error (default 30h).",
                 elements = [
                     Age(title=_("Warning above synchronisation age"),
                         default_value = 93600, 
                         help=_("If the synchronisation is older than the specified time in minutes, the check changes to warning. (24h=1440m; 26h=1560m)")
                     ),
                     Age(title=_("Critical at or above synchronisation age"),
                         default_value = 108000,
                         help=_("If the synchronisation is older than the specified time in minutes, the check changes to critical. (24h=1440m; 26h=1560m)")
                     ),
                 ]
             )
            )
        ]
    ),
    TextAscii(
        title = _("Description"),
        allow_empty = True
    ),
    match_type = "dict",
)
