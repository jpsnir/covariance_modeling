import gtsam
import numpy as np
import typing as T
import matplotlib.pyplot as plt
import gtsam.utils.plot as gtsam_plot

ODOMETRY_NOISE = gtsam.noiseModel.Diagonal.Sigmas(np.array([0.02, 0.02, 0.01]))
PRIOR_NOISE = gtsam.noiseModel.Diagonal.Sigmas(np.array([0.01, 0.01, 0.01]))


def circular_simulation():
    factor = 1
    graph = gtsam.NonlinearFactorGraph()   
    N = 11
    theta_max = np.pi/2
    pts = np.zeros([N ,3])
    noisy_pts = np.zeros([N, 3])
    for i, th in enumerate(np.linspace(0, theta_max , N)):
        pts[i, :] = np.array([np.cos(th), np.sin(th), th])
        noisy_pts[i, :] = pts[i, :] + factor*np.random.randn(1, 3)
    
    priorMean = gtsam.Pose2(pts[0, 0], pts[0, 1], 0.0)
    graph.add(gtsam.PriorFactorPose2(0, priorMean, PRIOR_NOISE))
    odometry = np.diff(pts, axis=0)
    
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

def simulation_2():
    graph = gtsam.NonlinearFactorGraph()
    graph.add(gtsam.PriorFactorPose2(0, gtsam.Pose2(0, 0 , 0), PRIOR_NOISE ))
    graph.add(gtsam.BetweenFactorPose2(0, 1, gtsam.Pose2(2, 0, 0), ODOMETRY_NOISE))
    graph.add(gtsam.BetweenFactorPose2(1, 2, gtsam.Pose2(2, 0, np.pi/3), ODOMETRY_NOISE))
    graph.add(gtsam.BetweenFactorPose2(2, 3, gtsam.Pose2(2, 0, np.pi/3), ODOMETRY_NOISE))
    graph.add(gtsam.BetweenFactorPose2(3, 4, gtsam.Pose2(2, 0, np.pi/3), ODOMETRY_NOISE))
    
    initial = gtsam.Values()
    initial.insert(0, gtsam.Pose2(0.5, 0.0, 0.2))
    initial.insert(1, gtsam.Pose2(2.3, 0.1, -0.2))
    initial.insert(2, gtsam.Pose2(4.1, 0.1, np.pi/2))
    initial.insert(3, gtsam.Pose2(4.0, 2.0, np.pi))
    initial.insert(4, gtsam.Pose2(2.1, 2.1, -np.pi))
    
    params = gtsam.LevenbergMarquardtParams()
    optimizer = gtsam.LevenbergMarquardtOptimizer(graph, initial, params)
    
    result = optimizer.optimize()
    marginals = gtsam.Marginals(graph, result)
    for i in range( 0, 5):
        gtsam_plot.plot_pose2(0, result.atPose2(i), 0.5, marginals.marginalCovariance(i))
    
    plt.axis('equal')
    plt.title("After optimization")
    plt.grid(True)
    plt.show()
    
if __name__ == "__main__":
    #circular_simulation()
    simulation_2()