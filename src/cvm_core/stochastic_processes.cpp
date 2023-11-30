#include <Eigen/src/Core/Matrix.h>
#include <random>
#include <stochastic_process.h>

/*
 * Implements different stochastic processes
 */
namespace cvm {
StochasticProcess::StochasticProcess() {
  // save the seed for repeating the results
  N = 100;
  setupWhiteNoiseProcess();
  constructed = true;
}

StochasticProcess::StochasticProcess(const int N) {
  this->N = N;
  setupWhiteNoiseProcess();
  constructed = true;
}

StochasticProcess::StochasticProcess(const int N, const std::function<double(double)> process){
    this->N = N;
    seed_value = rd();
    mt_gen.seed(seed_value);
    X_ptr = std::make_shared<Eigen::VectorXf>(N);

    // lambda
    distribution_function = std_normal();
    this->process = process;
    this->constructed = true;
}

StochasticProcess::StochasticProcess(const int N, const std::function<double(double)> process, const std::function <double(std::mt19937&)> distribution_fn){
    this->N = N;
    seed_value = rd();
    mt_gen.seed(seed_value);
    X_ptr = std::make_shared<Eigen::VectorXf>(N);

    this->distribution_function = distribution_fn;
    this->process = process;
    this->constructed = true;
}


void StochasticProcess::setupWhiteNoiseProcess() {
  X_ptr = std::make_shared<Eigen::VectorXf>(N);
  // initialize the mersenne twister generator
  // mt gen generates uniform random numbers.
  seed_value = rd();
  mt_gen.seed(seed_value);
  // default constructor will create
  // everything with normal distribution.
  // normal distribution is inbuilt in random library

  // lambda
  distribution_function = std_normal();
  process = [](double x) { return x; };
}


std::shared_ptr<Eigen::VectorXf> StochasticProcess::operator()() {
  generate();
  return X_ptr;
}

std::shared_ptr<Eigen::VectorXf> StochasticProcess::generate() {
  for (int i = 0; i < N; i++) {
    double element = distribution_function(mt_gen);
    (*X_ptr)(i) = process(element);
  }
  return X_ptr;
}

std::shared_ptr<Eigen::MatrixXf> StochasticProcess::generate_matrix(){
}
}; // namespace cvm
