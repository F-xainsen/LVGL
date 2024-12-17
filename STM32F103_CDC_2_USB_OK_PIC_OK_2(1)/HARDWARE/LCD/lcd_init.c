#include "lcd_init.h"
#include "delay.h"
#include "usart.h"

void LCD_GPIO_Init(void)
{
	GPIO_InitTypeDef  GPIO_InitStructure;
 	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA, ENABLE);	 //ʹ��A�˿�ʱ��
	GPIO_InitStructure.GPIO_Pin = GPIO_Pin_4|GPIO_Pin_5|GPIO_Pin_6|GPIO_Pin_7|GPIO_Pin_0|GPIO_Pin_1;	 
 	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_Out_PP; 		 //�������
	GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;//�ٶ�50MHz
 	GPIO_Init(GPIOA, &GPIO_InitStructure);	  //��ʼ��GPIOB
 	GPIO_SetBits(GPIOA,GPIO_Pin_4|GPIO_Pin_5|GPIO_Pin_6|GPIO_Pin_7|GPIO_Pin_0|GPIO_Pin_1);
}

/******************************************************************************
      ����˵����LCD��������д�뺯��
      ������ݣ�dat  Ҫд��Ĵ�������
      ����ֵ��  ��
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
      ����˵����LCDд������
      ������ݣ�dat д�������
      ����ֵ��  ��
******************************************************************************/
void LCD_WR_DATA8(u8 dat)
{
	LCD_Writ_Bus(dat);
}


/******************************************************************************
      ����˵����LCDд������
      ������ݣ�dat д�������
      ����ֵ��  ��
******************************************************************************/
void LCD_WR_DATA(u16 dat)
{
	LCD_Writ_Bus(dat>>8);
	LCD_Writ_Bus(dat);
}


/******************************************************************************
      ����˵����LCDд������
      ������ݣ�dat д�������
      ����ֵ��  ��
******************************************************************************/
void LCD_WR_REG(u8 dat)
{
	LCD_DC_Clr();//д����
	LCD_Writ_Bus(dat);
	LCD_DC_Set();//д����
}


/*************************************
*@brief TFT_SetWindows
*@details ������ʾ���ڴ�С
*@param[in] startX��X��ʼ����
*			startY��Y��ʼ����
*			width:��
*			height:��
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
	LCD_WR_REG(0x2A);		//��������X�����������0x2A
	//����SC[15:0]	->	������ʼ�е�ַ��Ҳ��������X����ʼ����
	LCD_WR_DATA(startX);
	//����EC[15:0]	->	���ô���X��������е�ַ����Ϊ����usXwidth�Ǵ��ڳ��ȣ�����ҪתΪ�е�ַ�ٷ���
	LCD_WR_DATA(startX+width -1);

	LCD_WR_REG(0x2B);		//��������Y�����������0x2B
	//����SP[15:0]	->	������ʼ�е�ַ��Ҳ��������Y����ʼ����
	LCD_WR_DATA(startY);
	//����EP[15:0]	->	���ô���Y��������е�ַ����Ϊ����usYheight�Ǵ��ڸ߶ȣ�����ҪתΪ�е�ַ�ٷ���
	LCD_WR_DATA((startY+height-1));
	LCD_WR_REG(0x2C);			//��ʼ��GRAM��д����
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
	LCD_GPIO_Init();//��ʼ��GPIO
	
	LCD_RES_Clr();//��λ
	delay_ms(100);
	LCD_RES_Set();
	delay_ms(100);
	
	//LCD_BLK_Set();//�򿪱���
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

#if DISPLAY_OVERTURN//����ת��ʾ
	lcd_data |= (1<<5);//��ת��ʾ
#else
	lcd_data |= (0<<5);	
#endif
	LCD_WR_DATA8(lcd_data);
	
	LCD_WR_REG(0x2A); //������ʾ���� x����ʼ���������� 
	LCD_WR_DATA8((start_x>>8)&0xff);
	LCD_WR_DATA8(start_x&0xff);
	LCD_WR_DATA8((end_x>>8)&0xff);
	LCD_WR_DATA8(end_x&0xff);

	LCD_WR_REG(0x2B); //������ʾ���� Y����ʼ����������
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
	LCD_WR_REG(0x21); 		//����
	
	LCD_WR_REG(0x29); //Display on 
}








