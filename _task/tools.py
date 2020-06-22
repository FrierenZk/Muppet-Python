import json

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
        }
    }
}

with open("build_list.json", 'w') as file:
    data = json.dumps(x, indent=4, sort_keys=True)
    file.write(data)
    file.close()
