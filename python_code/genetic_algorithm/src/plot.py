import matplotlib.pyplot as plt

def my_plot(data_x, data_y):
    fig = plt.figure(111)
    axes1 = fig.add_subplot(111)
    axes1.plot(data_x,data_y,color='black')
    axes1.scatter(data_x, data_y, color='black')
    plt.show()

if __name__=="__main__":
    my_plot([1,2,3],[2,1,3])
