#include <cmath>
#include <eigen3/Eigen/Dense>
#include <iostream>
#include <random>
#include <memory>

/*
 * @brief: Stochastic process implements a one-dimensional random sequence <X_1, X_2,
 * ..., X_n> where each element X_i is independent.
 *
 *
 * The implementations are inspired from the book:
 * Probability, statistics and random processes - stark
 * and woods. We use Mersenne twister for our random number generator and seed is
 * generated from random device. The default generated numbers are uniformly
 * distribution, however the random library provides some more implementations
 * of distributions transforming the uniform random numbers to their respective
 * distribution. This is done using inverse cdf principle which will provide the
 * distribution
 */

namespace cvm {
class StochasticProcess {
public:
  /*
   * @brief : Default constructor
   */
  StochasticProcess() = default;

  /*
   * @brief : constructor to initialize the number of elements.
   */
  StochasticProcess(const int N);

  /* @brief: constructor that implements a normally distribution with given
   * process function
   */
  StochasticProcess(const int N, const std::function<double(double)> process);

  /* @brief: constructor implements user defined pdf and process function for generating the
   * elements of stochastic process.
   */
  StochasticProcess(const int N, const std::function<double(double)> &process,
                    const std::function<double(double)> &inv_cdf);

  //public methods
  /*
   * @brief: resets the stochastic process,
   * @details: generates new seed and initializes the mersenee twister generator
   * again.
   */
  virtual void reset();

  /*
   * @brief: generate the eigen vector of random numbers, given the base
   * distribution and base process function.
   */
  virtual std::shared_ptr<Eigen::VectorXf> generate();

  // Inspired from
  // https://github.com/SpectacularAI/SLAM-module/blob/9029de256e49898077dd17e65518ae6abe248aa1/id.cpp#L7

  // Operators
  // reinitialize the stochastic process
  virtual StochasticProcess operator+(const StochasticProcess &Y);
  virtual StochasticProcess operator-(const StochasticProcess &Y);
  virtual StochasticProcess operator*(const StochasticProcess &Y);

  // generator function:
  // std::function can take functions, functors, lambda-functions,
  // For member methods of other classes, we need to overload these methods or
  // use template programming
  virtual void setProcess(std::function<double(double)> process_generator);
  virtual void setDistribution(std::function<double(double)> inv_cdf);

public:
  // size
  int N = 100;

private:
  std::random_device rd;
  std::mt19937 generator;
  std::function<double(double)> process;
  std::function<double(double)> inv_cdf;
  // raw data
  std::shared_ptr<Eigen::VectorXf> X;
};
}; // namespace cvm
