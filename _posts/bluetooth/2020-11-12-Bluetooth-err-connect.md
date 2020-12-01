断开连接: 

## app_SmtChgCse_SetDisconnectedPhone 收到断开事件


可能导致

1.  App_Media.c # APP_Media_PushMediaEvent 逻辑判断错误?(排除,log看不是)

2. APP_PowerOff.c #  APP_PowerOff_Loade xr    (看log是它) 

   <--- APP_Conn_SetCustPhoneConnect 

  3. App_SmartChgCase.c# app_SmtChgCse_ChgCaseOffHandler   

     <--- app_SmtChgCse_CaseOff <--- app_SmtChgCse_StateHandler#SMART_CASE_OFF_IND  <--- AppChargeBattery.c # APP_ChgBat_Init switch#CASE_TYPE_ONE_WIRE

  

  

  

  2. App_SmartChgCase.c# app_SmtChgCse_LidOffHandler

     <---  APP_AirApp_EnableBleAdv 

     ​	在外面的是从机,

  3. App_SmartChgCase.c# APP_SmtChgCse_MCSyncConnCfmCheck

   ( 下面可能)

  4.  APP_MCSync_Rho.c   #  APP_MCSync_Rho_RoleChangeIndHandler

  5.  app_MCSync_Rho_SetFinishHandler

  6.   app_AwsMce_SyncPowerOffHandler 













###  del

> del

``` c
printf("wpf ... chg mute and all in box ,pause music , !isDefaultRolePartner: %d, GetBatStatus %d",!BtAwsMce_IsDefaultRolePartner(),APP_ChgBat_GetBatStatus());
			 //主机入仓, 判断两只耳机都已入仓,停止播放
			 if(!BtAwsMce_IsDefaultRolePartner()) 
			 {
				if(APP_ChgBat_GetBatStatus() >= APP_BAT_CHARGER_IN){
					//APP_CusTimer_CheckPlayStateAndDoAction(FALSE); //调用暂停音乐

					printf("wpf ...  pause music # App_Battery > APP_ChgBat_UpdateBatStatus");
					//APP_CustomerSetTimer(CUSTOMER_TIMER_ID_PAUSE, NULL, 0, 3 * ONE_SEC);
					
				}
			 }	
```



