import os

from atorch.common.singleton import SingletonMeta


class EnvSetting(metaclass=SingletonMeta):
    # TODO: config the num in moe module which is more comprehensive
    MOE_FSDP_PREFETCH_NUM = int(os.getenv("MOE_FSDP_PREFETCH_NUM", 1))
    DISABLE_CHECKPOINT_PATCH = bool(os.getenv("ATORCH_DISABLE_CHECKPOINT_PATCH", False))
