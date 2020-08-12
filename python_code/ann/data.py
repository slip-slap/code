import csv
import numpy as np



class data:
    def __init__(self,batch=60,total_data_number=240):
        self.batch = batch
        self.total_data_number = total_data_number
        self.current = 0
        self.data = self.get_data()

    def get_batch_train_data(self):

        # check whether out of range
        if(self.current+self.batch>self.total_data_number):
            self.current = 0
        train_data = self.data[self.current:self.current+self.batch]
        # reset current
        self.current = self.current + self.batch
        return train_data

    def get_test_data(self):
        test_data = self.data[240:300]
        return test_data


    def get_data(self,file_path="./train_data/",file_name="train_data.csv"):
        data= []
        with open(file_path+file_name,'r') as my_file:
            csv_reader = csv.reader(my_file,delimiter=',')
            for i in csv_reader:
                for j in range(len(i)):
                    i[j]=float(i[j])
                data.append(i)

        # convert list to array
        data = np.asarray(data,float)

        # data normalization
        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                data[i,j] = data[i,j]/max(data[:,j])

        for i in range(data.shape[0]):
            if(data[i,13]>0):
                data[i,13] = 1
        return data

    def get_batch_train_data_with_specific_attributes(self, index):
        batch_data = self.get_batch_train_data()
        list_result = list()
        for i in range(batch_data.shape[0]):
            included_attribute = list()
            for j in range(len(index)):
                if(index[j]==1):
                    included_attribute.append(batch_data[i,j])
            list_result.append(included_attribute)
        # convet list to array
        array_result= np.asarray(list_result,float)
        return array_result


if __name__ == '__main__':
     data = data(10)
     train_data =data.get_batch_train_data()
     #index = np.random.randint(0,2,(14))
     #result = data.get_batch_train_data_with_specific_attributes(index)
     test_data = data.get_test_data()
     print(train_data)


# save normalized data
"""
with open("normalized.data",'w') as handler:
    csv_handler = csv.writer(handler,delimiter=',')
    for i in range(data.shape[0]):
        csv_handler.writerow(data[i,:])
"""




