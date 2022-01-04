from effect import Effect
import numpy as np

# a function to convert a numpy array from any format to a float32 format
def convert_to_float32(data: np.ndarray) -> np.ndarray:
    if data.dtype == np.int16:
        return np.float32(data) / 32768.0
    elif data.dtype == np.int32:
        return np.float32(data) / 2147483648.0
    elif data.dtype == np.float32:
        return data
    elif data.dtype == np.float64:
        return np.float32(data) / float(np.iinfo(np.int32).max)
    else:
        raise TypeError(f"Unsupported data type: {data.dtype}")

# a function to convert a numpy array from any format to a int16 format
def convert_to_int16(data: np.ndarray) -> np.ndarray:
    if data.dtype == np.int16:
        return data
    elif data.dtype == np.int32:
        return np.int16(data >> 16)
    elif data.dtype == np.float32:
        return np.int16(data * 32767.0)
    elif data.dtype == np.float64:
        return np.int16(data * 32767.0)
    else:
        raise TypeError(f"Unsupported data type: {data.dtype}")

# a function to convert a numpy array from any format to a int32 format
def convert_to_int32(data: np.ndarray) -> np.ndarray:
    if data.dtype == np.int16:
        return np.int32(data << 16)
    elif data.dtype == np.int32:
        return data
    elif data.dtype == np.float32:
        return np.int32(data * 2147483647.0)
    elif data.dtype == np.float64:
        return np.int32(data * 2147483647.0)
    else:
        raise TypeError(f"Unsupported data type: {data.dtype}")


class Float32(Effect):

    def apply_effect(self, data: np.ndarray) -> np.ndarray:
        return convert_to_float32(data)


class Int16(Effect):
    
    def apply_effect(self, data: np.ndarray) -> np.ndarray:
        return convert_to_int16(data)

class Int32(Effect):
    
    def apply_effect(self, data: np.ndarray) -> np.ndarray:
        return convert_to_int32(data)
