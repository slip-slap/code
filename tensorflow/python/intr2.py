import os

def get_subdir(path):
    """
    Args:
      path: 路径
    Return:
      返回值为一个list，位该path下的所有文件夹名字，不包括隐藏文件夹
    """
    subdir = []
    if(os.path.exists(path)):
        files = os.listdir(path)
        for file in files:
            #判断是否为隐藏文件夹
            if file.startswith('.'):
                pass
            else:
                m = os.path.join(path,file)
                if(os.path.isdir(m)):
                    h = os.path.split(m)
                    subdir.append(h[1])

    else:
        print("argument is wring, the directory do not exist")
    print(subdir)
    return subdir

if __name__ == "__main__":
    get_subdir("/Users/kismet")

