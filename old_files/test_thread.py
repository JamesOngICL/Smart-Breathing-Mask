
import queue
import threading
import time

# Class
class RunThreader(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        print(f"Output \n ** Starting the thread - {self.name}")
        process_queue(self.name)
        print(f" ** Completed the thread - {self.name}")

# Process thr queue
def process_queue(queue_name):
    while True:
        try:
            value = my_queue.get(block=False)
        except queue.Empty:
            return
        else:
            print_multiply(value,queue_name)
            time.sleep(2)

# function to multiply
def print_multiply(x,name):
    output_value = []
    for i in range(1, x + 1):
        output_value.append(i * x)
        print(f" \n *** The multiplication result for the {x} is - {output_value}",i," From ",name)

# Input variables
input_values = [{"James":5},2, 4, 6, 5,10,3]

# fill the queue
my_queue = queue.Queue()
for x in input_values:
    my_queue.put(x)

#shows that 
print(my_queue.get())
time.sleep(1)
# initializing and starting 3 threads
thread1 = RunThreader('First')
thread2 = RunThreader('Second')

# Start the threads
thread1.start()
thread2.start()

'''

A lot of threads can be used and initialized but we should only use one.  

thread3.start()
thread4.start()

'''
# Join the threads
'''
Apparently it works as follows, if we don't do thread.join() we can't get the threads to merge values. 


'''
thread1.join()
thread2.join()



'''
# thread3.join()
# thread4.join()
'''