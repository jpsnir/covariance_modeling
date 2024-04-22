import gtsam
import gtsam.imuBias
import numpy as np
import typing as T
import matplotlib.pyplot as plt
import gtsam.utils.plot as gtsam_plot
import matplotlib.animation as animation

ODOMETRY_NOISE = gtsam.noiseModel.Diagonal.Sigmas(np.array([0.02, 0.02, 0.01]))
PRIOR_NOISE = gtsam.noiseModel.Diagonal.Sigmas(np.array([0.01, 0.01, 0.01]))



def pose_graph_simulation_square():
    """
    *(5)----*(4)----*(3)
    |                 |
    |                 |
    *(0)----*(1)----*(2)
    |
    *(6)
    An odometry factor given by between factors is represented in
    terms of relative measurements from previous frames.  
    """
    graph = gtsam.NonlinearFactorGraph()
    # factors are assigned in the local coordinate frame of the current frame for a between factor.
    graph.add(gtsam.PriorFactorPose2(0, gtsam.Pose2(0, 0 , 0), PRIOR_NOISE ))
    # move along x axis of current frame
    graph.add(gtsam.BetweenFactorPose2(0, 1, gtsam.Pose2(2, 0, 0), ODOMETRY_NOISE))
    # move along x axis of current frame, and rotate by np.pi/2 making x axis pointing to 
    # global y axis
    graph.add(gtsam.BetweenFactorPose2(1, 2, gtsam.Pose2(2, 0, np.pi/2), ODOMETRY_NOISE))
    # move along x axis of current frame, and rotate by np.pi/2 making x axis pointing to 
    # global -x axis
    graph.add(gtsam.BetweenFactorPose2(2, 3, gtsam.Pose2(2, 0, np.pi/2), ODOMETRY_NOISE))
    # move along x axis of current frame, 
    graph.add(gtsam.BetweenFactorPose2(3, 4, gtsam.Pose2(2, 0, 0), ODOMETRY_NOISE))
    # move along x axis of current frame, 
    graph.add(gtsam.BetweenFactorPose2(4, 5, gtsam.Pose2(2, 0, 0), ODOMETRY_NOISE))
    # move along y axis of current frame,rotate by  np.pi making it parallel to
    # x axis of global frame
    graph.add(gtsam.BetweenFactorPose2(5, 6, gtsam.Pose2(0, 3, np.pi/2), ODOMETRY_NOISE))
    graph.add(gtsam.BetweenFactorPose2(6, 7, gtsam.Pose2(0, 2, np.pi/2), ODOMETRY_NOISE))
    
    # Values are assigned in the global frame.
    initial = gtsam.Values()
    initial.insert(0, gtsam.Pose2(0.5, 0.0, 0.2))
    initial.insert(1, gtsam.Pose2(2.3, 0.1, -0.2))
    initial.insert(2, gtsam.Pose2(4.1, 0.1, np.pi/2))
    initial.insert(3, gtsam.Pose2(4.0, 2.0, np.pi))
    initial.insert(4, gtsam.Pose2(2.1, 2.1, np.pi))
    initial.insert(5, gtsam.Pose2(0, 2.1, np.pi))
    initial.insert(6, gtsam.Pose2(0, 1.5, -3*np.pi/2))
    initial.insert(7, gtsam.Pose2(2.5, 0.5, 0))
    
    params = gtsam.LevenbergMarquardtParams()
    optimizer = gtsam.LevenbergMarquardtOptimizer(graph, initial, params)
    
    result = optimizer.optimize()
    marginals = gtsam.Marginals(graph, result)
    for i in range( 0, 8):
        gtsam_plot.plot_pose2(0, result.atPose2(i), 0.5, marginals.marginalCovariance(i))
    
    plt.axis('equal')
    plt.title("After optimization")
    plt.grid(True)
    plt.show()

