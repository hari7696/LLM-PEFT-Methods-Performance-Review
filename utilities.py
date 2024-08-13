import pickle
def print_line(length = 50):
    print("-"* length)


def save_pickle(object, file_name):
    with open(file_name, 'wb') as handle:
        pickle.dump(object, handle, protocol=pickle.HIGHEST_PROTOCOL)

def load_pickle(file_name):
    with open(file_name, 'rb') as handle:
        b = pickle.load(handle)
    return b
