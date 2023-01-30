
import queue
import threading
import time
import json
import random 

class post_to_server(threading.Thread):
    def __init__(self,name):
        threading.Thread.__init__(self)
        #characterizes the type of thread. Should this be
        self.name = name
    
    def run(self):
        #accesses the queues and puts data inside. 
        print("Running a Post Thread - Takes Value from Queue")
        simulate_server(self.name)
        print("Thread is Terminating",self.name)
        

def init_queue(make_q):
    curr_time = time.time()
    elapse_time = 0
    try:
        while elapse_time<15:
            elapse_time = time.time()-curr_time

            gen_random = random.randint(0,9)
            with open("debug.txt","a") as outp:
                outp.write(str(gen_random)+"\n")
            outp.close()
            time.sleep(0.4)

            make_q.put(gen_random)
    except KeyboardInterrupt:
        return


def simulate_server(thread_name):
    curr_time = time.time()

    elapse_time = 0 

    while elapse_time<15:
        elapse_time = time.time()-curr_time
        try:
            get_val = make_q.get(block=False)
            # if KeyboardInterrupt:
            #     break
        except queue.Empty:
            # if KeyboardInterrupt:
            #     break
            continue

        else:
            #posts this value to a JSON    
            # if KeyboardInterrupt:
            #     break          
            dict_val = {"temperature":get_val,"Thread":thread_name}
            with open("my_test.json","a") as outp:
                json.dump(dict_val,outp)
                json.dump("\n",outp)
            outp.close()
    return

    


#makes a queue where we can push data
make_q = queue.Queue()

#puts value into the multithreaded target
value_thread = threading.Thread(target=init_queue,args=(make_q,),daemon=True)

thread_post = post_to_server("my_test")
value_thread.start()
thread_post.start()

curr_time = time.time()

elapse_time = 0 
print("first elapse",elapse_time)
while elapse_time<15:
    elapse_time = time.time()-curr_time

value_thread.join()
thread_post.join()
