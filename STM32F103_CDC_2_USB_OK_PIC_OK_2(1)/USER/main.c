#include "sys.h"
#include "delay.h"
#include "usart.h" 
#include "led.h" 		 	 
#include "lcd.h" 
#include "usb_lib.h"
#include "hw_config.h"
#include "usb_pwr.h"	 
 #include "lcd_init.h"
 #include "pic.h"

/************************************************
 ALIENTEK战舰STM32开发板实验48
USB虚拟串口 实验 
 技术支持：www.openedv.com
 淘宝店铺：http://eboard.taobao.com 
 关注微信公众平台微信号："正点原子"，免费获取STM32资料。
 广州市星翼电子科技有限公司  
 作者：正点原子 @ALIENTEK
************************************************/


 int main(void)
 {	 
 	float tt=0;
	u16 j;
	u8 new_y,k=5;
	//const uint16_t bmp_array[];
	u16 times=0;   
		
	
	u8 usbstatus=0;	
	delay_init();	    	 //延时函数初始化	  
	NVIC_PriorityGroupConfig(NVIC_PriorityGroup_2);	 //设置NVIC中断分组2:2位抢占优先级，2位响应优先级
	
	uart_init(115200);	 	//串口初始化为115200
	LED_Init();		  		//初始化与LED连接的硬件接口

	delay_ms(1800);
	USB_Port_Set(0); 	//USB先断开
	delay_ms(700);
	USB_Port_Set(1);	//USB再次连接
 	Set_USBClock();   
 	USB_Interrupts_Config();    
 	USB_Init();	    
	
	
	LCD_Init();//LCD初始化
	delay_ms(100);
	LCD_BLK_Set();//打开背光
	
	LCD_Fill(0,0,TFT_SCREEN_WIDTH,TFT_SCREEN_HEIGHT,WHITE);//清屏
	
	delay_ms(100);
	//TFT_display_image(bmp_array, 100, 100);
	
	//LCD_ShowPicture(0,0,320,240,gImage_5);//640字节
	
	
	//LCD_ShowPicture(0,100,320,100,gImage_5);
	while(1)
	{
	
		
		//LCD_ShowFloatNum1(280,224,tt,4,RED,WHITE,16);
		//tt+=0.11;	
		
		if(usbstatus!=bDeviceState)//USB连接状态发生了改变.
		{
			usbstatus=bDeviceState;//记录新的状态
			if(usbstatus==CONFIGURED)
			{
				LED1=0;//DS1亮
			}else
			{
				LED1=1;//DS1灭
			}
		
		}
		//USART_SendData(USART1,0XAAAA);	//处理数据（其实就是保存数据） 
		
		//printf("%d\r\n",k);
		GET_RX_BUFF_and_Send_Lcd();
		
	}
}

