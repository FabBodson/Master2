import Lab1_Agents_Task1_World as World
import random


def random_agent():
    # Choose a direction
    move = random.choice(["turn_left", "turn_right", "forward", "backward"])

    # Choose how long will the robot move in that direction
    moving_time = random.randint(4000, 10000)

    # Choose speed
    speed = random.randint(1, 6)

    if move == "turn_left":
        print(f"Moving left for {moving_time // 1000} seconds")  # The '//1000' is for a proper layout
        motorSpeed = dict(speedLeft=0, speedRight=speed)

    elif move == "turn_right":
        print(f"Moving right for {moving_time // 1000} seconds")
        motorSpeed = dict(speedLeft=speed, speedRight=0)

    elif move == "forward":
        print(f"Moving forward for {moving_time // 1000} seconds")
        motorSpeed = dict(speedLeft=speed, speedRight=speed)

    elif move == "backward":
        print(f"Moving backward for {moving_time // 1000} seconds")
        motorSpeed = dict(speedLeft=-speed, speedRight=-speed)

    else:
        motorSpeed = dict(speedLeft=0, speedRight=0)

    return motorSpeed, moving_time


class FixedAgent:
    def __init__(self):
        # Initialization of the time of the sequences
        self.time_sequence = 0

    def move(self, simulationTime):

        motorSpeed = dict(speedLeft=0, speedRight=0)
        speed = 3

        # Here is the sequence of operations
        # We take the actual time of the simulation and substract the start time of the sequence to get the difference
        # of time since the beginning of the sequence. So we can compare the time spend for each moving.

        # This is to adjust the Pioneer at the start of the sequence
        if (simulationTime - self.time_sequence) < 200:
            motorSpeed = dict(speedLeft=speed, speedRight=0)

        elif (simulationTime - self.time_sequence) < 19000:
            motorSpeed = dict(speedLeft=speed, speedRight=speed)

        # This is a turn left
        elif (simulationTime - self.time_sequence) < 20855:
            motorSpeed = dict(speedLeft=0, speedRight=speed)

        elif (simulationTime - self.time_sequence) < 39000:
            motorSpeed = dict(speedLeft=speed, speedRight=speed)

        elif (simulationTime - self.time_sequence) < 40850:
            motorSpeed = dict(speedLeft=0, speedRight=speed)

        elif (simulationTime - self.time_sequence) < 50000:
            motorSpeed = dict(speedLeft=speed, speedRight=speed)

        elif (simulationTime - self.time_sequence) < 51900:
            motorSpeed = dict(speedLeft=0, speedRight=speed)

        elif (simulationTime - self.time_sequence) < 54000:
            motorSpeed = dict(speedLeft=speed, speedRight=speed)

        elif (simulationTime - self.time_sequence) < 55850:
            motorSpeed = dict(speedLeft=speed, speedRight=0)

        elif (simulationTime - self.time_sequence) < 61000:
            motorSpeed = dict(speedLeft=speed, speedRight=speed)

        elif (simulationTime - self.time_sequence) < 62900:
            motorSpeed = dict(speedLeft=speed, speedRight=0)

        elif (simulationTime - self.time_sequence) < 65000:
            motorSpeed = dict(speedLeft=speed, speedRight=speed)

        elif (simulationTime - self.time_sequence) < 66900:
            motorSpeed = dict(speedLeft=0, speedRight=speed)

        elif (simulationTime - self.time_sequence) < 71000:
            motorSpeed = dict(speedLeft=speed, speedRight=speed)

        elif (simulationTime - self.time_sequence) < 72900:
            motorSpeed = dict(speedLeft=0, speedRight=speed)

        elif (simulationTime - self.time_sequence) < 92000:
            motorSpeed = dict(speedLeft=speed, speedRight=speed)

        elif (simulationTime - self.time_sequence) < 93750:
            motorSpeed = dict(speedLeft=0, speedRight=speed)

        else:
            print("End of sequence.\nSequence time reset to 0")
            self.time_sequence = simulationTime

        World.setMotorSpeeds(motorSpeed)
        print("Trying to collect a block...", World.collectNearestBlock()[0])


class MemoryAgent:
    def __init__(self):
        # Key is blockName and Value is distance to block
        self.memory = {}

    def move(self, simulationTime):
        left_sensor = World.getSensorReading("ultraSonicSensorLeft")
        right_sensor = World.getSensorReading("ultraSonicSensorRight")
        energy = World.getSensorReading("energySensor")

        left_speed = 1
        right_speed = 1

        if energy['direction'] < 0:
            # Collecting the return message and block info
            got_block, block = World.collectNearestBlock()
            print("Trying to collect a block...", got_block, block)

            # If a block was collected, saving its name and time of collection to the memory
            if got_block == "Energy collected :)":
                self.memory[block[0]] = block[1]

            if right_sensor < 0.5:
                right_speed = 0.5
                left_speed = 0
            else:
                right_speed = 1.5
                left_speed = 0.5

        else:
            got_block, block = World.collectNearestBlock()
            print("Trying to collect a block...", got_block, block)
            if got_block == "Energy collected :)":
                self.memory[block[0]] = block[1]

            if left_sensor < 0.5:
                right_speed = 0
                left_speed = 0.5

        motorSpeed = dict(speedLeft=left_speed, speedRight=right_speed)
        World.setMotorSpeeds(motorSpeed)

        # Checking if there is minimum 1 element in the dictionary
        if self.memory:
            # Getting time when last block was collected
            last_block_time = list(self.memory.values())[-1]

            # If it's been more thant 10 seconds since the last block was collected,
            # the strategy becomes random for some random time then come back to reflex strategy
            if (simulationTime - last_block_time) >= 10000:
                print("CHANGING STRATEGY TO RANDOM")
                # The memory is reset so it will not be biased next iteration
                self.memory = {}
                motorSpeed, moving_time = random_agent()
                stop_time = simulationTime + moving_time
                if simulationTime < stop_time:
                    World.execute(motorSpeed, moving_time, -1)

                print("END OF RANDOM STRATEGY")
