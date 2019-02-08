#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#include "dgilib-5.7.244/dgilib.h"

// Wireshark filter:
// usb.dst == "1.9.0" || usb.src == "1.9.0"

enum
{
    O32_LITTLE_ENDIAN = 0x03020100ul,
    O32_BIG_ENDIAN = 0x00010203ul,
    O32_PDP_ENDIAN = 0x01000302ul,      /* DEC PDP-11 (aka ENDIAN_LITTLE_WORD) */
    O32_HONEYWELL_ENDIAN = 0x02030001ul /* Honeywell 316 (aka ENDIAN_BIG_WORD) */
};

static const union { unsigned char bytes[4]; uint32_t value; } o32_host_order =
    { { 0, 1, 2, 3 } };

#define O32_HOST_ORDER (o32_host_order.value)


void phex(unsigned char * str, unsigned char len)
{
    for (unsigned char i = 0; i < len; ++i)
        printf("%.2x ", str[i]);
//    printf("\n");
}

int main()
{
    if (O32_HOST_ORDER == O32_LITTLE_ENDIAN) {
        printf("Is little endian\n");
    } else if (O32_HOST_ORDER == O32_BIG_ENDIAN) {
        printf("Is big endian\n");
    }
    int res = 0;

    int major_version = get_major_version();
    printf("major_version: %d\n", major_version);
    int minor_version = get_minor_version();
    printf("minor_version: %d\n", minor_version);
    int build_number = get_build_number();
    printf("build_number: %d\n", build_number);


    discover();

    int device_count = get_device_count();
    printf("device_count: %d\n", device_count);
    int index = 0;
    char sn[255];
    printf("%d ", get_device_serial(index, sn));
    printf("device_serial: %s\n", sn);
    char name[255];
    printf("%d ", get_device_name(index, name));
    printf("device_name: %s\n", name);

    dgi_handle_t dgi_hndl;
//    power_handle_t power_h;
//
    Initialize(&dgi_hndl);

    //int execute_pam_cmd(dgi_hndl, unsigned char* cmd, unsigned int cmd_len, unsigned char* resp, unsigned int* resp_len);

    int msd_mode = is_msd_mode(sn);
    printf("msd_mode: %d\n", msd_mode);

//    int nmbed = 1;
//    printf("%d set_mode %d\n", set_mode(sn, nmbed), nmbed);

//    msd_mode = is_msd_mode(sn);
//    printf("msd_mode: %d\n", msd_mode);

    int c_status = connection_status(dgi_hndl);
    printf("connection_status: %d\n", c_status);

	res = connect(sn, &dgi_hndl);
    printf("%d connect\n", res);

    c_status = connection_status(dgi_hndl);
    printf("connection_status: %d\n", c_status);

    printf("Resetting %s ", name);
    printf("%d", target_reset(dgi_hndl, true));
    for (int i = 0; i < 10; i++) {
        printf(".");
        for (int j = 0;j < 47483647; j++) {}
    }
    printf("%d", target_reset(dgi_hndl, false));
    printf(" Done\n");

    c_status = connection_status(dgi_hndl);
    printf("connection_status: %d\n", c_status);

    unsigned char major = 0;
    unsigned char minor = 0;
    res = get_fw_version(dgi_hndl, &major, &minor);
    printf("%d fw_version major: %d, minor: %d\n", res, major, minor);

//    unsigned char* interfaces = 0;
    unsigned char interfaces[10] = {'\0'};
    unsigned char count;
    res = interface_list(dgi_hndl, interfaces, &count);
    //interfaces[254] = '\0';
    //count[254] = '\0';
    printf("%d interface_list: ", res);
    phex(interfaces, 10);
    printf(", count: %d\n", count);

//    unsigned char cmd[1] = {0x00};
//    unsigned int cmd_len = 0x0000;
//    unsigned char resp[255] = {' '};
//    unsigned int resp_len = 255;
//    printf("%d ", execute_pam_cmd(dgi_hndl, cmd, cmd_len, resp, &resp_len));
//    printf("pam_cmd: %s, cmd_len: %d, resp: %s, resp_len: %d\n", cmd, cmd_len, resp, resp_len);
//
//    unsigned char cmd1[1] = {0x02};
//    unsigned int cmd_len1 = 0x0000;
//    unsigned char resp1[255] = {' '};
//    unsigned int resp_len1 = 255;
//    printf("%d ", execute_pam_cmd(dgi_hndl, cmd1, cmd_len1, resp1, &resp_len1));
//    printf("pam_cmd: %s, cmd_len: %d, resp: %s, resp_len: %d\n", cmd1, cmd_len1, resp1, resp_len1);

//    start_polling(dgi_hndl);
//
//    stop_polling(dgi_hndl);

    res = disconnect(dgi_hndl);
    printf("%d disconnect\n", res);
    c_status = connection_status(dgi_hndl);
    printf("connection_status: %d\n", c_status);

//    uint8_t gpio_map = 0;
//    printf("gpio_map of %d is %d\n", gpio_map, get_gpio_map(dgi_hndl, &gpio_map));

    UnInitialize(dgi_hndl);

    printf("\n\nHello world!\n");
    return res;
}

//void *DeviceStatusChangedCallBack(const char* str1, const char* str2, bool b1)
//{
//    printf("%s, %s, %d", str1, str2, b1);
//}
