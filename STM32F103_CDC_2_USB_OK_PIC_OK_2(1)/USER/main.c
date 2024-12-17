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
 ALIENTEKս��STM32������ʵ��48
USB���⴮�� ʵ�� 
 ����֧�֣�www.openedv.com
 �Ա����̣�http://eboard.taobao.com 
 ��ע΢�Ź���ƽ̨΢�źţ�"����ԭ��"����ѻ�ȡSTM32���ϡ�
 ������������ӿƼ����޹�˾  
 ���ߣ�����ԭ�� @ALIENTEK
************************************************/


 int main(void)
 {	 
 	float tt=0;
	u16 j;
	u8 new_y,k=5;
	//const uint16_t bmp_array[];
	u16 times=0;   
		
	
	u8 usbstatus=0;	
	delay_init();	    	 //��ʱ������ʼ��	  
	NVIC_PriorityGroupConfig(NVIC_PriorityGroup_2);	 //����NVIC�жϷ���2:2λ��ռ���ȼ���2λ��Ӧ���ȼ�
	
	uart_init(115200);	 	//���ڳ�ʼ��Ϊ115200
	LED_Init();		  		//��ʼ����LED���ӵ�Ӳ���ӿ�

	delay_ms(1800);
	USB_Port_Set(0); 	//USB�ȶϿ�
	delay_ms(700);
	USB_Port_Set(1);	//USB�ٴ�����
 	Set_USBClock();   
 	USB_Interrupts_Config();    
 	USB_Init();	    
	
	
	LCD_Init();//LCD��ʼ��
	delay_ms(100);
	LCD_BLK_Set();//�򿪱���
	
	LCD_Fill(0,0,TFT_SCREEN_WIDTH,TFT_SCREEN_HEIGHT,WHITE);//����
	
	delay_ms(100);
	//TFT_display_image(bmp_array, 100, 100);
	
	//LCD_ShowPicture(0,0,320,240,gImage_5);//640�ֽ�
	
	
	//LCD_ShowPicture(0,100,320,100,gImage_5);
	while(1)
	{
	
		
		//LCD_ShowFloatNum1(280,224,tt,4,RED,WHITE,16);
		//tt+=0.11;	
		
		if(usbstatus!=bDeviceState)//USB����״̬�����˸ı�.
		{
			usbstatus=bDeviceState;//��¼�µ�״̬
			if(usbstatus==CONFIGURED)
			{
				LED1=0;//DS1��
			}else
			{
				LED1=1;//DS1��
			}
		
		}
		//USART_SendData(USART1,0XAAAA);	//�������ݣ���ʵ���Ǳ������ݣ� 
		
		//printf("%d\r\n",k);
		GET_RX_BUFF_and_Send_Lcd();
		
	}
}

