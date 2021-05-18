from lineSearch import lineSearch
from objectiveF import objectiveF
from gradient import gradient
from hessian import *

from numpy import linalg as LA


def updateHessian(hessian_, s, v):
    r = 1 / ((v.T).dot(s))
    A = np.eye(5) - np.outer((r * s), v.T)
    B = np.eye(5) - np.outer((r * v), s.T)
    C = np.outer((r * s), s.T)
    hessian_ = np.dot(np.dot(A, hessian_), B) + C
    return(hessian_)
    

def bfgs(x_0, x, y, errorFile):
    a_max = 2
    epsilon = 10**(-6)
    iterations = 0
    errorList = []

    # Check if Hessian matrix is positive defined.
    # If it is not positive defined then update Hessian 
    # matrix with a positive one
    hessian_ = hessian(x)    
    if(not(checkHessianPositive(hessian_))):
        print("Hessian is not positive defined.")
        hessian_ = convertHessianIntoPositiveMatrix(hessian_, 1)

    errorFile.write("Initial error: " + str(objectiveF(x_0, x, y)) + "\n")
    errorList.append(objectiveF(x_0, x, y))
    print("Initial error: " + str(objectiveF(x_0, x, y)))


    while(LA.norm(gradient(x_0, x, y)) > epsilon):
        if(iterations == 1000):
            break

        # Select direction
        p = (-1) * (hessian_.dot(gradient(x_0, x, y)))

        # Select step
        a_star = lineSearch(x_0, p, a_max, x, y)

        # Update point x_0
        x_prev = x_0
        x_0 = x_0 + (a_star * p)

        # Update s_k
        s = x_0 - x_prev

        # Update y_k
        v = gradient(x_0, x, y) - gradient(x_prev, x, y)

        # Update hessian matrix. Check if hessian is positive defined and if not convert it into positive one. 
        hessian_ = updateHessian(hessian_, s, v)
        if(not(checkHessianPositive(hessian_))):
            print("Hessian is not positive defined.")
            hessian_ = convertHessianIntoPositiveMatrix(hessian_, 1)

        iterations += 1

        # Update error file
        errorFile.write("Iteration " + str(iterations) + ": " + str(objectiveF(x_0, x, y)) + "\n")
        errorFile.flush()
        errorList.append(objectiveF(x_0, x, y))
        print("Error: " + str(objectiveF(x_0, x, y)))

    print("Optimizer: " + str(x_0))
    print("Total iteraions: " + str(iterations))
    print("||Gradient f (x_k)|| = " + str(LA.norm(gradient(x_0, x, y))))
    return(x_0, errorList)