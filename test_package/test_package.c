#include "azure_umqtt_c/mqtt_client.h"

int main(void) {
		static const uint8_t TEST_PACKET_ID = (uint8_t)0x12;
		static const char* TEST_TOPIC_NAME = "topic Name";
		static const char* TEST_SUBSCRIPTION_TOPIC = "subTopic";
		static const uint8_t* TEST_MESSAGE = (const uint8_t*)"Message to send";
		static const int TEST_MSG_LEN = sizeof(TEST_MESSAGE)/sizeof(TEST_MESSAGE[0]);

		MQTT_MESSAGE_HANDLE handle = mqttmessage_create(TEST_PACKET_ID, TEST_TOPIC_NAME, DELIVER_AT_LEAST_ONCE, TEST_MESSAGE, TEST_MSG_LEN);
    return 0;
}
