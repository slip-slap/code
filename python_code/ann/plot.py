import matplotlib.pyplot as plt

def my_plot(data_x, data_y):
    fig = plt.figure(111)
    axes1 = fig.add_subplot(111)
    axes1.plot(data_x,data_y,color='black')
    axes1.set_xlabel("generation")
    axes1.set_ylabel("fitness")
    axes1.set_xlim(0,6)
    axes1.set_ylim(0.3,0.7)
    axes1.scatter(data_x, data_y, color='black')
    plt.show()

if __name__=="__main__":
    my_plot([1,2,3,4,5],[0.48,0.48,0.5,0.5,0.5])
