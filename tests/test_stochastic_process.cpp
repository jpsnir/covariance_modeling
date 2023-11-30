#include <gtest/gtest.h>
#include <cmath>
#include <random>
#include <stochastic_process.h>
#include <cassert>

using cvm::StochasticProcess;
using cvm::Exponential;
//TEST(NullObject, Valid){
//    class A{
//    public:
//        A() = default;
//    };
//    EXPECT_TRUE(A());
//}
TEST(BuildStochasticProcess, Constructor1){
    EXPECT_TRUE(StochasticProcess().constructed);
}

TEST(BuildStochasticProcess, Constructor2){
    EXPECT_TRUE(StochasticProcess(1000).constructed);
}

TEST(BuildStochasticProcess, Constructor3){
    int a = 2; int b = 4;
    auto process = [a, b] (double x){
        return a*x + b;
    };

    Exponential exp(0.1);
    EXPECT_TRUE(StochasticProcess(1000, process, exp()).constructed);
}

TEST(StochasticProcess, generate_numbers){
    StochasticProcess sp(1000);
    std::shared_ptr<Eigen::VectorXf> x_ptr = sp.generate();
    std::cout << " Mean of the vector: " << (*x_ptr).mean() << std::endl;
    auto a = (*x_ptr).array().square().mean();
    std::cout << " Variance of the vector: " << a << std::endl;
    EXPECT_NEAR((*x_ptr).mean(), 0 , 0.05);
    EXPECT_NEAR(a, 1 , 0.1);


}

int main(int argc, char **argv) {
  ::testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
}
