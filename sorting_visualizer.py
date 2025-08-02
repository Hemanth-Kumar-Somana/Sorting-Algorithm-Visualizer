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
        self.delay = 1500  # milliseconds
        self.show_summary = False
        
    def get_ordinal(self, n):
        """Get ordinal number (1st, 2nd, 3rd, etc.)"""
        if 10 <= n % 100 <= 20:
            suffix = 'th'
        else:
            suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
        return f"{n}{suffix}"
        
    def get_user_input(self):
        """Get input from terminal"""
        print("=" * 50)
        print("SORTING ALGORITHM VISUALIZER")
        print("=" * 50)
        
        # Get array size
        while True:
            try:
                size = int(input("Enter array size (3-10): "))
                if 3 <= size <= 10:
                    break
                else:
                    print("Please enter a size between 3 and 10")
            except ValueError:
                print("Please enter a valid integer")
        
        # Get array elements
        while True:
            try:
                print(f"Enter {size} elements separated by spaces:")
                elements = list(map(int, input().split()))
                if len(elements) == size:
                    self.array = elements
                    break
                else:
                    print(f"Please enter exactly {size} elements")
            except ValueError:
                print("Please enter valid integers")
        
        # Get sorting algorithm
        print("\nSelect sorting algorithm:")
        print("1. Bubble Sort")
        print("2. Quick Sort")
        print("3. Merge Sort")
        print("4. Selection Sort")
        print("5. Insertion Sort")
        print("6. Heap Sort")
        print("7. Counting Sort")
        
        while True:
            try:
                choice = int(input("Enter your choice (1-7): "))
                if choice in [1, 2, 3, 4, 5, 6, 7]:
                    algorithms = {
                        1: "bubble", 2: "quick", 3: "merge", 
                        4: "selection", 5: "insertion", 6: "heap", 7: "counting"
                    }
                    return algorithms[choice]
                else:
                    print("Please enter a number between 1 and 7")
            except ValueError:
                print("Please enter a valid integer")
    
    def bubble_sort_steps(self, arr):
        """Generate bubble sort steps"""
        steps = []
        arr_copy = arr.copy()
        n = len(arr_copy)
        
        # Initial state
        steps.append({
            'array': arr_copy.copy(),
            'description': f'Initial Unsorted array',
            'comparing': [],
            'swapped': False,
            'pivot': -1,
            'pointers': [],
            'condition': ''
        })
        
        for i in range(n):
            swapped = False
            for j in range(0, n - i - 1):
                # Compare elements - show condition
                condition = f"Compare: {arr_copy[j]} {'>' if arr_copy[j] > arr_copy[j+1] else '<=' if arr_copy[j] < arr_copy[j+1] else '=='} {arr_copy[j+1]}"
                
                steps.append({
                    'array': arr_copy.copy(),
                    'description': f'Compare {self.get_ordinal(j+1)} and {self.get_ordinal(j+2)} elements',
                    'comparing': [j, j+1],
                    'swapped': False,
                    'pivot': -1,
                    'pointers': [],
                    'condition': condition
                })
                
                if arr_copy[j] > arr_copy[j + 1]:
                    # Show condition result before swap
                    steps.append({
                        'array': arr_copy.copy(),
                        'description': f'Since {arr_copy[j]} > {arr_copy[j+1]}, we need to swap',
                        'comparing': [j, j+1],
                        'swapped': False,
                        'pivot': -1,
                        'pointers': [],
                        'condition': f'Condition: {arr_copy[j]} > {arr_copy[j+1]} → SWAP needed'
                    })
                    
                    # Swap
                    arr_copy[j], arr_copy[j + 1] = arr_copy[j + 1], arr_copy[j]
                    swapped = True
                    steps.append({
                        'array': arr_copy.copy(),
                        'description': f'Swap: {arr_copy[j+1]} ↔ {arr_copy[j]}',
                        'comparing': [j, j+1],
                        'swapped': True,
                        'pivot': -1,
                        'pointers': [],
                        'condition': f'After swap: [{arr_copy[j]}, {arr_copy[j+1]}]'
                    })
                else:
                    steps.append({
                        'array': arr_copy.copy(),
                        'description': f'Since {arr_copy[j]} ≤ {arr_copy[j+1]}, no swap needed',
                        'comparing': [j, j+1],
                        'swapped': False,
                        'pivot': -1,
                        'pointers': [],
                        'condition': f'Condition: {arr_copy[j]} ≤ {arr_copy[j+1]} → No swap'
                    })
            
            if not swapped:
                steps.append({
                    'array': arr_copy.copy(),
                    'description': f'Pass {i+1} complete - No swaps made, array is sorted!',
                    'comparing': [],
                    'swapped': False,
                    'pivot': -1,
                    'pointers': [],
                    'condition': 'All elements are in correct order'
                })
                break
            else:
                steps.append({
                    'array': arr_copy.copy(),
                    'description': f'Pass {i+1} complete - Largest element moved to position {n-i}',
                    'comparing': [],
                    'swapped': False,
                    'pivot': -1,
                    'pointers': [],
                    'condition': f'Continue to next pass...'
                })
        
        # Final sorted array
        steps.append({
            'array': arr_copy.copy(),
            'description': 'Bubble Sort Complete - Array is now sorted!',
            'comparing': [],
            'swapped': False,
            'pivot': -1,
            'pointers': [],
            'condition': 'All elements: a₁ ≤ a₂ ≤ a₃ ≤ ... ≤ aₙ'
        })
        
        return steps

    def selection_sort_steps(self, arr):
        """Generate selection sort steps"""
        steps = []
        arr_copy = arr.copy()
        n = len(arr_copy)
        
        # Initial state
        steps.append({
            'array': arr_copy.copy(),
            'description': 'Initial Unsorted array',
            'comparing': [],
            'swapped': False,
            'pivot': -1,
            'pointers': [],
            'condition': ''
        })
        
        for i in range(n):
            min_idx = i
            
            steps.append({
                'array': arr_copy.copy(),
                'description': f'Find minimum element in unsorted portion [position {i+1} to {n}]',
                'comparing': [i],
                'swapped': False,
                'pivot': -1,
                'pointers': [i],
                'condition': f'Current minimum: {arr_copy[min_idx]} at position {min_idx+1}'
            })
            
            for j in range(i + 1, n):
                steps.append({
                    'array': arr_copy.copy(),
                    'description': f'Compare current minimum {arr_copy[min_idx]} with {arr_copy[j]}',
                    'comparing': [min_idx, j],
                    'swapped': False,
                    'pivot': -1,
                    'pointers': [i],
                    'condition': f'Condition: {arr_copy[j]} < {arr_copy[min_idx]} ?'
                })
                
                if arr_copy[j] < arr_copy[min_idx]:
                    min_idx = j
                    steps.append({
                        'array': arr_copy.copy(),
                        'description': f'New minimum found: {arr_copy[min_idx]} at position {min_idx+1}',
                        'comparing': [min_idx],
                        'swapped': False,
                        'pivot': -1,
                        'pointers': [i],
                        'condition': f'Update minimum: {arr_copy[min_idx]} < previous minimum'
                    })
                else:
                    steps.append({
                        'array': arr_copy.copy(),
                        'description': f'{arr_copy[j]} ≥ {arr_copy[min_idx]}, keep current minimum',
                        'comparing': [min_idx, j],
                        'swapped': False,
                        'pivot': -1,
                        'pointers': [i],
                        'condition': f'No change: {arr_copy[j]} ≥ {arr_copy[min_idx]}'
                    })
            
            if min_idx != i:
                steps.append({
                    'array': arr_copy.copy(),
                    'description': f'Swap minimum {arr_copy[min_idx]} with element at position {i+1}',
                    'comparing': [i, min_idx],
                    'swapped': False,
                    'pivot': -1,
                    'pointers': [],
                    'condition': f'Swap: {arr_copy[i]} ↔ {arr_copy[min_idx]}'
                })
                
                arr_copy[i], arr_copy[min_idx] = arr_copy[min_idx], arr_copy[i]
                
                steps.append({
                    'array': arr_copy.copy(),
                    'description': f'Minimum element placed at position {i+1}',
                    'comparing': [i, min_idx],
                    'swapped': True,
                    'pivot': -1,
                    'pointers': [],
                    'condition': f'After swap: position {i+1} = {arr_copy[i]}'
                })
            else:
                steps.append({
                    'array': arr_copy.copy(),
                    'description': f'Element at position {i+1} is already minimum, no swap needed',
                    'comparing': [i],
                    'swapped': False,
                    'pivot': -1,
                    'pointers': [],
                    'condition': f'No swap needed: {arr_copy[i]} already in correct position'
                })
        
        # Final sorted array
        steps.append({
            'array': arr_copy.copy(),
            'description': 'Selection Sort Complete - Array is now sorted!',
            'comparing': [],
            'swapped': False,
            'pivot': -1,
            'pointers': [],
            'condition': 'All elements: a₁ ≤ a₂ ≤ a₃ ≤ ... ≤ aₙ'
        })
        
        return steps

    def insertion_sort_steps(self, arr):
        """Generate insertion sort steps"""
        steps = []
        arr_copy = arr.copy()
        n = len(arr_copy)
        
        # Initial state
        steps.append({
            'array': arr_copy.copy(),
            'description': 'Initial array - first element is considered sorted',
            'comparing': [],
            'swapped': False,
            'pivot': -1,
            'pointers': [0],
            'condition': 'Sorted portion: [0], Unsorted portion: [1..n-1]'
        })
        
        for i in range(1, n):
            key = arr_copy[i]
            j = i - 1
            
            steps.append({
                'array': arr_copy.copy(),
                'description': f'Insert element {key} from position {i+1} into sorted portion',
                'comparing': [i],
                'swapped': False,
                'pivot': -1,
                'pointers': [i],
                'condition': f'Key = {key}, compare with sorted elements from right to left'
            })
            
            while j >= 0 and arr_copy[j] > key:
                steps.append({
                    'array': arr_copy.copy(),
                    'description': f'Compare {key} with {arr_copy[j]} at position {j+1}',
                    'comparing': [j, i],
                    'swapped': False,
                    'pivot': -1,
                    'pointers': [],
                    'condition': f'Condition: {arr_copy[j]} > {key} → Shift {arr_copy[j]} right'
                })
                
                arr_copy[j + 1] = arr_copy[j]
                
                steps.append({
                    'array': arr_copy.copy(),
                    'description': f'Shift {arr_copy[j+1]} to position {j+2}',
                    'comparing': [j, j+1],
                    'swapped': True,
                    'pivot': -1,
                    'pointers': [],
                    'condition': f'Shifted: {arr_copy[j+1]} moved right'
                })
                
                j -= 1
                i = j + 1  # Update i for visualization
            
            if j >= 0:
                steps.append({
                    'array': arr_copy.copy(),
                    'description': f'Compare {key} with {arr_copy[j]} - found correct position',
                    'comparing': [j, j+1],
                    'swapped': False,
                    'pivot': -1,
                    'pointers': [],
                    'condition': f'Condition: {arr_copy[j]} ≤ {key} → Stop shifting'
                })
            
            arr_copy[j + 1] = key
            
            steps.append({
                'array': arr_copy.copy(),
                'description': f'Insert {key} at position {j+2}',
                'comparing': [j+1],
                'swapped': True,
                'pivot': -1,
                'pointers': [],
                'condition': f'Key {key} inserted in correct position'
            })
        
        # Final sorted array
        steps.append({
            'array': arr_copy.copy(),
            'description': 'Insertion Sort Complete - Array is now sorted!',
            'comparing': [],
            'swapped': False,
            'pivot': -1,
            'pointers': [],
            'condition': 'All elements: a₁ ≤ a₂ ≤ a₃ ≤ ... ≤ aₙ'
        })
        
        return steps

    def heap_sort_steps(self, arr):
        """Generate heap sort steps"""
        steps = []
        arr_copy = arr.copy()
        n = len(arr_copy)
        
        # Initial state
        steps.append({
            'array': arr_copy.copy(),
            'description': 'Initial array - Build max heap first',
            'comparing': [],
            'swapped': False,
            'pivot': -1,
            'pointers': [],
            'condition': 'Convert array to max heap structure'
        })
        
        def heapify(arr, n, i, steps, phase="build"):
            largest = i
            left = 2 * i + 1
            right = 2 * i + 2
            
            # Find largest among root, left child and right child
            if left < n:
                steps.append({
                    'array': arr.copy(),
                    'description': f'Compare parent {arr[i]} with left child {arr[left]}',
                    'comparing': [i, left],
                    'swapped': False,
                    'pivot': -1,
                    'pointers': [],
                    'condition': f'Left child: {arr[left]} {">" if arr[left] > arr[largest] else "≤"} parent: {arr[largest]}'
                })
                
                if arr[left] > arr[largest]:
                    largest = left
            
            if right < n:
                steps.append({
                    'array': arr.copy(),
                    'description': f'Compare current largest {arr[largest]} with right child {arr[right]}',
                    'comparing': [largest, right],
                    'swapped': False,
                    'pivot': -1,
                    'pointers': [],
                    'condition': f'Right child: {arr[right]} {">" if arr[right] > arr[largest] else "≤"} current largest: {arr[largest]}'
                })
                
                if arr[right] > arr[largest]:
                    largest = right
            
            # Swap and continue heapifying if root is not largest
            if largest != i:
                steps.append({
                    'array': arr.copy(),
                    'description': f'Swap parent {arr[i]} with largest child {arr[largest]}',
                    'comparing': [i, largest],
                    'swapped': False,
                    'pivot': -1,
                    'pointers': [],
                    'condition': f'Maintain heap property: swap {arr[i]} ↔ {arr[largest]}'
                })
                
                arr[i], arr[largest] = arr[largest], arr[i]
                
                steps.append({
                    'array': arr.copy(),
                    'description': f'After swap - continue heapifying subtree',
                    'comparing': [i, largest],
                    'swapped': True,
                    'pivot': -1,
                    'pointers': [],
                    'condition': f'Swapped: parent = {arr[i]}, child = {arr[largest]}'
                })
                
                heapify(arr, n, largest, steps, phase)
        
        # Build heap (rearrange array)
        for i in range(n // 2 - 1, -1, -1):
            steps.append({
                'array': arr_copy.copy(),
                'description': f'Heapify subtree rooted at index {i}',
                'comparing': [i],
                'swapped': False,
                'pivot': -1,
                'pointers': [i],
                'condition': f'Process node {arr_copy[i]} at position {i+1}'
            })
            heapify(arr_copy, n, i, steps, "build")
        
        steps.append({
            'array': arr_copy.copy(),
            'description': 'Max heap built successfully!',
            'comparing': [],
            'swapped': False,
            'pivot': -1,
            'pointers': [],
            'condition': 'Heap property: parent ≥ children for all nodes'
        })
        
        # Extract elements from heap one by one
        for i in range(n - 1, 0, -1):
            steps.append({
                'array': arr_copy.copy(),
                'description': f'Extract maximum {arr_copy[0]} from heap',
                'comparing': [0, i],
                'swapped': False,
                'pivot': -1,
                'pointers': [],
                'condition': f'Move max element {arr_copy[0]} to sorted position {i+1}'
            })
            
            # Move current root to end
            arr_copy[0], arr_copy[i] = arr_copy[i], arr_copy[0]
            
            steps.append({
                'array': arr_copy.copy(),
                'description': f'Swapped max element to position {i+1}',
                'comparing': [0, i],
                'swapped': True,
                'pivot': -1,
                'pointers': [],
                'condition': f'Sorted portion: [{i+1}..{n}], Heap portion: [1..{i}]'
            })
            
            # Call heapify on the reduced heap
            if i > 1:
                steps.append({
                    'array': arr_copy.copy(),
                    'description': f'Restore heap property for reduced heap of size {i}',
                    'comparing': [0],
                    'swapped': False,
                    'pivot': -1,
                    'pointers': [0],
                    'condition': f'Heapify root with {i} elements remaining'
                })
                heapify(arr_copy, i, 0, steps, "extract")
        
        # Final sorted array
        steps.append({
            'array': arr_copy.copy(),
            'description': 'Heap Sort Complete - Array is now sorted!',
            'comparing': [],
            'swapped': False,
            'pivot': -1,
            'pointers': [],
            'condition': 'All elements: a₁ ≤ a₂ ≤ a₃ ≤ ... ≤ aₙ'
        })
        
        return steps

    def counting_sort_steps(self, arr):
        """Generate counting sort steps"""
        steps = []
        arr_copy = arr.copy()
        n = len(arr_copy)
        
        # Find the maximum element
        max_val = max(arr_copy)
        min_val = min(arr_copy)
        range_val = max_val - min_val + 1
        
        # Initial state
        steps.append({
            'array': arr_copy.copy(),
            'description': 'Initial array for Counting Sort',
            'comparing': [],
            'swapped': False,
            'pivot': -1,
            'pointers': [],
            'condition': f'Range: {min_val} to {max_val}, Size: {range_val}'
        })
        
        # Create count array
        count = [0] * range_val
        
        steps.append({
            'array': arr_copy.copy(),
            'description': f'Initialize count array of size {range_val}',
            'comparing': [],
            'swapped': False,
            'pivot': -1,
            'pointers': [],
            'condition': f'Count array: {count} (index 0 represents value {min_val})'
        })
        
        # Count occurrences
        for i in range(n):
            count[arr_copy[i] - min_val] += 1
            steps.append({
                'array': arr_copy.copy(),
                'description': f'Count element {arr_copy[i]} at position {i+1}',
                'comparing': [i],
                'swapped': False,
                'pivot': -1,
                'pointers': [],
                'condition': f'Count[{arr_copy[i]}] = {count[arr_copy[i] - min_val]}, Count array: {count}'
            })
        
        # Modify count array to store cumulative count
        for i in range(1, range_val):
            count[i] += count[i - 1]
            steps.append({
                'array': arr_copy.copy(),
                'description': f'Calculate cumulative count for index {i}',
                'comparing': [],
                'swapped': False,
                'pivot': -1,
                'pointers': [],
                'condition': f'Cumulative count[{i}] = {count[i]}, Array: {count}'
            })
        
        steps.append({
            'array': arr_copy.copy(),
            'description': 'Cumulative count array shows final positions',
            'comparing': [],
            'swapped': False,
            'pivot': -1,
            'pointers': [],
            'condition': f'Final count array: {count}'
        })
        
        # Build output array
        output = [0] * n
        
        # Build the output array from right to left
        for i in range(n - 1, -1, -1):
            val = arr_copy[i]
            pos = count[val - min_val] - 1
            output[pos] = val
            count[val - min_val] -= 1
            
            steps.append({
                'array': output.copy(),
                'description': f'Place {val} at position {pos + 1} in output array',
                'comparing': [pos],
                'swapped': True,
                'pivot': -1,
                'pointers': [],
                'condition': f'Element {val} goes to position {pos + 1}, update count[{val}] = {count[val - min_val]}'
            })
        
        # Copy output array back to original
        for i in range(n):
            arr_copy[i] = output[i]
        
        # Final sorted array
        steps.append({
            'array': arr_copy.copy(),
            'description': 'Counting Sort Complete - Array is now sorted!',
            'comparing': [],
            'swapped': False,
            'pivot': -1,
            'pointers': [],
            'condition': 'All elements: a₁ ≤ a₂ ≤ a₃ ≤ ... ≤ aₙ'
        })
        
        return steps
    
    def quick_sort_steps(self, arr):
        """Generate quick sort steps"""
        steps = []
        arr_copy = arr.copy()
        
        # Initial state
        steps.append({
            'array': arr_copy.copy(),
            'description': 'Initial Unsorted array',
            'comparing': [],
            'swapped': False,
            'pivot': -1,
            'pointers': [],
            'condition': ''
        })
        
        def partition(arr, low, high, steps):
            pivot_idx = high
            pivot = arr[pivot_idx]
            
            steps.append({
                'array': arr.copy(),
                'description': f'Choose pivot: element at position {pivot_idx + 1}',
                'comparing': [],
                'swapped': False,
                'pivot': pivot_idx,
                'pointers': [],
                'condition': f'Pivot = {pivot} (last element)'
            })
            
            left = low
            right = high - 1
            
            steps.append({
                'array': arr.copy(),
                'description': 'Initialize left and right pointers',
                'comparing': [],
                'swapped': False,
                'pivot': pivot_idx,
                'pointers': [left, right],
                'condition': f'Left pointer at position {left+1}, Right pointer at position {right+1}'
            })
            
            while left <= right:
                # Move left pointer
                while left <= right and arr[left] < pivot:
                    steps.append({
                        'array': arr.copy(),
                        'description': f'Check left element: {arr[left]} < {pivot}?',
                        'comparing': [left],
                        'swapped': False,
                        'pivot': pivot_idx,
                        'pointers': [left, right],
                        'condition': f'Condition: {arr[left]} < {pivot} → TRUE, move left pointer'
                    })
                    left += 1
                    
                    if left <= right:
                        steps.append({
                            'array': arr.copy(),
                            'description': f'Move left pointer to position {left+1}',
                            'comparing': [],
                            'swapped': False,
                            'pivot': pivot_idx,
                            'pointers': [left, right],
                            'condition': f'Left pointer now at element {arr[left] if left < len(arr) else "end"}'
                        })
                
                if left <= right:
                    steps.append({
                        'array': arr.copy(),
                        'description': f'Left element check: {arr[left]} < {pivot}?',
                        'comparing': [left],
                        'swapped': False,
                        'pivot': pivot_idx,
                        'pointers': [left, right],
                        'condition': f'Condition: {arr[left]} < {pivot} → FALSE, stop left pointer'
                    })
                
                # Move right pointer
                while left <= right and arr[right] > pivot:
                    steps.append({
                        'array': arr.copy(),
                        'description': f'Check right element: {arr[right]} > {pivot}?',
                        'comparing': [right],
                        'swapped': False,
                        'pivot': pivot_idx,
                        'pointers': [left, right],
                        'condition': f'Condition: {arr[right]} > {pivot} → TRUE, move right pointer'
                    })
                    right -= 1
                    
                    if left <= right:
                        steps.append({
                            'array': arr.copy(),
                            'description': f'Move right pointer to position {right+1}',
                            'comparing': [],
                            'swapped': False,
                            'pivot': pivot_idx,
                            'pointers': [left, right],
                            'condition': f'Right pointer now at element {arr[right] if right >= 0 else "start"}'
                        })
                
                if left <= right:
                    steps.append({
                        'array': arr.copy(),
                        'description': f'Right element check: {arr[right]} > {pivot}?',
                        'comparing': [right],
                        'swapped': False,
                        'pivot': pivot_idx,
                        'pointers': [left, right],
                        'condition': f'Condition: {arr[right]} > {pivot} → FALSE, stop right pointer'
                    })
                
                # Check if swap needed
                if left <= right:
                    if left < right:
                        steps.append({
                            'array': arr.copy(),
                            'description': f'Pointers haven\'t crossed - swap needed',
                            'comparing': [left, right],
                            'swapped': False,
                            'pivot': pivot_idx,
                            'pointers': [left, right],
                            'condition': f'Left({arr[left]}) and Right({arr[right]}) need swapping'
                        })
                        
                        arr[left], arr[right] = arr[right], arr[left]
                        steps.append({
                            'array': arr.copy(),
                            'description': f'Swap: {arr[right]} ↔ {arr[left]}',
                            'comparing': [left, right],
                            'swapped': True,
                            'pivot': pivot_idx,
                            'pointers': [left, right],
                            'condition': f'After swap: position {left+1}={arr[left]}, position {right+1}={arr[right]}'
                        })
                    
                    left += 1
                    right -= 1
                    
                    if left <= high - 1:
                        steps.append({
                            'array': arr.copy(),
                            'description': 'Move both pointers inward',
                            'comparing': [],
                            'swapped': False,
                            'pivot': pivot_idx,
                            'pointers': [left, right] if right >= low else [left],
                            'condition': f'Continue partitioning with new pointer positions'
                        })
            
            # Place pivot in correct position
            if left != pivot_idx:
                steps.append({
                    'array': arr.copy(),
                    'description': f'Pointers crossed - place pivot in correct position',
                    'comparing': [left, pivot_idx],
                    'swapped': False,
                    'pivot': pivot_idx,
                    'pointers': [],
                    'condition': f'Swap pivot {arr[pivot_idx]} with element at position {left+1} ({arr[left]})'
                })
                
                arr[left], arr[pivot_idx] = arr[pivot_idx], arr[left]
                steps.append({
                    'array': arr.copy(),
                    'description': f'Pivot placed correctly at position {left+1}',
                    'comparing': [left, pivot_idx],
                    'swapped': True,
                    'pivot': left,
                    'pointers': [],
                    'condition': f'Pivot {arr[left]} is now in its final sorted position'
                })
            else:
                steps.append({
                    'array': arr.copy(),
                    'description': f'Pivot already in correct position',
                    'comparing': [],
                    'swapped': False,
                    'pivot': left,
                    'pointers': [],
                    'condition': f'Pivot {arr[left]} was already in its correct position'
                })
            
            return left
        
        def quicksort_recursive(arr, low, high, steps):
            if low < high:
                pi = partition(arr, low, high, steps)
                if pi > low + 1:
                    steps.append({
                        'array': arr.copy(),
                        'description': f'Recursively sort left subarray [positions {low+1} to {pi}]',
                        'comparing': [],
                        'swapped': False,
                        'pivot': -1,
                        'pointers': [],
                        'condition': f'Left subarray: {arr[low:pi]}'
                    })
                quicksort_recursive(arr, low, pi - 1, steps)
                
                if pi < high - 1:
                    steps.append({
                        'array': arr.copy(),
                        'description': f'Recursively sort right subarray [positions {pi+2} to {high+1}]',
                        'comparing': [],
                        'swapped': False,
                        'pivot': -1,
                        'pointers': [],
                        'condition': f'Right subarray: {arr[pi+1:high+1]}'
                    })
                quicksort_recursive(arr, pi + 1, high, steps)
        
        quicksort_recursive(arr_copy, 0, len(arr_copy) - 1, steps)
        
        # Final sorted array
        steps.append({
            'array': arr_copy.copy(),
            'description': 'Quick Sort Complete - Array is now sorted!',
            'comparing': [],
            'swapped': False,
            'pivot': -1,
            'pointers': [],
            'condition': 'All subarrays merged: a₁ ≤ a₂ ≤ a₃ ≤ ... ≤ aₙ'
        })
        
        return steps
    
    def merge_sort_steps(self, arr):
        """Generate merge sort steps"""
        steps = []
        arr_copy = arr.copy()
        
        # Initial state
        steps.append({
            'array': arr_copy.copy(),
            'description': 'Initial Unsorted array',
            'comparing': [],
            'swapped': False,
            'pivot': -1,
            'pointers': [],
            'merge_ranges': [],
            'condition': ''
        })
        
        def merge_sort_recursive(arr, left, right, steps, temp_arr):
            if left < right:
                mid = (left + right) // 2
                
                # Divide
                steps.append({
                    'array': temp_arr.copy(),
                    'description': f'Divide: Split array into two halves',
                    'comparing': [],
                    'swapped': False,
                    'pivot': -1,
                    'pointers': [],
                    'merge_ranges': [(left, mid), (mid + 1, right)],
                    'condition': f'Left: {arr[left:mid+1]}, Right: {arr[mid+1:right+1]}'
                })
                
                merge_sort_recursive(arr, left, mid, steps, temp_arr)
                merge_sort_recursive(arr, mid + 1, right, steps, temp_arr)
                
                # Merge
                merge(arr, left, mid, right, steps, temp_arr)
        
        def merge(arr, left, mid, right, steps, temp_arr):
            left_arr = arr[left:mid + 1]
            right_arr = arr[mid + 1:right + 1]
            
            steps.append({
                'array': temp_arr.copy(),
                'description': f'Merge subarrays: {left_arr} and {right_arr}',
                'comparing': [],
                'swapped': False,
                'pivot': -1,
                'pointers': [],
                'merge_ranges': [(left, mid), (mid + 1, right)],
                'condition': f'Comparing elements from both subarrays'
            })
            
            i = j = 0
            k = left
            
            while i < len(left_arr) and j < len(right_arr):
                left_val = left_arr[i]
                right_val = right_arr[j]
                
                # Show comparison
                steps.append({
                    'array': temp_arr.copy(),
                    'description': f'Compare: {left_val} vs {right_val}',
                    'comparing': [k],
                    'swapped': False,
                    'pivot': -1,
                    'pointers': [],
                    'merge_ranges': [],
                    'condition': f'Condition: {left_val} {"≤" if left_val <= right_val else ">"} {right_val}'
                })
                
                if left_val <= right_val:
                    temp_arr[k] = left_val
                    i += 1
                    steps.append({
                        'array': temp_arr.copy(),
                        'description': f'Since {left_val} ≤ {right_val}, place {left_val} at position {k + 1}',
                        'comparing': [k],
                        'swapped': False,
                        'pivot': -1,
                        'pointers': [],
                        'merge_ranges': [],
                        'condition': f'Take from left subarray: {left_val} → position {k+1}'
                    })
                else:
                    temp_arr[k] = right_val
                    j += 1
                    steps.append({
                        'array': temp_arr.copy(),
                        'description': f'Since {right_val} < {left_val}, place {right_val} at position {k + 1}',
                        'comparing': [k],
                        'swapped': False,
                        'pivot': -1,
                        'pointers': [],
                        'merge_ranges': [],
                        'condition': f'Take from right subarray: {right_val} → position {k+1}'
                    })
                
                k += 1
            
            # Copy remaining elements from left subarray
            while i < len(left_arr):
                temp_arr[k] = left_arr[i]
                steps.append({
                    'array': temp_arr.copy(),
                    'description': f'Copy remaining element from left: {left_arr[i]}',
                    'comparing': [k],
                    'swapped': False,
                    'pivot': -1,
                    'pointers': [],
                    'merge_ranges': [],
                    'condition': f'Left subarray not empty: {left_arr[i]} → position {k+1}'
                })
                i += 1
                k += 1
                
            # Copy remaining elements from right subarray
            while j < len(right_arr):
                temp_arr[k] = right_arr[j]
                steps.append({
                    'array': temp_arr.copy(),
                    'description': f'Copy remaining element from right: {right_arr[j]}',
                    'comparing': [k],
                    'swapped': False,
                    'pivot': -1,
                    'pointers': [],
                    'merge_ranges': [],
                    'condition': f'Right subarray not empty: {right_arr[j]} → position {k+1}'
                })
                j += 1
                k += 1
            
            # Copy merged result back to original array
            for idx in range(left, right + 1):
                arr[idx] = temp_arr[idx]
            
            # Show merge completion
            steps.append({
                'array': temp_arr.copy(),
                'description': f'Merge complete for range [{left+1}..{right+1}]',
                'comparing': [],
                'swapped': False,
                'pivot': -1,
                'pointers': [],
                'merge_ranges': [],
                'condition': f'Merged result: {temp_arr[left:right+1]}'
            })
        
        temp_array = arr_copy.copy()
        merge_sort_recursive(arr_copy, 0, len(arr_copy) - 1, steps, temp_array)
        
        # Final sorted array
        steps.append({
            'array': arr_copy.copy(),
            'description': 'Merge Sort Complete - Array is now sorted!',
            'comparing': [],
            'swapped': False,
            'pivot': -1,
            'pointers': [],
            'merge_ranges': [],
            'condition': 'Final result: All subarrays merged in sorted order'
        })
        
        return steps
    
    def create_summary_view(self):
        """Create summary view showing all steps in table format"""
        if self.summary_frame:
            self.summary_frame.destroy()
        
        # Hide main controls
        for widget in self.root.winfo_children():
            if widget != self.summary_frame:
                widget.pack_forget()
        
        # Create summary frame
        self.summary_frame = tk.Frame(self.root, bg='white')
        self.summary_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        summary_title = tk.Label(self.summary_frame, text="All Steps Summary", 
                                font=('Arial', 18, 'bold'), bg='white')
        summary_title.pack(pady=(0, 20))
        
        # Create scrollable frame
        canvas = tk.Canvas(self.summary_frame, bg='white')
        scrollbar = ttk.Scrollbar(self.summary_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='white')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Display each step
        for step_num, step_data in enumerate(self.steps):
            step_frame = tk.Frame(scrollable_frame, bg='white', relief='solid', borderwidth=1)
            step_frame.pack(fill='x', pady=5, padx=10)
            
            # Step header
            header_text = f"Step {step_num}" if step_num > 0 else "Initial"
            step_header = tk.Label(step_frame, text=header_text, 
                                  font=('Arial', 12, 'bold'), bg='lightgray')
            step_header.pack(fill='x', pady=2)
            
            # Step description
            desc_label = tk.Label(step_frame, text=step_data['description'], 
                                 font=('Arial', 10), bg='white', wraplength=800)
            desc_label.pack(pady=2)
            
            # Array visualization
            array_frame = tk.Frame(step_frame, bg='white')
            array_frame.pack(pady=5)
            
            array = step_data['array']
            comparing = step_data.get('comparing', [])
            pivot = step_data.get('pivot', -1)
            pointers = step_data.get('pointers', [])
            swapped = step_data.get('swapped', False)
            
            for i, value in enumerate(array):
                # Determine cell color
                color = 'white'
                if i == pivot:
                    color = 'yellow'
                elif i in comparing:
                    color = 'lightblue' if not swapped else 'lightcoral'
                elif i in pointers:
                    color = 'lightgreen'
                
                cell = tk.Label(array_frame, text=str(value), width=6, height=2,
                               bg=color, relief='solid', borderwidth=1,
                               font=('Arial', 12, 'bold'))
                cell.pack(side='left', padx=1)
            
            # Condition
            condition = step_data.get('condition', '')
            if condition:
                condition_label = tk.Label(step_frame, text=f"Logic: {condition}", 
                                          font=('Arial', 9, 'italic'), bg='lightgray',
                                          wraplength=800)
                condition_label.pack(pady=2, fill='x')
        
        # Back button
        back_btn = tk.Button(self.summary_frame, text="← Back to Animation", 
                            font=('Arial', 12), command=self.show_main_view,
                            bg='lightblue')
        back_btn.pack(pady=20)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def show_main_view(self):
        """Show main animation view"""
        if self.summary_frame:
            self.summary_frame.destroy()
            self.summary_frame = None
        
        self.show_summary = False
        
        # Recreate main interface
        self.create_main_interface()
        self.update_display()
    
    def create_main_interface(self):
        """Create the main interface elements"""
        # Title
        title_label = tk.Label(self.root, text=f"{self.current_algorithm.title()} Sort Visualization", 
                              font=('Arial', 20, 'bold'), bg='white')
        title_label.pack(pady=20)
        
        # Canvas for array visualization
        canvas_frame = tk.Frame(self.root, bg='white')
        canvas_frame.pack(pady=20)
        
        canvas_width = len(self.array) * self.cell_width + 100
        canvas_height = 150
        self.canvas = tk.Canvas(canvas_frame, width=canvas_width, height=canvas_height, 
                               bg='white', highlightthickness=1, highlightbackground='black')
        self.canvas.pack()
        
        # Step description
        self.step_label = tk.Label(self.root, text="", font=('Arial', 14), 
                                  bg='white', wraplength=800, justify='center')
        self.step_label.pack(pady=(10, 5))
        
        # Condition display
        self.condition_label = tk.Label(self.root, text="", font=('Arial', 12, 'italic'), 
                                       bg='lightgray', wraplength=800, justify='center',
                                       relief='solid', borderwidth=1, pady=5)
        self.condition_label.pack(pady=(5, 20), padx=20, fill='x')
        
        # Control buttons
        button_frame = tk.Frame(self.root, bg='white')
        button_frame.pack(pady=20)
        
        prev_btn = tk.Button(button_frame, text="← Previous", font=('Arial', 12),
                            command=self.prev_step, bg='lightblue')
        prev_btn.pack(side=tk.LEFT, padx=10)
        
        next_btn = tk.Button(button_frame, text="Next →", font=('Arial', 12),
                            command=self.next_step, bg='lightgreen')
        next_btn.pack(side=tk.LEFT, padx=10)
        
        auto_btn = tk.Button(button_frame, text="Auto Play", font=('Arial', 12),
                            command=self.auto_play, bg='yellow')
        auto_btn.pack(side=tk.LEFT, padx=10)
        
        reset_btn = tk.Button(button_frame, text="Reset", font=('Arial', 12),
                             command=self.reset_visualization, bg='lightcoral')
        reset_btn.pack(side=tk.LEFT, padx=10)
        
        summary_btn = tk.Button(button_frame, text="View All Steps", font=('Arial', 12),
                               command=self.create_summary_view, bg='lightpink')
        summary_btn.pack(side=tk.LEFT, padx=10)
        
        # Step counter
        self.step_counter = tk.Label(self.root, text="", font=('Arial', 12), bg='white')
        self.step_counter.pack(pady=10)
    
    def create_gui(self, algorithm):
        """Create the visualization GUI"""
        self.current_algorithm = algorithm
        self.root = tk.Tk()
        self.root.title(f"{algorithm.title()} Sort Visualization")
        self.root.geometry("1200x700")
        self.root.configure(bg='white')
        
        # Generate steps based on algorithm
        if algorithm == "bubble":
            self.steps = self.bubble_sort_steps(self.array)
        elif algorithm == "quick":
            self.steps = self.quick_sort_steps(self.array)
        elif algorithm == "merge":
            self.steps = self.merge_sort_steps(self.array)
        elif algorithm == "selection":
            self.steps = self.selection_sort_steps(self.array)
        elif algorithm == "insertion":
            self.steps = self.insertion_sort_steps(self.array)
        elif algorithm == "heap":
            self.steps = self.heap_sort_steps(self.array)
        elif algorithm == "counting":
            self.steps = self.counting_sort_steps(self.array)
        
        self.create_main_interface()
        self.update_display()
        
    def draw_array(self, step_data):
        """Draw the array with highlighting"""
        self.canvas.delete("all")
        
        array = step_data['array']
        comparing = step_data.get('comparing', [])
        pivot = step_data.get('pivot', -1)
        pointers = step_data.get('pointers', [])
        swapped = step_data.get('swapped', False)
        
        start_x = 50
        start_y = 50
        
        for i, value in enumerate(array):
            x1 = start_x + i * self.cell_width
            y1 = start_y
            x2 = x1 + self.cell_width - 10
            y2 = y1 + self.cell_height
            
            # Determine cell color
            color = 'white'
            if i == pivot:
                color = 'yellow'
            elif i in comparing:
                color = 'lightblue' if not swapped else 'lightcoral'
            elif i in pointers:
                color = 'lightgreen'
            
            # Draw cell
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='black', width=2)
            
            # Draw value
            text_x = x1 + (self.cell_width - 10) // 2
            text_y = y1 + self.cell_height // 2
            self.canvas.create_text(text_x, text_y, text=str(value), 
                                  font=('Arial', 16, 'bold'))
        
        # Draw pointer labels for quicksort
        if pointers:
            for i, pos in enumerate(pointers):
                if pos < len(array):
                    x = start_x + pos * self.cell_width + (self.cell_width - 10) // 2
                    y = start_y + self.cell_height + 20
                    label = 'L' if i == 0 else 'R'
                    self.canvas.create_text(x, y, text=label, font=('Arial', 12, 'bold'))
                    # Draw arrow
                    self.canvas.create_polygon(x-5, y-15, x+5, y-15, x, y-5, fill='black')
    
    def update_display(self):
        """Update the display with current step"""
        if 0 <= self.current_step < len(self.steps):
            step_data = self.steps[self.current_step]
            
            # Update array visualization
            self.draw_array(step_data)
            
            # Update step description
            step_num = f"Step {self.current_step}" if self.current_step > 0 else "Initial"
            description = step_data['description']
            self.step_label.config(text=f"{step_num}: {description}")
            
            # Update condition display
            condition = step_data.get('condition', '')
            if condition:
                self.condition_label.config(text=f"Logic: {condition}")
            else:
                self.condition_label.config(text="")
            
            # Update step counter
            self.step_counter.config(text=f"Step {self.current_step + 1} of {len(self.steps)}")
    
    def next_step(self):
        """Go to next step"""
        if self.current_step < len(self.steps) - 1:
            self.current_step += 1
            self.update_display()
    
    def prev_step(self):
        """Go to previous step"""
        if self.current_step > 0:
            self.current_step -= 1
            self.update_display()
    
    def auto_play(self):
        """Auto play through all steps"""
        def play():
            while self.current_step < len(self.steps) - 1:
                time.sleep(self.delay / 1000)
                self.root.after(0, self.next_step)
        
        thread = threading.Thread(target=play)
        thread.daemon = True
        thread.start()
    
    def reset_visualization(self):
        """Reset to first step"""
        self.current_step = 0
        self.update_display()
    
    def run(self):
        """Main run method"""
        algorithm = self.get_user_input()
        
        print(f"\nStarting {algorithm.title()} Sort visualization...")
        print("Opening visualization window...")
        
        self.create_gui(algorithm)
        self.root.mainloop()

# Main execution
if __name__ == "__main__":
    visualizer = SortingVisualizer()
    visualizer.run()
