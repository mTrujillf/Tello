#Copyright © 2018 Naturalpoint
#
#Licensed under the Apache License, Version 2.0 (the "License")
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at
#
#http://www.apache.org/licenses/LICENSE-2.0
#
#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.


# OptiTrack NatNet direct depacketization sample for Python 3.x
#
# Uses the Python NatNetClient.py library to establish a connection (by creating a NatNetClient),
# and receive data via a NatNet connection and decode it using the NatNetClient library.

import sys
import time
from NatNetClient import NatNetClient
import DataDescriptions
import MoCapData
import math
#import detectorTeclas as dt
import numpy as np
from time import sleep
import libardrone

def altura_deseada1_int(t,yaw,x,y,z,ize):
    
    a = 0.75
    f = 0.03
    w1 = 2 * math.pi * f
    kp = 80.0
    kr = 40.0
        
    f2 = 0.025
    w3 = 2 * math.pi * f2
    
    ki = 5
    
    zDes = -0.8
    ze   = z - zDes
    zDesdot = 0
    w = kp * ze - zDesdot + ki*ize
    
    ize = ize + 0.5*ze
    
    
    #dwhdot = gamma*(-w + dwh - gamma*z)
    #dwh = dwh + .05 * dwhdot
    
    #w = -w
    
    return 0,0,int(w),0,ize

def altura_deseada1(t,yaw,x,y,z,dwh):
    
    a = 0.75
    f = 0.03
    w1 = 2 * math.pi * f
    kp = 80.0
    kr = 40.0
        
    f2 = 0.025
    w3 = 2 * math.pi * f2
    
    gamma = -20
    
    zDes = -0.8
    ze   = z - zDes
    zDesdot = 0
    w = kp * ze - zDesdot + dwh - gamma * z
    
    
    dwhdot = gamma*(-w + dwh - gamma*z)
    dwh = dwh + .05 * dwhdot
    
    #w = -w
    
    return 0,0,int(w),0,dwh

def altura_deseada2(t,yaw,x,y,z,dwh):
    
    a = 0.75
    f = 0.03
    w1 = 2 * math.pi * f
    kp = 80.0
    kr = 40.0
        
    f2 = 0.025
    w3 = 2 * math.pi * f2
    
    gamma = -10
    
    zDes = -1.3
    ze   = z - zDes
    zDesdot = 0
    w = kp * ze - zDesdot + dwh - gamma * z
    
    
    dwhdot = gamma*(-w + dwh - gamma*z)
    dwh = dwh + .05 * dwhdot
    
    #w = -w
    
    return 0,0,int(w),0,dwh




def circulo_con_rotacion (t,yaw,x,y,z,dwh):
    
    a = 0.5
    f = 0.03
    w1 = 2 * math.pi * f
    kp = 80.0
    kr = 40.0
        
    f2 = 0.025
    w3 = 2 * math.pi * f2
    
    xDes = a * math.sin(w1*t)
    xe = x - xDes
    xDesdot = a*w1*math.cos(w1*t)
    
    
    yDes = a * math.cos(w1*t)
    ye = y - yDes
    yDesdot = -a*w1*math.sin(w1*t)
    
    xMatrix = np.array([x,y])
    xDesMatrix = np.array([xDes,yDes])
    
    Rpsi = np.array([[math.cos(yaw),-math.sin(yaw)],[math.sin(yaw),math.cos(yaw)]])
    psiDes= math.atan2(yDes,xDes)-math.pi/2
    RpsiDes = np.array([[math.cos(psiDes),-math.sin(psiDes)],[math.sin(psiDes),math.cos(psiDes)]])
    RpsiT = Rpsi.transpose()
    
    xeMatrix = xMatrix - xDesMatrix
    
    xDesdotMatrix = np.array([xDesdot,yDesdot])
    
    vMatrix = np.dot(RpsiT ,(xDesdotMatrix - (kp*xeMatrix)))
    
    psiDesdot = ((xDes*yDesdot) - (yDes*xDesdot))/(a*a)
    
    RpsiDesdot = np.array([[(-math.sin(psiDes)*psiDesdot),(-math.cos(psiDes)*psiDesdot)],
                  [(math.cos(psiDes)*psiDesdot),(-math.sin(psiDes)*psiDesdot)]])
    
    RpsiDesT = RpsiDes.transpose()
    
    RpsiDesRpsiDesdot = np.dot(RpsiDesT,RpsiDesdot)
    
    
    Rgorro = np.dot(RpsiDesT,Rpsi)
    RgorroT = Rgorro.transpose()
    Pa = (1/2) *  (Rgorro - RgorroT)
    paElemento = Pa[1][0]
    
    rd = RpsiDesRpsiDesdot[1][0]
    
    
    r = rd - kr * paElemento
    u = int(vMatrix[0])
    v = int(vMatrix[1])
    
    gamma = 0
    
    
    
    zDes = -1.0
    ze   = z - zDes
    zDesdot = 0
    w = -kp * ze + zDesdot - dwh + gamma * z
    w = -w
    
    dwhdot = gamma*(w + dwh - gamma*z)
    dwh = dwh + .05 * dwhdot
    
    return int(v),int(u),int(w),int(r),dwh



