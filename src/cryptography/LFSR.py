import numpy as np
import nistrng


# used https://github.com/InsaneMonster/NistRng for nist sp-800 22 tests


class LFSR():
    def __init__(self, init_state: list, func: list):
        self.state = init_state
        func.sort()
        if func[-1] > len(self.state) or not len(func) > 1:
            raise ValueError('Invalid function')
        func.pop()
        self.func = func

    def clock(self):
        new_value = 0
        for tap in self.func:
            new_value ^= self.state[len(self.state)-1-tap]
        self.state.insert(0,new_value)
        return self.state.pop()
    
    def __str__(self):
        return ' '.join(map(str, self.state))

def checkـnist(bit_sequence):

    binary_sequence: np.ndarray = np.array(bit_sequence, dtype=int)
    eligible_battery: dict = nistrng.check_eligibility_all_battery(binary_sequence, nistrng.SP800_22R1A_BATTERY)

    print("Eligible tests from NIST-SP800-22r1a:")
    for name in eligible_battery.keys():
        print("- " + name)

    results = nistrng.run_all_battery(binary_sequence, eligible_battery, False)     
    print("Test results:")
    for result, elapsed_time in results:
        if result.passed:
            print(f"- PASSED - score: {np.round(result.score, 3)} - {result.name} - elapsed time: {elapsed_time} ms")
        else:
            print(f"- FAILED - score: {np.round(result.score, 3)} - {result.name} - elapsed time: {elapsed_time} ms")

        # https://github.com/dj-on-github/sp800_22_tests
        # https://github.com/InsaneMonster/NistRng
            
def main():
    np.random.seed = 42
    init = list(np.random.randint(2,size=31))
    func = [31,0,3]
    #  the func x^31 + x^3 + 1 is a prime polymial function 

    lfsr = LFSR(init, func) 
    outputs = []
    states = set()

    for _ in range(1_000_000):
        if str(lfsr) in states:
            break
        states.add(str(lfsr))
        outputs.append(lfsr.clock())
        # print(f"{_} -> {lfsr}")

    print(len(states)==2**len(init)-1,len(states))

    checkـnist(outputs)



    
            
main()

# test results:
'''
Test results:
- PASSED - score: 0.99 - Monobit - elapsed time: 1 ms
- PASSED - score: 0.144 - Frequency Within Block - elapsed time: 1 ms
- PASSED - score: 0.057 - Runs - elapsed time: 233 ms
- PASSED - score: 0.636 - Longest Run Ones In A Block - elapsed time: 124 ms
- FAILED - score: 0.0 - Binary Matrix Rank - elapsed time: 1835 ms
- FAILED - score: 0.0 - Discrete Fourier Transform - elapsed time: 58 ms
- PASSED - score: 0.356 - Non Overlapping Template Matching - elapsed time: 2250 ms
- PASSED - score: 0.011 - Maurers Universal - elapsed time: 610 ms
- FAILED - score: 0.0 - Linear Complexity - elapsed time: 104043 ms
- FAILED - score: 0.0 - Serial - elapsed time: 24761 ms
- FAILED - score: 0.0 - Approximate Entropy - elapsed time: 16906 ms
- FAILED - score: 0.0 - Cumulative Sums - elapsed time: 723 ms
- FAILED - score: 0.63 - Random Excursion - elapsed time: 3440 ms
- FAILED - score: 0.0 - Random Excursion Variant - elapsed time: 16 ms
'''