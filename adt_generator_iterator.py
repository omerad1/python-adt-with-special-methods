import copy
from functools import total_ordering
import math
from hw8_lib import Stack
from hw8_lib import BinarySearchTree


class ByteNode:
    def __init__(self, byte):
        """
        constructor
        :param byte: (object) string with length of 8 chars when every char is 0 or 1.
        """
        self.byte = byte
        self.next = None
        if type(byte) != str:
            raise TypeError("Can only get type : str")
        if len(byte) != 8:
            raise ValueError("Not the right length")
        for i in byte:
            if i != '1' and i != '0':
                raise ValueError("The allowed chars is only '1' or '0'")

    def get_byte(self):
        """
        this method returns byte
        :return: (str) byte
        """
        return self.byte

    def get_next(self):
        """
        this method will return the next field
        :return: (bytenode/none) next
        """
        return self.next

    def set_next(self, next):
        """
        this method updates the next node
        :param next: (byteNode) next
        :return: none
        """
        self.next = next

    def __repr__(self):
        """
        represents the byte
        :return: (str) string that represents the byte
        """
        return f'[{self.get_byte()}]=>'


@total_ordering
class LinkedListBinaryNum:
    def __init__(self, num=0):
        """
        constructor
        :param num: (int) non - negative number in decimal base
        """
        if type(num) != int:
            raise TypeError("Can only receive Type: int")
        if num < 0:
            raise ValueError("Can only receive non-negative numbers")
        num_a = copy.deepcopy(num)
        binary = ''
        if num_a == 0:
            binary = '00000000'
        else:
            while num_a > 0:
                binary += f'{(num_a % 2)}'
                num_a //= 2
        bn = copy.deepcopy(binary)[::-1]
        if num < 256:
            bn1 = bn.zfill(8)
        elif len(bn) % 8 == 0:
            bn1 = bn[0:8]
        else:
            bn1 = bn[0:len(bn) % 8].zfill(8)

        self.head = ByteNode(bn1)
        self.size = math.ceil(len(bn) / 8)
        if self.size > 1:
            i = copy.deepcopy(self.size) - 1  # 2
            if len(bn) % 8 == 0:
                start = 8
                end = 16
            else:
                start = len(bn) % 8
                end = len(bn) % 8 + 8
            while i > 0:
                new_node = ByteNode(bn[start:end])
                n = self.head
                while n.get_next() is not None:
                    n = n.get_next()
                n.set_next(new_node)
                start += 8
                end += 8
                i -= 1

    def add_MSB(self, byte):
        """
        method that adds ByteNode as MSB in the linked lst
        :param byte:(str) byte
        :return:None
        """
        byte = ByteNode(byte)

        byte.set_next(self.head)
        self.head = byte
        self.size += 1


    def __len__(self):
        """
        method that returns the number of bytes in the linked list
        :return: (int) size of the linked list
        """
        return copy.deepcopy(self.size)

    def __str__(self):  # end user
        """
        method that represents the number for printing uses
        :return: (str) string that represents the object
        """
        nodes = ''
        curr = self.head
        while curr:
            nodes += f'{curr.get_byte()}|'
            curr = curr.next
        return f'|{nodes}'

    def __repr__(self):  # developer
        """
        method that represents the number in binary base.
        :return: (str) string that shows the number of the bytes and where they point at
        """
        if self.size == 1:
            return f'LinkedListBinaryNum with {self.size} Byte, Bytes map: {self.head}None'
        else:
            nodes = ''
            curr = self.head
            while curr:
                nodes += str(curr)
                curr = curr.next
            return f'LinkedListBinaryNum with {self.size} Bytes, Bytes map: {nodes}None'

    def __getitem__(self, item):
        """
        method that gets index and returns the byte in this index
        :param item:
        :return:
        """
        if type(item) != int:
            raise TypeError("Can only except Type: int")
        if item >= len(self) or item <= -(len(self)) - 1:
            raise IndexError("Index out of range")
        curr = self.head
        if item < 0:
            j = len(self) + item
            while j > 0:
                curr = curr.get_next()
                j -= 1
            return curr.get_byte()
        else:
            i = copy.deepcopy(item)
            while i > 0:
                curr = curr.get_next()
                i -= 1
            return curr.get_byte()

    # Order relations:
    def __eq__(self, other):
        """
        check if two linked lists are equal
        :param other:(object) other
        :return:(bool) True if they equal and False if isn't
        """

        a = self.head
        b = other.head
        while a is not None and b is not None:
            if a.get_byte() != b.get_byte():
                return False
            a = a.get_next()
            b = b.get_next()
        return a == None and b == None

    def __gt__(self, other):
        """
        check if self is bigger then other
        :param other: (object) Other
        :return: (bool) True if self>other and False if isn't
        """
        if not (isinstance(other, LinkedListBinaryNum) or isinstance(other, int)):
            raise TypeError("Wrong input Type!")
        if other < 0:
            raise ValueError("Wrong input Type!")
        if type(other) == int:
            other = LinkedListBinaryNum(other)
        a = self.head
        b = other.head
        if len(self) > len(other):
            return True
        if len(self) < len(other):
            return False
        else:
            while a is not None and b is not None:
                if int(a.get_byte()) > int(b.get_byte()):
                    return True
                if int(a.get_byte()) < int(b.get_byte()):
                    return False
                if int(a.get_byte()) == int(b.get_byte()):
                    a = a.get_next()
                    b = b.get_next()
            return False

    def __add__(self, other):
        """
        adding operator that returns new linked list
        :param other: (object) other
        :return:(LinkedListBinaryNum) object
        """
        if not (isinstance(other, LinkedListBinaryNum) or isinstance(other, int)):
            raise TypeError("Wrong input Type!")
        if type(other) == int:
            if other < 0:
                raise ValueError("Wrong input Type!")
            else:
                other = LinkedListBinaryNum(other)
        num1 = str(self).replace('|', '')
        num2 = str(other).replace('|', '')
        max_lengh = max(len(num1), len(num2))
        num1 = num1.zfill(max_lengh)
        num2 = num2.zfill(max_lengh)
        res = ''
        curry = 0
        for i in range(max_lengh - 1, -1, -1):
            r = curry
            if num1[i] == '1':
                r += 1
            if num2[i] == '1':
                r += 1
            if r % 2 == 1:
                res = '1' + res
            else:
                res = '0' + res
            if r < 2:
                curry = 0
            else:
                curry = 1
        if curry != 0:
            res = '1' + res
        res_a = res.zfill(max_lengh)
        if res_a[0:7] == '00000000':
            res_a = res_a[7:]
        res_b = LinkedListBinaryNum()
        res_b.head = None
        size = math.ceil(len(res_a) / 8)
        if len(res_a)%8 ==0:
            start = len(res_a) - 8
            end = len(res_a)
            while size>0:
                new_node = res_a[start:end]
                res_b.add_MSB(new_node)
                start -=8
                end -= 8
                size -=1
        return res_b

    def __sub__(self, other):
        """
        Subtraction operator that returns a new LinkedListBinaryNum object. If the input is not LinkedListBinaryNum or
        an integer a TypeError exception should be thrown
        if the input is a negative integer a ValueError exception should be thrown,
        if the value of another greater than the self value a ValueError exception should be thrown.
        :param other:(object) Other
        :return:(LinkedListBinaryNum) object
        """
        if not (isinstance(other, LinkedListBinaryNum) or isinstance(other, int)):
            raise TypeError("Wrong input Type!")
        if type(other) == int:
            other = LinkedListBinaryNum(other)
        num1 = str(self).replace('|', '')
        num2 = str(other).replace('|', '')
        if num2 > num1:
            raise ValueError("Wrong input Type!")
        num1 = str(self).replace('|', '')
        num2 = str(other).replace('|', '')
        max_len = max(len(num1), len(num2))
        a = num1.zfill(max_len)
        b = num2.zfill(max_len)
        res = ''
        curry = 0
        if num1 == num2:
            return LinkedListBinaryNum(0)
        for i in range(max_len - 1, -1, -1):
            num = int(a[i]) - int(b[i]) - curry
            if num % 2 == 1:
                res += '1'
            else:
                res += '0'
            if num < 0:
                curry = 1
            else:
                curry = 0
        if curry != 0:
            res = '01' + res
        if int(res) == 0:
            res = 0
        return LinkedListBinaryNum(int(res[::-1], 2))
    #
    def __radd__(self, other):
        return self.__add__(other)


