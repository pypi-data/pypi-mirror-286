#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <iostream>
#include <cmath>
#include <algorithm>
#include <random>
#include <stdexcept>
#include <vector>
#include <sstream>

namespace py = pybind11;

// Modular simulated annealing algorithm
template <typename T>
std::vector<T> anneal(
    py::function funct, // The function to be minimized
    std::vector<T> initial, // Initial guess - the starting set of parameters for simulated annealing process
    py::function neighbor,  // Neighbor function - generates a new set of parameters based on the current set
    int iterations = 100,  // Number of iterations to run the algorithm for
    py::function temperature = py::cpp_function([](int iter) { return pow(0.999, iter); }), // Temperature schedule - determines the temperature at each iteration
    py::function acceptance = py::cpp_function([](double new_value, double current_value, double temperature) {
        
        if (temperature > 1 || temperature <= 0){
        std::cerr << "Warning: Temperature outside (0,1], temperature scheduling likely incorrect! Current temperature: " << temperature << std::endl;
    }
    if (new_value < current_value){
        return 1.0;
    }
    double probability = exp(-(new_value - current_value) / temperature); // Calculate the acceptance probability
    return probability;
}), // Acceptance probability - determines whether to accept a new set of parameters based on the current set and temperature
    int verbose = 1 // Verbosity level - 0 for final output, 1 for output at each iteration
) {


    // Candidate class to store parameters that have been accepted as well as their values
    class Candidate {
    public:
        std::vector<T> params; // Parameters for each candidate solution
        double value; // Value of each candidate solution
        
        Candidate(const std::vector<T>& p, double v) : params(p), value(v) {}
    };

    double iv = funct(initial).template cast<double>(); // Calculate the value of the initial guess
    Candidate current(initial, iv); // Create the current candidate variable, to store the current accepted guess, and set it as the initial guess provided
    Candidate best(initial, iv); // Create the best candidate variable, to store our best guess, and set it as the initial guess provided

    double temp = temperature(0).template cast<double>(); // Initial temperature
    std::mt19937 rng(std::random_device{}()); // Random number generator
    std::uniform_real_distribution<> dist(0.0, 1.0); // Uniform distribution for acceptance probability

    // For every iteration...
    for (int iter = 0; iter < iterations; ++iter) {
        double new_temp = temperature(iter).template cast<double>(); // Calculate the temperature for the current iteration
        if (new_temp > temp) {
            std::cerr << "Warning: Temperature must be decreasing. Current temperature: " << new_temp << " Previous temperature: " << temp << std::endl;
        }
        temp = new_temp; // Update the temperature

        std::vector<T> new_params = neighbor(current.params).template cast<std::vector<T>>(); // Generate a new set of parameters based on the current set
        double new_val = funct(new_params).template cast<double>(); // Calculate the value of the new set of parameters

        if (new_val < best.value) { // If the new set of parameters is better than the best set of parameters...
            best = Candidate(new_params, new_val); // Set the new set of parameters as the best candidate
        }

        if (verbose == 1) {
            std::cout << "Iteration: " << iter << " Best value: " << best.value << std::endl; // Output the iteration number and the best value
            std::cout << "Current value: " << current.value << std::endl; // Output the current value
            std::cout << "Best value: " << best.value << std::endl; // Output the best value
        }

        double prob = acceptance(new_val, current.value, temp).template cast<double>();
        if (prob < 0.0 || prob > 1.0) { // If the acceptance probability is not within 0 and 1..
            throw std::invalid_argument("Acceptance probability must fall between 0 and 1!"); // Throw an exception
        }

        if (dist(rng) < prob) { // If the new set of parameters is accepted...
            current = Candidate(new_params, new_val); // Set the new set of parameters as the current set
        }
    }

    std::cout << "Best value: " << best.value << std::endl;
    return best.params; // Return the best parameters
}

PYBIND11_MODULE(annealing, m) { // Define the Python module
    // Define a function to minimize a function of doubles
    m.def("anneal_double", &anneal<double>,
        py::arg("funct"), // Define the function to be minimized
        py::arg("initial"), // Define the initial parameters
        py::arg("neighbor"), // Define the neighbor generation function
        py::arg("iterations") = 100, // Define the number of iterations
        py::arg("temperature") = py::cpp_function([](int iter) { return pow(0.999, iter); }), // Define the temperature schedule function with a default value
        py::arg("acceptance") = py::cpp_function([](double new_value, double current_value, double temperature) {
        
        if (temperature > 1 || temperature <= 0){
        std::cerr << "Warning: Temperature outside (0,1], temperature scheduling likely incorrect! Current temperature: " << temperature << std::endl;
    }
    if (new_value < current_value){
        return 1.0;
    }
    double probability = exp(-(new_value - current_value) / temperature); // Calculate the acceptance probability
    return probability;
}), // Define the acceptance probability function
        py::arg("verbose") = 1, // Define the verbosity with a default value of 1
        "Uses simulated annealing to minimize a function of double inputs" // Define the docstring
    );

    // Define a function to minimize a function of integers
    m.def("anneal_int", &anneal<int>,
        py::arg("funct"), // Define the function to be minimized
        py::arg("initial"), // Define the initial parameters
        py::arg("neighbor"), // Define the neighbor generation function
        py::arg("iterations") = 100, // Define the number of iterations
        py::arg("temperature") = py::cpp_function([](int iter) { return pow(0.999, iter); }), // Define the temperature schedule function with a default value
        py::arg("acceptance"), // Define the acceptance probability function
        py::arg("verbose") = 1, // Define the verbosity with a default value of 1
        "Uses simulated annealing to minimize a function of integer inputs" // Define the docstring
    );

    // Define a function to minimize a function of strings
    m.def("anneal_string", &anneal<std::string>,
        py::arg("funct"), // Define the function to be minimized
        py::arg("initial"), // Define the initial parameters
        py::arg("neighbor"), // Define the neighbor generation function
        py::arg("iterations") = 100, // Define the number of iterations
        py::arg("temperature") = py::cpp_function([](int iter) { return pow(0.999, iter); }), // Define the temperature schedule function with a default value
        py::arg("acceptance"), // Define the acceptance probability function
        py::arg("verbose") = 1, // Define the verbosity with a default value of 1
        "Uses simulated annealing to minimize a function of string inputs" // Define the docstring
    );

}