def pose_graph_simulation_circular():
    """
       *  *
       
    *       *
    
    *       *
      
       *  * 
    """
    
    factor = 1
    graph = gtsam.NonlinearFactorGraph()   
    N = 11
    theta_max = 2*np.pi
    pts = np.zeros([N ,3])
    noisy_pts = np.zeros([N, 3])
    odometry = np.zeros([N-1, 3])
    for i, th in enumerate(np.linspace(0, theta_max , N)):
        pts[i, :] = np.array([np.cos(th), np.sin(th), th])
        noisy_pts[i, :] = pts[i, :] + factor*np.random.randn(1, 3)
        if i != 0:
            cur_theta = pts[i-1, 2]
            # this rotation matrix transforms the vector in local frame 
            # to world frame
            R = np.array([[np.cos(cur_theta), -np.sin(cur_theta)],
                          [np.sin(cur_theta), np.cos(cur_theta)]]
            )
            # we want delta_xy in local frame, therefore 
            # the we need inverse of the rotation matrix 
            # and get the between factor odometry relationship.
            delta_xy_local = R.T@(pts[i, :2] - pts[i-1, :2])
            
            # theta can be obtained from 
            delta_theta_local = pts[i, 2] - pts[i-1, 2]
            odometry[i-1, :] = np.array([delta_xy_local[0], delta_xy_local[1], delta_theta_local]) 
    priorMean = gtsam.Pose2(pts[0, 0], pts[0, 1], 0)
    graph.add(gtsam.PriorFactorPose2(0, priorMean, PRIOR_NOISE))
    #odometry = np.diff(pts, axis=0)
       
    
    for id, o in enumerate(odometry):
        graph.add(gtsam.BetweenFactorPose2(id, id + 1, gtsam.Pose2(o[0], o[1], o[2]), ODOMETRY_NOISE))
    fig, ax = plt.subplots(1, 1)
    ax.plot(pts[:, 0], pts[:, 1], "--*")
    ax.plot(noisy_pts[:, 0], noisy_pts[:, 1], "--*r")
    ax.set_title(" Actual trajectory")  
    
    print(f"\n Factor graph : \n {graph}")
    initial = gtsam.Values()
    for i, pt in enumerate(noisy_pts):
        if pt[2] <= np.pi:
            initial.insert(i, gtsam.Pose2(pt[0], pt[1], pt[2]))
        else:
            initial.insert(i, gtsam.Pose2(pt[0], pt[1], - (2*np.pi - pt[2])))
    print(f"\n Initial estimate = {initial}")
    params = gtsam.LevenbergMarquardtParams()
    optimizer = gtsam.LevenbergMarquardtOptimizer(graph, initial, params)
    result = optimizer.optimize()
    
    marginals = gtsam.Marginals(graph, result)
    
    
    for i in range( 0, N):
        gtsam_plot.plot_pose2(0, result.atPose2(i), 0.5, marginals.marginalCovariance(i))
    
    plt.axis('equal')
    plt.title("After optimization")
    plt.grid(True)
    plt.show()

def stationary_imu_simulation():
    graph = gtsam.NonlinearFactorGraph()
    # 1. generate stationary measurements
    scenario = gtsam.AcceleratingScenario(
        nRb = gtsam.Rot3(np.eye(3)),
        p0 = np.zeros([3, 1]),
        v0 = np.zeros([3, 1]),
        a_n = np.zeros([3, 1]),
        omega_b = np.zeros([3, 1]),
    )
    
    # IMU noise and gravity
    g = 9.81
    params = gtsam.PreintegrationParams.MakeSharedU(g)
    kGyroSigma = np.radians(0.5)/60
    kAccelSigma = 0.1/60
    params.setGyroscopeCovariance(kGyroSigma**2 * np.identity(3, float))
    params.setAccelerometerCovariance(kGyroSigma**2 * np.identity(3, float))
    params.setIntegrationCovariance(1e-7**2 *np.identity(3 ,float))
    
    # Imu bias
    bias = gtsam.imuBias.ConstantBias(
        biasAcc=np.array([0, 0.1, 0.1]),
        biasGyro=np.array([0, 0, 0])
    )
    
    runner = gtsam.ScenarioRunner(scenario, params, imuSampleTime=0.01, bias=bias)
    fig, ax = plt.subplots(3, 2)
    def update(t):
        omega = runner.measuredAngularVelocity(t)
        acc = runner.measuredSpecificForce(t)
        for i in range(0, 3):
            ax[i][0].scatter(t, omega[i])
        
        for i in range(0, 3):
            ax[i][1].scatter(t, acc[i])
    
    ani = animation.FuncAnimation(fig, update, frames=np.linspace(0, 10, 1000))
    plt.show()
            
    
if __name__ == "__main__":
    #pose_graph_simulation_square()
    #pose_graph_simulation_circular()
    stationary_imu_simulation()