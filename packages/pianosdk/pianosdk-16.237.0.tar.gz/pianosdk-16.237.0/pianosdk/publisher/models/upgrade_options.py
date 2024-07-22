from datetime import date, datetime
from pydantic.main import BaseModel
from typing import Optional
from pianosdk.publisher.models.show_option_in_channel_details import ShowOptionInChannelDetails
from pianosdk.publisher.models.upgrade_option import UpgradeOption
from typing import List


class UpgradeOptions(BaseModel):
    upgrade_options: Optional['List[UpgradeOption]'] = None
    show_option_in_details: Optional['List[ShowOptionInChannelDetails]'] = None


UpgradeOptions.model_rebuild()
