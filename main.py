import pygame
import random
import time
import tkinter as tk
from tkinter import simpledialog, messagebox
import sys

# Global flag to stop sorting
stop_requested = False

WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLUE = (100, 149, 237)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

# Default visualization settings
VISUALIZE = True
DELAY_COMPARISION = 10
DELAY_SHIFT = 20
DELAY_SWAP = 30

root = tk.Tk()
root.withdraw()

messagebox.showinfo(
    "Help - Sorting Visualizer",
    "This tool visualizes how sorting algorithms work.\n\n"
    "Key Controls:\n"
    "- S: Selection Sort\n"
    "- I: Insertion Sort\n"
    "- B: Bubble Sort\n"
    "- M: Merge Sort\n"
    "- Q: Quick Sort\n"
    "- L: Shell Sort\n"
    "- C: Count Sort\n"
    "- R: Shuffle Array\n"
    "- H: Show this Help Menu\n"
    "- ESC: Cancel Ongoing Sort\n"
    "- T: Change Delay Settings"
)

# config = simpledialog.askstring("Configuration", "Use default settings? (yes/no)")
# if config and config.lower() == 'no':
#     use_visuals = simpledialog.askstring("Visualization", "Enable visualization? (yes/no)")
#     if use_visuals and use_visuals.lower() == 'no':
#         VISUALIZE = False
#     DELAY_COMPARISION = int(simpledialog.askstring("Delay", "Delay for comparisons (ms):", initialvalue=str(DELAY_COMPARISION)) or DELAY_COMPARISION)
#     DELAY_SHIFT = int(simpledialog.askstring("Delay", "Delay for shifts (ms):", initialvalue=str(DELAY_SHIFT)) or DELAY_SHIFT)
#     DELAY_SWAP = int(simpledialog.askstring("Delay", "Delay for swaps (ms):", initialvalue=str(DELAY_SWAP)) or DELAY_SWAP)

pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sorting Visualizer - Press H for Help")
FONT = pygame.font.SysFont('Arial', 24)

array = [random.randint(10, HEIGHT - 10) for _ in range(100)]

def draw_text(text, pos, color=BLACK):
    rendered = FONT.render(text, True, color)
    win.blit(rendered, pos)

def check_for_exit():
    global stop_requested
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            stop_requested = True

def draw_array(array, color_positions={}, delay=10, message=""):
    check_for_exit()
    win.fill(WHITE)
    bar_width = WIDTH // len(array)
    for i, val in enumerate(array):
        color = color_positions.get(i, BLUE)
        pygame.draw.rect(win, color, (i * bar_width, HEIGHT - val, bar_width, val))
    if message:
        draw_text(message, (10, 10))
    pygame.display.update()
    pygame.time.delay(delay if VISUALIZE else 0)

# Sorting algorithms
def selection_sort(array):
    global stop_requested
    stop_requested = False
    for i in range(len(array)):
        if stop_requested:
            return
        min_idx = i
        for j in range(i + 1, len(array)):
            if stop_requested:
                return
            if array[j] < array[min_idx]:
                min_idx = j
            draw_array(array, color_positions={j: RED, min_idx: YELLOW}, delay=DELAY_COMPARISION)
        array[i], array[min_idx] = array[min_idx], array[i]
        draw_array(array, color_positions={i: GREEN, min_idx: GREEN}, delay=DELAY_SWAP)

def insertion_sort(array):
    global stop_requested
    stop_requested = False
    for i in range(1, len(array)):
        if stop_requested:
            return
        key = array[i]
        j = i - 1
        while j >= 0 and array[j] > key:
            if stop_requested:
                return
            array[j + 1] = array[j]
            draw_array(array, color_positions={j: RED}, delay=DELAY_SHIFT)
            j -= 1
        array[j + 1] = key
        draw_array(array, color_positions={j + 1: GREEN}, delay=DELAY_SHIFT)

def bubble_sort(array):
    global stop_requested
    stop_requested = False
    for i in range(len(array)):
        if stop_requested:
            return
        for j in range(0, len(array) - i - 1):
            if stop_requested:
                return
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]
                draw_array(array, color_positions={j: RED, j + 1: GREEN}, delay=DELAY_SWAP)

def merge_sort_wrapper(array):
    global stop_requested
    stop_requested = False

    def merge_sort(arr, l, r):
        if stop_requested:
            return
        if l < r:
            m = (l + r) // 2
            merge_sort(arr, l, m)
            merge_sort(arr, m + 1, r)
            merge(arr, l, m, r)

    def merge(arr, l, m, r):
        if stop_requested:
            return
        left = arr[l:m + 1]
        right = arr[m + 1:r + 1]
        i = j = 0
        k = l
        while i < len(left) and j < len(right):
            if stop_requested:
                return
            if left[i] < right[j]:
                arr[k] = left[i]
                i += 1
            else:
                arr[k] = right[j]
                j += 1
            draw_array(arr, color_positions={k: GREEN}, delay=DELAY_COMPARISION)
            k += 1
        while i < len(left):
            if stop_requested:
                return
            arr[k] = left[i]
            i += 1
            k += 1
        while j < len(right):
            if stop_requested:
                return
            arr[k] = right[j]
            j += 1
            k += 1

    merge_sort(array, 0, len(array) - 1)

