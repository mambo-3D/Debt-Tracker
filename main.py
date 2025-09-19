# Deni v2 - Debt and Budget Tracker (Basic Logic Added)
# Author:Mambo-3D)
# ---------------------------------------------------------
# Deni v2.5 - Added Savings Goals + Basic Reports + Charts
# --------------------------------------------------------

import customtkinter as ctk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# --------------------- App Setup ------------------------
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class DeniApp(ctk.CTk):
    """
    Deni: Debt + Budget Tracker
    Version 2.5: Income/Expenses + Debts + Savings + Reports + Charts
    """

    def __init__(self):
        super().__init__()

        # ------------------ Window Setup -------------------
        self.title("Deni - Debt & Budget Tracker")
        self.geometry("1000x650")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ------------------ Data Storage -------------------
        self.income = 0
        self.expenses = []
        self.debts = []
        self.savings_goal = {"name": None, "target": 0, "saved": 0}

        # ------------------ Sidebar ------------------------
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nswe")

        self.logo = ctk.CTkLabel(self.sidebar, text="Deni", font=("Arial", 24, "bold"))
        self.logo.pack(pady=20)

        self.dashboard_btn = ctk.CTkButton(self.sidebar, text="Dashboard", command=self.show_dashboard)
        self.dashboard_btn.pack(pady=10)

        self.debts_btn = ctk.CTkButton(self.sidebar, text="Debts", command=self.show_debts)
        self.debts_btn.pack(pady=10)

        self.budget_btn = ctk.CTkButton(self.sidebar, text="Budget", command=self.show_budget)
        self.budget_btn.pack(pady=10)

        self.savings_btn = ctk.CTkButton(self.sidebar, text="Savings", command=self.show_savings)
        self.savings_btn.pack(pady=10)

        self.reports_btn = ctk.CTkButton(self.sidebar, text="Reports", command=self.show_reports)
        self.reports_btn.pack(pady=10)

        # ------------------ Main Frame ---------------------
        self.main_frame = ctk.CTkFrame(self, corner_radius=10)
        self.main_frame.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        # Load Dashboard by default
        self.show_dashboard()

    # ------------------ Helper ---------------------------
    def clear_main(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    # ------------------ Dashboard ------------------------
    def show_dashboard(self):
        self.clear_main()
        total_expenses = sum(self.expenses) if self.expenses else 0
        total_debts = sum([d["amount"] for d in self.debts]) if self.debts else 0
        balance = self.income - total_expenses

        title = ctk.CTkLabel(self.main_frame, text="📊 Dashboard", font=("Arial", 20, "bold"))
        title.pack(pady=10)

        ctk.CTkLabel(self.main_frame, text=f"Total Income: {self.income} Ksh", font=("Arial", 16)).pack(pady=5)
        ctk.CTkLabel(self.main_frame, text=f"Total Expenses: {total_expenses} Ksh", font=("Arial", 16)).pack(pady=5)
        ctk.CTkLabel(self.main_frame, text=f"Balance: {balance} Ksh", font=("Arial", 16, "bold")).pack(pady=5)
        ctk.CTkLabel(self.main_frame, text=f"Outstanding Debts: {total_debts} Ksh", font=("Arial", 16, "bold")).pack(pady=10)

    # ------------------ Debts ----------------------------
    def show_debts(self):
        self.clear_main()
        title = ctk.CTkLabel(self.main_frame, text="💰 Debts", font=("Arial", 20, "bold"))
        title.pack(pady=10)

        name_entry = ctk.CTkEntry(self.main_frame, placeholder_text="Debt Name")
        name_entry.pack(pady=5)

        amount_entry = ctk.CTkEntry(self.main_frame, placeholder_text="Amount (Ksh)")
        amount_entry.pack(pady=5)

        interest_entry = ctk.CTkEntry(self.main_frame, placeholder_text="Interest Rate (%)")
        interest_entry.pack(pady=5)

        def add_debt():
            try:
                name = name_entry.get()
                amount = float(amount_entry.get())
                interest = float(interest_entry.get())
                if amount <= 0 or interest < 0:
                    raise ValueError("Values must be positive")
                self.debts.append({"name": name, "amount": amount, "interest": interest})
                messagebox.showinfo("Success", f"Debt '{name}' added!")
                self.show_debts()
            except ValueError:
                messagebox.showerror("Error", "Enter valid numbers for amount/interest.")

        ctk.CTkButton(self.main_frame, text="Add Debt", command=add_debt).pack(pady=10)

        if self.debts:
            for d in self.debts:
                ctk.CTkLabel(self.main_frame, text=f"{d['name']} - {d['amount']} Ksh @ {d['interest']}%").pack()

    # ------------------ Budget ---------------------------
    def show_budget(self):
        self.clear_main()
        title = ctk.CTkLabel(self.main_frame, text="📅 Budget", font=("Arial", 20, "bold"))
        title.pack(pady=10)

        income_entry = ctk.CTkEntry(self.main_frame, placeholder_text="Enter Monthly Income (Ksh)")
        income_entry.pack(pady=5)

        expense_entry = ctk.CTkEntry(self.main_frame, placeholder_text="Add Expense (Ksh)")
        expense_entry.pack(pady=5)

        def set_income():
            try:
                self.income = float(income_entry.get())
                if self.income < 0:
                    raise ValueError
                messagebox.showinfo("Success", f"Income set: {self.income} Ksh")
                self.show_dashboard()
            except ValueError:
                messagebox.showerror("Error", "Enter a valid income number.")

        def add_expense():
            try:
                amount = float(expense_entry.get())
                if amount <= 0:
                    raise ValueError
                self.expenses.append(amount)
                messagebox.showinfo("Success", f"Expense {amount} Ksh added!")
                self.show_budget()
            except ValueError:
                messagebox.showerror("Error", "Enter a valid expense amount.")

        ctk.CTkButton(self.main_frame, text="Set Income", command=set_income).pack(pady=5)
        ctk.CTkButton(self.main_frame, text="Add Expense", command=add_expense).pack(pady=5)

        if self.expenses:
            for e in self.expenses:
                ctk.CTkLabel(self.main_frame, text=f"Expense: {e} Ksh").pack()

    # ------------------ Savings --------------------------
    def show_savings(self):
        self.clear_main()
        title = ctk.CTkLabel(self.main_frame, text="💎 Savings Goal", font=("Arial", 20, "bold"))
        title.pack(pady=10)

        goal_entry = ctk.CTkEntry(self.main_frame, placeholder_text="Goal Name (e.g., Laptop)")
        goal_entry.pack(pady=5)

        target_entry = ctk.CTkEntry(self.main_frame, placeholder_text="Target Amount (Ksh)")
        target_entry.pack(pady=5)

        save_entry = ctk.CTkEntry(self.main_frame, placeholder_text="Amount to Save Now (Ksh)")
        save_entry.pack(pady=5)

        def set_goal():
            try:
                name = goal_entry.get()
                target = float(target_entry.get())
                if target <= 0:
                    raise ValueError
                self.savings_goal = {"name": name, "target": target, "saved": 0}
                messagebox.showinfo("Success", f"Savings goal '{name}' set at {target} Ksh!")
                self.show_savings()
            except ValueError:
                messagebox.showerror("Error", "Enter a valid target.")

        def add_savings():
            try:
                amount = float(save_entry.get())
                if amount <= 0:
                    raise ValueError
                if self.savings_goal["target"] == 0:
                    messagebox.showwarning("No Goal", "Set a savings goal first.")
                    return
                self.savings_goal["saved"] += amount
                messagebox.showinfo("Saved", f"Added {amount} Ksh to savings!")
                self.show_savings()
            except ValueError:
                messagebox.showerror("Error", "Enter a valid savings amount.")

        ctk.CTkButton(self.main_frame, text="Set Goal", command=set_goal).pack(pady=5)
        ctk.CTkButton(self.main_frame, text="Add Savings", command=add_savings).pack(pady=5)

        if self.savings_goal["target"] > 0:
            progress = (self.savings_goal["saved"] / self.savings_goal["target"]) * 100
            ctk.CTkLabel(self.main_frame, text=f"Goal: {self.savings_goal['name']}").pack(pady=5)
            ctk.CTkLabel(self.main_frame, text=f"Saved: {self.savings_goal['saved']} / {self.savings_goal['target']} Ksh").pack(pady=5)
            bar = ctk.CTkProgressBar(self.main_frame, width=300)
            bar.set(progress / 100)
            bar.pack(pady=10)

    # ------------------ Reports --------------------------
    def show_reports(self):
        self.clear_main()
        title = ctk.CTkLabel(self.main_frame, text="📑 Reports", font=("Arial", 20, "bold"))
        title.pack(pady=10)

        # Calculate summary
        total_expenses = sum(self.expenses) if self.expenses else 0
        total_debts = sum([d["amount"] for d in self.debts]) if self.debts else 0
        balance = self.income - total_expenses
        saved = self.savings_goal["saved"]

        summary = f"""
        Income: {self.income} Ksh
        Expenses: {total_expenses} Ksh
        Balance: {balance} Ksh
        Debts: {total_debts} Ksh
        Savings: {saved} Ksh
        """
        ctk.CTkLabel(self.main_frame, text=summary, justify="left").pack(pady=20)

        # Show Pie Chart of finances
        fig, ax = plt.subplots(figsize=(4, 4))
        labels = ["Expenses", "Debts", "Savings", "Balance"]
        values = [total_expenses, total_debts, saved, max(balance, 0)]
        ax.pie(values, labels=labels, autopct="%1.1f%%", startangle=90)
        ax.set_title("Financial Breakdown")

        canvas = FigureCanvasTkAgg(fig, master=self.main_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

# ------------------ Run --------------------------
if __name__ == "__main__":
    app = DeniApp()
    app.mainloop()
