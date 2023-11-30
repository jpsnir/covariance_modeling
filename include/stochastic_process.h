#ifndef STOCHASTIC_PROCESS
#include <cmath>
#include <eigen3/Eigen/Dense>
#include <iostream>
#include <memory>
#include "distribution_generators.h"

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
  StochasticProcess();

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
  StochasticProcess(const int N, const std::function<double(double)> process,
                    const std::function<double(std::mt19937&)> dist_fn);

  ~StochasticProcess() = default;
  /*
   * @brief: generate the eigen vector of random numbers, given the base
   * distribution and base process function.
   * @details: The generate function, when it is called generates a sequence of
   * random numbers stored in an eigen vector. Each call of generate() function
   * seeds the mersenne twister generator again, and generates a new random
   * sequence from the given process function and distribution function.
   */
  virtual std::shared_ptr<Eigen::VectorXf> generate();
  /*
   * @brief: operator () performs the same things as generate function ()
   * @see generate()
   */
  virtual std::shared_ptr<Eigen::VectorXf> operator()();
  virtual std::shared_ptr<Eigen::MatrixXf> generate_matrix();
  // reinitialize the stochastic process
  //virtual StochasticProcess operator+(const StochasticProcess &Y);
  //virtual StochasticProcess operator-(const StochasticProcess &Y);
  //virtual StochasticProcess operator*(const StochasticProcess &Y);
  // generator function:
  // std::function can take functions, functors, lambda-functions,
  // For member methods of other classes, we need to overload these methods or
  // use template programming
  void setProcess(std::function<double(double)> process_generator);
  void setDistribution(std::function<double(double)> inv_cdf);

private:
  void initialize_generator(const std::function<double(double)> &process, const std::function<double(std::mt19937&)> &dist_fn);
  void setupWhiteNoiseProcess();
public:
  // size
  int N = 100;
  bool constructed = false;

private:
  unsigned seed_value = 0;
  std::random_device rd;
  std::mt19937 mt_gen;
  std::function<double(double)> process;
  std::function<double(std::mt19937&)> distribution_function;
  // raw data
  std::shared_ptr<Eigen::VectorXf> X_ptr;
  StandardNormal std_normal;
};
}; // namespace cvm

#endif