class DoublyLinkedNode:
    """
    constructor
    """

    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

    def get_data(self):
        """
        get data
        :return: (object) data
        """
        return self.data

    def set_next(self, next):
        """
        defining next node
        :param next: (DoublyLinkedNode)
        :return:None
        """
        self.next = next

    def get_next(self):
        """
        get next node
        :return:defining next node
        """
        return self.next

    def get_prev(self):
        """
        get prev node
        :return: (DoublyLinkedNode)
        """
        return self.prev

    def set_prev(self, prev):
        """
        define prev node
        :param prev: defining next node
        :return: None
        """
        self.prev = prev

    def __repr__(self):
        """
        represents the node
        :return:(str) node
        """
        return f'=>[{self.get_data()}]<='


class DoublyLinkedList:
    def __init__(self):
        """
        constructor
        """
        self.head = None
        self.tail = None
        self.size = 0

    def __len__(self):
        """
        the number of nodes in the linked list
        :return:(int) number of nodes
        """
        return self.size

    def add_at_start(self, data):
        """
        method that adds the data at the beginning of the list
        :param data:(object) data
        :return:None
        """
        new_node = DoublyLinkedNode(data)
        if self.is_empty():
            self.head = new_node
            self.tail = new_node
            self.size = 1
            return
        else:
            next_node = self.head
            new_node.set_next(next_node)
            next_node.set_prev(new_node)
            self.head = new_node
            self.size += 1
            return

    def remove_from_end(self):
        """
        method that removes and returns the data from the last
         link in the list or an exception of the StopIteration type if the list is empty.
        :return:(object) the data from the link that has been removed
        """
        if self.is_empty():
            raise StopIteration("The list in Empty !")
        if self.size == 1:
            data = self.head.get_data()
            self.head = None
            self.tail = None
            self.size -= 1
            return data
        else:
            removed = self.tail  # del_node
            temp = removed.get_prev()  # prev_node
            removed.set_prev(None)
            temp.set_next(None)
            self.tail = temp
            self.size -= 1
            return removed.get_data()

    def get_tail(self):
        """
        returns the tail of the doublylinkedlist
        :return:(object) tail
        """
        return self.tail

    def get_head(self):
        """
        returns the head of the doublylinkedlist
        :return:(object) head
        """
        return self.head

    def __repr__(self):
        """
        represents the doubly linked list
        :return: (str) doubly linked list
        """
        if self.is_empty():
            return 'Head==><==Tail'
        else:
            nodes = ''
            curr = self.get_head()
            while curr:
                nodes += str(curr)
                curr = curr.get_next()
            return f'Head={nodes}=Tail'

    def is_empty(self):
        """
        check if the linked list is empty
        :return: True if the size is 0 and False if isn't
        """
        if self.size == 0:
            return True
        else:
            return False


