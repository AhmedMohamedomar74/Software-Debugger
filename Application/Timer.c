#include "Timer.h"
static void Check_MAX(u8 * duty);
static void Check_MIN(u8 * duty);
void PWM_init()
{
	/*set fast PWM mode with non-inverted output*/
	TCCR0 = (1<<WGM00) | (1<<WGM01) | (1<<COM01) | (1<<CS00);
	DDRB|=(1<<PB3);  /*set OC0 pin as output*/
}

void inc_speed ()
{
    unsigned char duty;
    Check_MAX(&duty);
    OCR0 = duty;        
}

void dec_speed ()
{
   unsigned char duty;
    Check_MIN(&duty);
    OCR0 = duty;  
}

static void Check_MIN(u8 * duty)
{
    if ((*(duty)  >= 0) && (*(duty)  < 10))
    {
        *(duty) =0; 
    }
    else
    {
        *(duty) -= 10;
    }
}

static void Check_MAX(u8 * duty)
{
    if (*(duty)  < 250)
    {
        *(duty) +=10;
    }
    else
    {
        *(duty) = 255;
    }
    
}