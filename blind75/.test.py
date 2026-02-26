def longestConsecutive(nums):
    num_set = set(nums)
    longest = 0

    for num in num_set:
        if num - 1 not in num_set:   # start of sequence
            current = num
            length = 1

            while current + 1 in num_set:
                current += 1
                length += 1

            longest = max(longest, length)

    return longest


nums = [100,4,200,1,3,2]
print(longestConsecutive(nums))