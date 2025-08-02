import tkinter as tk
from tkinter import ttk
import time
import threading

class SortingVisualizer:
    def __init__(self):
        self.root = None
        self.canvas = None
        self.step_label = None
        self.condition_label = None
        self.summary_frame = None
        self.array = []
        self.steps = []
        self.current_step = 0
        self.cell_width = 80
        self.cell_height = 50
        self.delay = 1500
        self.show_summary = False
        
    def get_ordinal(self, n):
        return f"{n}{'th' if 10 <= n % 100 <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')}"
    
    def add_step(self, array, desc, comparing=[], swapped=False, pivot=-1, pointers=[], condition='', merge_ranges=[]):
        self.steps.append({
            'array': array.copy(),
            'description': desc,
            'comparing': comparing,
            'swapped': swapped,
            'pivot': pivot,
            'pointers': pointers,
            'condition': condition,
            'merge_ranges': merge_ranges
        })
        
    def get_user_input(self):
        print("=" * 50)
        print("SORTING ALGORITHM VISUALIZER")
        print("=" * 50)
        
        while True:
            try:
                size = int(input("Enter array size (3-10): "))
                if 3 <= size <= 10: break
                print("Please enter a size between 3 and 10")
            except ValueError:
                print("Please enter a valid integer")
        
        while True:
            try:
                print(f"Enter {size} elements separated by spaces:")
                elements = list(map(int, input().split()))
                if len(elements) == size:
                    self.array = elements
                    break
                print(f"Please enter exactly {size} elements")
            except ValueError:
                print("Please enter valid integers")
        
        print("\nSelect sorting algorithm:")
        algorithms = ["Bubble", "Quick", "Merge", "Selection", "Insertion", "Heap", "Counting"]
        for i, alg in enumerate(algorithms, 1):
            print(f"{i}. {alg} Sort")
        
        while True:
            try:
                choice = int(input("Enter your choice (1-7): "))
                if 1 <= choice <= 7:
                    return algorithms[choice-1].lower()
                print("Please enter a number between 1 and 7")
            except ValueError:
                print("Please enter a valid integer")

    def bubble_sort_steps(self, arr):
        self.steps = []
        arr_copy = arr.copy()
        n = len(arr_copy)
        
        self.add_step(arr_copy, 'Initial Unsorted array')
        
        for i in range(n):
            swapped = False
            for j in range(0, n - i - 1):
                condition = f"Compare: {arr_copy[j]} {'>' if arr_copy[j] > arr_copy[j+1] else '<='} {arr_copy[j+1]}"
                self.add_step(arr_copy, f'Compare {self.get_ordinal(j+1)} and {self.get_ordinal(j+2)} elements', [j, j+1], condition=condition)
                
                if arr_copy[j] > arr_copy[j + 1]:
                    self.add_step(arr_copy, f'Since {arr_copy[j]} > {arr_copy[j+1]}, we need to swap', [j, j+1], condition=f'Condition: {arr_copy[j]} > {arr_copy[j+1]} → SWAP needed')
                    arr_copy[j], arr_copy[j + 1] = arr_copy[j + 1], arr_copy[j]
                    swapped = True
                    self.add_step(arr_copy, f'Swap: {arr_copy[j+1]} ↔ {arr_copy[j]}', [j, j+1], True, condition=f'After swap: [{arr_copy[j]}, {arr_copy[j+1]}]')
                else:
                    self.add_step(arr_copy, f'Since {arr_copy[j]} ≤ {arr_copy[j+1]}, no swap needed', [j, j+1], condition=f'Condition: {arr_copy[j]} ≤ {arr_copy[j+1]} → No swap')
            
            if not swapped:
                self.add_step(arr_copy, f'Pass {i+1} complete - No swaps made, array is sorted!', condition='All elements are in correct order')
                break
            else:
                self.add_step(arr_copy, f'Pass {i+1} complete - Largest element moved to position {n-i}', condition='Continue to next pass...')
        
        self.add_step(arr_copy, 'Bubble Sort Complete - Array is now sorted!', condition='All elements: a₁ ≤ a₂ ≤ a₃ ≤ ... ≤ aₙ')
        return self.steps

    def selection_sort_steps(self, arr):
        self.steps = []
        arr_copy = arr.copy()
        n = len(arr_copy)
        
        self.add_step(arr_copy, 'Initial Unsorted array')
        
        for i in range(n):
            min_idx = i
            self.add_step(arr_copy, f'Find minimum element in unsorted portion [position {i+1} to {n}]', [i], pointers=[i], condition=f'Current minimum: {arr_copy[min_idx]} at position {min_idx+1}')
            
            for j in range(i + 1, n):
                self.add_step(arr_copy, f'Compare current minimum {arr_copy[min_idx]} with {arr_copy[j]}', [min_idx, j], pointers=[i], condition=f'Condition: {arr_copy[j]} < {arr_copy[min_idx]} ?')
                
                if arr_copy[j] < arr_copy[min_idx]:
                    min_idx = j
                    self.add_step(arr_copy, f'New minimum found: {arr_copy[min_idx]} at position {min_idx+1}', [min_idx], pointers=[i], condition=f'Update minimum: {arr_copy[min_idx]} < previous minimum')
                else:
                    self.add_step(arr_copy, f'{arr_copy[j]} ≥ {arr_copy[min_idx]}, keep current minimum', [min_idx, j], pointers=[i], condition=f'No change: {arr_copy[j]} ≥ {arr_copy[min_idx]}')
            
            if min_idx != i:
                self.add_step(arr_copy, f'Swap minimum {arr_copy[min_idx]} with element at position {i+1}', [i, min_idx], condition=f'Swap: {arr_copy[i]} ↔ {arr_copy[min_idx]}')
                arr_copy[i], arr_copy[min_idx] = arr_copy[min_idx], arr_copy[i]
                self.add_step(arr_copy, f'Minimum element placed at position {i+1}', [i, min_idx], True, condition=f'After swap: position {i+1} = {arr_copy[i]}')
            else:
                self.add_step(arr_copy, f'Element at position {i+1} is already minimum, no swap needed', [i], condition=f'No swap needed: {arr_copy[i]} already in correct position')
        
        self.add_step(arr_copy, 'Selection Sort Complete - Array is now sorted!', condition='All elements: a₁ ≤ a₂ ≤ a₃ ≤ ... ≤ aₙ')
        return self.steps

    def insertion_sort_steps(self, arr):
        self.steps = []
        arr_copy = arr.copy()
        n = len(arr_copy)
        
        self.add_step(arr_copy, 'Initial array - first element is considered sorted', pointers=[0], condition='Sorted portion: [0], Unsorted portion: [1..n-1]')
        
        for i in range(1, n):
            key = arr_copy[i]
            j = i - 1
            
            self.add_step(arr_copy, f'Insert element {key} from position {i+1} into sorted portion', [i], pointers=[i], condition=f'Key = {key}, compare with sorted elements from right to left')
            
            while j >= 0 and arr_copy[j] > key:
                self.add_step(arr_copy, f'Compare {key} with {arr_copy[j]} at position {j+1}', [j, i], condition=f'Condition: {arr_copy[j]} > {key} → Shift {arr_copy[j]} right')
                arr_copy[j + 1] = arr_copy[j]
                self.add_step(arr_copy, f'Shift {arr_copy[j+1]} to position {j+2}', [j, j+1], True, condition=f'Shifted: {arr_copy[j+1]} moved right')
                j -= 1
                i = j + 1
            
            if j >= 0:
                self.add_step(arr_copy, f'Compare {key} with {arr_copy[j]} - found correct position', [j, j+1], condition=f'Condition: {arr_copy[j]} ≤ {key} → Stop shifting')
            
            arr_copy[j + 1] = key
            self.add_step(arr_copy, f'Insert {key} at position {j+2}', [j+1], True, condition=f'Key {key} inserted in correct position')
        
        self.add_step(arr_copy, 'Insertion Sort Complete - Array is now sorted!', condition='All elements: a₁ ≤ a₂ ≤ a₃ ≤ ... ≤ aₙ')
        return self.steps

    def heap_sort_steps(self, arr):
        self.steps = []
        arr_copy = arr.copy()
        n = len(arr_copy)
        
        self.add_step(arr_copy, 'Initial array - Build max heap first', condition='Convert array to max heap structure')
        
        def heapify(arr, n, i):
            largest = i
            left = 2 * i + 1
            right = 2 * i + 2
            
            if left < n:
                self.add_step(arr, f'Compare parent {arr[i]} with left child {arr[left]}', [i, left], condition=f'Left child: {arr[left]} {">" if arr[left] > arr[largest] else "≤"} parent: {arr[largest]}')
                if arr[left] > arr[largest]:
                    largest = left
            
            if right < n:
                self.add_step(arr, f'Compare current largest {arr[largest]} with right child {arr[right]}', [largest, right], condition=f'Right child: {arr[right]} {">" if arr[right] > arr[largest] else "≤"} current largest: {arr[largest]}')
                if arr[right] > arr[largest]:
                    largest = right
            
            if largest != i:
                self.add_step(arr, f'Swap parent {arr[i]} with largest child {arr[largest]}', [i, largest], condition=f'Maintain heap property: swap {arr[i]} ↔ {arr[largest]}')
                arr[i], arr[largest] = arr[largest], arr[i]
                self.add_step(arr, f'After swap - continue heapifying subtree', [i, largest], True, condition=f'Swapped: parent = {arr[i]}, child = {arr[largest]}')
                heapify(arr, n, largest)
        
        for i in range(n // 2 - 1, -1, -1):
            self.add_step(arr_copy, f'Heapify subtree rooted at index {i}', [i], pointers=[i], condition=f'Process node {arr_copy[i]} at position {i+1}')
            heapify(arr_copy, n, i)
        
        self.add_step(arr_copy, 'Max heap built successfully!', condition='Heap property: parent ≥ children for all nodes')
        
        for i in range(n - 1, 0, -1):
            self.add_step(arr_copy, f'Extract maximum {arr_copy[0]} from heap', [0, i], condition=f'Move max element {arr_copy[0]} to sorted position {i+1}')
            arr_copy[0], arr_copy[i] = arr_copy[i], arr_copy[0]
            self.add_step(arr_copy, f'Swapped max element to position {i+1}', [0, i], True, condition=f'Sorted portion: [{i+1}..{n}], Heap portion: [1..{i}]')
            
            if i > 1:
                self.add_step(arr_copy, f'Restore heap property for reduced heap of size {i}', [0], pointers=[0], condition=f'Heapify root with {i} elements remaining')
                heapify(arr_copy, i, 0)
        
        self.add_step(arr_copy, 'Heap Sort Complete - Array is now sorted!', condition='All elements: a₁ ≤ a₂ ≤ a₃ ≤ ... ≤ aₙ')
        return self.steps

    def counting_sort_steps(self, arr):
        self.steps = []
        arr_copy = arr.copy()
        n = len(arr_copy)
        
        max_val, min_val = max(arr_copy), min(arr_copy)
        range_val = max_val - min_val + 1
        
        self.add_step(arr_copy, 'Initial array for Counting Sort', condition=f'Range: {min_val} to {max_val}, Size: {range_val}')
        
        count = [0] * range_val
        self.add_step(arr_copy, f'Initialize count array of size {range_val}', condition=f'Count array: {count} (index 0 represents value {min_val})')
        
        for i in range(n):
            count[arr_copy[i] - min_val] += 1
            self.add_step(arr_copy, f'Count element {arr_copy[i]} at position {i+1}', [i], condition=f'Count[{arr_copy[i]}] = {count[arr_copy[i] - min_val]}, Count array: {count}')
        
        for i in range(1, range_val):
            count[i] += count[i - 1]
            self.add_step(arr_copy, f'Calculate cumulative count for index {i}', condition=f'Cumulative count[{i}] = {count[i]}, Array: {count}')
        
        self.add_step(arr_copy, 'Cumulative count array shows final positions', condition=f'Final count array: {count}')
        
        output = [0] * n
        for i in range(n - 1, -1, -1):
            val = arr_copy[i]
            pos = count[val - min_val] - 1
            output[pos] = val
            count[val - min_val] -= 1
            self.add_step(output, f'Place {val} at position {pos + 1} in output array', [pos], True, condition=f'Element {val} goes to position {pos + 1}, update count[{val}] = {count[val - min_val]}')
        
        for i in range(n):
            arr_copy[i] = output[i]
        
        self.add_step(arr_copy, 'Counting Sort Complete - Array is now sorted!', condition='All elements: a₁ ≤ a₂ ≤ a₃ ≤ ... ≤ aₙ')
        return self.steps
    
    def quick_sort_steps(self, arr):
        self.steps = []
        arr_copy = arr.copy()
        
        self.add_step(arr_copy, 'Initial Unsorted array')
        
        def partition(arr, low, high):
            pivot_idx = high
            pivot = arr[pivot_idx]
            
            self.add_step(arr, f'Choose pivot: element at position {pivot_idx + 1}', pivot=pivot_idx, condition=f'Pivot = {pivot} (last element)')
            
            left = low
            right = high - 1
            
            self.add_step(arr, 'Initialize left and right pointers', pivot=pivot_idx, pointers=[left, right], condition=f'Left pointer at position {left+1}, Right pointer at position {right+1}')
            
            while left <= right:
                while left <= right and arr[left] < pivot:
                    self.add_step(arr, f'Check left element: {arr[left]} < {pivot}?', [left], pivot=pivot_idx, pointers=[left, right], condition=f'Condition: {arr[left]} < {pivot} → TRUE, move left pointer')
                    left += 1
                    if left <= right:
                        self.add_step(arr, f'Move left pointer to position {left+1}', pivot=pivot_idx, pointers=[left, right], condition=f'Left pointer now at element {arr[left] if left < len(arr) else "end"}')
                
                if left <= right:
                    self.add_step(arr, f'Left element check: {arr[left]} < {pivot}?', [left], pivot=pivot_idx, pointers=[left, right], condition=f'Condition: {arr[left]} < {pivot} → FALSE, stop left pointer')
                
                while left <= right and arr[right] > pivot:
                    self.add_step(arr, f'Check right element: {arr[right]} > {pivot}?', [right], pivot=pivot_idx, pointers=[left, right], condition=f'Condition: {arr[right]} > {pivot} → TRUE, move right pointer')
                    right -= 1
                    if left <= right:
                        self.add_step(arr, f'Move right pointer to position {right+1}', pivot=pivot_idx, pointers=[left, right], condition=f'Right pointer now at element {arr[right] if right >= 0 else "start"}')
                
                if left <= right:
                    self.add_step(arr, f'Right element check: {arr[right]} > {pivot}?', [right], pivot=pivot_idx, pointers=[left, right], condition=f'Condition: {arr[right]} > {pivot} → FALSE, stop right pointer')
                
                if left <= right:
                    if left < right:
                        self.add_step(arr, f'Pointers haven\'t crossed - swap needed', [left, right], pivot=pivot_idx, pointers=[left, right], condition=f'Left({arr[left]}) and Right({arr[right]}) need swapping')
                        arr[left], arr[right] = arr[right], arr[left]
                        self.add_step(arr, f'Swap: {arr[right]} ↔ {arr[left]}', [left, right], True, pivot=pivot_idx, pointers=[left, right], condition=f'After swap: position {left+1}={arr[left]}, position {right+1}={arr[right]}')
                    
                    left += 1
                    right -= 1
                    
                    if left <= high - 1:
                        self.add_step(arr, 'Move both pointers inward', pivot=pivot_idx, pointers=[left, right] if right >= low else [left], condition=f'Continue partitioning with new pointer positions')
            
            if left != pivot_idx:
                self.add_step(arr, f'Pointers crossed - place pivot in correct position', [left, pivot_idx], pivot=pivot_idx, condition=f'Swap pivot {arr[pivot_idx]} with element at position {left+1} ({arr[left]})')
                arr[left], arr[pivot_idx] = arr[pivot_idx], arr[left]
                self.add_step(arr, f'Pivot placed correctly at position {left+1}', [left, pivot_idx], True, pivot=left, condition=f'Pivot {arr[left]} is now in its final sorted position')
            else:
                self.add_step(arr, f'Pivot already in correct position', pivot=left, condition=f'Pivot {arr[left]} was already in its correct position')
            
            return left
        
        def quicksort_recursive(arr, low, high):
            if low < high:
                pi = partition(arr, low, high)
                if pi > low + 1:
                    self.add_step(arr, f'Recursively sort left subarray [positions {low+1} to {pi}]', condition=f'Left subarray: {arr[low:pi]}')
                quicksort_recursive(arr, low, pi - 1)
                
                if pi < high - 1:
                    self.add_step(arr, f'Recursively sort right subarray [positions {pi+2} to {high+1}]', condition=f'Right subarray: {arr[pi+1:high+1]}')
                quicksort_recursive(arr, pi + 1, high)
        
        quicksort_recursive(arr_copy, 0, len(arr_copy) - 1)
        self.add_step(arr_copy, 'Quick Sort Complete - Array is now sorted!', condition='All subarrays merged: a₁ ≤ a₂ ≤ a₃ ≤ ... ≤ aₙ')
        return self.steps
    
    def merge_sort_steps(self, arr):
        self.steps = []
        arr_copy = arr.copy()
        
        self.add_step(arr_copy, 'Initial Unsorted array')
        
        def merge_sort_recursive(arr, left, right, temp_arr):
            if left < right:
                mid = (left + right) // 2
                self.add_step(temp_arr, f'Divide: Split array into two halves', merge_ranges=[(left, mid), (mid + 1, right)], condition=f'Left: {arr[left:mid+1]}, Right: {arr[mid+1:right+1]}')
                
                merge_sort_recursive(arr, left, mid, temp_arr)
                merge_sort_recursive(arr, mid + 1, right, temp_arr)
                merge(arr, left, mid, right, temp_arr)
        
        def merge(arr, left, mid, right, temp_arr):
            left_arr = arr[left:mid + 1]
            right_arr = arr[mid + 1:right + 1]
            
            self.add_step(temp_arr, f'Merge subarrays: {left_arr} and {right_arr}', merge_ranges=[(left, mid), (mid + 1, right)], condition=f'Comparing elements from both subarrays')
            
            i = j = 0
            k = left
            
            while i < len(left_arr) and j < len(right_arr):
                left_val, right_val = left_arr[i], right_arr[j]
                
                self.add_step(temp_arr, f'Compare: {left_val} vs {right_val}', [k], condition=f'Condition: {left_val} {"≤" if left_val <= right_val else ">"} {right_val}')
                
                if left_val <= right_val:
                    temp_arr[k] = left_val
                    i += 1
                    self.add_step(temp_arr, f'Since {left_val} ≤ {right_val}, place {left_val} at position {k + 1}', [k], condition=f'Take from left subarray: {left_val} → position {k+1}')
                else:
                    temp_arr[k] = right_val
                    j += 1
                    self.add_step(temp_arr, f'Since {right_val} < {left_val}, place {right_val} at position {k + 1}', [k], condition=f'Take from right subarray: {right_val} → position {k+1}')
                
                k += 1
            
            while i < len(left_arr):
                temp_arr[k] = left_arr[i]
                self.add_step(temp_arr, f'Copy remaining element from left: {left_arr[i]}', [k], condition=f'Left subarray not empty: {left_arr[i]} → position {k+1}')
                i, k = i + 1, k + 1
                
            while j < len(right_arr):
                temp_arr[k] = right_arr[j]
                self.add_step(temp_arr, f'Copy remaining element from right: {right_arr[j]}', [k], condition=f'Right subarray not empty: {right_arr[j]} → position {k+1}')
                j, k = j + 1, k + 1
            
            for idx in range(left, right + 1):
                arr[idx] = temp_arr[idx]
            
            self.add_step(temp_arr, f'Merge complete for range [{left+1}..{right+1}]', condition=f'Merged result: {temp_arr[left:right+1]}')
        
        temp_array = arr_copy.copy()
        merge_sort_recursive(arr_copy, 0, len(arr_copy) - 1, temp_array)
        self.add_step(arr_copy, 'Merge Sort Complete - Array is now sorted!', condition='Final result: All subarrays merged in sorted order')
        return self.steps
    
    def create_summary_view(self):
        if self.summary_frame:
            self.summary_frame.destroy()
        
        for widget in self.root.winfo_children():
            if widget != self.summary_frame:
                widget.pack_forget()
        
        self.summary_frame = tk.Frame(self.root, bg='white')
        self.summary_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        summary_title = tk.Label(self.summary_frame, text="All Steps Summary", font=('Arial', 18, 'bold'), bg='white')
        summary_title.pack(pady=(0, 20))
        
        canvas = tk.Canvas(self.summary_frame, bg='white')
        scrollbar = ttk.Scrollbar(self.summary_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='white')
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        for step_num, step_data in enumerate(self.steps):
            step_frame = tk.Frame(scrollable_frame, bg='white', relief='solid', borderwidth=1)
            step_frame.pack(fill='x', pady=5, padx=10)
            
            header_text = f"Step {step_num}" if step_num > 0 else "Initial"
            step_header = tk.Label(step_frame, text=header_text, font=('Arial', 12, 'bold'), bg='lightgray')
            step_header.pack(fill='x', pady=2)
            
            desc_label = tk.Label(step_frame, text=step_data['description'], font=('Arial', 10), bg='white', wraplength=800)
            desc_label.pack(pady=2)
            
            array_frame = tk.Frame(step_frame, bg='white')
            array_frame.pack(pady=5)
            
            array = step_data['array']
            comparing = step_data.get('comparing', [])
            pivot = step_data.get('pivot', -1)
            pointers = step_data.get('pointers', [])
            swapped = step_data.get('swapped', False)
            
            for i, value in enumerate(array):
                color = 'white'
                if i == pivot:
                    color = 'yellow'
                elif i in comparing:
                    color = 'lightblue' if not swapped else 'lightcoral'
                elif i in pointers:
                    color = 'lightgreen'
                
                cell = tk.Label(array_frame, text=str(value), width=6, height=2, bg=color, relief='solid', borderwidth=1, font=('Arial', 12, 'bold'))
                cell.pack(side='left', padx=1)
            
            condition = step_data.get('condition', '')
            if condition:
                condition_label = tk.Label(step_frame, text=f"Logic: {condition}", font=('Arial', 9, 'italic'), bg='lightgray', wraplength=800)
                condition_label.pack(pady=2, fill='x')
        
        back_btn = tk.Button(self.summary_frame, text="← Back to Animation", font=('Arial', 12), command=self.show_main_view, bg='lightblue')
        back_btn.pack(pady=20)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def show_main_view(self):
        if self.summary_frame:
            self.summary_frame.destroy()
            self.summary_frame = None
        
        self.show_summary = False
        self.create_main_interface()
        self.update_display()
    
    def create_main_interface(self):
        title_label = tk.Label(self.root, text=f"{self.current_algorithm.title()} Sort Visualization", font=('Arial', 20, 'bold'), bg='white')
        title_label.pack(pady=20)
        
        canvas_frame = tk.Frame(self.root, bg='white')
        canvas_frame.pack(pady=20)
        
        canvas_width = len(self.array) * self.cell_width + 100
        canvas_height = 150
        self.canvas = tk.Canvas(canvas_frame, width=canvas_width, height=canvas_height, bg='white', highlightthickness=1, highlightbackground='black')
        self.canvas.pack()
        
        self.step_label = tk.Label(self.root, text="", font=('Arial', 14), bg='white', wraplength=800, justify='center')
        self.step_label.pack(pady=(10, 5))
        
        self.condition_label = tk.Label(self.root, text="", font=('Arial', 12, 'italic'), bg='lightgray', wraplength=800, justify='center', relief='solid', borderwidth=1, pady=5)
        self.condition_label.pack(pady=(5, 20), padx=20, fill='x')
        
        button_frame = tk.Frame(self.root, bg='white')
        button_frame.pack(pady=20)
        
        buttons = [
            ("← Previous", self.prev_step, 'lightblue'),
            ("Next →", self.next_step, 'lightgreen'),
            ("Auto Play", self.auto_play, 'yellow'),
            ("Reset", self.reset_visualization, 'lightcoral'),
            ("View All Steps", self.create_summary_view, 'lightpink')
        ]
        
        for text, command, color in buttons:
            btn = tk.Button(button_frame, text=text, font=('Arial', 12), command=command, bg=color)
            btn.pack(side=tk.LEFT, padx=10)
        
        self.step_counter = tk.Label(self.root, text="", font=('Arial', 12), bg='white')
        self.step_counter.pack(pady=10)
    
    def create_gui(self, algorithm):
        self.current_algorithm = algorithm
        self.root = tk.Tk()
        self.root.title(f"{algorithm.title()} Sort Visualization")
        self.root.geometry("1200x700")
        self.root.configure(bg='white')
        
        sort_methods = {
            "bubble": self.bubble_sort_steps,
            "quick": self.quick_sort_steps,
            "merge": self.merge_sort_steps,
            "selection": self.selection_sort_steps,
            "insertion": self.insertion_sort_steps,
            "heap": self.heap_sort_steps,
            "counting": self.counting_sort_steps
        }
        
        self.steps = sort_methods[algorithm](self.array)
        self.create_main_interface()
        self.update_display()
        
    def draw_array(self, step_data):
        self.canvas.delete("all")
        
        array = step_data['array']
        comparing = step_data.get('comparing', [])
        pivot = step_data.get('pivot', -1)
        pointers = step_data.get('pointers', [])
        swapped = step_data.get('swapped', False)
        
        start_x, start_y = 50, 50
        
        for i, value in enumerate(array):
            x1 = start_x + i * self.cell_width
            y1 = start_y
            x2 = x1 + self.cell_width - 10
            y2 = y1 + self.cell_height
            
            color = 'white'
            if i == pivot:
                color = 'yellow'
            elif i in comparing:
                color = 'lightblue' if not swapped else 'lightcoral'
            elif i in pointers:
                color = 'lightgreen'
            
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='black', width=2)
            
            text_x = x1 + (self.cell_width - 10) // 2
            text_y = y1 + self.cell_height // 2
            self.canvas.create_text(text_x, text_y, text=str(value), font=('Arial', 16, 'bold'))
        
        if pointers:
            for i, pos in enumerate(pointers):
                if pos < len(array):
                    x = start_x + pos * self.cell_width + (self.cell_width - 10) // 2
                    y = start_y + self.cell_height + 20
                    label = 'L' if i == 0 else 'R'
                    self.canvas.create_text(x, y, text=label, font=('Arial', 12, 'bold'))
                    self.canvas.create_polygon(x-5, y-15, x+5, y-15, x, y-5, fill='black')
    
    def update_display(self):
        if 0 <= self.current_step < len(self.steps):
            step_data = self.steps[self.current_step]
            
            self.draw_array(step_data)
            
            step_num = f"Step {self.current_step}" if self.current_step > 0 else "Initial"
            description = step_data['description']
            self.step_label.config(text=f"{step_num}: {description}")
            
            condition = step_data.get('condition', '')
            self.condition_label.config(text=f"Logic: {condition}" if condition else "")
            
            self.step_counter.config(text=f"Step {self.current_step + 1} of {len(self.steps)}")
    
    def next_step(self):
        if self.current_step < len(self.steps) - 1:
            self.current_step += 1
            self.update_display()
    
    def prev_step(self):
        if self.current_step > 0:
            self.current_step -= 1
            self.update_display()
    
    def auto_play(self):
        def play():
            while self.current_step < len(self.steps) - 1:
                time.sleep(self.delay / 1000)
                self.root.after(0, self.next_step)
        
        thread = threading.Thread(target=play)
        thread.daemon = True
        thread.start()
    
    def reset_visualization(self):
        self.current_step = 0
        self.update_display()
    
    def run(self):
        algorithm = self.get_user_input()
        
        print(f"\nStarting {algorithm.title()} Sort visualization...")
        print("Opening visualization window...")
        
        self.create_gui(algorithm)
        self.root.mainloop()

if __name__ == "__main__":
    visualizer = SortingVisualizer()
    visualizer.run()
