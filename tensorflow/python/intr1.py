import os 

for root, dirs, files in os.walk("/Users/kismet"):
    for name in dirs:
        print(os.path.join(root,name))
