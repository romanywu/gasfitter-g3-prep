import tkinter as tk
from tkinter import filedialog, messagebox

class FlashcardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Flashcard App")
        self.flashcards = []
        self.current_index = 0
        self.incorrect_answers = []

        # UI Elements
        self.instruction_label = tk.Label(root, text="Click the button to load a textbook:")
        self.instruction_label.pack(pady=10)

        self.load_button = tk.Button(root, text="Load Textbook", command=self.load_textbook)
        self.load_button.pack(pady=10)

        self.flashcard_label = tk.Label(root, text="", wraplength=400, justify="center")
        self.flashcard_label.pack(pady=20)

        self.answer_entry = tk.Entry(root)
        self.answer_entry.pack(pady=10)

        self.submit_button = tk.Button(root, text="Submit Answer", command=self.check_answer)
        self.submit_button.pack(pady=10)

        self.result_label = tk.Label(root, text="")
        self.result_label.pack(pady=10)

    def load_textbook(self):
        file_path = filedialog.askopenfilename(title="Select Textbook File", filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
            self.flashcards = self.process_textbook(content)
            if self.flashcards:
                self.current_index = 0
                self.incorrect_answers = []
                self.show_flashcard()
            else:
                messagebox.showerror("Error", "No flashcards could be created from the textbook.")

    def process_textbook(self, content):
        # Split the textbook content into flashcards (e.g., Q&A pairs)
        # Example format: "Question: ... Answer: ..."
        flashcards = []
        lines = content.splitlines()
        for line in lines:
            if "Question:" in line and "Answer:" in line:
                parts = line.split("Answer:")
                question = parts[0].replace("Question:", "").strip()
                answer = parts[1].strip()
                flashcards.append((question, answer))
        return flashcards

    def show_flashcard(self):
        if self.current_index < len(self.flashcards):
            question, _ = self.flashcards[self.current_index]
            self.flashcard_label.config(text=f"Question: {question}")
            self.answer_entry.delete(0, tk.END)
            self.result_label.config(text="")
        else:
            self.flashcard_label.config(text="All questions completed!")
            self.answer_entry.pack_forget()
            self.submit_button.pack_forget()
            self.show_incorrect_answers()

    def check_answer(self):
        if self.current_index < len(self.flashcards):
            _, correct_answer = self.flashcards[self.current_index]
            user_answer = self.answer_entry.get().strip()
            if user_answer.lower() == correct_answer.lower():
                self.result_label.config(text="Correct!", fg="green")
            else:
                self.result_label.config(text=f"Incorrect! Correct answer: {correct_answer}", fg="red")
                self.incorrect_answers.append(self.current_index + 1)  # Record question number
            self.current_index += 1
            self.root.after(1000, self.show_flashcard)

    def show_incorrect_answers(self):
        if self.incorrect_answers:
            incorrect_str = ", ".join(map(str, self.incorrect_answers))
            messagebox.showinfo("Review", f"Questions answered incorrectly: {incorrect_str}")
        else:
            messagebox.showinfo("Review", "You answered all questions correctly!")

# Run the application
root = tk.Tk()
app = FlashcardApp(root)
root.mainloop()