    #ifndef __LCD_INIT_H
#define __LCD_INIT_H

#include "sys.h"

#define DISPLAY_OVERTURN 1			//是否翻转显示 1：开启翻转 0：不开启
#define DISPLAY_BOTTOM_TO_TOP 0		//屏幕显示方向 1：从下往上显示 0：从上往下显示
#define DISPLAY_RIGHT_TO_LEFT 1		//屏幕显示方向 1：从右往左显示 0：从左往右显示

#if DISPLAY_OVERTURN
#define TFT_SCREEN_WIDTH 	320
#define TFT_SCREEN_HEIGHT 	240
#define TFT_Y_OFFSET 		0	//Y轴（列）的偏移地址
#define TFT_X_OFFSET 		0	//X轴（行）的偏移地址
#else
#define TFT_SCREEN_WIDTH 	240
#define TFT_SCREEN_HEIGHT 	320
#define TFT_Y_OFFSET 		0	//Y轴（列）的偏移地址
#define TFT_X_OFFSET 		0	//X轴（行）的偏移地址
#endif

//-----------------LCD端口定义---------------- 
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



void LCD_GPIO_Init(void);//初始化GPIO
void LCD_Writ_Bus(u8 dat);//模拟SPI时序
void LCD_WR_DATA8(u8 dat);//写入一个字节
void LCD_WR_DATA(u16 dat);//写入两个字节
void LCD_WR_REG(u8 dat);//写入一个指令
void TFT_SetWindows(uint16_t startX,uint16_t startY,uint16_t width,uint16_t height);//设置坐标函数
void LCD_Init(void);//LCD初始化
#endif