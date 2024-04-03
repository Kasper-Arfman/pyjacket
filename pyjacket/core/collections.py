from collections import Counter

class CustomCounter(Counter):
    """
    Build a counter-dict for an iterable. 
    Features:
     - delete key if count reaches 0
     - initialize key to 0 if it doesn't exist
    """

    def __setitem__(self, key, value):
        if value == 0:
            if key in self:
                del self[key]
        else:
            super().__setitem__(key, value)


if __name__ == '__main__':

    def main():
        # Example usage
        custom_counter = CustomCounter()
        custom_counter['apple'] = 3
        custom_counter['banana'] = 0

        print(custom_counter)  # Output: CustomCounter({'apple': 3, 'banana': 2})

        custom_counter['apple'] -= 1
        # custom_counter['banana'] -= 1

        print(custom_counter)  # Output: CustomCounter({'apple': 2})

    main()