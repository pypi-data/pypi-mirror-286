from gemnify_sdk.scripts.instance import ContractInstance
from gemnify_sdk.scripts.http import HTTP
from gemnify_sdk.scripts.contracts.order import Order

class MarketOrder(Order):
    def __init__(self, config) -> None:
        super().__init__(config)
        self.config = config
        self.instance = ContractInstance(config, 'PositionRouter')

    def create_increase_position(self, *args, value):
        return self.instance.create_transaction("createIncreasePosition", args, value)

    def create_decrease_position(self, *args, value):
        return self.instance.create_transaction("createDecreasePosition", args, value)

    def get_min_execution_fee(self):
        return self.instance.call_function("minExecutionFee")

    def get_position(self, *args):
        instance = ContractInstance(self.config, 'Vault')
        result = instance.call_function("getPosition", args)
        if isinstance(result, tuple) and len(result) == 9:
            keys = [
                "size",
                "collateral",
                "average_price",
                "entry_borrowing_rate",
                "funding_fee_amount_per_size",
                "claimable_funding_amount_per_size",
                "reserve_amount",
                "realised_pnl",
                "last_increased_time"
            ]
            return dict(zip(keys, result))
        else:
            raise ValueError("Unexpected result format or length")

    def get_position_info(self, market, user, tx_hash):
        http = HTTP(self.config)
        info = http.post(
            "getPositionsByAccountAndMarket",
            payload={
                "market": market,
                'account': user,
                "status": 20000
            }
        )
        print(info)

    def check_position_status(self):
        pass
    #
    # def get_order_index(self, tx_hash):
    #     order = self.get_order_info(tx_hash)
    #     return order["id"]
    #
    # def get_order_status(self, tx_hash):
    #     order = self.get_order_info(tx_hash)
    #     return order["status"]
