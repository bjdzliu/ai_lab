def activations_memory(num_layers, seq_len, batch_size, hidden_dim, num_heads, precision=16):
    "Returns amount of GPU VRAM (in GB) required to store intermediate activations for traditional Transformer Encoder block"
    mem_bytes = num_layers * precision * seq_len * batch_size * hidden_dim * (
        16 + 2/precision + 2*num_heads*seq_len/hidden_dim + num_heads*seq_len/(precision*hidden_dim))
    return round(mem_bytes / 10**9, 2)

result=activations_memory(num_layers=32, seq_len=4096, batch_size=1, hidden_dim=4096, num_heads=32)


import torch

def calculate_memory(sequence_length, hidden_size, batch_size, dtype=torch.float32, num_layers=1):
    """
    Calculate the memory usage for activations of a neural network during forward pass.
    
    Parameters:
    - sequence_length: Length of the input sequence (e.g., number of words in a sentence).
    - hidden_size: Size of the hidden layer (e.g., the dimensionality of the embeddings).
    - batch_size: Number of sequences processed in parallel (batch size).
    - dtype: Data type of the model weights (default is float32, can be changed to float16 for lower precision).
    - num_layers: Number of layers in the network (default is 1 for a simple network).
    
    Returns:
    - memory_in_GB: Memory used for activations in gigabytes (GB).
    """
    # Calculate the size of one activation (batch_size, sequence_length, hidden_size)
    num_elements_per_layer = batch_size * sequence_length * hidden_size
    
    # If there are multiple layers, the activations will be stored for each layer
    total_elements = num_elements_per_layer * num_layers
    
    # Memory usage in bytes: num_elements * size of each element (in bytes)
    element_size = torch.tensor(0, dtype=dtype).element_size()  # Get the size of each element in bytes
    
    total_memory_bytes = total_elements * element_size
    
    # Convert bytes to gigabytes (1 GB = 1e9 bytes)
    memory_in_GB = total_memory_bytes / 1e9
    
    return memory_in_GB


# Example usage
sequence_length = 4096  # Length of each input sequence (e.g., 128 tokens)
hidden_size = 4096      # Hidden size (e.g., 768 for a typical BERT model)
batch_size = 1        # Batch size (number of sequences processed in parallel)
num_layers = 32       # Number of layers (e.g., 12 layers for BERT)

memory_required = calculate_memory(sequence_length, hidden_size, batch_size, dtype=torch.float32, num_layers=num_layers)

print(f"Memory required for activations: {memory_required:.4f} GB")