def sin_sobre_z(t,yaw,x,y,z,dwh):
    a = 0.5
    f = 0.03
    w1 = 2 * math.pi * f
    kp = 110.0
    kr = 40.0
        
    f2 = 0.025
    w3 = 2 * math.pi * f2
    
    zDes = -1.5 + a * math.sin(w1*t)
    zDesdot = a*w1*math.cos(w1*t)
    ze   = z - zDes
    w = -kp * (ze + zDesdot)
    w = -w
  
    return 0,0,int(w),0,dwh


def despegue_manual (t,yaw,x,y,z,dwh):
    
    a0 = 0.125
    a1 = 8
    hd = -1.0
    kp = 40
    
    zd = hd*((math.tanh(a0*(t-a1)) +1)/2)
    
    zdDot =  a0*(hd)*(math.tanh(a0*(t-a1))*math.tanh(a0*(t-a1))-1)
    
    ze = z - zd
    
    w = -kp*ze + zdDot
    w = -w
    
    return 0,0,int(w),0,dwh


# This is a callback function that gets connected to the NatNet client
# and called once per mocap frame.
def receive_new_frame(data_dict):
    order_list=[ "frameNumber", "markerSetCount", "unlabeledMarkersCount", "rigidBodyCount", "skeletonCount",
                "labeledMarkerCount", "timecode", "timecodeSub", "timestamp", "isRecording", "trackedModelsChanged" ]
    dump_args = False
    if dump_args == True:
        out_string = "    "
        for key in data_dict:
            out_string += key + "="
            if key in data_dict :
                out_string += data_dict[key] + " "
            out_string+="/"
        print(out_string)

# This is a callback function that gets connected to the NatNet client. It is called once per rigid body per frame
def receive_rigid_body_frame( new_id, position, rotation,frame_actual,dwh):

    if frame_actual%6 == 0:
        if (new_id == 3):
            #t_frame = (self.frame_actual - start_frame) * 1/120
            #metodo = getKeyboradInput(metodo)#Detecta si se apretó alguna tecla para detener.
            t = time.time() - timeStart 
            datos_vuelta = list()
            pos_actual = position
            rot_actual = rotation
            t_nano = time.time_ns() - t_nano_start 
            x = -pos_actual[0]
            z = -pos_actual[1]
            y = -pos_actual[2]
            
            x = np.float32(x)
            z = np.float32(z)
            y = np.float32(y)
            
            q11,q31,q21,q01 = rot_actual
                
            roll = math.atan(((2 * q21*q31) + (2 * q01*q11))/((2 * q01*q01) + (2 * q31*q31) - 1 ))
            pitch = (-math.asin((2 * q11*q31) - (2 * q01*q21)))
            yaw = math.atan2(((2 * q11*q21) + (2*q01*q31)), ((2 * q01*q01) + (2 * q11*q11) - 1)) 
            yaw = -yaw
            yaw =  np.float32(yaw)

            v,u,w,r,dwh = metodo(t,yaw,x,y,z,dwh)
            
            #datos_vuelta.append(xDes)
            datos_vuelta.append(x)
            #datos_vuelta.append(yDes)
            datos_vuelta.append(y)
            datos_vuelta.append(z)
            datos_vuelta.append(v)
            datos_vuelta.append(u)
            datos_vuelta.append(w)
            datos_vuelta.append(r)
            datos_vuelta.append(dwh)
    #        datos_vuelta.append(t_frame)
            datos_vuelta.append(t)
            datos_vuelta.append(frame_actual)
            
            datos.append(datos_vuelta)
            

    
            print("----------------------------------------")
    #            print("Frame:                 " + str(self.frame_actual))
            #print("Tiempo sin frame:      " + str(t))
    #            print("Tiempo con frame:      " + str(t_frame))
            #print("Determinante de yaw:   " + str(yaw))
            print("v:                     " + str(v))
            print("u:                     " + str(u))
            print("w:                     " + str(w))
            print("r:                     " + str(r))
            print("Determinante de x:     " + str(x))
            print("Determinante de y:     " + str(y))
            print("Determinante de z:     " + str(z))
            #print("Determinante de t:     " + str(t))                
            print("----------------------------------------")
            
            
            v = v/100
            u = -u/100
            w = w/100
            r = r/100
            arDrone.move(v, u, w, r)
            #tello.send_rc_control(v, u, w, r)
            #contVueltasDadas = contVueltasDadas + 1
            
    return dwh

