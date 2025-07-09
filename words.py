import random
import time
import os
import sys
import threading
from colorama import init, Fore, Style

# Initialize colorama for Windows color support
init()

class WordMemorizationGame:
    def __init__(self):
        self.file_path = 'word_list.txt'
        self.timer_running = False
        
    def clear_screen(self):
        """Clear the console screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def get_random_words(self, count):
        """Get a list of random words."""
        try:
            with open(self.file_path, 'r') as file:
                word_list = [line.strip() for line in file if len(line.strip()) > 1]
                
                # Ensure we don't ask for more words than available
                count = min(count, len(word_list))
                return random.sample(word_list, count)
        except FileNotFoundError:
            print(f"{Fore.RED}Error: Word list file '{self.file_path}' not found.{Style.RESET_ALL}")
            sys.exit(1)
        print("".join(row))

    def display_words(self, words):
        """Display words in a formatted way - 2 words per line."""
        print(f"\n{Fore.CYAN}=== MEMORIZE THESE WORDS ==={Style.RESET_ALL}\n")
    
        for i in range(0, len(words), 2):
            # Get the current word and next word (if it exists)
            word1 = words[i]
            word2 = words[i + 1] if i + 1 < len(words) else ""
        
            # Display two words side by side with consistent spacing
            if word2:
                print(f"{Fore.GREEN}• {word1:<20} • {word2}{Style.RESET_ALL}")
            else:
                print(f"{Fore.GREEN}• {word1}{Style.RESET_ALL}")

    def display_timer(self, start_time):
        """Display a running timer."""
        while self.timer_running:
            elapsed = time.time() - start_time
            minutes = int(elapsed // 60)
            seconds = int(elapsed % 60)
            sys.stdout.write(f"\r{Fore.YELLOW}Time elapsed: {minutes:02d}:{seconds:02d}{Style.RESET_ALL}")
            sys.stdout.flush()
            time.sleep(0.1)
        
    def timed_memorization(self, words, seconds):
        """Run timed memorization session."""
        self.clear_screen()
        self.display_words(words)
                
        print(f"\n{Fore.YELLOW}Time remaining: {seconds} seconds{Style.RESET_ALL}")
                
        # Countdown timer
        for remaining in range(seconds, 0, -1):
            sys.stdout.write(f"\r{Fore.YELLOW}Time remaining: {remaining} seconds{Style.RESET_ALL}")
            sys.stdout.flush()
            time.sleep(1)
                
        self.clear_screen()
        print(f"\n{Fore.RED}Time's up! Try to recall the words you memorized.{Style.RESET_ALL}\n")
        
    def untimed_memorization(self, words):
        """Run untimed memorization session."""
        self.clear_screen()
        self.display_words(words)
                
        print(f"\n{Fore.YELLOW}Press Enter when you're finished memorizing...{Style.RESET_ALL}")
        
        # Record start time and start timer display
        start_time = time.time()
        self.timer_running = True
        
        # Start timer display in a separate thread
        timer_thread = threading.Thread(target=self.display_timer, args=(start_time,))
        timer_thread.daemon = True
        timer_thread.start()
        
        input()  # Wait for user to press Enter
        
        # Stop the timer thread
        self.timer_running = False
        timer_thread.join(timeout=0.5)  # Wait for thread to finish
        
        # Calculate elapsed time
        elapsed_time = time.time() - start_time
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
                
        self.clear_screen()
        print(f"\n{Fore.RED}Now try to recall the words you memorized.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}You spent {minutes} minutes and {seconds} seconds memorizing.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}That's about {elapsed_time/len(words):.2f} seconds per word.{Style.RESET_ALL}\n")
        
    def show_answer(self, words):
        """Show the words that were to be memorized - 2 words per line."""
        print(f"\n{Fore.CYAN}The words were:{Style.RESET_ALL}\n")
        
        for i in range(0, len(words), 2):
            # Get the current word and next word (if it exists)
            word1 = words[i]
            word2 = words[i + 1] if i + 1 < len(words) else ""
            
            # Display two words side by side with consistent spacing
            if word2:
                print(f"{Fore.GREEN}• {word1:<20} • {word2}{Style.RESET_ALL}")
            else:
                print(f"{Fore.GREEN}• {word1}{Style.RESET_ALL}")
        
    def get_positive_integer(self, prompt):
        """Get a positive integer from user input."""
        while True:
            try:
                value = int(input(prompt))
                if value <= 0:
                    print(f"{Fore.RED}Please enter a positive number.{Style.RESET_ALL}")
                    continue
                return value
            except ValueError:
                print(f"{Fore.RED}Please enter a valid number.{Style.RESET_ALL}")
        
    def get_yes_no_input(self, prompt):
        """Get a yes/no response from user."""
        response = input(prompt).lower()
        return response in ['y', 'yes']
        
    def run(self):
        """Main function to run the word memorization program."""
        self.clear_screen()
        print(f"{Fore.CYAN}=== WORD MEMORIZATION PROGRAM ==={Style.RESET_ALL}\n")
                
        try:
            # Get user input for word count
            word_count = self.get_positive_integer("How many words do you want to memorize? ")
                        
            # Ask if user wants timed memorization
            is_timed = self.get_yes_no_input("Would you like this to be timed? (y/n): ")
                        
            # Get random words
            words = self.get_random_words(word_count)
                        
            # Run appropriate memorization mode
            if is_timed:
                seconds = self.get_positive_integer("How many seconds do you want to spend memorizing? ")
                self.timed_memorization(words, seconds)
            else:
                self.untimed_memorization(words)
                        
            # Ask if user wants to see the words again
            if self.get_yes_no_input("Would you like to see the words again? (y/n): "):
                self.show_answer(words)
                
        except KeyboardInterrupt:
            print(f"\n\n{Fore.YELLOW}Program interrupted by user.{Style.RESET_ALL}")
            self.timer_running = False  # Make sure to stop the timer thread
                
        print(f"\n{Fore.CYAN}Thank you for using the Word Memorization Program!{Style.RESET_ALL}")

if __name__ == "__main__":
    game = WordMemorizationGame()
    game.run()
