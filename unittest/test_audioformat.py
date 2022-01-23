import unittest
import numpy as np
from audio_effects.audioformat import Int16, Float32, Int32, Float64

class TestInt16(unittest.TestCase):

    def test_int16_to_int16(self):
        # create a random array of data of data type int16
        test_data = np.random.randint(-32768, 32767, 10).astype(np.int16)
        # create an instance of Int16
        int16 = Int16()
        # apply the effect to the data
        result = int16.apply_effect(test_data)
        # check if the result is the same as the input
        self.assertTrue(np.array_equal(test_data, result))
    
    def test_int16_to_float32(self):
        # create a random array of data of data type int16
        test_data = np.random.randint(-32768, 32767, 10).astype(np.int16)
        # create an instance of Float32
        float32 = Float32()
        # apply the effect to the data
        result = float32.apply_effect(test_data)
        # create expected result
        expected_result = test_data.astype(np.float32) / 32767.0
        self.assertTrue(np.array_equal(expected_result, result))
    
    def test_int16_to_int32(self):
        # create a random array of data of data type int16
        test_data = np.random.randint(-32768, 32767, 10).astype(np.int16)
        # create an instance of Int32
        int32 = Int32()
        # apply the effect to the data
        result = int32.apply_effect(test_data)
        # create expected result
        expected_result = test_data.astype(np.int32) << 16
        self.assertTrue(np.array_equal(expected_result, result))
    
    def test_int16_to_float64(self):
        # create a random array of data of data type int16
        test_data = np.random.randint(-32768, 32767, 10).astype(np.int16)
        # create an instance of Float64
        float64 = Float64()
        # apply the effect to the data
        result = float64.apply_effect(test_data)
        # create expected result
        expected_result = test_data.astype(np.float64)/32767.0
        self.assertTrue(np.array_equal(expected_result, result))


class TestInt32(unittest.TestCase):

    def test_int32_to_int16(self):
        # create a random array of data of data type int32
        test_data = np.random.randint(-2**31,(2**31) - 1 , 10).astype(np.int32)
        # create an instance of Int16
        int16 = Int16()
        # apply the effect to the data
        result = int16.apply_effect(test_data)
        # create expected result
        expected_result = test_data >> 16
        self.assertTrue(np.array_equal(expected_result, result))
    
    def test_int32_to_float32(self):
        # create a random array of data of data type int32
        test_data = np.random.randint(-2**31,(2**31) - 1 , 10).astype(np.int32)
        # create an instance of Float32
        float32 = Float32()
        # apply the effect to the data
        result = float32.apply_effect(test_data)
        # create expected result
        expected_result = test_data.astype(np.float32) / 2147483647.0
        self.assertTrue(np.array_equal(expected_result, result))
    
    def test_int32_to_int32(self):
        # create a random array of data of data type int32
        test_data = np.random.randint(-2**31,(2**31) - 1 , 10).astype(np.int32)
        # create an instance of Int32
        int32 = Int32()
        # apply the effect to the data
        result = int32.apply_effect(test_data)
        # check if the result is the same as the input
        self.assertTrue(np.array_equal(test_data, result))
    
    def test_int32_to_float64(self):
        # create a random array of data of data type int32
        test_data = np.random.randint(-2**31,(2**31) - 1 , 10).astype(np.int32)
        # create an instance of Float64
        float64 = Float64()
        # apply the effect to the data
        result = float64.apply_effect(test_data)
        # create expected result
        expected_result = test_data.astype(np.float64)/2147483647.0
        self.assertTrue(np.array_equal(expected_result, result))

    
class TestFloat32(unittest.TestCase):

    def test_float32_to_int16(self):
        # create a random array of data of data type float32
        test_data = np.random.rand(10).astype(np.float32)
        # create an instance of Int16
        int16 = Int16()
        # apply the effect to the data
        result = int16.apply_effect(test_data)
        # create expected result
        expected_result = (test_data * 32767.0).astype(np.int16)
        self.assertTrue(np.array_equal(expected_result, result))
    
    def test_float32_to_float32(self):
        # create a random array of data of data type float32
        test_data = np.random.rand(10).astype(np.float32)
        # create an instance of Float32
        float32 = Float32()
        # apply the effect to the data
        result = float32.apply_effect(test_data)
        # check if the result is the same as the input
        self.assertTrue(np.array_equal(test_data, result))
    
    def test_float32_to_int32(self):
        # create a random array of data of data type float32
        test_data = np.random.rand(10).astype(np.float32)
        # create an instance of Int32
        int32 = Int32()
        # apply the effect to the data
        result = int32.apply_effect(test_data)
        # create expected result
        expected_result = (test_data * 2147483647.0).astype(np.int32)
        self.assertTrue(np.array_equal(expected_result, result))
    
    def test_float32_to_float64(self):
        # create a random array of data of data type float32
        test_data = np.random.rand(10).astype(np.float32)
        # create an instance of Float64
        float64 = Float64()
        # apply the effect to the data
        result = float64.apply_effect(test_data)
        # create expected result
        expected_result = test_data.astype(np.float64)
        self.assertTrue(np.array_equal(expected_result, result))

class TestFloat64(unittest.TestCase):

    def test_float64_to_int16(self):
        # create a random array of data of data type float64
        test_data = np.random.rand(10).astype(np.float64)
        # create an instance of Int16
        int16 = Int16()
        # apply the effect to the data
        result = int16.apply_effect(test_data)
        # create expected result
        expected_result = (test_data * 32767.0).astype(np.int16)
        self.assertTrue(np.array_equal(expected_result, result))
    
    def test_float64_to_float32(self):
        # create a random array of data of data type float64
        test_data = np.random.rand(10).astype(np.float64)
        # create an instance of Float32
        float32 = Float32()
        # apply the effect to the data
        result = float32.apply_effect(test_data)
        # create expected result
        expected_result = test_data.astype(np.float32)
        self.assertTrue(np.array_equal(expected_result, result))
    
    def test_float64_to_int32(self):
        # create a random array of data of data type float64
        test_data = np.random.rand(10).astype(np.float64)
        # create an instance of Int32
        int32 = Int32()
        # apply the effect to the data
        result = int32.apply_effect(test_data)
        # create expected result
        expected_result = (test_data * 2147483647.0).astype(np.int32)
        self.assertTrue(np.array_equal(expected_result, result))
    
    def test_float64_to_float64(self):
        # create a random array of data of data type float64
        test_data = np.random.rand(10).astype(np.float64)
        # create an instance of Float64
        float = Float64()
        # apply the effect to the data
        result = float.apply_effect(test_data)
        # check if the result is the same as the input
        self.assertTrue(np.array_equal(test_data, result))

