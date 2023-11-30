#ifndef DISTRIBUTION_GENERATORS_H
#include <functional>
#include <iostream>
#include <random>

/* @brief: interface class for generating different distributions
 */
namespace cvm {
class DistributionGenerator {
public:
  DistributionGenerator() = default;

  /* @brief Functor definition to be inherited by subclasses
   * to create generator functions using inverse cdf principle
   */
  virtual std::function<double(std::mt19937 &)> operator()() = 0;
};

/* @brief: For standard normal distribution, we will use the inbuilt
 * std::normal_distribution class in random library. This uses box muller
 * method to generate numbers from a normal distribution.
 */
class StandardNormal : public DistributionGenerator {
public:
  StandardNormal() = default;

  std::function<double(std::mt19937 &)> operator()() override {
    auto generator = [](std::mt19937 &mt_gen) -> double {
      std::normal_distribution<double> std_normal(0, 1);
      return std_normal(mt_gen);
    };
    return generator;
  };
};
class Exponential : public DistributionGenerator {
public:
  Exponential(double l) : lambda(l) {}
  std::function<double(std::mt19937 &)> operator()() override {
    auto generator = [this](std::mt19937 &mt_gen) -> double {
      std::exponential_distribution<double> exp_dist(lambda);
      return exp_dist(mt_gen);
    };
    return generator;
  }
  double lambda;
};
}; // namespace cvm
#endif
