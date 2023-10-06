# Random number generation fundamentals

This library requires generation of pseudo random numbers.
For simulation purposes, we need random numbers that are independent.
Two important choices need to be made:
1. Type of pseudo random number generator.
2. Seed generation algorithm - manual/ automatic (cryptographic)

**Some important points (Need to verify):**
If we create a sequence of random numbers from the same seed, feed them 
to the rows of a matrix


For most common applications, such as Monte Carlo simulations or statistical analyses, 
generating random numbers in chunks and treating each chunk as independent is a reasonable and common practice,
as it simplifies the analysis and ensures that each chunk exhibits the desired statistical properties.
However, it's important to note that the independence within each chunk doesn't extend to overlapping chunks or to individual numbers within a chunk. If you were to overlap the chunks or compare individual numbers within the same chunk, you might find some correlation due to the sequential nature of PRNGs.

The Mersenne Twister is known for its good statistical properties, such as a uniform distribution and low correlation between numbers. It passes various statistical tests for randomness. The Mersenne Twister has an extremely long period, which means it can produce a vast number of unique random sequences before repeating. This long period helps ensure that the generated numbers are not easily predictable.

For a PRNG, its quality depends on the maximum length of sequence it can take on and quality of seed itself.
The maximum length of sequence depends on implementation.

The autocorrelation of generated random numbers can be a useful tool to assess the quality of random number generated.
Keep in mind that some degree of autocorrelation is expected in pseudorandom sequences, especially at small lags, due to the deterministic nature of PRNGs. However, the correlations should be small and not exhibit any predictable pattern if the PRNG is of high quality and the seed is sufficiently unpredictable.

## Example:
If we are generating 10000 random numbers from a pseudo random number generator ( Mersenee twister is a good choice) with a seed from a device.
Then, for practical purposes of simulation and maintaining statistical properties, each number (although correlated) can be treated as independent because of the statistical properties. 

If we generate 10000 random numbers, dividing them into 10 chunks of 1000 numbers each, we can do in the following
1. 10 different PRNGs with 1 seed.
2. 1 PRNG with 10 different seeds.
3. 1 PRNG with 1 seed.

**NOTE**: special case is seed is generated from a random device

Case 1 and 2 will produce random numbers of equivalent quality, given all the PRNGS are of the same quality.
There is an overhead of calling the random device but it gives you the best seed for a PRNG. 

The chunks of 1000 numbers which do not overlap can still be treated as independent but they will be of lower quality than case 1 and 2 in terms of statistical properties. But, for some simulation applications this is sufficient. When the length of the sequence is much larger than the period of random number generator, in that situation, case 3 wont produce independent chunks of random numbers. 