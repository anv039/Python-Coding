import tkinter as tk
from tkinter import messagebox, filedialog
import pandas as pd

# Quiz class to handle quiz data
class Quiz:
    def __init__(self, questions):
        self.questions = questions
        self.current_question = 0
        self.score = 0

    def get_current_question(self):
        return self.questions[self.current_question]["Question"]

    def get_current_options(self):
        return [
            self.questions[self.current_question]["Option1"],
            self.questions[self.current_question]["Option2"],
            self.questions[self.current_question]["Option3"],
            self.questions[self.current_question]["Option4"],
        ]

    def check_answer(self, selected_option):
        correct_answer = self.questions[self.current_question]["Answer"]
        if selected_option == correct_answer:
            self.score += 1
            return True
        return False

    def next_question(self):
        self.current_question += 1
        return self.current_question < len(self.questions)

# Function to load quiz data from an Excel file
def load_quiz_data_from_excel():
    # Ask user to select an Excel file
    file_path = filedialog.askopenfilename(
        title="Open Quiz Excel File",
        filetypes=[("Excel Files", "*.xlsx *.xls")]
    )
    
    if not file_path:
        messagebox.showerror("Error", "No file was selected.")
        return None

    try:
        # Read the Excel file into a DataFrame
        df = pd.read_excel(file_path)

        # Strip whitespace from column names to prevent key errors
        df.columns = df.columns.str.strip()

        # Check if the required columns are present
        required_columns = ["Question", "Option1", "Option2", "Option3", "Option4", "Answer"]
        if not all(col in df.columns for col in required_columns):
            messagebox.showerror("Error", "Excel file is missing required columns.")
            return None

        # Convert DataFrame to a list of dictionaries
        quiz_data = df.to_dict(orient="records")
        return quiz_data
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load file: {e}")
        return None

# QuizApp class to manage GUI using tkinter
class QuizApp:
    def __init__(self, root, quiz):
        self.root = root
        self.root.title("Online Quiz Application")
        self.root.geometry("500x400")
        self.quiz = quiz

        self.question_label = tk.Label(root, text="", font=("Arial", 14))
        self.question_label.pack(pady=20)

        self.options_var = tk.StringVar()
        self.option_buttons = []

        for i in range(4):
            btn = tk.Radiobutton(root, text="", variable=self.options_var, value="", font=("Arial", 12))
            btn.pack(pady=5)
            self.option_buttons.append(btn)

        self.submit_button = tk.Button(root, text="Submit", command=self.submit_answer)
        self.submit_button.pack(pady=20)

        self.next_button = tk.Button(root, text="Next", command=self.next_question)
        self.next_button.pack(pady=10)

        self.result_label = tk.Label(root, text="", font=("Arial", 12))
        self.result_label.pack()

        self.display_question()

    def display_question(self):
        question = self.quiz.get_current_question()
        options = self.quiz.get_current_options()
        self.question_label.config(text=question)
        self.options_var.set(None)

        for i, option in enumerate(options):
            self.option_buttons[i].config(text=option, value=option)

        self.result_label.config(text="")
        self.submit_button.config(state=tk.NORMAL)
        self.next_button.config(state=tk.DISABLED)

    def submit_answer(self):
        selected_option = self.options_var.get()
        if not selected_option:
            messagebox.showwarning("Warning", "Please select an option.")
            return

        is_correct = self.quiz.check_answer(selected_option)
        if is_correct:
            self.result_label.config(text="Correct!", fg="green")
        else:
            correct_answer = self.quiz.questions[self.quiz.current_question]["Answer"]
            self.result_label.config(text=f"Wrong! The correct answer was: {correct_answer}", fg="red")

        self.submit_button.config(state=tk.DISABLED)
        self.next_button.config(state=tk.NORMAL)

    def next_question(self):
        if self.quiz.next_question():
            self.display_question()
        else:
            messagebox.showinfo("Quiz Finished", f"Your score: {self.quiz.score}/{len(self.quiz.questions)}")
            self.root.destroy()

# Main function to run the quiz app
def main():
    root = tk.Tk()
    quiz_data = load_quiz_data_from_excel()
    if quiz_data:
        quiz = Quiz(quiz_data)
        app = QuizApp(root, quiz)
        root.mainloop()

if __name__ == "__main__":
    main()
