import os.path

from rotarysaw.basic import *

try:
    import paho.mqtt.client as mqtt
except ModuleNotFoundError:
    log.error("Module not found: pip3 install paho-mqtt")
    sys.exit(1)


def utf2str(x):
    if isinstance(x, bytes):
        return x.decode('utf8')
    if isinstance(x, str):
        return x
    raise Exception(f"What did you feed me? {x}")

class NoAuthentication(Exception):
    pass

CertKey = namedtuple('CertKey', ['certificate', 'key'])
class SimpleMQTT(mqtt.Client):
    def __init__(self, utf8=True, authentication=True, certfile=None, username=None, password=None, initial_subscriptions=None, aggressive_certificate=True):
        super().__init__(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)


        if username is not None:
            if password is None:
                log.warning("Username set but password blank")
            self.username_pw_set(username, password)

        self.ca = os.path.dirname(os.path.abspath(__file__)) + os.sep + 'ca.crt'
        if not os.path.exists(self.ca):
            raise FileNotFoundError(f"{self.ca} is missing")

        self.authentication = authentication
        self.certfile = certfile
        self.keyfile = certfile


        self.on_connect = self.connect_handler
        self.on_message = self.message_handler
        self.on_disconnect = self.disconnect_handler
        self.payload2utf8 = utf8
        self.listeners = []

        self.initial_subscriptions = ['brokers']
        if initial_subscriptions is not None:
            self.initial_subscriptions += initial_subscriptions

        if aggressive_certificate:
            if certfile is None or not os.path.exists(self.certfile):
                cand = self.find_certificate()
                if cand is not None:
                    self.certfile = cand.certificate
                    self.keyfile = cand.key

        if self.authentication and ((not self.certfile or not os.path.exists(self.certfile)) and (self.username is None or self.password is None)):
            raise NoAuthentication("No certificate or credentials.")

        self.loop_start()

    def connect(self, hostname='mqtt.uraanikaivos.com'):
        if not self.certfile or not os.path.exists(self.certfile):
            if self.certfile is not None:
                log.warning(f"{self.certfile} missing for MQTT")

            self.certfile = None
            self.tls_set(self.ca, cert_reqs=True)
            self.connect_async(hostname, 3883, 60)
        else:
            self.tls_set(self.ca, self.certfile, self.keyfile, cert_reqs=True)
            self.connect_async(hostname, 8883, 60)

    def find_certificate(self) -> CertKey:
        from operator import iconcat
        ext = ['crt','cer','pem','key','PEM']
        files = reduce(iconcat, [glob(f'*.{t}') for t in ext], [])
        certificate = key = None
        for x in files:
            if re.match(r'ca\.', x, re.I):
                continue
            with open(x, 'r', encoding='utf8') as f:
                text = f.read()

            if search(r'BEGIN CERTIFICATE', text):
                certificate = x

            if search(r'PRIVATE KEY', text):
                # Contains a private key
                key = x

            if certificate and key:
                break

        if certificate and key:
            ret = CertKey(certificate, key)
            log.debug(f"Aggressive find found certificate: {repr(ret)}")
            return ret

        return None

    def qobject(self):
        if hasattr(self, '_qobj'):
            return self._qobj

        from PyQt6.QtCore import QObject, pyqtSignal

        class Signaler(QObject):
            receive = pyqtSignal(str, str)

            def __init__(self, parent):
                super().__init__(parent=None)
                super().__setattr__('parent', parent)

            def forward(self, msg):
                self.receive.emit(msg.topic, msg.payload)

            def __getattr__(self, item):
                return getattr(self.parent, item)

            def __setattr__(self, key, value):
                setattr(self.parent,key, value)

        self._qobj = Signaler(self)

        return self._qobj


    def register(self, topic, fn):
        self.listeners.append((topic, fn))

    def register_only_payload(self, topic, fn):
        self.register(topic, lambda msg: fn(msg.payload))

    def disconnect_handler(self, client, userdata, disconnect_flag, reason_code, properties):
        log.warning(f"MQTT disconnected: {reason_code}")
        while True:
            try:
                self.reconnect()
            except Exception as ex:
                log.debug(f"Disconnect_handler->reconnect handler exception {repr(ex)}")
                sleep(0.5)
            else:
                break

    def connect_handler(self, client, userdata, flags, reason_code, properties):
        log.debug(f"Connected with status {reason_code}")
        if reason_code == mqtt.MQTT_ERR_SUCCESS:
            for s in self.initial_subscriptions:
                self.subscribe(s)

    def message_handler(self, client, userdata, msg):
        if self.payload2utf8:
            msg.payload = msg.payload.decode('utf8')

        if hasattr(self,'_qobj'):
            self._qobj.forward(msg)

        if hasattr(self, 'debug'):
            log.debug(f"{msg.topic} {msg.payload}")

        for t, fn in self.listeners:
            try:
                if msg.topic[0:len(t)] == t:
                    fn(msg)
            except IndexError as ex:
                log.error(repr(ex))


class GenericDebug():
    def __init__(self, key, mq=None):
        connect_last = False
        self.mq = mq
        self.key = key

        if self.mq is None:
            self.mq = SimpleMQTT()
            connect_last = True

        self.mq.initial_subscriptions.append(key)

        if self.mq.is_connected():
            self.mq.subscribe(key)

        self.mq.register(key, self.handler)

        if connect_last:
            self.mq.connect()

    def handler(self, msg):
        pass


class Button(GenericDebug):
    def __init__(self, index=0, mq=None):
        self.index = index
        key = f'debug/button/{index}'
        super().__init__(key, mq)

    def pressed(self):
        log.debug(f"Button {self.index} pressed")

    def handler(self, msg):
        self.pressed()


class Slider(GenericDebug):
    def __init__(self, index=0, mq=None):
        self.index = index
        key = f'debug/slider/{index}'
        super().__init__(key, mq)
        self._value = None


    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        self.mq.publish(self.key, str(v), retain=True)
        #self._value = v

    def handler(self, msg):
        try:
            self._value = int(msg.payload)
            self.change(self.value)
        except ValueError:
            log.debug("Slider change cannot convert value")

    def change(self, val:int):
        log.debug(f"Slider changed to {val}")


if __name__ == '__main__':

    log.getLogger().setLevel(log.DEBUG)

    b = Button()
    sld = Slider()
    while True:
        if sld.value is not None:
            sld.value += 1
        sleep(1)

    sys.exit(0)

    s = SimpleMQTT()
    s.connect()

    s.register_only_payload('debug/kraut', lambda msg: print(msg))

    q = s.qobject()
    q.publish('debug/kraut','testi',qos=2)

    while True:
        q.publish('debug/kraut', 'testi')
        s.publish('debug/kraut','moi')
        sleep(1)
