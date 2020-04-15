"""
The template of the main script of the machine learning process
"""

import games.arkanoid.communication as comm
from games.arkanoid.communication import ( \
    SceneInfo, GameStatus, PlatformAction
)

def ml_loop():
    """
    The main loop of the machine learning process

    This loop is run in a separate process, and communicates with the game process.

    Note that the game process won't wait for the ml process to generate the
    GameInstruction. It is possible that the frame of the GameInstruction
    is behind of the current frame in the game process. Try to decrease the fps
    to avoid this situation.
    """

    # === Here is the execution order of the loop === #
    # 1. Put the initialization code here.
    ball_served = False

    # 2. Inform the game process that ml process is ready before start the loop.
    comm.ml_ready()

    prev1=[1,1]
    prev2=[1,1]
    prev3=[1,1]
    # 3. Start an endless loop.
    while True:
        # 3.1. Receive the scene information sent from the game process.
        scene_info = comm.get_scene_info()

        # 3.2. If the game is over or passed, the game process will reset
        #      the scene and wait for ml process doing resetting job.
        if scene_info.status == GameStatus.GAME_OVER or \
            scene_info.status == GameStatus.GAME_PASS:
            # Do some stuff if needed
            ball_served = False

            # 3.2.1. Inform the game process that ml process is ready
            comm.ml_ready()
            continue

        # 3.3. Put the code here to handle the scene information
        if not ball_served:
            comm.send_instruction(scene_info.frame, PlatformAction.SERVE_TO_LEFT)
            ball_served = True
            
        cur=[0,0] # a,b
        cur = list(scene_info.ball)
        plat = list(scene_info.platform)
        prev = prev3 # p,q = a,b
        prev3 = prev2
        prev2 = prev1
        prev1 = cur
        #print(cur)
        #print(prev)
        #print(plat)

        
        
            
        
        if (cur[1]-prev[1] > 0 and cur[1] > 150): # b-q
            m = (cur[1]-prev[1])/(cur[0]-prev[0]) # (b-q)/(a-p)
            point = cur[0]+((400-cur[1])/m)
            #print(m)
            #print('before:')
            #print(point)

            if (point > 200):
                if (int(point / 200) == 1):
                    point = 400-point#-(200-cur[0])
                elif (int(point / 200) == 2):
                    point = point-400#-(200-cur[0])
                elif (int(point / 200) == 3):
                    point = 800-point#-(200-cur[0])
            elif (point < 0):
                if (int(point / 200) == 0):
                    point = -point#+cur[0]
                elif (int(point / 200) == -1):
                    point = 400+point#+cur[0]
                elif (int(point / 200) == -2):
                    point = 400-point#+cur[0]
            #elif (point >= 0 or point <= 200):
            #print("after:")
            #print(point)
            #print('(a,b)')
            #print(cur[0],',',cur[1])
            #print('m:',m)
            
            if (plat[0]+20 > point):
                comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
            elif (plat[0]+20 < point):
                comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
            else:
                comm.send_instruction(scene_info.frame, PlatformAction.NONE)
            '''
            if (m > 0):
                if (point > 200 and m < 1):
                    comm.send_instruction(scene_info.frame, PlatformAction.NONE)                       
                else:
                    if (plat[0]+20 >= point):
                        comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
                    elif (plat[0]+20 < point):
                        comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
            else:
                if(point < 0 and m < -1):
                    comm.send_instruction(scene_info.frame, PlatformAction.NONE)
                else:
                    if (plat[0]+20 >= point):
                        comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
                    elif (plat[0]+20 < point):
                        comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
        else:
            if(plat[0]+20 > 100):
                comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
            elif(plat[0]+20 < 100):
                comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
            else:
                comm.send_instruction(scene_info.frame, PlatformAction.NONE)
        '''

        
        
        # 3.4. Send the instruction for this frame to the game process
        if not ball_served:
            comm.send_instruction(scene_info.frame, PlatformAction.SERVE_TO_LEFT)
            ball_served = True
        #else:
        #    comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)

        
