#include <atmel_start.h>
#include <string.h>

// Serial command syntax
#define CMD_PREFIX '#'
#define CMD_TERM '\r'
#define CMD_MAX_LEN 3

// Serial commands
#define CMD_STATUS "STA"
//#define CMD_DEBUG "DBG"
#define CMD_HELP "?"

// Standard serial responses
#define RESP_OK "OK\n"
//#define RESP_DBG_ON "DBG_ON\n"
//#define RESP_DBG_OFF "DBG_OFF\n"
#define ERR_UNKNOWN_CMD "ERR_UNKNOWN_CMD\n"
#define ERR_CMDLEN "ERR_CMDLEN\n"
#define ERR_PROTOCOL2 "ERR_PROTOCOL\n"

char command[CMD_MAX_LEN + 1];
//bool debug = false;

//int getCommand();
////void toggleDebug();
////void debug_print(String msg);
//void usage();

//// Debug output defines
//#define LOG_DBG_PREFIX "[DBG] "

// getCommand()
//
// Get a command from the serial port, checking for a proper envelope and length.
//
// Returns:
//          0 - If we received a properly enveloped command.
//   Non-zero - If we received an illegally formatted command.  A more
//              detailed error code will be returned via serial.
//
int getCommand()
{
	int rc = 1;
	char inbyte = 0;
	int  command_length = 0;
	
	//inbyte = getchar();
	scanf("%c", &inbyte);
	//printf("%c", inbyte);
	
	// Make sure the command start sequence is present.
	if (inbyte == CMD_PREFIX) {
		while ((inbyte != CMD_TERM) && (command_length <= CMD_MAX_LEN)) {
			//inbyte = getchar();
			scanf("%c", &inbyte);
			//printf("%c", inbyte);
			if ((inbyte > 0) && (inbyte != CMD_TERM)) {
				command[command_length] = inbyte;
				command_length++;
			}
		}
			
		// See if we exceeded the maximum command length.
		if (inbyte != CMD_TERM) {
			printf(ERR_CMDLEN);
			command[0] = '\0';
		} else {
			// Terminate the command string.
			command[command_length] = '\0';
			rc = 0;
		}
	} else {
		// Illegally formatted command or garbage (protocol error).
		printf(ERR_PROTOCOL2);
	}
	
	//printf(command);
	
	return rc;
}

//// debug_print()
////
//// Prints debug message to serial port if debugging output is enabled.
////
//// Parameters:
////   msg - The message to print.  A newline will be added automatically.
////
//void debug_print(String msg)
//{
	//if (debug) {
		//printf(LOG_DBG_PREFIX);
		//printf(msg);
	//}
//}

// usage()
//
// Prints usage details to serial port
//
void usage()
{
	printf("--- SAML11 ---\n\n");
	printf("Command Format:\n");
	printf("\t");
	printf("Prefix:");
	printf("\t\t");
	printf("#\n");
	printf("\t");
	printf("Terminator:");
	printf("\t");
	printf("\\r\n");
	printf("Commands:\n");
	printf("\t");
	printf(CMD_STATUS);
	printf("\t");
	printf("Return some status\n");  // TODO
	printf("\t");
	//printf(CMD_DEBUG);
	//printf("\t");
	//printf("Toggle debugging output");
	//printf("\t");
	printf(CMD_HELP);
	printf("\t");
	printf("Show usage information\n");

	// Terminate our serial response.
	printf(RESP_OK);
}

int main(void)
{
	/* Initializes MCU, drivers and middleware */
	atmel_start_init();
	
	/* Print protocol information */
	//usage();

	/* Replace with your application code */
	while (1) {
		//delay_ms(1000);
		// Attempt to get a command from the serial port
		if (getCommand() == 0) {
			//debug_print(String("Received command \"" + String(command) + "\""));
			if (strcmp(command, CMD_STATUS) == 0) {
				printf("Hello\n");
				printf(RESP_OK);
			} else if (strcmp(command, CMD_HELP) == 0) {
				usage();
			//} else if (strcmp(command, CMD_DEBUG) == 0) {
				//toggleDebug();
			} else {
				printf(ERR_UNKNOWN_CMD);
			}
			    
			// Clear the previous command
			command[0] = '\0';
		}
	}
}
