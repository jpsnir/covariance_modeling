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

int main(int argc, char **argv) {
  ::testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
}