def escribe_final ():

    streaming_client.shutdown()
    arDrone.land()
    timeFinal = time.time() - timeStart
    file = open('vuelo.txt','w')
    for item in datos:
        for rc in item:
            file.write(str(rc) + ",")
        file.write("\n")
    file.write(str(timeFinal))
    file.close()

def add_lists(totals, totals_tmp):
    totals[0]+=totals_tmp[0]
    totals[1]+=totals_tmp[1]
    totals[2]+=totals_tmp[2]
    return totals

def print_configuration(natnet_client):
    natnet_client.refresh_configuration()
    print("Connection Configuration:")
    print("  Client:          %s"% natnet_client.local_ip_address)
    print("  Server:          %s"% natnet_client.server_ip_address)
    print("  Command Port:    %d"% natnet_client.command_port)
    print("  Data Port:       %d"% natnet_client.data_port)

    if natnet_client.use_multicast:
        print("  Using Multicast")
        print("  Multicast Group: %s"% natnet_client.multicast_address)
    else:
        print("  Using Unicast")

    #NatNet Server Info
    application_name = natnet_client.get_application_name()
    nat_net_requested_version = natnet_client.get_nat_net_requested_version()
    nat_net_version_server = natnet_client.get_nat_net_version_server()
    server_version = natnet_client.get_server_version()

    print("  NatNet Server Info")
    print("    Application Name %s" %(application_name))
    print("    NatNetVersion  %d %d %d %d"% (nat_net_version_server[0], nat_net_version_server[1], nat_net_version_server[2], nat_net_version_server[3]))
    print("    ServerVersion  %d %d %d %d"% (server_version[0], server_version[1], server_version[2], server_version[3]))
    print("  NatNet Bitstream Requested")
    print("    NatNetVersion  %d %d %d %d"% (nat_net_requested_version[0], nat_net_requested_version[1],\
       nat_net_requested_version[2], nat_net_requested_version[3]))
    #print("command_socket = %s"%(str(natnet_client.command_socket)))
    #print("data_socket    = %s"%(str(natnet_client.data_socket)))


def print_commands(can_change_bitstream):
    outstring = "Commands:\n"
    outstring += "Return Data from Motive\n"
    outstring += "  s  send data descriptions\n"
    outstring += "  r  resume/start frame playback\n"
    outstring += "  p  pause frame playback\n"
    outstring += "     pause may require several seconds\n"
    outstring += "     depending on the frame data size\n"
    outstring += "Change Working Range\n"
    outstring += "  o  reset Working Range to: start/current/end frame = 0/0/end of take\n"
    outstring += "  w  set Working Range to: start/current/end frame = 1/100/1500\n"
    outstring += "Return Data Display Modes\n"
    outstring += "  j  print_level = 0 supress data description and mocap frame data\n"
    outstring += "  k  print_level = 1 show data description and mocap frame data\n"
    outstring += "  l  print_level = 20 show data description and every 20th mocap frame data\n"
    outstring += "Change NatNet data stream version (Unicast only)\n"
    outstring += "  3  Request 3.1 data stream (Unicast only)\n"
    outstring += "  4  Request 4.1 data stream (Unicast only)\n"
    outstring += "t  data structures self test (no motive/server interaction)\n"
    outstring += "c  show configuration\n"
    outstring += "h  print commands\n"
    outstring += "q  quit\n"
    outstring += "\n"
    outstring += "NOTE: Motive frame playback will respond differently in\n"
    outstring += "       Endpoint, Loop, and Bounce playback modes.\n"
    outstring += "\n"
    outstring += "EXAMPLE: PacketClient [serverIP [ clientIP [ Multicast/Unicast]]]\n"
    outstring += "         PacketClient \"192.168.10.14\" \"192.168.10.14\" Multicast\n"
    outstring += "         PacketClient \"127.0.0.1\" \"127.0.0.1\" u\n"
    outstring += "\n"
    print(outstring)

