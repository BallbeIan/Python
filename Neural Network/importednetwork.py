import numpy as np
import json

#creating network structure

inputs = 2
hidden_neurons = 8
output = 1

X = np.array([[0,0,1,1],
              [0,1,0,1]])

Y = np.array([[0,1,1,0]]) #FALSE, TRUE, TRUE, FALSE

def get_weights():
    with open('weights.json', 'r') as json_file:
        data = json.load(json_file)
    return data
data = get_weights()

def parameters(inputs, hidden_neurons, output):
    raw_weights = {
        'W1': (data["W1"]),
        'b1': (data["b1"]),
        'W2': (data["W2"]),
        'b2': (data["b2"])
    }
    return raw_weights
weights = parameters(inputs, hidden_neurons, output)

def relu(z):
    return np.maximum(0,z)

def sigmoid(z):
    return 1 / (1 + np.exp(-z))

def fpropagation(X, weights):
    activations = {'A0': X}
    L = 2
    for l in range(1, L):
       A_prev = activations[f'A{l-1}']
      
       W = weights[f'W{l}']
       b = weights[f'b{l}']
      
       Z = np.dot(W, A_prev) + b
      
       A = relu(Z)
      
       activations[f'Z{l}'] = Z
       activations[f'A{l}'] = A

    A_prev = activations[f'A{L-1}']
    W = weights[f'W{L}']
    b = weights[f'b{L}']
  
    Z = np.dot(W, A_prev) + b
  
    activations[f'Z{L}'] = Z
    activations[f'A{L}'] = A
  
    return A, activations
A = fpropagation(X, weights)

def loss(Y, A):
    m = Y.shape[1] 
    total_penalty = 0

    for i in range(m):
        answer = Y[0, i] 
        guess = A[0, i]

        if answer == 1:
            penalty = -np.log(guess)
        else:
            penalty = -np.log(1 - guess) 

        total_penalty += penalty

    loss = total_penalty / m
 
    return loss

loss = loss(Y, A)
print(loss)