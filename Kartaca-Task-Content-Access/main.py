import json
import websocket
import string

trans = str.maketrans(
    string.ascii_lowercase + string.ascii_uppercase,
    string.ascii_lowercase[::-1] + string.ascii_uppercase[::-1]
)


def atbash_decipher(encrypted_message):
    return encrypted_message.translate(trans)


def on_message(ws, message):
    print(message)

    if "ivtrhgizgrlmKvb" in message:
        registration_key = message.split("ivtrhgizgrlmKvb : ")[1].strip('}"')
        data = {
            "type": "REGISTER",
            "name": "Omer",
            "surname": "Yavuz",
            "email": "omer.yvz@protonmail.com",
            "registrationKey": atbash_decipher(registration_key)
        }
        ws.send(json.dumps(data))


def on_error(_, error):
    print(error)


def on_close(_):
    print("Connection closed")


def on_open(_):
    print("Connection opened")


def main():
    websocket.enableTrace(True)

    ws = websocket.WebSocketApp("wss://cekirdektenyetisenler.kartaca.com/ws",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)

    ws.on_open = on_open
    ws.run_forever()


if __name__ == "__main__":
    main()