def request_data_descriptions(s_client):
    # Request the model definitions
    s_client.send_request(s_client.command_socket, s_client.NAT_REQUEST_MODELDEF,    "",  (s_client.server_ip_address, s_client.command_port) )

def test_classes():
    totals = [0,0,0]
    print("Test Data Description Classes")
    totals_tmp = DataDescriptions.test_all()
    totals=add_lists(totals, totals_tmp)
    print("")
    print("Test MoCap Frame Classes")
    totals_tmp = MoCapData.test_all()
    totals=add_lists(totals, totals_tmp)
    print("")
    print("All Tests totals")
    print("--------------------")
    print("[PASS] Count = %3.1d"%totals[0])
    print("[FAIL] Count = %3.1d"%totals[1])
    print("[SKIP] Count = %3.1d"%totals[2])

def my_parse_args(arg_list, args_dict):
    # set up base values
    arg_list_len=len(arg_list)
    if arg_list_len>1:
        args_dict["serverAddress"] = arg_list[1]
        if arg_list_len>2:
            args_dict["clientAddress"] = arg_list[2]
        if arg_list_len>3:
            if len(arg_list[3]):
                args_dict["use_multicast"] = True
                if arg_list[3][0].upper() == "U":
                    args_dict["use_multicast"] = False

    return args_dict

def aterriza(t,yaw,x,y,z):
    
    a0 = 0.125
    a1 = 8
    hd = -1.0
    kp = 40
    
    zd = hd*((math.tanh(a0*(t-a1)) -1)/2)
    
    zdDot =  a0*(hd)*(math.tanh(a0*(t-a1))*math.tanh(a0*(t-a1))+1)
    
    ze = z - zd
    
    w = -kp*ze + zdDot
    w = -w
    
    return 0,0,int(w),0


