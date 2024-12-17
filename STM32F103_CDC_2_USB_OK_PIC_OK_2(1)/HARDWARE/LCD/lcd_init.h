    #ifndef __LCD_INIT_H
#define __LCD_INIT_H

#include "sys.h"

#define DISPLAY_OVERTURN 1			//�Ƿ�ת��ʾ 1��������ת 0��������
#define DISPLAY_BOTTOM_TO_TOP 0		//��Ļ��ʾ���� 1������������ʾ 0������������ʾ
#define DISPLAY_RIGHT_TO_LEFT 1		//��Ļ��ʾ���� 1������������ʾ 0������������ʾ

#if DISPLAY_OVERTURN
#define TFT_SCREEN_WIDTH 	320
#define TFT_SCREEN_HEIGHT 	240
#define TFT_Y_OFFSET 		0	//Y�ᣨ�У���ƫ�Ƶ�ַ
#define TFT_X_OFFSET 		0	//X�ᣨ�У���ƫ�Ƶ�ַ
#else
#define TFT_SCREEN_WIDTH 	240
#define TFT_SCREEN_HEIGHT 	320
#define TFT_Y_OFFSET 		0	//Y�ᣨ�У���ƫ�Ƶ�ַ
#define TFT_X_OFFSET 		0	//X�ᣨ�У���ƫ�Ƶ�ַ
#endif

//-----------------LCD�˿ڶ���---------------- 
#define LCD_SCLK_Clr() GPIO_ResetBits(GPIOA,GPIO_Pin_4)//SCL=SCLK
#define LCD_SCLK_Set() GPIO_SetBits(GPIOA,GPIO_Pin_4)

#define LCD_MOSI_Clr() GPIO_ResetBits(GPIOA,GPIO_Pin_5)//SDA=MOSI
#define LCD_MOSI_Set() GPIO_SetBits(GPIOA,GPIO_Pin_5)

#define LCD_RES_Clr()  GPIO_ResetBits(GPIOA,GPIO_Pin_6)//RES
#define LCD_RES_Set()  GPIO_SetBits(GPIOA,GPIO_Pin_6)

#define LCD_DC_Clr()   GPIO_ResetBits(GPIOA,GPIO_Pin_7)//DC
#define LCD_DC_Set()   GPIO_SetBits(GPIOA,GPIO_Pin_7)
 		     
#define LCD_CS_Clr()   GPIO_ResetBits(GPIOA,GPIO_Pin_0)//CS
#define LCD_CS_Set()   GPIO_SetBits(GPIOA,GPIO_Pin_0)

#define LCD_BLK_Clr()  GPIO_ResetBits(GPIOA,GPIO_Pin_1)//BLK
#define LCD_BLK_Set()  GPIO_SetBits(GPIOA,GPIO_Pin_1)



void LCD_GPIO_Init(void);//��ʼ��GPIO
void LCD_Writ_Bus(u8 dat);//ģ��SPIʱ��
void LCD_WR_DATA8(u8 dat);//д��һ���ֽ�
void LCD_WR_DATA(u16 dat);//д�������ֽ�
void LCD_WR_REG(u8 dat);//д��һ��ָ��
void TFT_SetWindows(uint16_t startX,uint16_t startY,uint16_t width,uint16_t height);//�������꺯��
void LCD_Init(void);//LCD��ʼ��
#endif