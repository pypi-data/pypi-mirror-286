from gemnify_sdk.scripts.http import HTTP
import time
class Order:
    def __init__(self, config) -> None:
        self.config = config

    def get_order_info(self, tx_hash):
        http = HTTP(self.config)
        start_time = time.time()

        while time.time() - start_time < 60:
            order = http.post(
                "getOrderByTx",
                payload={
                    'tx': tx_hash
                }
            )
            if order:
                return order
            time.sleep(0.5)
        raise RuntimeError("Order not found")

    def get_order_index_by_hash(self, tx_hash):
        order = self.get_order_info(tx_hash)
        if order:
            return order["order_index"]

    def check_order_status(self, tx_hash):
        order = self.get_order_info(tx_hash)
        if order:
            switch = {
                10000: "OrderReceived",
                10001: "OrderWaitingBlockConfirm",
                10002: "OrderConfirmed",
                10011: "OrderRejectedByKeeper",
                10012: "OrderRejectedByUser",
                10013: "OrderCanceledByContract"
            }
            return switch.get(order["status"], str(order["status"]))

