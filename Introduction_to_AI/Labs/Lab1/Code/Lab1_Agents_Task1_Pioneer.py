# Make sure to have the server side running in V-REP:
# in a child script of a V-REP scene, add following command
# to be executed just once, at simulation start:
#
# simExtRemoteApiStart(19999)
# then start simulation, and run this program.
#
# IMPORTANT: for each successful call to simxStart, there
# should be a corresponding call to simxFinish at the end!

import Lab1_Agents_Task1_World as World
import model

# connect to the server
robot = World.init()
# print important parts of the robot
print(sorted(robot.keys()))

START_SEQ_TIME = World.getSimulationTime()


def base_simulation():
    ##############################################
    # Reasoning: figure out which action to take #
    ##############################################
    motorSpeed = dict(speedLeft=0, speedRight=0)

    if simulationTime < 5000:
        motorSpeed = dict(speedLeft=1, speedRight=1.5)
    elif simulationTime < 10000:
        motorSpeed = dict(speedLeft=-1.5, speedRight=-1.0)
    elif simulationTime < 15000:
        print("Turning for a bit...", )
        World.execute(dict(speedLeft=2, speedRight=-2), 15000, -1)
        print("... got dizzy, stopping!")
        print("BTW, nearest energy block is at:", World.getSensorReading("energySensor"))
    else:
        motorSpeed = dict(speedLeft=0, speedRight=0)

    return motorSpeed


def reflex_agent():
    # Getting the sensors
    left_sensor = World.getSensorReading("ultraSonicSensorLeft")
    right_sensor = World.getSensorReading("ultraSonicSensorRight")
    energy = World.getSensorReading("energySensor")

    # Defining a basic speed
    left_speed = 1
    right_speed = 1
    print(f"Energy distance = {energy['distance']}\tLeft sensor = {left_sensor}\tRight sensor = {right_sensor}")

    if energy['direction'] < 0:
        print("Trying to collect a block...", World.collectNearestBlock()[0])
        if right_sensor < 0.5:
            right_speed = 0.5
            left_speed = 0
        else:
            right_speed = 1.5
            left_speed = 0.5

    else:
        print("Trying to collect a block...", World.collectNearestBlock()[0])
        if left_sensor < 0.5:
            right_speed = 0
            left_speed = 0.5

    motorSpeed = dict(speedLeft=left_speed, speedRight=right_speed)
    print(f"Motor speed = {motorSpeed}")

    World.setMotorSpeeds(motorSpeed)


fixed_agent = model.FixedAgent()
memory_agent = model.MemoryAgent()

try:
    while robot:  # main Control loop
        #######################################################
        # Perception Phase: Get information about environment #
        #######################################################
        simulationTime = World.getSimulationTime()
        if simulationTime % 1000 == 0:
            # print some useful info, but not too often
            print('Time:', simulationTime, \
                  'ultraSonicSensorLeft:', World.getSensorReading("ultraSonicSensorLeft"), \
                  "ultraSonicSensorRight:", World.getSensorReading("ultraSonicSensorRight"))
        """
        ### Random ###
        motorSpeed, moving_time = model.random_agent()
        stop_time = simulationTime + moving_time
        if simulationTime < stop_time:
            World.execute(motorSpeed, moving_time, -1)
        else:
            World.execute(dict(speedLeft=2, speedRight=-2), 15000, -1)
    
        """
        """
        ### Fixed ###
        fixed_agent.move(simulationTime)
        """

        """
        ### Reflex ###
        reflex_agent()
        """


        ### Memory ###
        memory_agent.move(simulationTime)


except KeyboardInterrupt:
    print(f"Total simulation time : {simulationTime} ({simulationTime/1000}s)")
