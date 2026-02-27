class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        string_map = {}
        left_index = 0
        longest = 0

        for right_index, char in enumerate(s):

            if char in string_map :
                left_index = string_map[char] + 1   # ✅ fix here

            string_map[char] = right_index

            longest = max(longest, right_index - left_index + 1)

        return longest

        #
        #     if char in string_map and string_map[char] >= left_index:
        #         left_index = string_map[char] + 1
        #
        #     string_map[char] = right_index
        #     longest = max(longest, right_index - left_index + 1)
        #
        # return longest


# print(Solution().lengthOfLongestSubstring("abcabcbb"))
# print(Solution().lengthOfLongestSubstring("dvdf"))
print(Solution().lengthOfLongestSubstring("pwwkew"))















# unique_nums = set(nums)
# longest = 0
#
# for num in unique_nums:
#     current_longest = 1
#     if num - 1 not in unique_nums:
#         current = num
#
#         while current + 1 in unique_nums:
#             current_longest += 1
#             current += 1
#     longest = max(longest, current_longest)
# return longest
