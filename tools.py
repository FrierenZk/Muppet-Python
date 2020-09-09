from json import dumps

x = {
    "trunk": {
        "fujian": {
            "projectName": "fujian",
            "profile": "catv_fujian_nocolor_hgu_xpon_wifi_cable_voice_usb"
        },
        "wisecable": {
            "projectName": "wisecable",
            "profile": "catv_wisecable_nocolor_hgu_xpon_wifi_nocable_novoice_nousb"
        },
        "hgustandard": {
            "projectName": "hgustandard",
            "profile": "catv_standard_nocolor_hgu_xpon_wifi_nocable_novoice_nousb"
        },
        "sfustandard": {
            "projectName": "sfustandard",
            "profile": "catv_standard_nocolor_sfu_xpon_nowifi_nocable_novoice_nousb"
        },
        "yueqing": {
            "projectName": "yueqing",
            "profile": "catv_yueqing_nocolor_hgu_xpon_wifi_nocable_novoice_nousb"
        },
        "jingning977": {
            "projectName": "jingning977",
            "profile": "catv_jingning_white_sfu_epon_nowifi_cable_novoice_nousb",
            "svnUpdate": False
        },
        "jingning": {
            "projectName": "jingning",
            "profile": "catv_jingning_white_sfu_epon_nowifi_cable_novoice_nousb"
        },
        "huashusfu": {
            "projectName": "huashusfu",
            "profile": "catv_huashu_nocolor_sfu_xpon_nowifi_cable_novoice_nousb"
        },
        "huashu": {
            "projectName": "huashu",
            "profile": "catv_huashu_nocolor_hgu_xpon_wifi_nocable_novoice_nousb"
        },
        "shaoxing": {
            "projectName": "shaoxing",
            "profile": "catv_shaoxing_nocolor_sfu_xpon_nowifi_cable_novoice_nousb"
        },
        "hunan": {
            "projectName": "hunan",
            "profile": "catv_hunan_nocolor_hgu_xpon_wifi_cable_voice_nousb"
        },
        "guangxi-trunk": {
            "projectName": "guangxi",
            "profile": "catv_guangxi_nocolor_sfu_xpon_nowifi_nocable_novoice_nousb"
        }
    },
    "tags": {
        "armenia": {
            "projectName": "armenia-1.0",
            "profile": "catv_armenia_nocolor_hgu_xpon_wifi_nocable_novoice_nousb"
        },
        "guangxi": {
            "projectName": "guangxi-1.0",
            "profile": "catv_guangxi_nocolor_hgu_xpon_wifi_cable_voice_usb"
        },
        "hunan3.0": {
            "projectName": "hunan-3.0",
            "profile": "catv_hunan_nocolor_hgu_xpon_wifi_cable_voice_nousb"
        },
        "mexico1.0": {
            "projectName": "mexico-1.0",
            "profile": "catv_mexicanos_nocolor_hgu_xpon_wifi_nocable_novoice_nousb"
        },
        "mexico2.0": {
            "projectName": "mexico-2.0",
            "profile": "catv_mexicanos_nocolor_hgu_xpon_wifi_nocable_novoice_nousb"
        },
        "shandong": {
            "projectName": "hunan-2.0",
            "profile": "catv_shandong16_nocolor_sfu_xpon_nowifi_cable_novoice_nousb"
        }
    },
    "7528": {
        "7528-sfu": {
            "projectName": "catv_general_black_sfu_gpon_nowifi_cable_novoice_nousb",
            "profile": "catv_general_black_sfu_gpon_nowifi_cable_novoice_nousb",
            "sourcesPath": "MTK-7528-SFU"
        },
        "7528-guangxi": {
            "projectName": "guangxi",
            "profile": "catv_guangxi_black_sfu_xpon_nowifi_cable_novoice_nousb",
            "sourcesPath": "MTK-7528-SFU"
        },
        "7528-wifi": {
            "projectName": "catv_general_black_hgu_gpon_wifi_cable_voice_usb",
            "profile": "catv_general_black_hgu_gpon_wifi_cable_voice_usb",
            "sourcesPath": "MTK-7528"
        },
        "7528-wifi2": {
            "projectName": "catv_general_black_hgu_gpon_wifi2_cable_voice_usb",
            "profile": "catv_general_black_hgu_gpon_wifi2_cable_voice_usb",
            "sourcesPath": "MTK-7528"
        },
        "7528-fujian": {
            "projectName": "fujian",
            "profile": "catv_fujian_black_hgu_gpon_wifi2_cable_voice_usb",
            "sourcesPath": "MTK-7528"
        }
    },
    "7580": {
        "7580": {
            "projectName": "MTK-7580",
            "profile": "CUC_en7580_7592_7615_OSGI_demo",
            "sourcesPath": "."
        }
    },
    "wifi6": {
        "wifi6": {
            "projectName": "wifi6",
            "profile": "CT_EN7561D_LE_7915D_AP_demo",
            "uploadPath": "."
        },
        "wifi6_new": {
            "projectName": "wifi6_new",
            "profile": "CT_EN7561D_LE_7915D_AP_demo",
            "uploadPath": "."
        }
    },
    "branches": {
        "henan": {
            "projectName": "FDT_henan",
            "profile": "catv_henan_nocolor_sfu_xpon_nowifi_nocable_novoice_nousb"
        },
        "ecuador": {
            "projectName": "FDT_ecuador",
            "profile": "catv_ecuador_nocolor_hgu_xpon_wifi_cable_voice_usb"
        },
        "tvecuador": {
            "projectName": "FDT_ecuador",
            "profile": "catv_tvecuador_nocolor_hgu_xpon_wifi_cable_voice_usb"
        }
    }
}

with open("build_list.json", 'w') as file:
    data = dumps(x, indent=4, sort_keys=True)
    file.write(data)
    file.close()

y = [
    {
        "name": "wifi6_new",
        "interval": 120
    }
]

with open("timer_list.json", 'w') as file:
    data = dumps(y, indent=4, sort_keys=True)
    file.write(data)
    file.close()

z = {
    "port": 21518
}

with open("server_settings.json", 'w') as file:
    data = dumps(z, indent=4, sort_keys=True)
    file.write(data)
    file.close()
