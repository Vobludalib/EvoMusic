import matplotlib
import miditoolkit
import numpy as np
import matplotlib.pyplot as plt

def plot_piano_roll(ind_pr, target_pr, output_image_path):
    # Plot the piano roll
    plt.figure(figsize=(12, 6))
    shown_pr = np.zeros(ind_pr.T.shape)
    for i in range(ind_pr.shape[0]):
        for j in range(ind_pr.shape[1]):
            if ind_pr[i, j] > 0 and target_pr[i, j] > 0:
                shown_pr[j, i] = 2  # Show matching notes in a different color
            if ind_pr[i,j] == 0 and target_pr[i, j] == 0:
                shown_pr[j, i] = 0 # Show matching spaces in a different color
            if ind_pr[i, j] > 0 and target_pr[i, j] == 0:
                shown_pr[j, i] = 1 # Show extra notes in a different color
            if ind_pr[i, j] == 0 and target_pr[i, j] > 0:
                shown_pr[j, i] = 3 # Show missing notes in a different color
    plt.imshow(shown_pr, aspect='auto', origin='lower', cmap='Dark2', extent=[0, ind_pr.shape[1]/100, 0, 128])
    plt.colorbar(label='Velocity')
    plt.xlabel('Time (s)')
    plt.ylabel('MIDI Note Number')
    plt.title('Piano Roll')
    plt.grid(False)

    # Save the plot as an image
    plt.savefig(output_image_path)
    plt.close()