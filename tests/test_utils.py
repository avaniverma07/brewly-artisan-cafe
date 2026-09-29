import unittest
from brewly.utils import (
    summation, count_occurrences, linear_search, selection_sort,
    find_kth_smallest, remove_duplicates, find_maximum,
    is_valid_email, hash_password,
)


class TestUtils(unittest.TestCase):

    def test_summation(self):
        self.assertEqual(summation([1, 2, 3, 4]), 10)
        self.assertEqual(summation([]), 0)

    def test_count_occurrences(self):
        self.assertEqual(count_occurrences([1, 2, 3, 4, 5], lambda x: x % 2 == 0), 2)

    def test_linear_search_found(self):
        data = [{"id": "A"}, {"id": "B"}]
        result = linear_search(data, "B", key_fn=lambda x: x["id"])
        self.assertEqual(result["id"], "B")

    def test_linear_search_not_found(self):
        data = [{"id": "A"}]
        self.assertIsNone(linear_search(data, "Z", key_fn=lambda x: x["id"]))

    def test_selection_sort_ascending(self):
        self.assertEqual(selection_sort([5, 3, 8, 1]), [1, 3, 5, 8])

    def test_selection_sort_descending(self):
        self.assertEqual(selection_sort([5, 3, 8, 1], reverse=True), [8, 5, 3, 1])

    def test_kth_smallest(self):
        values = [7, 2, 9, 4, 1]
        self.assertEqual(find_kth_smallest(values, 1), 1)
        self.assertEqual(find_kth_smallest(values, 3), 4)
        self.assertEqual(find_kth_smallest(values, 5), 9)

    def test_kth_smallest_out_of_range(self):
        with self.assertRaises(IndexError):
            find_kth_smallest([1, 2, 3], 10)

    def test_remove_duplicates(self):
        self.assertEqual(remove_duplicates([1, 2, 2, 3, 1, 4]), [1, 2, 3, 4])

    def test_find_maximum(self):
        self.assertEqual(find_maximum([3, 7, 2, 9, 5]), 9)
        self.assertIsNone(find_maximum([]))

    def test_valid_email(self):
        self.assertTrue(is_valid_email("user@example.com"))
        self.assertFalse(is_valid_email("not-an-email"))

    def test_password_hash_consistency(self):
        self.assertEqual(hash_password("secret123"), hash_password("secret123"))
        self.assertNotEqual(hash_password("secret123"), hash_password("other"))


if __name__ == "__main__":
    unittest.main()
