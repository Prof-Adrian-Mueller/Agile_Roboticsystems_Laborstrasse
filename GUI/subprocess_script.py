import rospy
import moveit_commander
import moveit_msgs.msg

def initialize_robot():
    rospy.init_node('dobot_controller', anonymous=True)

    robot = moveit_commander.RobotCommander()
    scene = moveit_commander.PlanningSceneInterface()
    group_name = "manipulator"  # Replace with your group name
    move_group = moveit_commander.MoveGroupCommander(group_name)

    return robot, scene, move_group

def move_robot(move_group, position):
    pose_goal = geometry_msgs.msg.Pose()
    pose_goal.orientation.w = 1.0
    pose_goal.position.x = position[0]
    pose_goal.position.y = position[1]
    pose_goal.position.z = position[2]

    move_group.set_pose_target(pose_goal)

    plan = move_group.go(wait=True)
    move_group.stop()
    move_group.clear_pose_targets()

    return plan

if __name__ == "__main__":
    robot, scene, move_group = initialize_robot()
    # Example: move to position (x, y, z)
    move_robot(move_group, [0.4, 0.1, 0.2])
