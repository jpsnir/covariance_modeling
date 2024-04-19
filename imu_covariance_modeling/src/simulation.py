import gtsam
import numpy as np
import typing as T
import matplotlib.pyplot as plt
import gtsam.utils.plot as gtsam_plot

ODOMETRY_NOISE = gtsam.noiseModel.Diagonal.Sigmas(np.array([0.2, 0.2, 0.1]))
PRIOR_NOISE = gtsam.noiseModel.Diagonal.Sigmas(np.array([0.3, 0.3, 0.1]))


def main():
    
    graph = gtsam.NonlinearFactorGraph()
    
    priorMean = gtsam.Pose2(0.0, 0.0, 0.0)
    graph.add(gtsam.PriorFactorPose2(1, priorMean, PRIOR_NOISE))
    
    odometry = gtsam.Pose2(2.0, 0.0, 0.0)
    graph.add(gtsam.BetweenFactorPose2(1, 2, odometry, ODOMETRY_NOISE))
    graph.add(gtsam.BetweenFactorPose2(2, 3, odometry, ODOMETRY_NOISE))
    
    print(f"\n Factor graph : \n {graph}")
    
    initial = gtsam.Values()
    initial.insert(1, gtsam.Pose2(0.5, 0.0, 0.2))
    initial.insert(2, gtsam.Pose2(2.3, 0.1, -0.2))
    initial.insert(3, gtsam.Pose2(4.1, 0.1, 0.1))
    print(f"\n Initial estimate = {initial}")
    
    params = gtsam.LevenbergMarquardtParams()
    optimizer = gtsam.LevenbergMarquardtOptimizer(graph, initial, params)
    result = optimizer.optimize()
    
    marginals = gtsam.Marginals(graph, result)
    
    
    for i in range( 1, 4):
        gtsam_plot.plot_pose2(0, result.atPose2(i), 0.5, marginals.marginalCovariance(i))
    
    plt.axis('equal')
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()