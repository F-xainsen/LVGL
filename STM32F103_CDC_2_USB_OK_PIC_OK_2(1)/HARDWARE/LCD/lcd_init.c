#include "lcd_init.h"
#include "delay.h"
#include "usart.h"

void LCD_GPIO_Init(void)
{
	GPIO_InitTypeDef  GPIO_InitStructure;
 	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA, ENABLE);	 //使能A端口时钟
	GPIO_InitStructure.GPIO_Pin = GPIO_Pin_4|GPIO_Pin_5|GPIO_Pin_6|GPIO_Pin_7|GPIO_Pin_0|GPIO_Pin_1;	 
 	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_Out_PP; 		 //推挽输出
	GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;//速度50MHz
 	GPIO_Init(GPIOA, &GPIO_InitStructure);	  //初始化GPIOB
 	GPIO_SetBits(GPIOA,GPIO_Pin_4|GPIO_Pin_5|GPIO_Pin_6|GPIO_Pin_7|GPIO_Pin_0|GPIO_Pin_1);
}

/******************************************************************************
      函数说明：LCD串行数据写入函数
      入口数据：dat  要写入的串行数据
      返回值：  无
******************************************************************************/
void LCD_Writ_Bus(u8 dat) 
{	
	u8 i;
	LCD_CS_Clr();
	for(i=0;i<8;i++)
	{			  
		LCD_SCLK_Clr();
		if(dat&0x80)
		{
		   LCD_MOSI_Set();
		}
		else
		{
		   LCD_MOSI_Clr();
		}
		LCD_SCLK_Set();
		dat<<=1;
	}	
	LCD_CS_Set();	
}


/******************************************************************************
      函数说明：LCD写入数据
      入口数据：dat 写入的数据
      返回值：  无
******************************************************************************/
void LCD_WR_DATA8(u8 dat)
{
	LCD_Writ_Bus(dat);
}


/******************************************************************************
      函数说明：LCD写入数据
      入口数据：dat 写入的数据
      返回值：  无
******************************************************************************/
void LCD_WR_DATA(u16 dat)
{
	LCD_Writ_Bus(dat>>8);
	LCD_Writ_Bus(dat);
}


/******************************************************************************
      函数说明：LCD写入命令
      入口数据：dat 写入的命令
      返回值：  无
******************************************************************************/
void LCD_WR_REG(u8 dat)
{
	LCD_DC_Clr();//写命令
	LCD_Writ_Bus(dat);
	LCD_DC_Set();//写数据
}


/*************************************
*@brief TFT_SetWindows
*@details 设置显示窗口大小
*@param[in] startX：X起始坐标
*			startY：Y起始坐标
*			width:宽
*			height:高
*@return void
*@author zx
*@date 2023-08-13
***************************************/
void TFT_SetWindows(uint16_t startX,uint16_t startY,uint16_t width,uint16_t height)
{
#if TFT_X_OFFSET
	startX += TFT_X_OFFSET;
#endif	
#if TFT_Y_OFFSET
	startY += TFT_Y_OFFSET;
#endif		
	LCD_WR_REG(0x2A);		//发送设置X轴坐标的命令0x2A
	//参数SC[15:0]	->	设置起始列地址，也就是设置X轴起始坐标
	LCD_WR_DATA(startX);
	//参数EC[15:0]	->	设置窗口X轴结束的列地址，因为参数usXwidth是窗口长度，所以要转为列地址再发送
	LCD_WR_DATA(startX+width -1);

	LCD_WR_REG(0x2B);		//发送设置Y轴坐标的命令0x2B
	//参数SP[15:0]	->	设置起始行地址，也就是设置Y轴起始坐标
	LCD_WR_DATA(startY);
	//参数EP[15:0]	->	设置窗口Y轴结束的列地址，因为参数usYheight是窗口高度，所以要转为行地址再发送
	LCD_WR_DATA((startY+height-1));
	LCD_WR_REG(0x2C);			//开始往GRAM里写数据
}

