
class CheckUtils:

    @staticmethod
    def is_last_sequence_in_order(arr):
        if len(arr) < 2:
            return True
        last_three = arr[-3:]
        last_three.sort()
        return last_three == list(range(last_three[0], last_three[-1] + 1))