# InfIK
A 3D inverse kinematics solver for robotic systems with any number of linked servo motors

## Features
* Any number of joints are supported
* Each joint can be uniquely constrained in cartesian coordinate space along any axis
    * The number of constraints equals the number of joints
* Each servo motor's axis can be aligned in any direction relative to the previous joint
* The solver can also predict the absolute location of any joint in the system if the position of each servo is known

## Joints
All joints in a system can be modeled by the `Joint` object, which contains 5 fields (These fields are defined in the *local space* of the current joint, meaning they are independent of the other joints in the system):
* `alpha` (const): The angle the rotation axis makes with the x-axis when projected onto the xy plane.
* `beta` (const): The angle the rotation axis makes with the xy plane.
* `length` (const): The length of this joint's lever arm, which is perpandicular to the rotation axis (the next joint orbits this joint)
* `height` (const): The distance along the rotation axis from the last joint (how much the rotation point should be offset along the axis)
* `theta`: The position of the servo, or the angular position around the rotation axis
![Alt text](/Examples/local_joint.png)
* `Red`: The rotation axis
* `Blue`: The path traced by the next joint (end of arm) as it moves through a full rotation
* `Green`: The arm
* `Orange`: The local space of the next joint with the unit vectors `i`, `j`, and `k` corresponding to the `x`, `y`, and `z`-axis respectively

### Local Joint Space
As mentioned, a joint is purely defined in its local space:
* The x-axis is collinear with the line connecting this joint with the previous one (along the length of the previous joint's lever arm)
* The z-axis is parallel to the rotation axis
* The y-axis is the cross product of the x and z axes, and will always face "forward" such that increasing the previous joint's position will move the current joint in the direction of the y-axis

Note that `theta` is relative to the xy plane, meaning if `alpha`,`beta`, and `theta` are `0`, the arm will lie along the y-axis. Increasing `alpha` will rotate the arm counterclockwise around the z-axis, while `beta` will have no effect if `theta` is `0`. Increasing `theta` will rotate the arm counterclockwise around its rotation axis.

## Constraints
Constraints are simple and have 3 fields:
* `joint_index`: The index of the joint to place this constraint on
* `axis`: The cartesian axis to constrain (`x:0`, `y:1`, `z:2`)
* `value`: The constraint value; what value should the joint's global position have along `axis`?
As mentioned, for the system to be solvable, the number of constraints must equal the number of joints

## How to Use
1. Import `IK_3D.py` and create an `IKSystem` object to model the system
    * `joints`: List of the joints in the system in the order they are connected
    * `constraints`: Unordered list of constraints to be placed on the system
    * `allowed_error` (optional): The maximum allowed difference between two consecutive guesses (Default: `1e-3`)
    * `max_iterations` (optional): The maximum number of iterations allowed before the solver concludes that it failed to converge (Default: `100`)
        * If this number is reached, the success flag returned from the `Solver.solve()` method will be `False`
2. Solve the system by calling `Solver.solve(IKSystem)` on any `IKSystem` object, which will return a list of servo positions in the same order as the joints in the system
    * These positions can also be accessed directly from `joints` in the `IKSystem` object (`Joint.theta`)