class DoublyLinkedListQueue:
    def __init__(self):
        """
        constructor
        """
        self.data = DoublyLinkedList()
        self.start = 0

    def enqueue(self, val):
        """
        adding value to the queue
        :param val:(object) value
        :return:None
        """
        self.data.add_at_start(val)

    def dequeue(self):
        """
        :return:
        """
        if self.data.get_head() is None:
            raise StopIteration("The Queue is Empty!")
        return self.data.remove_from_end()

    def __len__(self):
        """
        length
        :return:
        """
        return len(self.data)

    def is_empty(self):
        """
        check if the queue is empty
        :return: (Bool) True if the queue is empty and False if he isnt
        """
        return self.data.is_empty()

    def __repr__(self):
        """
        represents the doublylinkedlist
        :return: (str) doublylinkedlist
        """
        if len(self.data) == 0:
            return 'Newest=>[]<=Oldest'
        nodes = ''
        for i in range(len(self)):
            temp_s = self.dequeue()
            nodes = str(temp_s) + ',' + nodes
            self.enqueue(temp_s)
        nodes = nodes[:-1]
        return f'Newest=>[{nodes}]<=Oldest'

    def __iter__(self):
        """
        iterator
        :return: (object) self
        """
        self.start = 0
        return self

    def __next__(self):
        """
        implementation of the next value in the linked list
        :return: (object) item from the linked list
        """
        if len(self) == 0 or self.start == len(self):
            raise StopIteration
        else:
            holder = self
            item = holder.dequeue()
            holder.enqueue(item)
            self.start += 1
            return item


