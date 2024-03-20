import math

def fixed_point_iteration_for_arctanx(num_iterations):
    # Define the iteration function g(x) = arctan(x)
    def g(x):
        return math.atan(x)
    
    # Initial guess - choose a value in [4,5] as the starting point
    # Given the nature of the problem, starting closer to 0 might make more sense
    # since arctan(x) ranges from -pi/2 to pi/2, but we'll stick to instructions
    x_n = 4  # Midpoint of the interval as an arbitrary choice
    
    for i in range(num_iterations):
        x_next = g(x_n)
        
        # Print iteration details (optional)
        print(f"Iteration {i+1}: x = {x_next}")
        
        # Check if the solution is accurate to within 10^-4
        if abs(x_next - x_n) < 1e-4:
            print(f"Converged to {x_next} after {i+1} iterations")
            return x_next
        
        x_n = x_next
    
    print(f"Solution after {num_iterations} iterations is {x_n}, may not have converged")
    return x_n

# Example usage
num_iterations = 1000
solution = fixed_point_iteration_for_arctanx(num_iterations)
print(f"Solution: x = {solution}")

'''
output:

Iteration 1: x = 1.3258176636680326
Iteration 2: x = 0.924579787598783
Iteration 3: x = 0.7462303195612678
Iteration 4: x = 0.6410841446428066
Iteration 5: x = 0.5700819276496225
Iteration 6: x = 0.5181303631324816
Iteration 7: x = 0.47804647445062615
Iteration 8: x = 0.4459310497439469
              .
              .
              .
Iteration 337: x = 0.06681770469993202
Converged to 0.06681770469993202 after 337 iterations
Solution: x = 0.06681770469993202

'''