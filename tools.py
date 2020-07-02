from json import dumps

x = {
    "trunk": {
        "wuyi": {
            "name": "wuyi",
            "profile": "catv_wuyi_nocolor_sfu_xpon_nowifi_cable_novoice_nousb"
        },
        "fujian": {
            "name": "fujian",
            "profile": "catv_fujian_nocolor_hgu_xpon_wifi_cable_voice_usb"
        },
        "wisecable": {
            "name": "wisecable",
            "profile": "catv_wisecable_nocolor_hgu_xpon_wifi_nocable_novoice_nousb"
        },
        "hgustandard": {
            "name": "hgustandard",
            "profile": "catv_standard_nocolor_hgu_xpon_wifi_nocable_novoice_nousb"
        },
        "sfustandard": {
            "name": "sfustandard",
            "profile": "catv_standard_nocolor_sfu_xpon_nowifi_nocable_novoice_nousb"
        },
        "yueqing": {
            "name": "yueqing",
            "profile": "catv_yueqing_nocolor_hgu_xpon_wifi_nocable_novoice_nousb"
        },
        "jingning977": {
            "name": "jingning977",
            "profile": "catv_jingning_white_sfu_epon_nowifi_cable_novoice_nousb",
            "svn_update": False
        },
        "jingning": {
            "name": "jingning",
            "profile": "catv_jingning_white_sfu_epon_nowifi_cable_novoice_nousb"
        },
        "huashusfu": {
            "name": "huashusfu",
            "profile": "catv_huashu_nocolor_sfu_xpon_nowifi_cable_novoice_nousb"
        },
        "shaoxing": {
            "name": "shaoxing",
            "profile": "catv_shaoxing_nocolor_sfu_xpon_nowifi_cable_novoice_nousb"
        },
        "hunan": {
            "name": "hunan",
            "profile": "catv_hunan_nocolor_hgu_xpon_wifi_cable_voice_nousb"
        }
    },
    "tags": {
        "armenia": {
            "name": "armenia-1.0",
            "profile": "catv_armenia_nocolor_hgu_xpon_wifi_nocable_novoice_nousb"
        },
        "guangxi": {
            "name": "guangxi-1.0",
            "profile": "catv_guangxi_nocolor_hgu_xpon_wifi_cable_voice_usb"
        },
        "hunan3.0": {
            "name": "hunan-3.0",
            "profile": "catv_hunan_nocolor_hgu_xpon_wifi_cable_voice_nousb"
        }
    },
    "7528": {
        "7528-sfu": {
            "name": "catv_general_black_sfu_gpon_nowifi_cable_novoice_nousb",
            "profile": "catv_general_black_sfu_gpon_nowifi_cable_novoice_nousb",
            "sources": "MTK-7528-SFU"
        }
    },
    "7580": {
        "7580": {
            "name": "MTK-7580",
            "profile": "CUC_en7580_7592_7615_OSGI_demo",
            "sources": "."
        }
    },
    "wifi6": {
        "wifi6": {
            "name": ".",
            "profile": "CT_EN7561D_LE_7915D_AP_demo",
            "cleanup": True,
            "cleanupPath": "../"
        }
    }
}

with open("build_list.json", 'w') as file:
    data = dumps(x, indent=4, sort_keys=True)
    file.write(data)
    file.close()