class NumsManagment:
    def __init__(self, file_name):
        """
        constructor
        :param file_name:
        """
        self.file_name = file_name

    def is_line_pos_int(self, st):
        """
        method that checks if there is line in the file that represents non-negative int
        :param st: (str) string that has been read from the file
        :return: (bool) True if the string represents non-negative int and False if isn't
        """
        if st.isnumeric():
            return True
        else:
            return False

    def read_file_gen(self):
        """
        method that generate presentation of the next valid number in the file.
        :return: (generator)
        """
        with open(self.file_name, 'r') as file:
            return (LinkedListBinaryNum(int(line.rstrip('\n'))) for line in file.readlines() if
                    self.is_line_pos_int(line.rstrip('\n')))

    def stack_from_file(self):
        """
        method that use the read_file_gen in order to make stack full with the valid numbers from the file
        :return: (stack) stack that contains al the valid file numbers
        """
        stack = Stack()
        gen = self.read_file_gen()
        while True:
            try:
                stack.push(next(gen))
            except StopIteration:
                return stack

    def sort_stack_descending(self, s):  # TODO more tests !
        """
        method that gets only binary numbers and returns stack with thous numbers in descending order
        :param s:(stack(linkedlistbinarynum)) stack with binary numbers
        :return:(stack) stack with the values that has been in s but sorted in descending order
        """
        temp_stack = Stack()
        while len(s) > 0:
            current = s.pop()
            while True:
                if len(temp_stack) == 0:
                    temp_stack.push(current)
                    break
                elem = temp_stack.pop()
                if elem <= current:
                    temp_stack.push(elem)
                    temp_stack.push(current)
                    break
                else:
                    s.push(elem)
        return temp_stack

    def queue_from_file(self):
        """
        making queue from the valid numbers in the file
        :return: queue that contains all the valid numbers from the file
        """
        queue = DoublyLinkedListQueue()
        gen = self.read_file_gen()
        while True:
            try:
                queue.enqueue(next(gen))
            except StopIteration:
                return queue

    def set_of_bytes(self, q_of_nums):
        """
        method that gets queue of binary nums and returns set of bytes without multiplication
        :param q_of_nums: (queue(LinkedListBinaryNum)) queue that conatains binary nums
        :return: (set) set of bytes values
        """
        res_set = set()
        for i in q_of_nums:
            x = str(i).split('|')
            for n in x:
                res_set.add(str(n))
        res_set.remove("")
        return res_set

    def nums_bst(self):
        """
        method that generate binary search tree with the valid numbers
        :return:(binary search tree) bst that contains all the valid numbers from the file
        """
        gen = self.read_file_gen()
        res_bst = BinarySearchTree()
        while True:
            try:
                x = next(gen)
                b_num = x
                d_num = str(x).replace('|', '')
                d_num_a = int(d_num, 2)
                res_bst.insert(d_num_a, b_num)
            except StopIteration:
                return res_bst

    def bst_closest_gen(self, bst):
        """
        generate generator from the bst
        :param bst:(BinarySearchTree(LinkedListBinaryNum)) bst
        :return:(generator) generator that returns the two closest numbers in the file and make range
        for them.
        """
        iterator = copy.deepcopy(iter(bst))
        start_val = next(iterator)[0]
        second_val = next(iterator)[0]
        min_range = int(second_val) - int(start_val)
        min_val = 0
        res = (min_val, 0)
        try:
            for i in bst:
                if i[0] != start_val:
                    n = next(iterator)[0]
                    s_values = int(n - int(i[0]))
                    if s_values < min_range:
                        min_range = s_values
                        min_val = i[0]
                        res = (min_val, n)
        except StopIteration:
            return ((j, LinkedListBinaryNum(j)) for j in range(res[0], res[1] + 1))
