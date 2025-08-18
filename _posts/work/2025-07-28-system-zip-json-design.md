

## 系统压缩资源包设计

（4）设置需要密码---197@Paytm （5）默认时区GMT +5:30 IST （6）默认语言：英语  ，到设置里面



（3）预装客户Paytm Launcher，并且设备启动后应默认设置为 Paytm Launcher。---待提供  -- 设置为launcher ，apps节点里面有launcher对应的字段，表示这个需要 



应用签名证书- 上传，目前设计只有一个证书， 如果要更新多级证书，只能分多次更新资源包实现，一次更新一级证书-

是否可以改成支持传多个证书，







``` json

{
    no: "2222222",
    name: "系统更新版本-手动制作",
    author: "Apex",
    version: "0.0.1",
    protocol: "0.1",
    createDate: "2025-07-18 10:00:00",
    releaseDate: "2025-07-18 11:00:00"，
    viewAndControl: {
        resourceName: "系统更新版本-手动制作",
        model: "P1411",
        company: "sumboy代理商",
        resourceType: "Beta",
        description:"备注内容",
        deviceName: "",
        buildNumber: "R2351_KozenOS_combo_20250728",
        systemColor: "blue",
        screenMainStartLogo: "/viewAndControl/kaijilogo.jpg",
        screenMainStartAnimation: "/viewAndControl/animation.zip",
        screenMainStartWallpaper: "/viewAndControl/wallpaper.jpg",
        screenMainBrightness: 50,
        screenSecondaryLogo: "/viewAndControl/logo2.jpg",
        screenSecondaryBrightness: 50,
        defaultPrintingDensity: 50,
        defaultSpeakerVolume: 50,
    },
    appAndDesktop:{
        viewVirtualButton: [
            {
                show: true,
                keyValue: 111,
                keyLabel: "BACK KEY"
            }
        ],
        viewConfig: [
            {
                show: true,
                function: "Wifi"
            }
        ],
        appSignCert: "/appAndDesktop/sign.crt",
        apps: [
            {
                appName: "客户APK",
                version: "1.0.1"
                packageName: "xxx.xxx.xxx",
                size: 122222,
                featureAntiDeletion: "ON",
                featureLock: "ON",
                featurePowerBoot: "OFF",
                featureHiddenIcon: "-",
                featureWifiWhiteList: "ON",
                featureKiosk: "-"
            }
        ]
    },
    network: {
        apns: [
            {
                apnName: "myApn",
                apn: "",
                more: "....."
            }
        ],
        vpns: [
            {
                 vpnName: "myVpn",
                 vpnType: "IKEv2/IPSec MSCHAPV2",
                 vpnProxy: "xxx",
                 more: "....."
            }
        ],
        ntp: [
            {
                ntpLocation: "",
                ntpServer: "",
                description:"",
                more: "....."
            }
        ]
    },
    license: {
        privacyPolicyDocument: "/license/privacyPolicyDocument.pdf",
        kozenAppPrivacyPolicyDocument: "/license/kozenAppPrivacyPolicyDocument.pdf"
    }
}


```

