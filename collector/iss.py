from websockets.sync.client import connect
from urllib.parse import urlencode

from typing import Dict

class ISSDataStream:
    SERVER = "wss://push.lightstreamer.com/lightstreamer"
    ADAPTER_SET = "ISSLIVE"
    THIRD_PARTY_MAGIC_CID = "mgQkwtwdysogQz2BJ4Ji%20kOj2Bg"
    
    
    def __init__(self):
        self.ws = connect(self.SERVER, subprotocols=["TLCP-2.3.0.lightstreamer.com"])        

        self._lightstreamer_request("wsok", {})
        
        self._lightstreamer_request("create_session", {
            "LS_adapter_set": self.ADAPTER_SET,
            "LS_cid": self.THIRD_PARTY_MAGIC_CID,
            "LS_send_sync": "false",
            "LS_cause": "api"
        })

        self._lightstreamer_request("control", {
            "LS_reqId": "1",
            "LS_op": "add",
            "LS_subId": "1",
            "LS_mode": "MERGE",
            "LS_group": "USLAB000059",
            "LS_schema": "TimeStamp Value",
            "LS_snapshot": "true",
            "LS_requested_max_frequency": "unlimited",
            "LS_ack": "false"
        })
        
        while True:
            blob = self.ws.recv()
            for msg in blob.splitlines():               
                if not msg.startswith("U"):
                    continue
                
                _, subcription_id, item_id, fields = msg.split(",")
                print (item_id, fields)
            
    
    def _lightstreamer_request(self, method: str, data: Dict[str, str]):
        d = f"{method}\r\n{urlencode(data)}"
        self.ws.send(d)


    

if __name__ == "__main__":
    ISSDataStream()