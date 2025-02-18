from websockets import Subprotocol
from websockets.sync.client import connect
from urllib.parse import urlencode
from datetime import timedelta, datetime

from typing import Dict, List

class ISSDataStream:
    """
    A simple no-frills Lightstream client that connects to a public lightstreamer instance
    where NASA is pushing telemetry from the ISS.
    
    based on: https://lightstreamer.com/sdks/ls-generic-client/2.3.0/TLCP%20Specifications.pdf
    and: https://github.com/Lightstreamer/Lightstreamer-example-ISSLive-client-javascript
    """

    SERVER = "wss://push.lightstreamer.com/lightstreamer"
    ADAPTER_SET = "ISSLIVE"
    THIRD_PARTY_MAGIC_CID = "mgQkwtwdysogQz2BJ4Ji%20kOj2Bg"
        
    def __init__(self, initial_subscriptions: List[str] | None = None):
        self.ws = connect(self.SERVER, subprotocols=[Subprotocol("TLCP-2.3.0.lightstreamer.com")])

        self._lightstreamer_request("wsok", {})
        
        self._lightstreamer_request("create_session", {
            "LS_adapter_set": self.ADAPTER_SET,
            "LS_cid": self.THIRD_PARTY_MAGIC_CID,
            "LS_send_sync": "false",
            "LS_cause": "api"
        })

        self.sub_id = 1
        
        self.subscription_group_map: Dict[int, str] = {}
        
        if initial_subscriptions is not None:            
            for group in initial_subscriptions:
                self.subscribe(group)
        
        while True:
            # Type safety: decode=True forces str as a return type
            blob: str = self.ws.recv(decode=True) # type: ignore
            
            for msg in blob.splitlines():               
                if not msg.startswith("U"):
                    continue
                
                _, subscription_id, _, fields = msg.split(",")
                group = self.subscription_group_map[int(subscription_id)]
                timestamp, value = fields.split("|")
                
                print (datetime(2025, 1, 1, 0, 0, 0) + timedelta(hours=float(timestamp) - 24))
                
                
    def subscribe(self, group: str):
        self._lightstreamer_request("control", {
            "LS_reqId": "1",
            "LS_op": "add",
            "LS_subId": str(self.sub_id),
            "LS_mode": "MERGE",
            "LS_group": group,
            "LS_schema": "TimeStamp Value",
            "LS_snapshot": "true",
            "LS_requested_max_frequency": "unlimited",
            "LS_ack": "false"
        })
        
        self.subscription_group_map[self.sub_id] = group
        self.sub_id += 1
            
    
    def _lightstreamer_request(self, method: str, data: Dict[str, str]):
        d = f"{method}\r\n{urlencode(data)}"
        self.ws.send(d)


if __name__ == "__main__":
    ISSDataStream(["TIME_000001", "S0000005"])