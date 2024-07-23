import numpy as np

class Joint:    
    alpha = 0 
    beta = 0
    theta = 0
    length = 0
    height = 0
    
    sin_t = 0
    cos_t = 1
    sin_a = 0
    cos_a = 1
    sin_b = 0
    cos_b = 1
        

    def __init__(self, alpha, beta, length, height):
        self.alpha = alpha
        self.beta = beta
        self.length = length
        self.height = height
        self.sin_a = np.sin(alpha)
        self.cos_a = np.cos(alpha)
        self.sin_b = np.sin(beta)
        self.cos_b = np.cos(beta)
    
    def setTheta(self, theta):
        self.theta = theta
        self.sin_t = np.sin(self.theta)
        self.cos_t = np.cos(self.theta)

    def getAxisVector(self):
        return np.array([
            self.cos_b * self.cos_a,
            self.cos_b * self.sin_a,
            self.sin_b
        ])

    def getUnitVector(self):
        return np.array([
            -self.sin_t * self.sin_b * self.cos_a - self.cos_t * self.sin_a,
            self.cos_t * self.cos_a - self.sin_t * self.sin_b * self.sin_a,
            self.sin_t * self.cos_b
        ])

    def getLocalPosition(self):
        return self.getUnitVector() * self.length + self.getAxisVector() * self.height

    def getGlobalPosition(self, joint_index, joints):
        summation = [0,0,0]
        for i in range(joint_index + 1):
            prod = joints[i].getLocalPosition()
            for j in range(i):
                prod = Util.linearTransformation(prod, joints[i - j - 1].getRotationMatrix())
            summation += prod
        return summation

    def getLocalPositionDerivative(self):
        return self.length * np.array([
            self.sin_t * self.sin_a - self.cos_t * self.sin_b * self.cos_a,
            - self.sin_t * self.cos_a - self.cos_t * self.sin_b * self.sin_a,
            self.cos_t * self.cos_b
        ])

    def getRotationMatrix(self):
        r = self.getUnitVector()
        a = self.getAxisVector()
        return np.array([
            [r[0], a[1] * r[2] - a[2] * r[1], a[0]],
            [r[1], a[2] * r[0] - a[0] * r[2], a[1]],
            [r[2], a[0] * r[1] - a[1] * r[0], a[2]]
        ])

    def getRotationMatrixDerivative(self):
        r = self.getUnitVector()
        a = self.getAxisVector()
        return np.array([
            [self.sin_t * self.sin_a - self.cos_t * self.sin_b * self.cos_a,
            a[1] * self.cos_t * self.cos_b + a[2] * (self.sin_t * self.cos_a + self.cos_t * self.sin_b * self.sin_a),
            0],
            [-self.sin_t * self.cos_a - self.cos_t * self.sin_b * self.sin_a,
            a[2] * (self.sin_t * self.sin_a - self.cos_t * self.sin_b * self.cos_a) - a[0] * self.cos_t * self.cos_b,
            0],
            [self.cos_t * self.cos_b,
            a[0] * (-self.sin_t * self.cos_a - self.cos_t * self.sin_b * self.sin_a) 
                - a[1] * (self.sin_t * self.sin_a - self.cos_t * self.sin_b * self.cos_a),
            0]
        ])

class Constraint:
    joint_index = 0
    axis = 0 #0=x, 1=y, 2=z
    value = 0

    def __init__(self, joint_index, axis, value):
        self.joint_index = joint_index
        self.axis = axis
        self.value = value

class IKSystem:
    joints = []
    constraints = []
    allowed_error = 0
    max_iterations = 0

    def __init__(self, joints, constraints, allowed_error = 1e-3, max_iterations = 100):
        self.joints = joints
        self.constraints = constraints
        self.allowed_error = allowed_error
        self.max_iterations = max_iterations

class Solver:
    def constructJacobian(ik_system):
        #Cache table
        constrained_joints = [c.joint_index for c in ik_system.constraints]
        global_derivatives = {
            j:([Util.globalPositionDerivative(j, i, ik_system.joints) for i in range(len(ik_system.joints))]) for j in set(constrained_joints)
        }
        
        return np.array([[global_derivatives[row.joint_index][column][row.axis] for column in range(len(ik_system.joints))] for row in ik_system.constraints])

    def constructFunctionTable(ik_system):
        return np.array([ik_system.joints[c.joint_index].getGlobalPosition(c.joint_index, ik_system.joints)[c.axis] - c.value for c in ik_system.constraints])

    def convergePoint(guess, ik_system):
        Solver.updateJointPositions(guess, ik_system)
        return guess - Util.linearTransformation(Solver.constructFunctionTable(ik_system), np.linalg.inv(Solver.constructJacobian(ik_system)))

    def updateJointPositions(pos_set, ik_system):
        for i in range(len(pos_set)):
            ik_system.joints[i].setTheta(pos_set[i])

    def solve(ik_system):
        """
        Solve the system of joints to adhere to the given constraints
        Returns an array containing the angles of every joint in the system in the same order as the joint table,
        as well as the success state (whether or not the solver successfully converged)
        -You can also read these directly from the joint table of your IKSystem
        """
        if (len(ik_system.joints) != len(ik_system.constraints)):
            print("The number of joints in the system must equal the number of constraints!")
            return None, False

        guess = [0,0,0]
        converged = True
        for i in range(ik_system.max_iterations):
            lastGuess = guess
            guess = Solver.convergePoint(guess, ik_system)
            if ((np.abs(lastGuess - guess) < ik_system.allowed_error).all()):
                break
            if (i == ik_system.max_iterations - 1):
                print(f"Solver failed to converge! Last guess difference was {guess-lastGuess}, but the maximum is {ik_system.allowed_error}")
                converged = False
        guess = Util.angleWrap(guess)
        Solver.updateJointPositions(guess, ik_system)
        return guess, converged

class Util:
    def linearTransformation(v, m):
        size = len(v)
        if (size != len(m)):
            print(f"Illegal vector and matrix sizes for transformation! (v={size}, m={len(m)})")
            return None
        return np.array([sum([v[i] * m[j][i] for i in range(size)]) for j in range(size)])

    def globalPositionDerivative(joint_index, angle_index, joints):
        if (angle_index > joint_index): #Changing angles on joints "above" the current joint will not affect this joint
            return [0,0,0]
        last_pos = joints[angle_index].getLocalPositionDerivative()
        for j in range(angle_index):
            last_pos = Util.linearTransformation(last_pos, joints[angle_index - j - 1].getRotationMatrix())

        #Could be a source of problems in the future; indexing is a bit strange
        #Equation on back page of pt 2
        summation = [0,0,0]
        for i in range(angle_index + 1, joint_index + 1):
            prod = joints[i].getLocalPosition()
            for j in range(i - angle_index - 1):
                prod = Util.linearTransformation(prod, joints[i - j - 1].getRotationMatrix())
            prod = Util.linearTransformation(prod, joints[angle_index].getRotationMatrixDerivative())
            for j in range(i - angle_index, i):
                prod = Util.linearTransformation(prod, joints[i - j - 1].getRotationMatrix())
            summation += prod

        return last_pos + summation

    def angleWrap(angle):
        if isinstance(angle, list):
            return [Solver.angleWrap(i) for i in angle]
        return angle - np.round(angle / (2 * np.pi)) * 2 * np.pi