#include <eigen3/Eigen/Dense>
#include <StochasticProcess.h>
namespace cvm{
class StochasticProcessProperties{
  virtual Eigen::VectorXf mean();
  virtual Eigen::VectorXf std_dev();
  virtual Eigen::VectorXf auto_correlation();
  virtual Eigen::VectorXf output_power();
  virtual Eigen::VectorXf variance();
  virtual Eigen::VectorXf power_spectral_density();
  virtual Eigen::VectorXf
  cross_power_spectral_density(const StochasticProcess &Y);
};
};
