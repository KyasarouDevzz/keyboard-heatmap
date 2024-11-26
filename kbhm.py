import keyboard
from pynput import mouse
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np

# Rebind Esc to F5
keyboard.remap_key('esc', 'f5')

# Step 1: Track key presses
key_counts = defaultdict(int)

def on_key_press(event):
    if event.name != 'space':  # Exclude the spacebar
        key_counts[event.name] += 1

keyboard.on_press(on_key_press)

print("Start typing. Press 'F5' to stop logging keyboard inputs.")  # Updated stop key

# Track mouse clicks and movements
mouse_counts = {'left': 0, 'right': 0}
mouse_positions = []

def on_click(x, y, button, pressed):
    if pressed:
        if button == mouse.Button.left:
            mouse_counts['left'] += 1
        elif button == mouse.Button.right:
            mouse_counts['right'] += 1

def on_move(x, y):
    mouse_positions.append((x, y))

# Start mouse listener
mouse_listener = mouse.Listener(on_click=on_click, on_move=on_move)
mouse_listener.start()

keyboard.wait('f5')  # Wait for F5 instead of Esc

# Stop mouse listener
mouse_listener.stop()

# Step 2 & 3: Calculate keyboard percentages
total_presses = sum(key_counts.values())
key_percentages = {key: (count / total_presses) * 100 for key, count in key_counts.items()}

# Generate keyboard heatmap
keyboard_layout = [
    ['esc', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', 'backspace'],
    ['tab', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']', '\\'],
    ['capslock', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', "'", 'enter'],
    ['shift', 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/', 'shift'],
    ['ctrl', 'fn', 'windows', 'alt', 'space', 'alt', 'ctrl']
]

keyboard_heatmap = np.zeros((len(keyboard_layout), max(map(len, keyboard_layout))))

for row_idx, row in enumerate(keyboard_layout):
    for col_idx, key in enumerate(row):
        if key in key_percentages:
            keyboard_heatmap[row_idx, col_idx] = key_percentages[key]

plt.figure(figsize=(12, 8))

plt.subplot(1, 2, 1)
plt.imshow(keyboard_heatmap, cmap='Greens', interpolation='nearest')
plt.title('Keyboard Heatmap')
plt.colorbar(label='% of Use')

# Add labels to keyboard heatmap
for row_idx, row in enumerate(keyboard_layout):
    for col_idx, key in enumerate(row):
        if key in key_percentages:
            plt.text(col_idx, row_idx, key, ha='center', va='center', color='black')

# Generate mouse heatmap
mouse_positions = np.array(mouse_positions)
mouse_heatmap, xedges, yedges = np.histogram2d(mouse_positions[:, 0], mouse_positions[:, 1], bins=[50, 50])
mouse_heatmap = mouse_heatmap.T  # Transpose for correct orientation

plt.subplot(1, 2, 2)
plt.imshow(mouse_heatmap, cmap='Blues', interpolation='nearest')
plt.title('Mouse Heatmap')
plt.colorbar(label='Frequency')

plt.tight_layout()
plt.show()

# Print mouse click counts
print(f"Left mouse button clicks: {mouse_counts['left']}")
print(f"Right mouse button clicks: {mouse_counts['right']}")
