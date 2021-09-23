import time
start_time = time.time()
with open('data_log','a') as file:
    for i in range(10000):
        file.writelines('This is a test to see how long this takes.')

test_duration = time.time()-start_time
print('It took ' + str(test_duration) + ' s to write 1000 lines.')