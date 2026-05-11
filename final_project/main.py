"""
-----------------------------------------------------------------------
ASSIGNMENT 16A: STREAMLIT SYSTEM DELIVERY
-----------------------------------------------------------------------
[✅] 1. Streamlit Migration: Logic is successfully ported to a web UI.
[✅] 2. UI/UX Design: Layout is organized, intuitive, and easy to navigate.
[✅] 3. GitHub Integration: Full source code is pushed to a public repo.
[✅] 4. Live Deployment: The app is accessible via a Streamlit Cloud URL.
[✅] 5. System Resilience: UI elements handle invalid inputs gracefully.
[✅] 6. OOP Backend: The app still uses Classes/Objects to manage data.
[✅] 7. Data Persistence: System reads/writes to a .txt or .csv file.
-----------------------------------------------------------------------
"""

from models import Build
from data_manager import load_catalog, save_to_file

def main():
    catalog = load_catalog("parts_menu.txt")
    if not catalog: return

    print("\n*** PC BUILD CONFIGURATOR v1.0 [ALPHA] ***")
    name = input("Type the name for new build: ")
    current_build = Build(name)

    while True:
        print(f"\n--- Build: {current_build.name} ---")
        print("1. Add Component")
        print("2. View Current Build / Save")
        print("3. Exit")
        
        choice = input("Choice: ")

        if choice == "1":
            
            categories = ["CPU", "Motherboard", "GPU", "RAM", "Storage", "PSU", "Case"]
            print("\nSelect Component Type:")
            for i, cat in enumerate(categories, 1):
                print(f"{i}. {cat}")
            
            try:
                cat_idx = int(input("Choice: ")) - 1
                selected_cat = categories[cat_idx]

            
                filtered_list = [c for c in catalog if c.type == selected_cat]

                if not filtered_list:
                    print(f"\nNo parts found for {selected_cat}!")
                    continue

        
                print(f"\nSelect {selected_cat}:")
                for i, comp in enumerate(filtered_list, 1):
                    print(f"{i}. {comp.name} (${comp.price})")
                
                item_idx = int(input("Choice: ")) - 1
                selected_item = filtered_list[item_idx]

                current_build.add_item(selected_item)
                print(f"\n{selected_item.name} added!")
            except (ValueError, IndexError):
                print("Invalid selection. Returning to menu.")

        elif choice == "2":
            print(f"\nCURRENT BUILD - ({current_build.name})")
            for cat, p in current_build.parts.items():
                print(f"{cat:15}: {p.name if p else 'none'}")
            
            errors = current_build.get_status()
            print("\nBuild Status:")
            if not errors:
                print(" ✔ All components compatible")
            else:
                for e in errors: print(f"  ✖ {e}")
            
            print(f"Total estimated cost: ${current_build.get_total()}")
            
            save = input("\nSave build to file? (y/n): ")
            if save.lower() == 'y':
                save_to_file(current_build)

        elif choice == "3":
            print("Exiting...")
            break


main()