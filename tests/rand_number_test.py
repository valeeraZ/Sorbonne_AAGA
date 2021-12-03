import unittest

from rand_number import rand48, post_processing, generator_Java, reverse_java_rand48


class RandNumberTest(unittest.TestCase):
    def test_generator_Java(self):
        res = [generator_Java() for _ in range(6)]
        ans = [-956251568, -2113186618, 1962154824, 449949881, -1374163520, 392258983]
        self.assertEqual(res, ans, "generator Java Test fail")

    def test_reverse_java_rand48(self):
        v1 = -956251568
        v2 = -2113186618
        v3 = 1962154824
        v1_48 = reverse_java_rand48(v1, v2)
        v2_48 = rand48(v1_48)
        v3_48 = rand48(v2_48)
        self.assertEqual(post_processing(v3_48), v3, "reverse generator Java to rand48 fail")


if __name__ == '__main__':
    unittest.main()
