import matplotlib.pyplot as plt
import matplotlib as mpl
import copy
import os

class style:
    def __init__(self, name: str):
        self.name = name
        self.before = None

    def __enter__(self):
        self.before = copy.deepcopy(mpl.rcParams)
        self.use(self.name)
        # return self

    def __exit__(self, exc_type, exc_value, traceback):
        mpl.rcParams.update(self.before)

        # pprint.pprint(self.before)



    @classmethod
    def use(self, name: str):
        file_path = os.path.join(os.path.dirname(__file__), 'styles', f'{name.lower()}.mplstyle')
        plt.style.use(file_path)



if __name__ == "__main__":
    def test_plot():
        x = [1, 2, 3, 4]
        y = [3, 4, 7, 9]
        plt.plot(x, y)
        plt.show()


    def main():
        with style('Sprakel'):
            test_plot()
        test_plot()

    main()