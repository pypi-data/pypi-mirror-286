from typing import Optional

from anyscale_client.models.fine_tuned_model import FineTunedModel

from anyscale.cli_logger import BlockLogger
from anyscale.controllers.base_controller import BaseController


class ModelsController(BaseController):
    def __init__(
        self, log: Optional[BlockLogger] = None, initialize_auth_api_client: bool = True
    ):
        if log is None:
            log = BlockLogger()

        super().__init__(initialize_auth_api_client=initialize_auth_api_client)

        self.log = log
        self.log.open_block("Output")

    def retrieve_model(self, model_id: str) -> FineTunedModel:
        return self.anyscale_api_client.get_model(model_id)
