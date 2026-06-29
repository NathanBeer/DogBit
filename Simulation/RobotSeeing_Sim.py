import pybullet as p

def look_for_object(target_id, robot_id, threshold=1.0):
    pos_r, _ = p.getBasePositionAndOrientation(robot_id)
    pos_t, _ = p.getBasePositionAndOrientation(target_id)
    dist = ((pos_r[0]-pos_t[0])**2 + (pos_r[1]-pos_t[1])**2)**0.5
    return dist < threshold