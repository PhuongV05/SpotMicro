import math 
import csv
# Walking_Kinematics_6 implements stable gaits
# moves one leg at a time to ensure centre of mass is within footprint
L1 = 11.5
L2 = 12

# main runtime code calls on functions to swing each leg
def leg_move(L1, L2):
    f = open('E:\Working From Home\__Sixth Form\Computer Science\Computer Science NEA\spotmicroai\Walk_Angles.csv', 'w')
    f.truncate()
    rear_left_swing(L1, L2, f)
    front_right_swing(L1, L2, f)
    rear_right_swing(L1, L2, f)
    front_left_swing(L1, L2, f)
    f.close()
    
# find angles when x-coordinates are negative
def find_angles_n(x, y, z, L1, L2):
    L3 = (x**2 + z**2)**(1/2)
    angle_1 = math.atan(abs(x)/abs(z))
    angle_1 = (angle_1*180)/math.pi
    
    angle_2 = math.acos((L1**2+L3**2-L2**2)/(2*L1*L3))
    angle_2 = (angle_2*180)/math.pi
    
    angle_3 = 180 - (90 - (angle_2 + angle_1))
    
    angle_4 = math.acos((L1**2 + L2**2 - L3**2) / (2 * L1 * L2))
    angle_4 = (angle_4*180)/math.pi
    
    Leg_angle = angle_3
    Feet_angle = angle_4

    return Leg_angle, Feet_angle

# find angles when x-coordinates are positive
def find_angles_p(x, y, z, L1, L2):
    L3 = (x**2 + z**2)**(1/2)
    angle_1 = math.atan(abs(x)/abs(z))
    angle_1 = (angle_1*180)/math.pi
    
    angle_2 = math.acos((L1**2+L3**2-L2**2)/(2*L1*L3))
    angle_2 = (angle_2*180)/math.pi
    
    angle_3 = 180 - (90 - (angle_2 - angle_1))
    
    angle_4 = math.acos((L1**2 + L2**2 - L3**2) / (2 * L1 * L2))
    angle_4 = (angle_4*180)/math.pi
    
    Leg_angle = angle_3
    Feet_angle = angle_4

    return Leg_angle, Feet_angle

def find_angles_swing(x_swing, y_swing, z_swing, L1, L2):
    if x_swing <= 0:
        Leg_angle_swing, Feet_angle_swing = find_angles_n(x_swing, y_swing, z_swing, L1, L2)
    elif x_swing > 0:
        Leg_angle_swing, Feet_angle_swing = find_angles_p(x_swing, y_swing, z_swing, L1, L2)
    return Leg_angle_swing, Feet_angle_swing 
            
def find_angles_stand(x_stand, y_stand, z_stand, L1, L2):
    if x_stand <= 0:
        Leg_angle_stand, Feet_angle_stand = find_angles_n(x_stand, y_stand, z_stand, L1, L2)
    elif x_stand > 0: 
        Leg_angle_stand, Feet_angle_stand = find_angles_p(x_stand, y_stand, z_stand, L1, L2)
    return Leg_angle_stand, Feet_angle_stand 

# calculates swing phase of rear legs using position of x-swing
def swing_phase_rear(x_swing, L1, L2):
    z_swing = 2.5*(2.25-((x_swing)**2))**(1/2)-12
    # calculate and return angles
    Leg_angle_swing, Feet_angle_swing = find_angles_swing(x_swing, 0, z_swing, L1, L2)
    return Leg_angle_swing, Feet_angle_swing 

# calculates swing phase of front legs using position of x-swing
def swing_phase_front(x_swing, L1, L2):
    z_swing = 2.5*(2.25-((x_swing)**2))**(1/2)-10
    # calculate and return angles
    Leg_angle_swing, Feet_angle_swing = find_angles_swing(x_swing, 0, z_swing, L1, L2)
    return Leg_angle_swing, Feet_angle_swing 

# calculates stand phase of rear legs using position of x-stand, z-stand     
def stand_phase_rear(x_stand, z_stand, L1, L2):
    # calculate and return angles
    Leg_angle_stand, Feet_angle_stand = find_angles_stand(x_stand, 0, z_stand, L1, L2)
    return Leg_angle_stand, Feet_angle_stand

# calculates stand phase of front legs using position of x-stand, z-stand
def stand_phase_front(x_stand, z_stand, L1, L2):
    # calculate and return angles
    Leg_angle_stand, Feet_angle_stand = find_angles_stand(x_stand, 0, z_stand+2, L1, L2)
    return Leg_angle_stand, Feet_angle_stand
    
