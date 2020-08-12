def layer(node_a=3, node_b=4):
    print(str(node_a)+" "+ str(node_b))



class network:
    def __init__(self, a, b):
        self.a = a
        self.b = b


    def call(self):
        layer(self.a,self.b)

net_1 = network(1,2)
net_2 = network(0,9)

net_1.call()
net_2.call()



