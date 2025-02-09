from .unmasked import GetMaskDimensions, isMaskEmpty, GetRandomDimensions, AnyCast, isImageEmpty, AccMakeListNode

# Node class mappings
NODE_CLASS_MAPPINGS = {
    "GetMaskDimensions": GetMaskDimensions,
    "isMaskEmpty": isMaskEmpty,
    "GetRandomDimensions": GetRandomDimensions,
    "ACC_AnyCast": AnyCast,
    "isImageEmpty": isImageEmpty,
    "AccMakeListNode": AccMakeListNode
}

# Node display name mappings
NODE_DISPLAY_NAME_MAPPINGS = {
    "GetMaskDimensions": "Get Mask Dimensions",
    "isMaskEmpty": "Is Mask Empty",
    "GetRandomDimensions": "Get Random Dimensions",
    "ACC_AnyCast": "Any Cast",
    "isImageEmpty": "Is Image Empty",
    "AccMakeListNode": "Make List From Text",
}

WEB_DIRECTORY = "./web"
__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]