def quicksort(array):
    global stop_requested
    stop_requested = False

    def quick_sort(arr, low, high):
        if stop_requested:
            return
        if low < high:
            pi = partition(arr, low, high)
            quick_sort(arr, low, pi - 1)
            quick_sort(arr, pi + 1, high)

    def partition(arr, low, high):
        if stop_requested:
            return 0
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            if stop_requested:
                return 0
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                draw_array(arr, color_positions={i: GREEN, j: RED}, delay=DELAY_SWAP)
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        draw_array(arr, color_positions={i + 1: YELLOW, high: RED}, delay=DELAY_SWAP)
        return i + 1

    quick_sort(array, 0, len(array) - 1)

def shell_sort(array):
    global stop_requested
    stop_requested = False
    n = len(array)
    gap = n // 2
    while gap > 0:
        if stop_requested:
            return
        for i in range(gap, n):
            if stop_requested:
                return
            temp = array[i]
            j = i
            while j >= gap and array[j - gap] > temp:
                if stop_requested:
                    return
                array[j] = array[j - gap]
                draw_array(array, color_positions={j: RED}, delay=DELAY_SHIFT)
                j -= gap
            array[j] = temp
        gap //= 2

def count_sort(array):
    global stop_requested
    stop_requested = False
    max_val = max(array)
    count = [0] * (max_val + 1)
    for val in array:
        if stop_requested:
            return
        count[val] += 1
    k = 0
    for i in range(len(count)):
        if stop_requested:
            return
        for _ in range(count[i]):
            if stop_requested:
                return
            array[k] = i
            draw_array(array, color_positions={k: GREEN}, delay=DELAY_SWAP)
            k += 1

# Main loop
def main():
    global stop_requested
    run = True
    sorting = False
    algorithm = None
    sort_time_message = ""

    instructions = [
        "Instructions:",
        "Press S - Selection Sort",
        "Press I - Insertion Sort",
        "Press B - Bubble Sort",
        "Press M - Merge Sort",
        "Press Q - Quick Sort",
        "Press L - Shell Sort",
        "Press C - Count Sort",
        "Press R - Shuffle Array",
        "Press H - Show Help Again",
        "Press T - Change Delay Settings",
        "Press ESC - Cancel Sorting",
        "Close Window - Exit"
    ]

    while run:
        draw_array(array, message=sort_time_message)
        for idx, line in enumerate(instructions):
            draw_text(line, (10, 30 + idx * 20))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    sorting, algorithm = True, "selection"
                elif event.key == pygame.K_i:
                    sorting, algorithm = True, "insertion"
                elif event.key == pygame.K_b:
                    sorting, algorithm = True, "bubble"
                elif event.key == pygame.K_m:
                    sorting, algorithm = True, "merge"
                elif event.key == pygame.K_q:
                    sorting, algorithm = True, "quick"
                elif event.key == pygame.K_l:
                    sorting, algorithm = True, "shell"
                elif event.key == pygame.K_c:
                    sorting, algorithm = True, "count"
                elif event.key == pygame.K_r:
                    sorting = False
                    random.shuffle(array)
                    algorithm = None
                elif event.key == pygame.K_h:
                    messagebox.showinfo("Help", "\n".join(instructions))
                elif event.key == pygame.K_t:
                    use_visuals = simpledialog.askstring("Visualization", "Enable visualization? (yes/no)")
                    if use_visuals and use_visuals.lower() == 'no':
                        VISUALIZE = False
                    else:
                        VISUALIZE = True
                        globals()['DELAY_COMPARISION'] = int(simpledialog.askstring("Delay", "Comparisons (ms):", initialvalue=str(DELAY_COMPARISION)) or DELAY_COMPARISION)
                        globals()['DELAY_SHIFT'] = int(simpledialog.askstring("Delay", "Shifts (ms):", initialvalue=str(DELAY_SHIFT)) or DELAY_SHIFT)
                        globals()['DELAY_SWAP'] = int(simpledialog.askstring("Delay", "Swaps (ms):", initialvalue=str(DELAY_SWAP)) or DELAY_SWAP)

        if sorting:
            start = time.time()
            if algorithm == "selection":
                selection_sort(array)
            elif algorithm == "insertion":
                insertion_sort(array)
            elif algorithm == "bubble":
                bubble_sort(array)
            elif algorithm == "merge":
                merge_sort_wrapper(array)
            elif algorithm == "quick":
                quicksort(array)
            elif algorithm == "shell":
                shell_sort(array)
            elif algorithm == "count":
                count_sort(array)
            end = time.time()
            sort_time_message = f"{algorithm.capitalize()} Sort Time: {round(end - start, 4)} s" if not stop_requested else "Sorting Cancelled"
            sorting = False
            algorithm = None

    pygame.quit()

if __name__ == "__main__":
    main()
