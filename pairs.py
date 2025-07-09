import random
import time
import os
import sys
from colorama import init, Fore, Style

# Initialize colorama for Windows color support
init()

class WordPairDisplay:
    def __init__(self):
        self.file_path = 'word_list.txt'
    
    def clear_screen(self):
        """Clear the console screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def get_random_word_pairs(self, count):
        """Get a list of random word pairs."""
        try:
            with open(self.file_path, 'r') as file:
                word_list = [line.strip() for line in file if len(line.strip()) > 1]
            
            # Ensure we have enough words for the pairs
            if len(word_list) < count * 2:
                print(f"{Fore.RED}Error: Not enough words in file. Need at least {count * 2} words for {count} pairs.{Style.RESET_ALL}")
                sys.exit(1)
            
            # Get random words and pair them
            selected_words = random.sample(word_list, count * 2)
            pairs = []
            for i in range(0, len(selected_words), 2):
                pairs.append((selected_words[i], selected_words[i + 1]))
            
            return pairs
            
        except FileNotFoundError:
            print(f"{Fore.RED}Error: Word list file '{self.file_path}' not found.{Style.RESET_ALL}")
            sys.exit(1)
    
    def get_additional_pairs(self, existing_pairs, count):
        """Get additional word pairs that weren't used in the original display."""
        try:
            with open(self.file_path, 'r') as file:
                word_list = [line.strip() for line in file if len(line.strip()) > 1]
            
            # Get all words that were already used
            used_words = set()
            for pair in existing_pairs:
                used_words.add(pair[0])
                used_words.add(pair[1])
            
            # Get available words (not used in original pairs)
            available_words = [word for word in word_list if word not in used_words]
            
            # Ensure we have enough words for the additional pairs
            if len(available_words) < count * 2:
                print(f"{Fore.YELLOW}Warning: Not enough unused words for {count} additional pairs. Using random words from the full list.{Style.RESET_ALL}")
                # Fall back to using any words from the full list
                selected_words = random.sample(word_list, count * 2)
            else:
                selected_words = random.sample(available_words, count * 2)
            
            # Create pairs
            pairs = []
            for i in range(0, len(selected_words), 2):
                pairs.append((selected_words[i], selected_words[i + 1]))
            
            return pairs
            
        except FileNotFoundError:
            print(f"{Fore.RED}Error: Word list file '{self.file_path}' not found.{Style.RESET_ALL}")
            sys.exit(1)
    
    def display_word_pair(self, pair, pair_number, total_pairs):
        """Display a word pair in a formatted way."""
        self.clear_screen()
        
        word1, word2 = pair
        
        # Create a nice centered display
        print(f"\n{Fore.CYAN}=== WORD PAIR {pair_number} of {total_pairs} ==={Style.RESET_ALL}\n")
        
        # Calculate spacing for side-by-side display
        max_word_length = max(len(word1), len(word2))
        spacing = max(20, max_word_length + 10)  # Minimum 20 characters spacing
        
        # Display words side by side with proper spacing
        print(f"{Fore.GREEN}{word1:<{spacing}}{word2}{Style.RESET_ALL}")
        
        # Add some visual separation
        print(f"{Fore.YELLOW}{'─' * spacing}{'─' * len(word2)}{Style.RESET_ALL}")
    
    def show_answer(self, word_pairs, additional_pairs, additional_seconds, countdown =True):
        """Display all word pairs plus additional pairs for memorization review."""
        self.clear_screen()
        print(f"{Fore.CYAN}=== ALL WORD PAIRS - MEMORIZATION REVIEW ==={Style.RESET_ALL}\n")
        
        # Combine original pairs with additional pairs
        all_pairs = word_pairs + additional_pairs
        
        # Find the maximum word length for formatting
        max_word1_length = max(len(pair[0]) for pair in all_pairs)
        max_word2_length = max(len(pair[1]) for pair in all_pairs)
        spacing = max(20, max_word1_length + 5)
        
        # Display original pairs
        print(f"{Fore.MAGENTA}Original Pairs:{Style.RESET_ALL}")
        for i, (word1, word2) in enumerate(word_pairs, 1):
            print(f"{Fore.YELLOW}{i:2d}.{Style.RESET_ALL} {Fore.GREEN}{word1:<{spacing}}{word2}{Style.RESET_ALL}")
        
        # Display additional pairs if any
        if additional_pairs:
            print(f"\n{Fore.MAGENTA}Additional Pairs:{Style.RESET_ALL}")
            for i, (word1, word2) in enumerate(additional_pairs, len(word_pairs) + 1):
                print(f"{Fore.YELLOW}{i:2d}.{Style.RESET_ALL} {Fore.CYAN}{word1:<{spacing}}{word2}{Style.RESET_ALL}")
        
        # Add visual separation
        total_width = spacing + max_word2_length + 4
        print(f"\n{Fore.YELLOW}{'═' * total_width}{Style.RESET_ALL}")
        
        # Show totals
        print(f"{Fore.MAGENTA}Total: {len(word_pairs)} original + {len(additional_pairs)} additional = {len(all_pairs)} pairs{Style.RESET_ALL}")
        
        # Countdown for additional display time
        if countdown:
            self.countdown_display(additional_seconds, message='Review time remaining:')
    
    def get_positive_number(self, prompt, number_type=float):
        """Get a positive number from user input."""
        while True:
            try:
                value = number_type(input(prompt))
                if value <= 0:
                    print(f"{Fore.RED}Please enter a positive number.{Style.RESET_ALL}")
                    continue
                return value
            except ValueError:
                type_name = "number" if number_type == float else "integer"
                print(f"{Fore.RED}Please enter a valid {type_name}.{Style.RESET_ALL}")

    def get_mode_choice(self):
        """Get user's choice between speed mode and memorization mode."""
        while True:
            print(f"\n{Fore.CYAN}Choose mode:{Style.RESET_ALL}")
            print(f"{Fore.GREEN}1) Speed only{Style.RESET_ALL}")
            print(f"{Fore.GREEN}2) Memorization (includes 2 additional pairs in review){Style.RESET_ALL}")
            
            choice = input(f"\n{Fore.YELLOW}Enter your choice (1 or 2): {Style.RESET_ALL}").strip()
            
            if choice == '1':
                return 'speed'
            elif choice == '2':
                return 'memorization'
            else:
                print(f"{Fore.RED}Please enter 1 or 2.{Style.RESET_ALL}")

    def ask_show_again(self):
        """Ask user if they want to see the words again."""
        self.clear_screen()
        choice = input(f"\n{Fore.YELLOW}Do you want to see the word pairs again? (y/n): {Style.RESET_ALL}").strip().lower()
        if choice in ['y', 'yes']:
            return True
        elif choice in ['n', 'no']:
            return False
        else:
            print(f"{Fore.RED}Please enter 'y' for yes or 'n' for no.{Style.RESET_ALL}")

    def countdown_display(self, seconds, message = 'Next pair in:' ):
        """Display a progress bar countdown for the next pair."""
        print(f"\n{Fore.YELLOW}{message} {Style.RESET_ALL}")
        
        # Progress bar settings
        bar_width = 40
        update_interval = 0.1  # Update every 100ms for smooth animation
        total_updates = int(seconds / update_interval)
        
        for i in range(total_updates + 1):
            # Calculate progress
            progress = i / total_updates
            filled_length = int(bar_width * progress)
            
            # Create the progress bar
            bar = '█' * filled_length + '░' * (bar_width - filled_length)
            
            # Calculate remaining time
            remaining_time = seconds - (i * update_interval)
            
            # Display the progress bar with remaining time
            print(f"\r{Fore.CYAN}[{bar}] {progress:.0%} - {remaining_time:.1f}s remaining{Style.RESET_ALL}", 
                  end="", flush=True)
            
            # Sleep for the update interval (except on last iteration)
            if i < total_updates:
                time.sleep(update_interval)
        
        print(f"\n{Fore.GREEN}Ready!{Style.RESET_ALL}")

    def run(self):
        """Main function to run the word pair display program."""
        self.clear_screen()
        print(f"{Fore.CYAN}=== WORD PAIR DISPLAY PROGRAM ==={Style.RESET_ALL}\n")
        
        try:
            # Get user input
            total_pairs = int(self.get_positive_number("How many word pairs do you want to display? ", int))
            interval = self.get_positive_number("How many seconds between each pair? ", float)
            
            # Get mode choice
            mode = self.get_mode_choice()
            
            additional_seconds = 0
            if mode == 'memorization':
                additional_seconds = self.get_positive_number("How many additional seconds to display all pairs for review? ", float)
            
            # Get random word pairs
            word_pairs = self.get_random_word_pairs(total_pairs)
            
            self.countdown_display(3., message='Starting in:')
            
            # Display each pair
            for i, pair in enumerate(word_pairs, 1):
                self.display_word_pair(pair, i, total_pairs)
                
                # Wait for the specified interval before next pair (except for the last pair)
                if i <= total_pairs:
                    self.countdown_display(interval)
            
            # Handle memorization mode
            if mode == 'memorization':
                # Get 2 additional pairs for review
                additional_pairs = self.get_additional_pairs(word_pairs, 2)
                self.show_answer(word_pairs, additional_pairs, additional_seconds, countdown=True)
                # Show all pairs for review
                if self.ask_show_again():
                    self.show_answer(word_pairs, additional_pairs, additional_seconds, countdown=False)
            
            # Final message
            print(f"\n\n{Fore.CYAN}All {total_pairs} word pairs have been displayed!{Style.RESET_ALL}")
            if mode == 'speed':
                print(f"{Fore.GREEN}Each pair was shown for {interval} seconds.{Style.RESET_ALL}")
            else:
                print(f"{Fore.GREEN}Each pair was shown for {interval} seconds, with {additional_seconds} seconds for final review (including 2 additional pairs).{Style.RESET_ALL}")
            
        except KeyboardInterrupt:
            print(f"\n\n{Fore.YELLOW}Program interrupted by user.{Style.RESET_ALL}")
        except Exception as e:
            print(f"\n{Fore.RED}An error occurred: {e}{Style.RESET_ALL}")
        
        print(f"\n{Fore.CYAN}Thank you for using the Word Pair Display Program!{Style.RESET_ALL}")

if __name__ == "__main__":
    display = WordPairDisplay()
    display.run()
