# Name: James Wollenburg
# OSU Email: wollenbj@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 6: HashMap (Portfolio Assignment)
# Due Date: 12/2/2022
# Description: Python implementation of a separate chaining hash map. Hash functions are found in a6_include.py.
#              Includes a non-class function, find_mode, which finds the mode in a DynamicArray using a hash map.

from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Adds a key/value pair into the hash map. If a key already exists in the hash map, the value is updated.
        Resizes the hash map if the load factor is >= 1.

        :param key: A string that is hashed and is the key for a value.
        :param value: Any object that will represent the value in the key/value pair.
        """
        # doubles the capacity and add the empty linked lists
        if self.table_load() >= 1.0:
            self.resize_table(self._capacity*2)
        # inserts a key if it's not already in the hash map
        index = self._hash_function(key) % self._capacity
        if not self._buckets[index].contains(key):
            self._buckets[index].insert(key, value)
            self._size += 1
        # override duplicate keys
        else:
            llist = self._buckets[index]
            for node in llist:
                if node.key == key:
                    node.value = value

    def empty_buckets(self) -> int:
        """
        Returns a count of the empty buckets in the hash map.

        :return: An integer representing the count.
        """
        total = 0
        for index in range(self._capacity):
            if self._buckets[index].length() == 0:
                total += 1
        return total

    def table_load(self) -> float:
        """
        Returns the current table load factor.

        :return: A float representing the load factor.
        """
        return self._size / self._capacity

    def clear(self) -> None:
        """
        Clears the hash map of all values but does not alter the capacity. Replaces the data with new empty LinkedLists.
        """
        for index in range(self._buckets.length()):
            self._buckets[index] = LinkedList()
        self._size = 0

    def resize_table(self, new_capacity: int) -> None:
        """
        Resizes the hash map capacity to the passed value. Rehashes existing values

        :param new_capacity: An integer for the new capacity of the table.
        """
        if new_capacity < 1:
            return
        # save original map and capacity
        original_map = DynamicArray()
        for index in range(self._buckets.length()):
            original_map.append(self._buckets[index])
        # reset the current map (for rehashing)
        self._buckets = DynamicArray()
        self._size = 0
        # get the new capacity then update
        if self._is_prime(new_capacity):
            self._capacity = new_capacity
        else:
            self._capacity = self._next_prime(new_capacity)
        # fill in the new hashmap with empty linked lists
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())
        # populate the new hash map with the original values (now rehashed)
        for index in range(original_map.length()):
            llist = original_map[index]
            if llist.length() != 0:
                for node in llist:
                    self.put(node.key, node.value)

    def get(self, key: str):
        """
        Returns the value associated with the passed key.

        :param key: The string for a key to search for
        """
        # exit if that key isn't found
        if not self.contains_key(key):
            return
        else:
            index = self._hash_function(key) % self._capacity
            for node in self._buckets[index]:
                if node.key == key:
                    return node.value
                node.next

    def contains_key(self, key: str) -> bool:
        """
        Check if the hash map contains a key.

        :param key: The key to search for.

        :return: True if found, false if not.
        """
        index = self._hash_function(key) % self._capacity
        if self._buckets[index].contains(key):
            return True
        return False

    def remove(self, key: str) -> None:
        """
        Remove a key/value pair from the hash map.

        :param key: The key of the key/value pair to remove.
        """
        index = self._hash_function(key) % self._capacity
        if self.contains_key(key):
            self._buckets[index].remove(key)
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Gets all the key/value pairs in the hash map.

        :return: A dynamic array where each index contains a tuple for each key/value pair (key, value).
        """
        # go through each node and add the key/values to the results array.
        results = DynamicArray()
        for index in range(self._buckets.length()):
            if self._buckets[index].length() > 0:
                for node in self._buckets[index]:
                    results.append((node.key, node.value))
        return results

def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    Finds the mode(s) and frequency of a dynamic array.

    :param da: A dynamic array to find the mode in.

    :return: A tuple containing a dynamic array listing all elements that occurred at the mode frequency and the
    integer frequency that they occurred. (dynamic array, frequency).
    """
    # map passed values to a hash map O(n)
    map = HashMap()
    results = DynamicArray()
    map.resize_table(da.length())
    for index in range(da.length()):
        if not map.contains_key(da[index]):
            map.put(da[index], 1)
        else:
            map.put(da[index], map.get(da[index]) + 1)
    # extract all the nodes from the hash map and establish the maximum frequency O(n)
    map_data = map.get_keys_and_values()
    max_freq = 1
    for index in range(map_data.length()):
        if map_data[index][1] > max_freq:
            max_freq = map_data[index][1]
    # append all the elements that occurred at the maximum frequency O(n)
    for index in range(map_data.length()):
        if map_data[index][1] == max_freq:
            results.append(map_data[index][0])

    return results, max_freq

# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(23, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(53, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