# swings rear left leg
def rear_left_swing(L1, L2, f):
    writer = csv.writer(f, lineterminator = '\n')
    # initial x-coordinates of legs, different starting point for each leg
    x_rear_left = -1.5
    x_rear_right = 0.5
    x_front_left = 1.5
    x_front_right = -0.5
    shoulder_rear = 80
    shoulder_front = 100
    leg_height_right = -10
    leg_height_left = -14
    # calculates rear left leg movements
    while x_rear_left <= 1.5:
        rear_leg_left, rear_feet_left = swing_phase_rear(x_rear_left, L1, L2)
        rear_leg_right, rear_feet_right = stand_phase_rear(x_rear_right, leg_height_right, L1, L2)
        front_leg_left, front_feet_left = stand_phase_front(x_front_left, leg_height_left, L1, L2)
        front_leg_right, front_feet_right = stand_phase_front(x_front_right, leg_height_right, L1, L2)
        # 20 increments
        # stand phase 3 times as long as swing phase
        # legs in stand phase while only one leg in swing phase at a time
        x_rear_left += 0.03
        x_rear_right -= 0.01
        x_front_left -= 0.01
        x_front_right -= 0.01
        row = [shoulder_front, rear_leg_left, rear_feet_left, shoulder_front, 180 - (rear_leg_right), 180 - (rear_feet_right), shoulder_rear, front_leg_left, front_feet_left, shoulder_rear, 180 - (front_leg_right), 180 - (front_feet_right)]
        writer.writerow(row)
        print(row)
    # calculate shoulder movement
    while shoulder_rear <= 90:
        rear_leg_left, rear_feet_left = stand_phase_rear(x_rear_left, leg_height_left, L1, L2)
        rear_leg_right, rear_feet_right = stand_phase_rear(x_rear_right, leg_height_right, L1, L2)
        front_leg_left, front_feet_left = stand_phase_front(x_front_left, leg_height_left, L1, L2)
        front_leg_right, front_feet_right = stand_phase_front(x_front_right, leg_height_right, L1, L2)
        # same number of shoulder increments as leg
        shoulder_rear += 1
        shoulder_front -= 1
        leg_height_right -= 0.2
        leg_height_left += 0.2
        # writes to Walk_Angles.csv
        row = [shoulder_front, rear_leg_left, rear_feet_left, shoulder_front, 180 - (rear_leg_right), 180 - (rear_feet_right), shoulder_rear, front_leg_left, front_feet_left, shoulder_rear, 180 - (front_leg_right), 180 - (front_feet_right)]
        writer.writerow(row)
        print(row)

# swings front right leg
def front_right_swing(L1, L2, f):
    writer = csv.writer(f, lineterminator = '\n')
    # initiate starting positions (end of last swing phase)
    x_rear_left = 1.5
    x_rear_right = -0.5
    x_front_left = 0.5
    x_front_right = -1.5
    shoulder_rear = 90
    shoulder_front = 90
    leg_height_right = -12
    leg_height_left = -12
    while shoulder_rear <= 100:
        rear_leg_left, rear_feet_left = stand_phase_rear(x_rear_left, leg_height_left, L1, L2)
        rear_leg_right, rear_feet_right = stand_phase_rear(x_rear_right, leg_height_right, L1, L2)
        front_leg_left, front_feet_left = stand_phase_front(x_front_left, leg_height_left, L1, L2)
        front_leg_right, front_feet_right = stand_phase_front(x_front_right, leg_height_right, L1, L2)
        shoulder_rear += 1
        shoulder_front -= 1
        leg_height_right -= 0.2
        leg_height_left += 0.2
        row = [shoulder_front, rear_leg_left, rear_feet_left, shoulder_front, 180 - (rear_leg_right), 180 - (rear_feet_right), shoulder_rear, front_leg_left, front_feet_left, shoulder_rear, 180 - (front_leg_right), 180 - (front_feet_right)]
        writer.writerow(row)
        print(row)
    while x_front_right <= 1.5:
        rear_leg_left, rear_feet_left = stand_phase_rear(x_rear_left, leg_height_left, L1, L2)
        rear_leg_right, rear_feet_right = stand_phase_rear(x_rear_right, leg_height_right, L1, L2)
        front_leg_left, front_feet_left = stand_phase_front(x_front_left, leg_height_left, L1, L2)
        front_leg_right, front_feet_right = swing_phase_front(x_front_right, L1, L2)
        x_rear_left -= 0.01
        x_rear_right -= 0.01
        x_front_left -= 0.01
        x_front_right += 0.03
        row = [shoulder_front, rear_leg_left, rear_feet_left, shoulder_front, 180 - (rear_leg_right), 180 - (rear_feet_right), shoulder_rear, front_leg_left, front_feet_left, shoulder_rear, 180 - (front_leg_right), 180 - (front_feet_right)]
        writer.writerow(row)
        print(row)

