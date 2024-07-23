from typing import List


class TransactionAssetDTO:
    def __init__(self, amount: float, unit: str):
        self.amount: float = amount
        self.unit: str = unit


class TransactionInputDTO:
    def __init__(self, address: str, assets: List[TransactionAssetDTO]):
        self.address: str = address
        self.assets: List[TransactionAssetDTO] = assets


class TransactionOutputDTO:
    def __init__(self, address: str, assets: List[TransactionAssetDTO]):
        self.address: str = address
        self.assets: List[TransactionAssetDTO] = assets


class TransactionDTO:
    def __init__(
        self,
        blockchain: str,
        address: str,
        tx_hash: str,
        inputs: List[TransactionInputDTO],
        outputs: List[TransactionOutputDTO],
        message: str = None,
    ):
        self.blockchain: str = blockchain
        self.address: str = address
        self.tx_hash: str = tx_hash
        self.inputs: List[TransactionInputDTO] = inputs
        self.outputs: List[TransactionOutputDTO] = outputs
        self.message: str = message

    def __repr__(self) -> str:
        if not self.message:
            return self.tx_hash

        return f"{self.tx_hash} / {self.message}"
