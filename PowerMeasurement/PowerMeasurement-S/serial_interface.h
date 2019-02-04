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

#ifndef SERIAL_INTERFACE_H_
#define SERIAL_INTERFACE_H_

#include "stdio_start.h"
#include <string.h>

// Serial command syntax
#define CMD_PREFIX '#'
#define CMD_TERM '\r'
#define CMD_MAX_LEN 3

// Serial commands
#define CMD_STATUS "STA"
#define CMD_DEBUG "DBG"
#define CMD_HELP "?"

// Standard serial responses
#define RESP_OK "OK\n"
#define RESP_DBG_ON "DBG_ON\n"
#define RESP_DBG_OFF "DBG_OFF\n"
#define ERR_UNKNOWN_CMD "ERR_UNKNOWN_CMD\n"
#define ERR_CMDLEN "ERR_CMDLEN\n"
#define ERR_PROTOCOL2 "ERR_PROTOCOL\n"

int get_command(char * command);
void toggle_debug(bool * debug);
void debug_print(char * info, char * argument, bool * debug);
void usage();
void serial_command(char * command);

// Debug output defines
#define LOG_DBG_PREFIX "[DBG] "

#endif /* SERIAL_INTERFACE_H_ */