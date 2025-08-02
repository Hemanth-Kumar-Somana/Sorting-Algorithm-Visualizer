# Sorting Algorithm Visualizer

A comprehensive Python application that provides interactive visualizations for popular sorting algorithms. This tool helps students and developers understand how different sorting algorithms work through step-by-step visual demonstrations.

## Features

### Supported Algorithms
- **Bubble Sort** - Compare adjacent elements and swap if needed
- **Quick Sort** - Divide-and-conquer with pivot partitioning
- **Merge Sort** - Divide-and-conquer with merging
- **Selection Sort** - Find minimum and place in correct position
- **Insertion Sort** - Insert elements into sorted portion
- **Heap Sort** - Build max heap and extract elements
- **Counting Sort** - Count occurrences for non-comparison sorting

### Visualization Features
- **Step-by-step Animation** - Navigate through each step manually
- **Auto Play Mode** - Automatic progression through all steps
- **Color-coded Elements** - Visual indicators for different operations:
  - 🟡 **Yellow**: Pivot element (Quick Sort)
  - 🔵 **Light Blue**: Elements being compared
  - 🔴 **Light Coral**: Elements being swapped
  - 🟢 **Light Green**: Pointer positions
- **Detailed Logic Display** - Shows conditions and decisions at each step
- **Complete Step Summary** - View all steps in a scrollable table format

### Interactive Controls
- **Previous/Next Buttons** - Manual step navigation
- **Auto Play** - Automated visualization
- **Reset** - Return to initial state
- **View All Steps** - Complete summary view

## Requirements

- Python 3.6 or higher
- tkinter (usually included with Python)
- No additional external dependencies required

## Installation

1. **Clone or download** the repository:
   ```bash
   git clone <repository-url>
   cd sorting-visualizer
   ```

2. **Ensure Python is installed**:
   ```bash
   python --version
   ```

3. **Run the application**:
   ```bash
   python sorting_visualizer.py
   ```

## Usage

### Getting Started

1. **Run the program**:
   ```bash
   python sorting_visualizer.py
   ```

2. **Enter array details**:
   - Array size (3-10 elements)
   - Array elements (space-separated integers)

3. **Choose sorting algorithm**:
   ```
   Select sorting algorithm:
   1. Bubble Sort
   2. Quick Sort
   3. Merge Sort
   4. Selection Sort
   5. Insertion Sort
   6. Heap Sort
   7. Counting Sort
   ```

4. **Interact with the visualization**:
   - Use **Next →** and **← Previous** to navigate steps
   - Click **Auto Play** for automatic progression
   - Click **View All Steps** for complete summary
   - Use **Reset** to return to the beginning

### Example Input
```
Enter array size (3-10): 5
Enter 5 elements separated by spaces: 64 34 25 12 22
Enter your choice (1-7): 1
```

## Algorithm Details

### Bubble Sort
- **Time Complexity**: O(n²)
- **Space Complexity**: O(1)
- **Method**: Compare adjacent elements and swap if out of order
- **Visualization**: Shows comparisons and swaps clearly

### Quick Sort
- **Time Complexity**: O(n log n) average, O(n²) worst case
- **Space Complexity**: O(log n)
- **Method**: Partition around pivot, recursively sort subarrays
- **Visualization**: Shows pivot selection, partitioning, and recursive calls

### Merge Sort
- **Time Complexity**: O(n log n)
- **Space Complexity**: O(n)
- **Method**: Divide array, sort halves, merge sorted halves
- **Visualization**: Shows division and merging process

### Selection Sort
- **Time Complexity**: O(n²)
- **Space Complexity**: O(1)
- **Method**: Find minimum element and place in correct position
- **Visualization**: Shows minimum finding and swapping

### Insertion Sort
- **Time Complexity**: O(n²)
- **Space Complexity**: O(1)
- **Method**: Insert each element into correct position in sorted portion
- **Visualization**: Shows insertion and shifting process

### Heap Sort
- **Time Complexity**: O(n log n)
- **Space Complexity**: O(1)
- **Method**: Build max heap, extract maximum elements
- **Visualization**: Shows heap building and extraction

### Counting Sort
- **Time Complexity**: O(n + k) where k is range of elements
- **Space Complexity**: O(k)
- **Method**: Count occurrences, calculate positions
- **Visualization**: Shows counting and placement process

## Code Structure

```
sorting_visualizer.py
├── SortingVisualizer Class
│   ├── User Input Methods
│   │   └── get_user_input()
│   ├── Algorithm Implementation
│   │   ├── bubble_sort_steps()
│   │   ├── quick_sort_steps()
│   │   ├── merge_sort_steps()
│   │   ├── selection_sort_steps()
│   │   ├── insertion_sort_steps()
│   │   ├── heap_sort_steps()
│   │   └── counting_sort_steps()
│   ├── GUI Components
│   │   ├── create_gui()
│   │   ├── create_main_interface()
│   │   ├── draw_array()
│   │   └── update_display()
│   ├── Navigation Controls
│   │   ├── next_step()
│   │   ├── prev_step()
│   │   ├── auto_play()
│   │   └── reset_visualization()
│   └── Summary View
│       ├── create_summary_view()
│       └── show_main_view()
```

## Educational Benefits

### For Students
- **Visual Learning**: See exactly how algorithms work step-by-step
- **Logic Understanding**: Detailed condition explanations at each step
- **Comparison**: Easy to compare different algorithm approaches
- **Interactive**: Control pace of learning

### For Educators
- **Teaching Tool**: Perfect for classroom demonstrations
- **Comprehensive**: Covers most fundamental sorting algorithms
- **Detailed Steps**: Each step explained with conditions and logic
- **Summary View**: Quick overview of entire process

## Customization

### Modifying Visualization Speed
Change the delay in milliseconds:
```python
self.delay = 1500  # Default: 1.5 seconds between steps
```

### Adding New Algorithms
1. Create a new method following the pattern: `algorithm_name_steps(self, arr)`
2. Add to the algorithm selection in `get_user_input()`
3. Add case in `create_gui()` method

### Customizing Colors
Modify colors in the `draw_array()` method:
```python
# Current color scheme
color = 'white'      # Default
if i == pivot:
    color = 'yellow'     # Pivot
elif i in comparing:
    color = 'lightblue'  # Comparing
elif i in pointers:
    color = 'lightgreen' # Pointers
```

## Troubleshooting

### Common Issues

1. **"tkinter not found" error**:
   - On Ubuntu/Debian: `sudo apt-get install python3-tk`
   - On macOS: Reinstall Python from python.org
   - On Windows: Reinstall Python with tkinter option checked

2. **Window too small**:
   - Adjust window size in `create_gui()` method
   - Modify `self.root.geometry("1200x700")`

3. **Array too large**:
   - Current limit is 10 elements for optimal visualization
   - Increase limit by modifying validation in `get_user_input()`

## Contributing

Contributions are welcome! Areas for improvement:
- Additional sorting algorithms (Radix Sort, Shell Sort, etc.)
- Better visualization animations
- Performance metrics display
- Export functionality for educational materials
- Mobile-responsive design

## License

This project is open source and available under the MIT License.

## Acknowledgments

- Designed for educational purposes
- Inspired by the need for visual algorithm learning tools
- Built with Python's tkinter for cross-platform compatibility

---

**Happy Learning! 🚀**

*This tool is designed to make sorting algorithms accessible and understandable for everyone, from beginners to advanced programmers.*
