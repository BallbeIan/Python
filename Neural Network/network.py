import numpy as np

# Setting the network's structure
n_input = 2
n_hidden = 8
n_output = 1


def initialize_parameters(n_input, n_hidden, n_output):
    """Sets the starting weights and biases the neurons will use to begin the learning process. Weight tables are filled
    with small random numbers while the bias tables are filled with zeros. The inputs are multiplied by these settings
    to make a guess, and training adjusts all the numbers accordingly.
    We use seed(1) so results are reproducible and only change when we change the code."""
    np.random.seed(1)
    weights = {
        'W1': np.random.randn(n_hidden, n_input) * 0.01,
        'b1': np.zeros((n_hidden, 1)),
        'W2': np.random.randn(n_output, n_hidden) * 0.01,
        'b2': np.zeros((n_output, 1))
    }
    return weights


def relu(z):
    """ReLU turns any negative raw score from the hidden neurons into 0, switching that neuron off, and leaves
    positive numbers unchanged so they pass their score along."""
    return np.maximum(0, z)


def sigmoid(z):
    """Sigmoid squashes the output neuron's raw score (z) into a number between 0 and 1. Close to 0 means it's sure
    the answer is 0, close to 1 means it's sure the answer is 1, and 0.5 means it has no idea."""
    return 1 / (1 + np.exp(-z))


def forward_propagation(X, weights):
    """The hidden neurons apply ReLU to their raw scores, then the output neuron applies sigmoid to its raw score,
    giving the network's guess. This repeats every epoch after the weights and biases have been adjusted."""
    W1, b1 = weights['W1'], weights['b1']
    W2, b2 = weights['W2'], weights['b2']

    Z1 = np.dot(W1, X) + b1
    A1 = relu(Z1)
    Z2 = np.dot(W2, A1) + b2
    A2 = sigmoid(Z2)

    cache = (Z1, A1, W1, b1, Z2, A2, W2, b2)
    return A2, cache


def compute_loss(Y, A2):
    """Gives a penalty according to how confident and right/wrong each guess was, then averages the penalties
    into one number: the loss."""
    m = Y.shape[1]
    A2 = np.clip(A2, 1e-8, 1 - 1e-8)  # avoid log(0) when the network becomes very confident
    total_penalty = 0

    for i in range(m):
        answer = Y[0, i]
        guess = A2[0, i]

        if answer == 1:
            penalty = -np.log(guess)
        else:
            penalty = -np.log(1 - guess)

        total_penalty += penalty

    return total_penalty / m


def backward_propagation(X, Y, cache):
    """Works out how much each weight and bias has to change (the gradients): which direction and by how much.
    update_parameters then applies them."""
    (Z1, A1, W1, b1, Z2, A2, W2, b2) = cache
    m = X.shape[1]

    dZ2 = A2 - Y
    dW2 = 1 / m * np.dot(dZ2, A1.T)
    db2 = 1 / m * np.sum(dZ2, axis=1, keepdims=True)

    dA1 = np.dot(W2.T, dZ2)
    dZ1 = dA1 * (Z1 > 0)  # ReLU derivative
    dW1 = 1 / m * np.dot(dZ1, X.T)
    db1 = 1 / m * np.sum(dZ1, axis=1, keepdims=True)

    return {'dW1': dW1, 'db1': db1, 'dW2': dW2, 'db2': db2}


def update_parameters(weights, gradients, learning_rate):
    """Subtracts a small correction from the old values, which gives us the new values."""
    weights['W1'] -= learning_rate * gradients['dW1']
    weights['b1'] -= learning_rate * gradients['db1']
    weights['W2'] -= learning_rate * gradients['dW2']
    weights['b2'] -= learning_rate * gradients['db2']
    return weights


def learning_process(X, Y, n_input, n_hidden, n_output, epochs, learning_rate):
    weights = initialize_parameters(n_input, n_hidden, n_output)

    for i in range(epochs):
        A2, cache = forward_propagation(X, weights)
        loss = compute_loss(Y, A2)
        gradients = backward_propagation(X, Y, cache)
        weights = update_parameters(weights, gradients, learning_rate)

        if i % 100 == 0:
            print(f"---> Epoch {i}, Loss: {loss:.4f}")

    return weights


def predict(X, weights):
    A2, _ = forward_propagation(X, weights)
    return A2 > 0.5


# XOR truth table: each column is one example
X = np.array([[0, 0, 1, 1],
              [0, 1, 0, 1]])
Y = np.array([[0, 1, 1, 0]])  # False True True False

trained_weights = learning_process(X, Y, n_input, n_hidden, n_output, epochs=1000, learning_rate=0.1)

predictions = predict(X, trained_weights)
print(f"---> Predictions: {predictions}")