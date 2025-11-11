import tkinter as tk
from tkinter import ttk, messagebox
import threading
import subprocess
import time
import webbrowser

from test_cases import test_cases
from executor import query_model
from analyzer import analyze_response


class LLMTestGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("LLM Security Test Framework")

        # Modele do wyboru
        self.models = {"mistral": tk.BooleanVar(value=True), "gemma3": tk.BooleanVar(value=True)}

        # Kategorie promptów (dynamiczne z test_cases)
        self.categories = {cat: tk.BooleanVar(value=True) for cat in test_cases.keys()}

        self.create_widgets()
        self.log("Framework ready")

    def create_widgets(self):
        frame = ttk.Frame(self.root, padding="10")
        frame.grid(row=0, column=0, sticky="nsew")

        # Modele checkboxy
        ttk.Label(frame, text="Wybierz modele do testów:").grid(row=0, column=0, sticky="w")
        for i, (model, var) in enumerate(self.models.items(), start=1):
            ttk.Checkbutton(frame, text=model, variable=var).grid(row=i, column=0, sticky="w")

        # Kategorie checkboxy
        ttk.Label(frame, text="Wybierz kategorie promptów:").grid(row=0, column=1, sticky="w")
        for i, (cat, var) in enumerate(self.categories.items(), start=1):
            ttk.Checkbutton(frame, text=cat, variable=var).grid(row=i, column=1, sticky="w")

        # Przycisk startu testu
        self.start_btn = ttk.Button(frame, text="Start Tests", command=self.start_tests_thread)
        self.start_btn.grid(row=1, column=2, rowspan=2, sticky="ns")

        # Pole logów
        ttk.Label(frame, text="Log:").grid(row=3, column=0, sticky="w")
        self.log_text = tk.Text(frame, width=80, height=20)
        self.log_text.grid(row=4, column=0, columnspan=3, sticky="nsew")

        # Przycisk otwarcia raportu
        self.report_btn = ttk.Button(frame, text="Open HTML Report", command=self.open_report)
        self.report_btn.grid(row=5, column=2, sticky="e")

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def log(self, msg):
        self.log_text.insert(tk.END, msg + "\n")
        self.log_text.see(tk.END)
        self.root.update()

    def start_tests_thread(self):
        t = threading.Thread(target=self.run_tests)
        t.daemon = True
        t.start()

    def run_tests(self):
        self.start_btn.config(state=tk.DISABLED)
        selected_models = [m for m, var in self.models.items() if var.get()]
        selected_categories = [c for c, var in self.categories.items() if var.get()]

        if not selected_models or not selected_categories:
            messagebox.showerror("Error", "Wybierz przynajmniej jeden model i kategorię promptów")
            self.start_btn.config(state=tk.NORMAL)
            return

        results = []
        for model in selected_models:
            self.log(f"Testing model: {model}")
            for category in selected_categories:
                prompts = test_cases.get(category, [])
                for prompt in prompts:
                    self.log(f"Sending prompt: {prompt}")
                    response = query_model(model, prompt)
                    alert = analyze_response(response)
                    self.log(f"Response: {response[:150]}... Alert: {alert}")
                    results.append((model, category, prompt, response, alert))
                    time.sleep(1)

        self.generate_html_report(results)
        self.log("Tests completed.")
        self.start_btn.config(state=tk.NORMAL)

    def generate_html_report(self, results):
        html_content = "<html><head><title>LLM Security Test Report</title></head><body>"
        html_content += "<h1>LLM Security Test Report</h1>"
        html_content += "<table border='1' style='border-collapse:collapse;'><tr><th>Model</th><th>Category</th><th>Prompt</th><th>Response</th><th>Alert</th></tr>"
        for model, category, prompt, response, alert in results:
            row_color = "#FFCCCC" if alert else "#CCFFCC"
            safe_prompt = prompt.replace('<','&lt;').replace('>','&gt;')
            safe_response = response.replace('<','&lt;').replace('>','&gt;')
            html_content += f"<tr style='background-color:{row_color};'><td>{model}</td><td>{category}</td><td>{safe_prompt}</td><td>{safe_response[:300]}</td><td>{alert}</td></tr>"
        html_content += "</table></body></html>"

        with open("llm_security_test_report.html", "w", encoding="utf-8") as f:
            f.write(html_content)
        self.log("Generated llm_security_test_report.html")

    def open_report(self):
        try:
            webbrowser.open("llm_security_test_report.html")
        except Exception as e:
            messagebox.showerror("Error", f"Nie można otworzyć pliku: {e}")

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Czy na pewno chcesz zakończyć?"):
            self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = LLMTestGUI(root)
    root.mainloop()
