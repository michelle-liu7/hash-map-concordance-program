# Author: Michelle Liu
# Class: CS 261
# Date: 6/10/2020
# hash_map.py
# ===================================================
# Implement a hash map with chaining
# ===================================================

class SLNode:
    def __init__(self, key, value):
        self.next = None
        self.key = key
        self.value = value

    def __str__(self):
        return '(' + str(self.key) + ', ' + str(self.value) + ')'


class LinkedList:
    def __init__(self):
        self.head = None
        self.size = 0

    def add_front(self, key, value):
        """Create a new node and inserts it at the front of the linked list
        Args:
            key: the key for the new node
            value: the value for the new node"""
        new_node = SLNode(key, value)
        new_node.next = self.head
        self.head = new_node
        self.size = self.size + 1

    def remove(self, key):
        """Removes node from linked list
        Args:
            key: key of the node to remove """
        if self.head is None:
            return False
        if self.head.key == key:
            self.head = self.head.next
            self.size = self.size - 1
            return True
        cur = self.head.next
        prev = self.head
        while cur is not None:
            if cur.key == key:
                prev.next = cur.next
                self.size = self.size - 1
                return True
            prev = cur
            cur = cur.next
        return False

    def contains(self, key):
        """Searches linked list for a node with a given key
        Args:
        	key: key of node
        Return:
        	node with matching key, otherwise None"""
        if self.head is not None:
            cur = self.head
            while cur is not None:
                if cur.key == key:
                    return cur
                cur = cur.next
        return None

    def __str__(self):
        out = '['
        if self.head != None:
            cur = self.head
            out = out + str(self.head)
            cur = cur.next
            while cur != None:
                out = out + ' -> ' + str(cur)
                cur = cur.next
        out = out + ']'
        return out


def hash_function_1(key):
    hash = 0
    for i in key:
        hash = hash + ord(i)
    return hash


def hash_function_2(key):
    hash = 0
    index = 0
    for i in key:
        hash = hash + (index + 1) * ord(i)
        index = index + 1
    return hash


class HashMap:
    """
    Creates a new hash map with the specified number of buckets.
    Args:
        capacity: the total number of buckets to be created in the hash table
        function: the hash function to use for hashing values
    """

    def __init__(self, capacity, function):
        self._buckets = []
        for i in range(capacity):
            self._buckets.append(LinkedList())
        self.capacity = capacity
        self._hash_function = function
        self.size = 0

    def clear(self):
        """
        Empties out the hash table deleting all links in the hash table.
        """
        # clear the buckets list and fill them in with empty linked list
        self._buckets = []
        for i in range(self.capacity):
            self._buckets.append(LinkedList())
        self.size = 0 # resize the hash table to 0

    def get(self, key):
        """
        Returns the value with the given key.
        Args:
            key: the value of the key to look for
        Return:
            The value associated to the key. None if the link isn't found.
        """
        index = self._hash_function(key) % self.capacity    # get the index of the bucket for key

        # check if the bucket(linked list) contains the key or not, and return appropriate value
        node = self._buckets[index].contains(key)
        if node is not None:
            return node.value
        return None

    def resize_table(self, capacity):
        """
        Resizes the hash table to have a number of buckets equal to the given
        capacity. All links need to be rehashed in this function after resizing
        Args:
            capacity: the new number of buckets.
        """
        new_buckets = []    # create a new buckets list
        for i in range(capacity):
            new_buckets.append(LinkedList())

        # iterate through every link in the original list and rehash them into the new buckets list
        for bucket in self._buckets:
            cur = bucket.head
            while cur is not None:
                index = self._hash_function(cur.key) % capacity
                new_buckets[index].add_front(cur.key, cur.value)
                cur = cur.next

        self.capacity = capacity    # set the capacity to the new capacity
        self._buckets = new_buckets # update self._buckets to point to the new buckets list

    def put(self, key, value):
        """
        Updates the given key-value pair in the hash table. If a link with the given
        key already exists, this will just update the value and skip traversing. Otherwise,
        it will create a new link with the given key and value and add it to the table
        bucket's linked list.

        Args:
            key: they key to use to has the entry
            value: the value associated with the entry
        """
        index = self._hash_function(key) % self.capacity    # get the index of the bucket for key

        # if the hash table contains the key, update value of the link with the the given key
        if self.contains_key(key) is True:
            node = self._buckets[index].contains(key)
            node.value = value
        # otherwise add the key/value pair as a new link and update hash table's size
        else:
            self._buckets[index].add_front(key, value)
            self.size += 1

    def remove(self, key):
        """
        Removes and frees the link with the given key from the table. If no such link
        exists, this does nothing. Remember to search the entire linked list at the
        bucket.
        Args:
            key: they key to search for and remove along with its value
        """
        index = self._hash_function(key) % self.capacity    # get the index of the bucket for key

        # if the hash table contains the key, then remove the link with the given key from the bucket containing it
        if self.contains_key(key) is True:
            self._buckets[index].remove(key)
            self.size -= 1

    def contains_key(self, key):
        """
        Searches to see if a key exists within the hash table

        Returns:
            True if the key is found False otherwise

        """
        # if a link with the given key exist in the hash table, return True
        if self.get(key) is not None:
            return True

        return False    # else return False

    def empty_buckets(self):
        """
        Returns:
            The number of empty buckets in the table
        """
        empty_buckets = 0   # initialize empty bucket count to 0

        # iterate through every bucket in the buckets list, increment empty bucket count if a bucket is empty
        for bucket in self._buckets:
            if bucket.head is None:
                empty_buckets += 1

        return empty_buckets    # return the count of empty buckets

    def table_load(self):
        """
        Returns:
            the ratio of (number of links) / (number of buckets) in the table as a float.

        """
        return float(self.size/self.capacity)

    def __str__(self):
        """
        Prints all the links in each of the buckets in the table.
        """

        out = ""
        index = 0
        for bucket in self._buckets:
            out = out + str(index) + ': ' + str(bucket) + '\n'
            index = index + 1
        return out

    def list_of_links(self):
        """
        Returns a list of tuples of links in the hash table in the form [(link1.key, link1.vale), ....]
        """
        links_list = []    # initializes an empty list

        # iterate through every link in the hash table and append (link.key, link.value) to links_list
        for bucket in self._buckets:
            cur = bucket.head
            while cur is not None:
                links_list.append((cur.key, cur.value))
                cur = cur.next

        return links_list   # return the list of tuples