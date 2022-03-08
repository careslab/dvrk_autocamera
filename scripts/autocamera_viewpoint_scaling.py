import numpy as np
import Queue

# pid = PID(1, 0.1, 0.05, setpoint=1)

class CameraMovementScaling:
    #This is a class that will start queues of tool movement and return a
    #value based on how much movement has happned with respect to a particular tool
    # for instance, if the left tool moves more than the right, the viepoint is \
    # scaled towards the left tool.  This is untested code. 

    def __init__(self):
        self.viewpoint = 0 # this is the returned ratio of the tool based on motion.
        
        #setup for two queues
        self.maxsize = 500 # 100 frames/ sec for 5 seconds.
        self.ltool_history = Queue.Queue(maxsize= self.maxsize)
        self.rtool_history = Queue.Queue(maxsize= self.maxsize)
        self.ltool_history.put(0)
        self.rtool_history.put(0) 
    
    def update(self, ltool, rtool):

        #if the history is full, remove the oldest value.
        if self.ltool_history.full():
            #remove an element from both.  FIFO... adds to the back removes from front.
            self.ltool_history.get()
            self.rtool_history.get()       
            print('popped')
        #add the new values to the queue
        self.ltool_history.put(ltool)
        self.rtool_history.put(rtool)

        #print(list(self.ltool_history.queue))

        #Should we wait until we have a full queue?

        right_tool_movement = 0
        left_tool_movement = 0

        #Take the derivitive of the tool movements thus far and add them together.
        left_tool_movement = np.sum(np.diff(list(self.ltool_history.queue)))
        right_tool_movement = np.sum(np.diff(list(self.ltool_history.queue)))

        print('LEFT')

        #if there is no movement, just return the mid point of the tools
        if (left_tool_movement + right_tool_movement) == 0:
            self.viewpoint = (ltool + rtool)/2
            #print(self.viewpoint)
        else: #if there is movment
            #compute the relative movment of each tool (0-1)
            relative_left = left_tool_movement/ (left_tool_movement + right_tool_movement);
            relative_right = 1.0 - relative_left
            #squew the midpoint between the left and right tool based on movement
            self.viewpoint = (ltool* relative_left + rtool * relative_right)
            print(self.viewpoint)
        
        return self.viewpoint

# Notes: make sure the queue's aren't filling up / is popping properly --> ITS GOOD, 
# check if the matrix math is being done properly (ltool / rtool), 
# check if np.diff and np.sum can be used with matrices