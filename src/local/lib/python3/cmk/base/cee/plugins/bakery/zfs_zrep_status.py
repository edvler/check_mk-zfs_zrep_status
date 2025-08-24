#!/usr/bin/env python3

#Author: Matthias Maderer
#E-Mail: matthias.maderer@web.de
#URL: https://github.com/edvler/check_mk-zfs_zrep_status
#License: GPLv2

#only CEE!
try:
    from pathlib import Path
    from typing import TypedDict
    from .bakery_api.v1 import Plugin, PluginConfig, register, OS, FileGenerator

    class ZfsZrepStatusBakeryConfig(TypedDict, total=False):
        deployment: bool

    def get_zfs_zrep_status_files(conf: ZfsZrepStatusBakeryConfig) -> FileGenerator:
        deployment = conf["deployment"]

        if deployment == False:
            return

        yield Plugin(
            base_os=OS.LINUX,
            source=Path("zfs_zrep_status")
        )

    register.bakery_plugin(
        name="zfs_zrep_status_bakery",
        files_function=get_zfs_zrep_status_files,
    )
except ModuleNotFoundError:
    pass