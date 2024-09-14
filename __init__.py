from .unmasked import GetMaskDimensions, isMaskEmpty, GetRandomDimensions

# Node class mappings
NODE_CLASS_MAPPINGS = {
    "GetMaskDimensions": GetMaskDimensions,
    "isMaskEmpty": isMaskEmpty,
    "GetRandomDimensions": GetRandomDimensions
}

# Node display name mappings
NODE_DISPLAY_NAME_MAPPINGS = {
    "GetMaskDimensions": "Get Mask Dimensions",
    "isMaskEmpty": "Is Mask Empty",
    "GetRandomDimensions": "Get Random Dimensions"
}

WEB_DIRECTORY = "./web"
__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]