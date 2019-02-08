#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#include "dgilib-5.7.244/dgilib.h"

// Wireshark filter:
// usb.dst == "1.9.0" || usb.src == "1.9.0"

#define INTERFACE_TIMESTAMP  0x00 // Service interface which appends timestamps to all received events on associated interfaces.
#define INTERFACE_SPI        0x20 // Communicates directly over SPI in Slave mode.
#define INTERFACE_USART      0x21 // Communicates directly over USART in Slave mode.
#define INTERFACE_I2C        0x22 // Communicates directly over I2C in Slave mode.
#define INTERFACE_GPIO       0x30 // Monitors and controls the state of GPIO pins.
#define INTERFACE_POWER_DATA 0x40 // Receives data from the attached power measurement co-processors.
#define INTERFACE_POWER_SYNC 0x41 // Receives sync events from the attached power measurement co-processors.
#define INTERFACE_RESERVED   0xFF // Special identifier used to indicate no interface.

#define NUM_INTERFACES 10
#define NUM_CONFIG_IDS 10
#define BUFFER_SIZE 10000000

int main()
{
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
    power_handle_t power_hndl;

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

    unsigned char interfaces[NUM_INTERFACES] = {'\0'};
    unsigned char interfaceCount;
    res = interface_list(dgi_hndl, interfaces, &interfaceCount);
    printf("%d interface_list:", res);
    for (unsigned char i = 0; i < NUM_INTERFACES; ++i)
        printf(" 0x%.2x", interfaces[i]);
    printf(", interfaceCount: %d\n", interfaceCount);

    //int interface_id = INTERFACE_POWER_DATA;
    int interface_id = INTERFACE_GPIO;
    bool enableTimestamp = true;
    res = interface_enable(dgi_hndl, interface_id, enableTimestamp);
    printf("%d interface_enable: 0x%.2x, enableTimestamp: %d\n", res, interface_id, enableTimestamp);

    unsigned int config_id[NUM_CONFIG_IDS];
    unsigned int config_value[NUM_CONFIG_IDS];
    unsigned int config_cnt;
    for (unsigned char i = 0; i < NUM_CONFIG_IDS; ++i) {
        config_id[i] = 0;
        config_value[i] = 0;
    }
    res = interface_get_configuration(dgi_hndl, interface_id, config_id, config_value, &config_cnt);
    printf("%d interface_get_configuration: 0x%.2x, config_cnt: %d\n", res, interface_id, config_cnt);
    for (unsigned char i = 0; i < config_cnt; ++i) {
        printf("\tconfig_id: %u, value: %u\n", config_id[i], config_value[i]);
    }

    config_value[0] = 0b0011;
    config_value[1] = 0b1100;
    res = interface_set_configuration(dgi_hndl, interface_id, config_id, config_value, config_cnt);
    printf("%d interface_set_configuration: 0x%.2x, config_cnt: %d\n", res, interface_id, config_cnt);
    for (unsigned char i = 0; i < config_cnt; ++i) {
        printf("\tconfig_id: %u, value: %u\n", config_id[i], config_value[i]);
    }

    res = interface_clear_buffer(dgi_hndl, interface_id);
    printf("%d interface_clear_buffer: 0x%.2x\n", res, interface_id);

    res = start_polling(dgi_hndl);
    printf("%d start_polling\n", res);

    unsigned char *readBuffer = malloc(sizeof(unsigned char)*BUFFER_SIZE);
    unsigned long long* timestamp = malloc(sizeof(unsigned long long)*BUFFER_SIZE);
    int length = 0;
    unsigned int ovf_index = 0;
    unsigned int ovf_length = 0;
    unsigned int ovf_entry_count = 0;
    res = interface_read_data(dgi_hndl, interface_id, readBuffer, timestamp, &length, &ovf_index, &ovf_length, &ovf_entry_count);
    printf("%d interface_read_data: 0x%.2x, length: %d, ovf_index: %u, ovf_length: %u, ovf_entry_count: %u\n", res, interface_id, length, ovf_index, ovf_length, ovf_entry_count);
    for (unsigned char i = 0; i < length; ++i) {
        printf("\t%.6d: buffer: %.4u, timestamp: %.4llu\n", i, readBuffer[i], timestamp[i]);
    }

//    unsigned char* buffer = malloc(sizeof(unsigned char)*255);
    unsigned char* writeBuffer[2] = {'\0'};
    int* writeLength = 2;
    res = interface_write_data(dgi_hndl, interface_id, writeBuffer, &writeLength);
    printf("%d interface_write_data: 0x%.2x, length: %d\n", res, interface_id, writeLength);

    res = interface_read_data(dgi_hndl, interface_id, readBuffer, timestamp, &length, &ovf_index, &ovf_length, &ovf_entry_count);
    printf("%d interface_read_data: 0x%.2x, length: %d, ovf_index: %u, ovf_length: %u, ovf_entry_count: %u\n", res, interface_id, length, ovf_index, ovf_length, ovf_entry_count);
    for (unsigned char i = 0; i < length; ++i) {
        printf("\t %.6d: buffer: %.4u, timestamp: %.4llu\n", i, readBuffer[i], timestamp[i]);
    }

    res = auxiliary_power_initialize(&power_hndl, dgi_hndl);
    printf("%d auxiliary_power_initialize\n", res);

    float* powerBuffer;
    double* powerTimestamp;
    size_t powerCount;
    size_t max_count = 256;
    int channel = 0;
    int powerType = 0;
    res = auxiliary_power_register_buffer_pointers(power_hndl, powerBuffer, powerTimestamp, &powerCount, max_count, channel, powerType);
    printf("%d auxiliary_power_register_buffer_pointers\n", res);

    res = auxiliary_power_calibration_is_valid(power_hndl);
    printf("%d auxiliary_power_calibration_is_valid\n", res);

    int calibrationType = 0;
    res = auxiliary_power_trigger_calibration(power_hndl, calibrationType);
    printf("%d auxiliary_power_trigger_calibration\n", res);

    uint8_t* calibrationData = malloc(sizeof(uint8_t)*16);;
    size_t calibrationLength = 16;
    res = auxiliary_power_get_calibration(power_hndl, calibrationData, calibrationLength);
    printf("%d auxiliary_power_get_calibration\n", res);

    int circuit;
    res = auxiliary_power_get_circuit_type(power_hndl, &circuit);
    printf("%d auxiliary_power_get_circuit_type: 0x%.2x\n", res, circuit);

    int powerStatus = auxiliary_power_get_status(power_hndl);
    printf("power_status: 0x%.2x\n", powerStatus);

//    int auxiliary_power_start(uint32_t power_hndl, int mode, int parameter)
//    int auxiliary_power_stop(uint32_t power_hndl)
//    int auxiliary_power_lock_data_for_reading(uint32_t power_hndl)
//    int auxiliary_power_copy_data(uint32_t power_hndl, float* buffer, double* timestamp, size_t* count, size_t max_count, int channel, int type)
//    int auxiliary_power_free_data(uint32_t power_hndl)

    res = auxiliary_power_unregister_buffer_pointers(power_hndl, channel, powerType);
    printf("%d auxiliary_power_unregister_buffer_pointers\n", res);

    res = auxiliary_power_uninitialize(power_hndl);
    printf("%d auxiliary_power_uninitialize\n", res);

    res = stop_polling(dgi_hndl);
    printf("%d stop_polling\n", res);

    res = interface_disable(dgi_hndl, interface_id);
    printf("%d interface_disable: 0x%.2x\n", res, interface_id);

    res = disconnect(dgi_hndl);
    printf("%d disconnect\n", res);
    c_status = connection_status(dgi_hndl);
    printf("connection_status: 0x%.2x\n", c_status);

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
