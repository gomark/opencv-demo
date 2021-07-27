camera_running = False
i = 1
j = 2

def test1():    
    global camera_running
    print('camera_running=' + str(camera_running))
    
    if (camera_running == True):
        exit

    camera_running = True

test1()
print(camera_running)