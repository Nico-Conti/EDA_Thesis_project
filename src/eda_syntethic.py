import numpy as np
import matplotlib.pyplot as plt

def generate_synthetic_EDA(num_samples, sampling_freq, state):
    time = np.arange(0, num_samples) / sampling_freq

    # Baseline signal - slowly varying component
    baseline = np.sin(1 * np.pi * 0.01 * time)  # Example: a sine wave as baseline

    # Phasic component - sparse impulse signal with varying filter parameters
    if state == 'neutral':
        num_peaks = np.random.randint(1, 6)  # Random number of peaks for neutral state
    elif state == 'active':
        num_peaks = np.random.randint(6, 21)  # Random number of peaks for active state

    phasic = np.zeros(num_samples)
    for _ in range(num_peaks):
        peak_time = np.random.randint(0, num_samples)
        tau1 = np.random.uniform(1, 40)  # Time constant 1 for each peak
        tau2 = np.random.uniform(0.2, 1)  # Time constant 2 for each peak
        impulse_response = np.exp(-time * tau1) - np.exp(-time * tau2)
        # Ensure the length of the impulse_response matches the length of the signal
        phasic_part = np.zeros(num_samples)
        if peak_time + len(impulse_response) < num_samples:
            phasic_part[peak_time:peak_time+len(impulse_response)] = np.random.uniform(0.5, 2.0) * impulse_response
        else:
            phasic_part[peak_time:] = np.random.uniform(0.5, 2.0) * impulse_response[:num_samples-peak_time]
        phasic += phasic_part

    # Gaussian noise
    noise = np.random.normal(0, 0.1, num_samples)  # Adjust noise parameters as needed

    # Combine components
    eda_signal = baseline + phasic + noise

    return eda_signal

# Example parameters
num_samples = 5760  # Number of samples
sampling_freq = 32  # Sampling frequency (Hz)

# Generate synthetic EDA signal for neutral state
synthetic_signal_neutral = generate_synthetic_EDA(num_samples, sampling_freq, 'neutral')

# Generate synthetic EDA signal for active state
synthetic_signal_active = generate_synthetic_EDA(num_samples, sampling_freq, 'active')

# Plotting synthetic EDA signals in subplots
plt.figure(figsize=(10, 8))

plt.subplot(2, 1, 1)
plt.plot(synthetic_signal_neutral, label='Neutral State')
plt.title('Synthetic EDA Signal for Neutral State')
plt.xlabel('Time')
plt.ylabel('Signal Amplitude')
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(synthetic_signal_active, label='Active State')
plt.title('Synthetic EDA Signal for Active State')
plt.xlabel('Time')
plt.ylabel('Signal Amplitude')
plt.legend()

plt.tight_layout()
plt.show()
