import paho.mqtt.subscribe as subscribe
print("subscribe mqtt active")
def on_message_print(client, userdata, message):
    print("%s %s" % (message.topic, message.payload))
    if userdata["message_count"] >= 5:
        # it's possible to stop the program by disconnecting
        client.disconnect()

subscribe.callback(on_message_print, "paho/test/topic", hostname="74.234.16.173", userdata={"message_count": 0})