import torch
import numbers

class GetMaskDimensions:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "mask": ("MASK",),
            }
        }

    RETURN_TYPES = ("INT", "INT", "INT", "INT",)
    RETURN_NAMES = ("width", "height", "x", "y",)
    FUNCTION = "execute"
    CATEGORY = "image"

    def execute(self, mask):
        def get_mask_dimensions(mask):
            # Assuming mask_tensor is of shape (1, H, W)
            mask_array = mask[0]

            # Find all coordinates where the mask is non-zero
            coordinates = torch.nonzero(mask_array, as_tuple=False)

            if coordinates.numel() == 0:
                # If there are no non-zero coordinates, return a zero-sized rectangle
                return 0, 0, 0, 0

            # Get the minimum and maximum x and y coordinates
            min_coords = torch.min(coordinates, dim=0)[0]
            max_coords = torch.max(coordinates, dim=0)[0]

            # Extract bounding box coordinates
            top_left_x = min_coords[1].item()
            top_left_y = min_coords[0].item()
            bottom_right_x = max_coords[1].item()
            bottom_right_y = max_coords[0].item()

            # Calculate width and height
            width = bottom_right_x - top_left_x + 1
            height = bottom_right_y - top_left_y + 1

            return width, height, top_left_x, top_left_y

        # Process the mask tensor to find cropping dimensions
        width, height, top_left_x, top_left_y = get_mask_dimensions(mask)

        # Return the results as node outputs
        return width, height, top_left_x, top_left_y
    
class isMaskEmpty:
  def __init__(self):
      pass
  
  @classmethod
  def INPUT_TYPES(s):
      return {
          "required": {
              "mask": ("MASK",),
          }
      }

  RETURN_TYPES = ("BOOLEAN",)
  RETURN_NAMES = ("boolean",)
  FUNCTION = "execute"
  CATEGORY = "image"

  def execute(self, mask):
      def is_mask_empty(mask):
        return not torch.any(mask == 1).item()

      isEmpty = is_mask_empty(mask)
      return (isEmpty,)  # Return the boolean value as a tuple
  
class isImageEmpty:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),  # IMAGE type is specific to ComfyUI inputs
            }
        }

    RETURN_TYPES = ("BOOLEAN",)  # Return type expected by ComfyUI
    RETURN_NAMES = ("is_empty",)  # Name of the returned value
    FUNCTION = "execute"
    CATEGORY = "accessories"  # Adjusted as per your request

    def execute(self, image):
        """
        Check if the image is completely black (all pixel values are zero).
        Assumes the image is a torch tensor in CHW format.
        """
        import torch  # Ensure torch is imported within the function's scope

        if not isinstance(image, torch.Tensor):
            raise TypeError("The input 'image' must be a torch.Tensor.")

        # Check if all pixel values in the tensor are zero
        is_empty = torch.all(image == 0.0).item()

        return (is_empty,)  # Return a tuple as required by ComfyUI


import random

class GetRandomDimensions:
    def __init__(self):
        self.is_changed_enabled = True

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "min_width": ("INT", {"default": 768, "step": 16, "display": "number"}),
                "min_height": ("INT", {"default": 768, "step": 16, "display": "number"}),
                "max_width": ("INT", {"default": 1280, "step": 16, "display": "number"}),
                "max_height": ("INT", {"default": 1280, "step": 16, "display": "number"}),
                "randomize": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ("INT", "INT")
    RETURN_NAMES = ("width", "height",)
    FUNCTION = "execute"
    CATEGORY = "image"
    OUTPUT_NODE = True

    def execute(self, min_width, min_height, max_width, max_height, randomize   ):
        def get_random_dimensions(min_val, max_val):
            min_div_16 = min_val // 16
            max_div_16 = max_val // 16
            if min_div_16 > max_div_16:
                raise ValueError("No numbers in the specified range are divisible by 16.")
            return random.randint(min_div_16, max_div_16) * 16

        if randomize:
            width = get_random_dimensions(min_width, max_width)
            height = get_random_dimensions(min_height, max_height)
        else:
            width, height = max_width, max_height
        
        # Setting the resolution string
        text = f"{width}x{height}"
        #return width, height
        return {"ui": {"text": text},
                "result": (width, height, text)}

# wildcard trick is taken from pythongossss's
class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False

ANY_TYPE = AnyType("*")

def try_cast(x, dst_type: str):
    result = x
    if dst_type == "STRING":
        result = str(x)
    elif dst_type == "INT":
        result = int(x)
    elif dst_type == "FLOAT" or dst_type == "NUMBER":
        result = float(x)
    elif dst_type == "BOOLEAN":
        if isinstance(x, numbers.Number):
            if x > 0:
                result = True
            else:
                result = False
        elif isinstance(x, str):
            try:
                x = float(x)
                if x > 0:
                    result = True
                else:
                    result = False
            except:
                result = bool(x)
        else:
            result = bool(x)
    return result


class AnyCast:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(self):
        return {
            "required": {
                "ANY" : (ANY_TYPE, {}),
                "TYPE": (["*", "STRING", "INT", "FLOAT", "BOOLEAN", "IMAGE", "LATENT", "MASK", "NOISE", "SAMPLER", "SIGMAS", "GUIDER", "MODEL", "CLIP", "VAE", "CONDITIONING"], {}),
            },
        }
    
    TITLE = "Any Cast"
    RETURN_TYPES = (ANY_TYPE, )
    FUNCTION = "run"
    CATEGORY = "Accessories"

    def run(self, ANY, TYPE):
        result = try_cast(ANY, TYPE)
        return (result, )