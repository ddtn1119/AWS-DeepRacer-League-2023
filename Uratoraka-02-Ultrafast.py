import math

def reward_function(params):
    # read input parameters
    speed = params['speed']
    car_on_track = params['all_wheels_on_track']
    heading = params['heading']
    steering_angle = params['steering_angle']
    waypoints = params['waypoints']
    closestWaypoints = params['closest_waypoints']
    
    # initialize reward weight
    speedWeight = 100
    headWeight = 100
    steerWeight = 50

    # initialize the reward based on current speed
    maxspReward = 10 * 10
    minspReward = 3.5 * 3.5
    absspReward = pow(speed, 2)
    speedReward = (absspReward - minspReward) / (maxspReward - minspReward) * speedWeight
    
    # penalize the car if it goes off track
    if not car_on_track:
        return 0.001
    
    # penalize the car if slow speed action space
    # the unit of speed is in m/s
    # penalize the car if the speed is less than 1 m/s
    if speed < 1.5:
        return 0.001
    elif (speed >= 1.5 and speed < 2.0):
        speedReward += 1 # reward additional 1 point if the speed is between 1.5 m/s and 1.99 m/s
    elif (speed >= 2.0 and speed < 3.5):
        speedReward += 5 # reward additional 5 points if the speed is between 2.0 m/s and 3.49 m/s
    elif (speed >= 3.5 and speed <= 4.0):
        speedReward += 10 # reward additional 10 points if the speed is between 3.5 m/s and 4.0 m/s
    
    # calculate the direction of the center line based on the closest waypoints
    prev_point = waypoints[closestWaypoints[0]]
    next_point = waypoints[closestWaypoints[1]]

    # calculate the direction by using the method arctan2(dy, dx), the result would be (-π, π) in radians
    dy = next_point[1] - prev_point[1]
    dx = next_point[0] - prev_point[0]
    trackDirection = math.atan2(dy, dx) 
    
    # convert the direction from radians to degrees
    trackDirection = math.degrees(trackDirection)

    # calculate the difference between the track direction and the car's heading direction
    directionDiff = abs(trackDirection - heading)
    if directionDiff > 180:
        directionDiff = 360 - directionDiff
    
    abs_headReward = 1 - (directionDiff / 180.0)
    headReward = abs_headReward * headWeight
    
    # reward the car if the steering angle is aligned with the direction difference
    abs_steering_reward = 1 - (abs(steering_angle - directionDiff) / 180.0)
    steerReward = abs_steering_reward * steerWeight

    # return the total reward
    totalReward = speedReward + headReward + steerReward
    return totalReward
