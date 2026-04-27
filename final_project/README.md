# PC Build Configurator v1.0 [ALPHA]

A final project for LOGIC ADD-100-001L

## ⚙ Features
* **Component Selection:** Choose from 10+ options across 7 categories (CPU, GPU, RAM, etc.).
* **Compatibility Engine:** * Checks for **Socket Mismatch** between CPU and Motherboard.
    * Checks for **RAM Mismatch** (DDR4 vs DDR5) compatibility with the CPU/Mobo.
    * Calculates **Power Requirements** to ensure the PSU can handle the system TDP.
* **Financial Tracking:** Automatically calculates the total estimated cost of your entire build.
* **Persistent Storage:** Save your completed builds to a `.txt` file.

## 📂 Project Structure
* `main.py`: The entry point containing the user interface and menu logic.
* `models.py`: Defines `Component` and `Build` classes, including compatibility logic.
* `data_manager.py`: Handles loading the parts catalog and saving builds to files.
* `parts_menu.txt`: A CSV-style database of available PC components.

## 💡 Possible Future Improvements
* ⭐ **Expanded Component Support(more categories):** Integrated logic for CPU Coolers and Miscellaneous peripherals.
* **Better Compatibility:** 
Add checks for Case size(making sure the GPU actually fits inside)
mobo form factor(ATX, mATX to the size of the case cases, and functionality towards miscellaneous components) 
and CPU Cooler clearance. 
* **Better Data Loading:** Change how parts are retrieved so the program runs even faster and easy to use as the list grows.
    ## Possible Solution:
    **JSON Migration:** Transition from .txt to .json for the parts menu to allow for nested data like "Dimensions" or "Color."
* ⭐ **Smart Suggestions:** If a part is incompatible, have the program suggest a fixed alternative automatically.

## ⭐ *priority* 

## 🛠️ Installation & Usage
1. Ensure you have all 3 pythons and parts menu installed.
2. Place all files in the same directory.
3. Open your terminal and navigate to the folder. 
4. Run the program:
   python main.py



cd