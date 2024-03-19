class HashMap:

    def __init__(self, initialCapacity=40):
        self.packageList = []
        for i in range(initialCapacity):
            self.packageList.append([])

    # Inserts a new item into the hash table.
    def insert(self, key, item):  # does both insert and update
        # get the bucket list where this item will go.
        bucket = hash(key) % len(self.packageList)
        bucket_list = self.packageList[bucket]

        # update key if it is already in the bucket
        for kv in bucket_list:
            # O(N)
            # print (key_value)
            if kv[0] == key:
                kv[1] = item
                return True
        # if not, insert the item to the end of the bucket list.
        key_value = [key, item]
        bucket_list.append(key_value)
        return True

    # remove from hash table
    def remove(self, key):
        position = hash(key) % len(self.packageList)
        target = self.packageList[position]

        if key in target:
            target.remove(key)

    # search for item in HashMap

    def search(self, key):
        bucket = hash(key) % len(self.packageList)
        bucket_list = self.packageList[bucket]
        for pair in bucket_list:
            if key == pair[0]:
                return pair[1]
        return None  # key does not match pair 0;