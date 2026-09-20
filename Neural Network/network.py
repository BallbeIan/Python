import numpy as np
import json

# Setting the networks structure
input = 2 
hidden = 8
output = 1 

def initialize_parameters(input, hidden, output):
    """Sets the starting weights and biases the neurons will use to being the learning process, weight tables will be filled 
    with samll random numbers while the bias table will be filled with zeros, then the imputs will be multiplied by these 
    setting to make a guess and the training will adjust all the numbers accordingly.
    We use seed(1) to ensure that the results are not affected by randomness and are only affected by the changes we make."""
    np.random.seed(1)
    weights = {
        'W1': np.random.randn(hidden, input) * 0.01,
        'b1': np.zeros((hidden, 1)),
        'W2': np.random.randn(output, hidden) * 0.01,
        'b2': np.zeros((output, 1))
    }
    return weights
weights = initialize_parameters(input, hidden, output)


def relu(z):
    """ReLU will turn any negative raw scores from the hidden neurons and make them 0 turning the neuron off, and leaves
    the positive numbers unchanged for them to pass their score along."""
    return np.maximum(0,z)

def sigmoid(z):
    """Sigmoid takes the raw score of the output neuron (z) and squashes it into a number between 0 and 1, the smaller
    the number the more sure it is that the right answer is 0, the larger the number the more sure it is that the
    number is 1 and 0.5 means it has no idea."""
    return 1 / (1 + np.exp(-z))


def forward_propagation(X, weights):
    """Here the hidden neurons are applying ReLU to their raw scores, then the output neuron is applying sigmoid to it's raw 
    score and this way we get the firs guess that the neetwork makes. And this cycle repeats on every epoch after the weights
    and bias' have been adjusted."""
    W1, b1 = weights['W1'], weights['b1']
    W2, b2 = weights['W2'], weights['b2']

    Z1 = np.dot(W1, X) + b1
    A1 = relu(Z1)
    Z2 = np.dot(W2, A1) + b2
    A2 = sigmoid(Z2)

    cache = (Z1, A1, W1, b1, Z2, A2, W2, b2)

    return A2, cache


def compute_loss(Y, A2):
    """compute_loss gives out the penalty according to how confident and right/wrong the gues wass and then averages the 
        penalties into one number which is the loss."""
    m = Y.shape[1] 
    total_penalty = 0

    for i in range(m):
        answer = Y[0, i] 
        guess = A2[0, i]

        if answer == 1:
            penalty = -np.log(guess)
        else:
            penalty = -np.log(1 - guess) 

        total_penalty += penalty

    loss = total_penalty / m 
    return loss

def backward_propagation(X, Y, cache):
    """Backward propagation will indicate how much the weights and biases have to change creating gradients. These 
    gradients will mark which direction and how much each value has to move, then the update_parameters function will update them."""
    (Z1, A1, W1, b1, Z2, A2, W2, b2) = cache
    m = X.shape[1]
    
    dZ2 = A2 - Y
    dW2 = 1/m * np.dot(dZ2, A1.T)
    db2 = 1/m * np.sum(dZ2, axis=1, keepdims=True)
    
    dA1 = np.dot(W2.T, dZ2)
    dZ1 = dA1 * (A1 > 0)
    dW1 = 1/m * np.dot(dZ1, X.T)
    db1 = 1/m * np.sum(dZ1, axis=1, keepdims=True)
    
    gradients = {
        'dW1': dW1,
        'db1': db1,
        'dW2': dW2,
        'db2': db2
    }
    
    return gradients

def update_parameters(weights, gradients, learning_rate):
    """Here we are subtracting a small correction from the old values which gives us the new value."""
    weights['W1'] -= learning_rate * gradients['dW1']
    weights['b1'] -= learning_rate * gradients['db1']
    weights['W2'] -= learning_rate * gradients['dW2']
    weights['b2'] -= learning_rate * gradients['db2']
    
    return weights

def learning_process(X, Y, input, hidden, output, epochs, learning_rate):
    weights = initialize_parameters(input, hidden, output)
    
    for i in range(epochs):
        # Forward propagation.
        A2, cache = forward_propagation(X, weights)
        
        # Compute the loss.
        loss = compute_loss(Y, A2)
        
        # Backward propagation.
        gradients = backward_propagation(X, Y, cache)
        
        # Update the parameters.
        weights = update_parameters(weights, gradients, learning_rate)
        
        # Print loss every 100 epochs.
        if i % 100 == 0:
            print(f"Epoch {i}, Loss: {loss:.4f}")
    
    return weights


X = np.array([[0, 0, 1, 1],
              [0, 1, 0, 1]]) 
Y = np.array([[0, 1, 1, 0]])  #False True True False

trained_weights = learning_process(X, Y, input, hidden, output, epochs=5000, learning_rate=0.5)

def predict(X, weights):
    A2, _ = forward_propagation(X, weights)
    predictions = A2 > 0.5
    return predictions

predictions = predict(X, trained_weights)
print(f"Predictions: {predictions}")

def numpy_visualizer(obj):
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    raise TypeError(f"Type {type(obj)} not serializable")


# Pass the function to the default parameter
json_data = json.dumps(weights, default=numpy_visualizer)
print(json_data)

with open("weights.json", "w") as file:
    json.dump(json_data, file, indent=4)