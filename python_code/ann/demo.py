import yaml

with open('configuration.yaml') as input_stream:
    data = yaml.load(input_stream, Loader=yaml.FullLoader)
    print(data['BATCH'])
