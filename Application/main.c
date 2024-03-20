#include "../MCAL/UART/UART.h"

u8 *Register_address; 
int main()
{
	UART_init(9600);
	while (1)
	{
		switch (UART_RxChar())
		{
			case '@':
				switch (UART_RxChar())
				{
					case 'R':
						Register_address = UART_RxChar();
						*Register_address = UART_RxChar();
						break;
					case 'W':
						Register_address = UART_RxChar();
						UART_TxChar(*Register_address);
						break;
					default:
						break;
				}
				break;
			case ';':
				break;	
		}
	}
	
}



