#include <Arduino.h>
#include <unity.h>

#include "data_utils.h"


void test_crc32_ascii_A(void) {
    TEST_ASSERT_EQUAL_UINT32(0xD3D99E8B, crc32_ascii("A"));
}


void test_crc32_ascii2_TEST(void) {
    TEST_ASSERT_EQUAL_UINT32(0xEEEA93B8, crc32_ascii("TEST"));
}


void test_crc32_ascii_g420pfSDAa(void) {
    TEST_ASSERT_EQUAL_UINT32(0xAC4B3205, crc32_ascii("g420pfSDAa"));
}


void test_crc32_ascii_null(void) {
    TEST_ASSERT_EQUAL_UINT32(0x00000000, crc32_ascii("\x00"));
}


void test_crc32_bytes_update(void) {
    uint32_t crc = 0;
    uint32_t buffer[4] = {0x56789ABC, 0xAAADFB44, 0x12345678, 0xABCDEF12};

    crc = crc32_bytes_update(crc, buffer, sizeof(uint32_t)*4);
    TEST_ASSERT_EQUAL_UINT32(0x92E18E18, crc);
}


void test_crc32_bytes_update_multiple(void) {
    uint32_t crc = 0;
    uint32_t buffer1[1] = {0x56789ABC};
    uint32_t buffer2[1] = {0xAAADFB44};
    uint32_t buffer3[1] = {0x12345678};
    uint32_t buffer4[1] = {0xABCDEF12};

    crc = crc32_bytes_update(crc, buffer1, sizeof(uint32_t)*1);
    crc = crc32_bytes_update(crc, buffer2, sizeof(uint32_t)*1);
    crc = crc32_bytes_update(crc, buffer3, sizeof(uint32_t)*1);
    crc = crc32_bytes_update(crc, buffer4, sizeof(uint32_t)*1);

    TEST_ASSERT_EQUAL_UINT32(0x92E18E18, crc);
}


void test_crc32_bytes_update_string(void) {
    uint32_t crc = 0;

    crc = crc32_bytes_update(crc, (void*)"This is 27 characters long.", sizeof(char)*27);
    TEST_ASSERT_EQUAL_UINT32(0xC47213D1, crc);
}


void setup() {
    delay(2000);

    UNITY_BEGIN();

    RUN_TEST(test_crc32_ascii_A);
    RUN_TEST(test_crc32_ascii2_TEST);
    RUN_TEST(test_crc32_ascii_g420pfSDAa);
    RUN_TEST(test_crc32_ascii_null);

    RUN_TEST(test_crc32_bytes_update);
    RUN_TEST(test_crc32_bytes_update_multiple);
    RUN_TEST(test_crc32_bytes_update_string);

    UNITY_END();
}


void loop() {
    
}