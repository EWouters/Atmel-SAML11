// Copyright 2016 Nathan Kinder and the Smart Card Removinator contributors
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//   http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#include "serial_interface.h"

// get_command()
//
// Get a command from the serial port, checking for a proper envelope and length.
//
// Returns:
//          0 - If we received a properly enveloped command.
//   Non-zero - If we received an illegally formatted command.  A more
//              detailed error code will be returned via serial.
//
int get_command(char * command)
{
	int rc = 1;
	char inbyte = 0;
	int  command_length = 0;
	
	scanf("%c", &inbyte);
	
	// Make sure the command start sequence is present.
	if (inbyte == CMD_PREFIX) {
		while ((inbyte != CMD_TERM) && (command_length <= CMD_MAX_LEN)) {
			scanf("%c", &inbyte);
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

char * serial_command()
{
	/* Print protocol information */
	//usage();
	
	char command[CMD_MAX_LEN + 1];
	//bool debug = false;
	
	/* Attempt to get a command from the serial port */
	if (get_command(&command) == 0) {
		//debug_print(String("Received command \"" + String(command) + "\""));
		if (strcmp(command, CMD_STATUS) == 0) {
			printf("Hello\n");
			printf(RESP_OK);
			} else if (strcmp(command, CMD_HELP) == 0) {
			usage();
			//} else if (strcmp(command, CMD_DEBUG) == 0) {
			//toggle_debug();
			} else {
			printf(ERR_UNKNOWN_CMD);
		}
				
		// Clear the previous command
		command[0] = '\0';
	}
	
	return command;
}
