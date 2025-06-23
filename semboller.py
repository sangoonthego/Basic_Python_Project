import random
import time
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def run_slot_machine():
    symbols = ["🍒", "🍋", "🍇", "⭐", "💎", "🔔"]
    
    while True:
        clear_screen()
        print("--- Slot Machine ---")
        input("Press Enter to spin...")

        for _ in range(10):
            a, b, c = random.choices(symbols, k=3)
            clear_screen()
            print("--- Slot Machine ---")
            print(f"| {a} | {b} | {c} |")
            time.sleep(0.15)
        
        print("\nHere is the result:")
        
        if a == b == c:
            print("🏆 JACKPOT! Awesome!")
        elif a == b or c == a:
            print("✨ Nice! Two matches.")
        else:
            print("😕 Try your luck again.")

        play_again = input("\nWanna play again? (y/n): ").lower()
        if play_again != 'y':
            break

if __name__ == "__main__":
    run_slot_machine()