# rear right leg swing      
def rear_right_swing(L1, L2, f):
    writer = csv.writer(f, lineterminator = '\n')
    x_rear_left = 0.5
    x_rear_right = -1.5
    x_front_left = -0.5
    x_front_right = 1.5
    shoulder_rear = 100
    shoulder_front = 80
    leg_height_right = -14
    leg_height_left = -10
    while x_rear_right <= 1.5:
        rear_leg_left, rear_feet_left = stand_phase_rear(x_rear_left, leg_height_left, L1, L2)
        rear_leg_right, rear_feet_right = swing_phase_rear(x_rear_right, L1, L2)
        front_leg_left, front_feet_left = stand_phase_front(x_front_left, leg_height_left, L1, L2)
        front_leg_right, front_feet_right = stand_phase_front(x_front_right, leg_height_right, L1, L2)
        x_rear_left -= 0.01
        x_rear_right += 0.03
        x_front_left -= 0.01
        x_front_right -= 0.01
        row = [shoulder_front, rear_leg_left, rear_feet_left, shoulder_front, 180 - (rear_leg_right), 180 - (rear_feet_right), shoulder_rear, front_leg_left, front_feet_left , shoulder_rear, 180 - (front_leg_right), 180 - (front_feet_right)]
        writer.writerow(row)
        print(row)
    while shoulder_rear >= 90:
        rear_leg_left, rear_feet_left = stand_phase_rear(x_rear_left, leg_height_left, L1, L2)
        rear_leg_right, rear_feet_right = stand_phase_rear(x_rear_right, leg_height_right, L1, L2)
        front_leg_left, front_feet_left = stand_phase_front(x_front_left, leg_height_left, L1, L2)
        front_leg_right, front_feet_right = stand_phase_front(x_front_right, leg_height_right, L1, L2)
        shoulder_rear -= 1
        shoulder_front += 1
        leg_height_right += 0.2
        leg_height_left -= 0.2
        row = [shoulder_front, rear_leg_left, rear_feet_left, shoulder_front, 180 - (rear_leg_right), 180 - (rear_feet_right), shoulder_rear, front_leg_left, front_feet_left , shoulder_rear, 180 - (front_leg_right), 180 - (front_feet_right)]
        writer.writerow(row)
        print(row)
    
# front left leg swing
def front_left_swing(L1, L2, f):
    writer = csv.writer(f, lineterminator = '\n')
    x_rear_left = -0.5
    x_rear_right = 1.5
    x_front_left = -1.5
    x_front_right = 0.5
    shoulder_rear = 90
    shoulder_front = 90
    leg_height_right = -12
    leg_height_left = -12
    while shoulder_rear >= 80:
        rear_leg_left, rear_feet_left = stand_phase_rear(x_rear_left, leg_height_left, L1, L2)
        rear_leg_right, rear_feet_right = stand_phase_rear(x_rear_right, leg_height_right, L1, L2)
        front_leg_left, front_feet_left = stand_phase_front(x_front_left, leg_height_left, L1, L2)
        front_leg_right, front_feet_right = stand_phase_front(x_front_right, leg_height_right, L1, L2)
        shoulder_rear -= 1
        shoulder_front += 1
        leg_height_right += 0.2
        leg_height_left -= 0.2
        row = [shoulder_front, rear_leg_left, rear_feet_left, shoulder_front, 180 - (rear_leg_right), 180 - (rear_feet_right), shoulder_rear, front_leg_left, front_feet_left, shoulder_rear, 180 - (front_leg_right), 180 - (front_feet_right)]
        writer.writerow(row)
        print(row)
    while x_front_left <= 1.5:
        rear_leg_left, rear_feet_left = stand_phase_rear(x_rear_left, leg_height_left, L1, L2)
        rear_leg_right, rear_feet_right = stand_phase_rear(x_rear_right, leg_height_right, L1, L2)
        front_leg_left, front_feet_left = swing_phase_front(x_front_left, L1, L2)
        front_leg_right, front_feet_right = stand_phase_front(x_front_right, leg_height_right, L1, L2)
        x_rear_left -= 0.01
        x_rear_right -= 0.01
        x_front_left += 0.03
        x_front_right -= 0.01
        row = [shoulder_front, rear_leg_left, rear_feet_left, shoulder_front, 180 - (rear_leg_right), 180 - (rear_feet_right), shoulder_rear, front_leg_left, front_feet_left, shoulder_rear, 180 - (front_leg_right), 180 - (front_feet_right)]
        writer.writerow(row)
        print(row)
    
leg_move(L1, L2)
    