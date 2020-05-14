#include <Arduino.h>
#include <unity.h>

#include "data_utils.h"


void test_crc32_ascii_A(void) {
    TEST_ASSERT_EQUAL(0xD3D99E8B, crc32_ascii("A"));
}

void test_crc32_ascii2_TEST(void) {
    TEST_ASSERT_EQUAL(0xEEEA93B8, crc32_ascii("TEST"));
}

void test_crc32_ascii_g420pfSDAa(void) {
    TEST_ASSERT_EQUAL(0xAC4B3205, crc32_ascii("g420pfSDAa"));
}

void test_crc32_ascii_null(void) {
    TEST_ASSERT_EQUAL(0x00000000, crc32_ascii("\x00"));
}

void setup() {
    delay(2000);

    UNITY_BEGIN();

    RUN_TEST(test_crc32_ascii_A);
    RUN_TEST(test_crc32_ascii2_TEST);
    RUN_TEST(test_crc32_ascii_g420pfSDAa);
    RUN_TEST(test_crc32_ascii_null);

    UNITY_END();
}


void loop() {
    
}