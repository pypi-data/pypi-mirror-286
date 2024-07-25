from fetchfox.apis.evm import openseaio
from fetchfox.blockchains.evm import Evm
from fetchfox.constants.blockchains import POLYGON
from fetchfox.constants.currencies import MATIC


class Polygon(Evm):
    def __init__(
        self,
        moralisio_api_key: str = None,
        openseaio_api_key: str = None,
        preprod: bool = False,
    ):
        super().__init__(
            name=POLYGON,
            currency=MATIC,
            logo="https://s2.coinmarketcap.com/static/img/coins/64x64/3890.png",
            moralisio_api_key=moralisio_api_key,
            openseaio_api_key=openseaio_api_key,
            preprod=preprod,
        )

    def explorer_url(self, *, address: str = None, collection_id: str = None, asset_id: str = None, tx_hash: str = None) -> str:
        if self.preprod:
            polygonscan_domain = "https://amoy.polygonscan.com"
        else:
            polygonscan_domain = "https://polygonscan.com"

        if address:
            return f"{polygonscan_domain}/address/{address.lower()}"

        if asset_id:
            assert collection_id
            return f"{polygonscan_domain}/token/{collection_id.lower()}?a={asset_id}"

        if collection_id:
            return f"{polygonscan_domain}/token/{collection_id.lower()}"

        if tx_hash:
            return f"{polygonscan_domain}/tx/{tx_hash.lower()}"

        return None

    def marketplace_url(self, *, collection_id: str = None, asset_id: str = None) -> str:
        if asset_id:
            assert collection_id
            return f"https://opensea.io/assets/matic/{collection_id.lower()}/{asset_id}"

        if collection_id:
            slug = openseaio.get_collection_slug(
                contract_address=collection_id,
                blockchain=self.name,
                api_key=self.openseaio_api_key,
            )

            return f"https://opensea.io/collection/{slug}"

        return None