if __name__ == "__main__":

    optionsDict = {}
    optionsDict["clientAddress"] = "192.168.1.146"
    optionsDict["serverAddress"] = "192.168.1.132"
    optionsDict["use_multicast"] = True

    # This will create a new NatNet client
    optionsDict = my_parse_args(sys.argv, optionsDict)
    streaming_client = NatNetClient()
    streaming_client.set_client_address(optionsDict["clientAddress"])
    streaming_client.set_server_address(optionsDict["serverAddress"])
    streaming_client.set_use_multicast(optionsDict["use_multicast"])
    
    
    print("1")
    #dt.init()
    arDrone = libardrone.ARDrone()
    print('2')
    arDrone.takeoff()
    print('3')
    #arDrone.move(0, 0, 0, 0)
    datos = list()
    sleep(3)
            
    timeStart = time.time()
    cont = 0
    t = 0.0
    contTotal = 0
    cont_frame = 0

    #start_frame = self.frame_actual
    #metodo = self.circulo_con_rotacion
    #frame_actual_vuelta = self.frame_actual
    t_nano_start = time.time_ns()
    t_start = time.time()
    metodo = circulo_con_rotacion

    # Configure the streaming client to call our rigid body handler on the emulator to send data out.
    streaming_client.new_frame_listener = receive_new_frame
    streaming_client.rigid_body_listener = receive_rigid_body_frame
    # Start up the streaming client now that the callbacks are set up.
    # This will run perpetually, and operate on a separate thread.
    
    
    
    is_running = streaming_client.run()
    if not is_running:
        print("ERROR: Could not start streaming client.")
        try:
            sys.exit(1)
        except SystemExit:
            print("...")
        finally:
            print("exiting")

    is_looping = True
    time.sleep(1)
    if streaming_client.connected() is False:
        print("ERROR: Could not connect properly.  Check that Motive streaming is on.")
        try:
            sys.exit(2)
        except SystemExit:
            print("...")
        finally:
            print("exiting")

    print_configuration(streaming_client)
    print("\n")
    print_commands(streaming_client.can_change_bitstream_version())


    while is_looping:
        inchars = input('Enter command or (\'h\' for list of commands)\n')
        
        if len(inchars)>0:
            c1 = inchars[0].lower()
            if c1 == 'h' :
                print_commands(streaming_client.can_change_bitstream_version())
            elif c1 == 'c' :
                print_configuration(streaming_client)
            elif c1 == 's':
                request_data_descriptions(streaming_client)
                time.sleep(1)
            elif c1 == 'y':
                metodo = altura_deseada2
            elif c1 == 'm':
                escribe_final()
                cont = 0
                while cont < 100:
                    arDrone.land()
                    cont += 1
                arDrone.halt()
            elif c1 == 'u':
                t_start = time.time()
                metodo = aterriza
                sleep(1.5)
                escribe_final()
            elif (c1 == '3') or (c1 == '4'):
                if streaming_client.can_change_bitstream_version():
                    tmp_major = 4
                    tmp_minor = 1
                    if(c1 == '3'):
                        tmp_major = 3
                        tmp_minor = 1
                    return_code = streaming_client.set_nat_net_version(tmp_major,tmp_minor)
                    time.sleep(1)
                    if return_code == -1:
                        print("Could not change bitstream version to %d.%d"%(tmp_major,tmp_minor))
                    else:
                        print("Bitstream version at %d.%d"%(tmp_major,tmp_minor))
                else:
                    print("Can only change bitstream in Unicast Mode")

            elif c1 == 'p':
                sz_command="TimelineStop"
                return_code = streaming_client.send_command(sz_command)
                time.sleep(1)
                print("Command: %s - return_code: %d"% (sz_command, return_code) )
            elif c1 == 'r':
                sz_command="TimelinePlay"
                return_code = streaming_client.send_command(sz_command)
                print("Command: %s - return_code: %d"% (sz_command, return_code) )
            elif c1 == 'o':
                tmpCommands=["TimelinePlay",
                            "TimelineStop",
                            "SetPlaybackStartFrame,0",
                            "SetPlaybackStopFrame,1000000",
                            "SetPlaybackLooping,0",
                            "SetPlaybackCurrentFrame,0",
                            "TimelineStop"]
                for sz_command in tmpCommands:
                    return_code = streaming_client.send_command(sz_command)
                    print("Command: %s - return_code: %d"% (sz_command, return_code) )
                time.sleep(1)
            elif c1 == 'w':
                tmp_commands=["TimelinePlay",
                            "TimelineStop",
                            "SetPlaybackStartFrame,10",
                            "SetPlaybackStopFrame,1500",
                            "SetPlaybackLooping,0",
                            "SetPlaybackCurrentFrame,100",
                            "TimelineStop"]
                for sz_command in tmp_commands:
                    return_code = streaming_client.send_command(sz_command)
                    print("Command: %s - return_code: %d"% (sz_command, return_code) )
                time.sleep(1)
            elif c1 == 't':
                test_classes()

            elif c1 == 'j':
                streaming_client.set_print_level(0)
                print("Showing only received frame numbers and supressing data descriptions")
            elif c1 == 'k':
                streaming_client.set_print_level(1)
                print("Showing every received frame")

            elif c1 == 'l':
                print_level = streaming_client.set_print_level(20)
                print_level_mod = print_level % 100
                if(print_level == 0):
                    print("Showing only received frame numbers and supressing data descriptions")
                elif (print_level == 1):
                    print("Showing every frame")
                elif (print_level_mod == 1):
                    print("Showing every %dst frame"%print_level)
                elif (print_level_mod == 2):
                    print("Showing every %dnd frame"%print_level)
                elif (print_level == 3):
                    print("Showing every %drd frame"%print_level)
                else:
                    print("Showing every %dth frame"%print_level)

            elif c1 == 'q':
                is_looping = False
                arDrone.land()
                escribe_final()
                
                break
            else:
                print("Error: Command %s not recognized"%c1)
            print("Ready...\n")
    print("exiting")
