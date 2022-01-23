from .effect import Effect
import numpy as np

# a function to convert a numpy array from any format to a float64 format
def convert_to_float64(data: np.ndarray) -> np.ndarray:
    if data.dtype == np.int16:
        return data.astype(np.float64) / 32767.0
    elif data.dtype == np.int32:
        return data.astype(np.float64) / 2147483647.0
    elif data.dtype == np.float32:
        return np.float64(data)
    elif data.dtype == np.float64:
        return data
    else:
        raise TypeError(f"Unsupported data type: {data.dtype}")

# a function to convert a numpy array from any format to a float32 format
def convert_to_float32(data: np.ndarray) -> np.ndarray:
    if data.dtype == np.int16:
        return data.astype(np.float32) / 32767.0
    elif data.dtype == np.int32:
        return data.astype(np.float32) / 2147483647.0
    elif data.dtype == np.float32:
        return data
    elif data.dtype == np.float64:
        return np.float32(data)
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
        return np.int32(data) << 16
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
    
    def info_str(self) -> str:
        return 'Float32'


class Int16(Effect):
    
    def apply_effect(self, data: np.ndarray) -> np.ndarray:
        return convert_to_int16(data)
    
    def info_str(self) -> str:
        return 'Int16'


class Int32(Effect):
    
    def apply_effect(self, data: np.ndarray) -> np.ndarray:
        return convert_to_int32(data)
    
    def info_str(self) -> str:
        return 'Int32'


class Float64(Effect):
    
    def apply_effect(self, data: np.ndarray) -> np.ndarray:
        return convert_to_float64(data)
    
    def info_str(self) -> str:
        return 'Float64'
