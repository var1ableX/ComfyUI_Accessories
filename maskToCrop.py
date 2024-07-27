import torch

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

