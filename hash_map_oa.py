# Name: James Wollenburg
# OSU Email: wollenbj@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 6: HashMap (Portfolio Assignment)
# Due Date: 12/2/2022
# Description: Python implementation of an open addressing hash map with quadratic probing. Hash functions
#              are found in a6_include.py. Includes an iterator/next method for the hash map.

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

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
        Increment from given number to find the closest prime number
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
        Adds a key/value pair into the hash map. If a key already exists in the hash map, just the value is updated.
        Resizes the hash map if the load factor is >= 0.5.

        :param key: A string that is hashed and is the key for a value.
        :param value: Any object that will represent the value in the key/value pair.
        """
        if self.table_load() >= 0.5:
            self.resize_table(self._capacity * 2)
        # add key/value if index is empty
        index = self._hash_function(key) % self._capacity
        if self._buckets[index] is None or self._buckets[index].is_tombstone:
            self._buckets[index] = HashEntry(key, value)
            self._size += 1
        # if just updating a key/value
        elif self.contains_key(key):
            if self._buckets[index].key == key:
                self._buckets[index].value = value
            # subsequent probes
            else:
                j = 1
                # since key is known to exist in table, probe until it's found
                while True:
                    index = (self._hash_function(key) + j ** 2) % self._capacity
                    if self._buckets[index].key == key:
                        self._buckets[index].value = value
                        return
                    j += 1
        # when the index is already occupied
        else:
            j = 1
            while self._buckets[index] is not None:
                index = (self._hash_function(key) + j ** 2) % self._capacity
                if self._buckets[index] is None or self._buckets[index].is_tombstone:
                    self._buckets[index] = HashEntry(key, value)
                    self._size += 1
                    return
                j += 1

    def table_load(self) -> float:
        """
        Returns the current table load factor.

        :return: A float representing the load factor.
        """
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Counts the number of empty buckets. Tombstone values are considered empty.
        """
        total = 0
        for value in self:
            total += 1
        return self._capacity - total

    def resize_table(self, new_capacity: int) -> None:
        """
        Resizes the hash map capacity to the passed value. Rehashes existing values and removes tombstones.

        :param new_capacity: An integer for the new capacity of the table.
        """
        if new_capacity < self._size:
            return
        # save original map and capacity
        original_map = DynamicArray()
        for index in range(self._buckets.length()):
            original_map.append(self._buckets[index])
        # reset the current map (for rehashing)
        self._buckets = DynamicArray()
        self._size = 0
        # update new_capacity to a prime if needed
        if self._is_prime(new_capacity):
            self._capacity = new_capacity
        else:
            self._capacity = self._next_prime(new_capacity)
        # fill in the new hashmap with None (also resizes the DynamicArray)
        for _ in range(self._capacity):
            self._buckets.append(None)
        # repopulate new map, removing tombstones
        for index in range(original_map.length()):
            if original_map[index] and not original_map[index].is_tombstone:
                self.put(original_map[index].key, original_map[index].value)

    def get(self, key: str) -> object:
        """
        Get the value associated with a key.

        :param key: The string key to retrieve the associated value.

        :return: The value.
        """
        index = self._hash_function(key) % self._capacity
        # check if the key exists in the list, if it doesn't result is None
        if self.contains_key(key):
            # on first probe
            if self._buckets[index].key == key:
                return self._buckets[index].value
            # subsequent probes
            else:
                j = 1
                # since key is known to exist in table, probe until it's found
                while True:
                    index = (self._hash_function(key) + j ** 2) % self._capacity
                    if self._buckets[index].key == key:
                        return self._buckets[index].value
                    j += 1

    def contains_key(self, key: str) -> bool:
        """
        Checks if a hash map contains a key.

        :param key: A string key to search for in the hash map.

        :return: True if found, false if not.
        """
        index = self._hash_function(key) % self._capacity
        # empty table or the first spot check results in None
        if self._size == 0 or not self._buckets[index]:
            return False
        # First possible index matches
        elif self._buckets[index].key == key:
            if self._buckets[index].is_tombstone is True:
                return False
            return True
        # Index is not none, check next w/ quadratic probing
        else:
            j = 1
            # probe until either key is found or None
            while self._buckets[index] is not None:
                index = (self._hash_function(key) + j**2) % self._capacity
                if self._buckets[index] and self._buckets[index].key == key:
                    if self._buckets[index].is_tombstone is True:
                        return False
                    return True
                j += 1
        return False

    def remove(self, key: str) -> None:
        """
        Remove a key/value pair from the hash map. Does not set the index to None, instead flips is_tombstone to True.

        :param key: The key of the key/value pair to remove.
        """
        index = self._hash_function(key) % self._capacity
        if self.contains_key(key):
            if self._buckets[index].key == key:
                self._buckets[index].is_tombstone = True
            else:
                j = 1
                # since key is known to exist in table, probe until it's found
                while True:
                    index = (self._hash_function(key) + j ** 2) % self._capacity
                    if self._buckets[index].key == key:
                        self._buckets[index].is_tombstone = True
                        self._size -= 1
                        return
                    j += 1
            self._size -= 1

    def clear(self) -> None:
        """
        Clears the hash map of all values but does not alter the capacity. Replaces them all with None and resets size.
        """
        for index in range(self._buckets.length()):
            self._buckets[index] = None
        self._size = 0

    def get_keys_and_values(self) -> DynamicArray:
        """
        Gets all the key/value pairs in the hash map. Skips tombstone elements.

        :return: A dynamic array where each index contains a tuple for each key/value pair (key, value).
        """
        results = DynamicArray()
        for bucket in self:
            results.append((bucket.key, bucket.value))
        return results

    def __iter__(self):
        """
        Creates an iterator for the HashMap class.
        """
        self._index = 0
        return self

    def __next__(self):
        """
        Returns the next value in the HashMap.
        """
        try:
            value = self._buckets[self._index]
            while value is None or value.is_tombstone is True:
                self._index += 1
                value = self._buckets[self._index]
        except DynamicArrayException:
            raise StopIteration
        self._index += 1

        return value


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

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

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
    m = HashMap(11, hash_function_1)
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

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