void LCD_Init(void)
{
	uint8_t lcd_data = 0x00;
	uint16_t start_x = 0;
	uint16_t end_x = TFT_SCREEN_WIDTH;
	uint16_t start_y = 0;
	uint16_t end_y = TFT_SCREEN_HEIGHT;
#if TFT_X_OFFSET
	start_x += TFT_X_OFFSET;
	end_x += TFT_X_OFFSET;
#endif	
#if TFT_Y_OFFSET
	start_y += TFT_Y_OFFSET;
	end_y += TFT_Y_OFFSET;
#endif	
	LCD_GPIO_Init();//初始化GPIO
	
	LCD_RES_Clr();//复位
	delay_ms(100);
	LCD_RES_Set();
	delay_ms(100);
	
	//LCD_BLK_Set();//打开背光
	LCD_BLK_Clr();
	delay_ms(100);
	
	LCD_WR_REG(0x11); //Sleep out
	delay_ms(120); //Delay 120ms
	
	LCD_WR_REG(0x3A); //65k mode
	LCD_WR_DATA8(0x05);
	LCD_WR_REG(0xC5); //VCOM
	LCD_WR_DATA8(0x1A);
	
	LCD_WR_REG(0x36);
#if DISPLAY_BOTTOM_TO_TOP
	lcd_data |= (1<<7);
#else	
	lcd_data |= (0<<7);
#endif
#if DISPLAY_RIGHT_TO_LEFT
	lcd_data |= (1<<6);
#else	
	lcd_data |= (0<<6);
#endif

#if DISPLAY_OVERTURN//不翻转显示
	lcd_data |= (1<<5);//翻转显示
#else
	lcd_data |= (0<<5);	
#endif
	LCD_WR_DATA8(lcd_data);
	
	LCD_WR_REG(0x2A); //设置显示区域 x轴起始及结束坐标 
	LCD_WR_DATA8((start_x>>8)&0xff);
	LCD_WR_DATA8(start_x&0xff);
	LCD_WR_DATA8((end_x>>8)&0xff);
	LCD_WR_DATA8(end_x&0xff);

	LCD_WR_REG(0x2B); //设置显示区域 Y轴起始及结束坐标
	LCD_WR_DATA8((start_y>>8)&0xff);
	LCD_WR_DATA8(start_y&0xff);
	LCD_WR_DATA8((end_y>>8)&0xff);
	LCD_WR_DATA8(end_y&0xff);
	
	//-------------ST7789V Frame rate setting-----------//
	LCD_WR_DATA8(0xb2);		//Porch Setting
	LCD_WR_DATA8(0x05);
	LCD_WR_DATA8(0x05);
	LCD_WR_DATA8(0x00);
	LCD_WR_DATA8(0x33);
	LCD_WR_DATA8(0x33);
	
	LCD_WR_REG(0xb7);			//Gate Control
	LCD_WR_DATA8(0x05);			//12.2v   -10.43v
	//--------------ST7789V Power setting---------------//
	LCD_WR_REG(0xBB);//VCOM
	LCD_WR_DATA8(0x3F);	
	
	
	LCD_WR_REG(0xC0);
	LCD_WR_DATA8(0x2C);
//	LCD_WR_DATA8(0x02);
//	LCD_WR_DATA8(0x84);
	
//	LCD_WR_REG(0xC1);
//	LCD_WR_DATA8(0xC5);
	LCD_WR_REG(0xC2);
	LCD_WR_DATA8(0x01);
//	LCD_WR_DATA8(0x00);

	LCD_WR_REG(0xC3);
	LCD_WR_DATA8(0x0F);
//	LCD_WR_DATA8(0x2A);

	LCD_WR_REG(0xC4);
	LCD_WR_DATA8(0x20);
//	LCD_WR_DATA8(0xEE);

	LCD_WR_REG(0xC6);				//Frame Rate Control in Normal Mode
	LCD_WR_DATA8(0X01);			//111Hz
	
	LCD_WR_REG(0xd0);				//Power Control 1
	LCD_WR_DATA8(0xa4);
	LCD_WR_DATA8(0xa1);
	
	LCD_WR_REG(0xE8);				//Power Control 1
	LCD_WR_DATA8(0x03);
	
	LCD_WR_REG(0xE9);				//Equalize time control
	LCD_WR_DATA8(0x09);
	LCD_WR_DATA8(0x09);
	LCD_WR_DATA8(0x08);
	//---------------------------------End ST7735S Power Sequence---------------------------------------//


	//------------------------------------ST7735S Gamma Sequence-----------------------------------------//
	LCD_WR_REG(0XE0);
	LCD_WR_DATA8(0xD0);
	LCD_WR_DATA8(0x05);
	LCD_WR_DATA8(0x09);
	LCD_WR_DATA8(0x09);
	LCD_WR_DATA8(0x08);
	LCD_WR_DATA8(0x14);
	LCD_WR_DATA8(0x28);
	LCD_WR_DATA8(0x33);
	LCD_WR_DATA8(0x3F);
	LCD_WR_DATA8(0x07);
	LCD_WR_DATA8(0x13);
	LCD_WR_DATA8(0x14);
	LCD_WR_DATA8(0x28);
	LCD_WR_DATA8(0x30);

	LCD_WR_REG(0XE1);
	LCD_WR_DATA8(0xD0);
	LCD_WR_DATA8(0x05);
	LCD_WR_DATA8(0x09);
	LCD_WR_DATA8(0x09);
	LCD_WR_DATA8(0x08);
	LCD_WR_DATA8(0x03);
	LCD_WR_DATA8(0x24);
	LCD_WR_DATA8(0x32);
	LCD_WR_DATA8(0x32);
	LCD_WR_DATA8(0x3B);
	LCD_WR_DATA8(0x14);
	LCD_WR_DATA8(0x13);
	LCD_WR_DATA8(0x28);
	LCD_WR_DATA8(0x2F);
	//------------------------------------End ST7735S Gamma Sequence-----------------------------------------//
	LCD_WR_REG(0x21); 		//反显
	
	LCD_WR_REG(0x29); //Display on 
}








