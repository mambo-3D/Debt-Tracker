# Deni v2 - Debt and Budget Tracker (Basic Logic Added)
# Author:Mambo-3D)
# ---------------------------------------------------------
# Features:
#  - Add Income and Expenses
#  - Track Debts (with name, amount, interest)
#  - Dashboard shows totals
# ---------------------------------------------------------

import customtkinter as ctk
from tkinter import messagebox  # for error/warning popups

# --------------------- App Setup ------------------------
ctk.set_appearance_mode("Dark")  # options: "System", "Light", "Dark"
ctk.set_default_color_theme("blue")  # options: "blue", "green", "dark-blue"

class DeniApp(ctk.CTk):
    """
    Deni: A Debt + Budget Tracker
    Version 2 = Adds income/expenses & debts logic
    """

    def __init__(self):
        super().__init__()

        # ------------------ Window Setup -------------------
        self.title("Deni - Debt & Budget Tracker")
        self.geometry("900x600")

        # Grid layout: sidebar (left) + main content (right)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ------------------ Data Storage -------------------
        self.income = 0
        self.expenses = []
        self.debts = []

        # ------------------ Sidebar ------------------------
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nswe")

        self.logo = ctk.CTkLabel(self.sidebar, text="Deni", font=("Arial", 24, "bold"))
        self.logo.pack(pady=20)

        # Navigation buttons
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

        # Show dashboard first
        self.show_dashboard()

    # ------------------ Helpers --------------------------
    def clear_main(self):
        """Clear all widgets in main frame before loading a new page"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    # ------------------ Dashboard ------------------------
    def show_dashboard(self):
        self.clear_main()

        # Calculate totals
        total_expenses = sum(self.expenses) if self.expenses else 0
        total_debts = sum([d["amount"] for d in self.debts]) if self.debts else 0
        balance = self.income - total_expenses

        title = ctk.CTkLabel(self.main_frame, text="📊 Dashboard", font=("Arial", 20, "bold"))
        title.pack(pady=10)

        income_lbl = ctk.CTkLabel(self.main_frame, text=f"Total Income: {self.income} Ksh", font=("Arial", 16))
        income_lbl.pack(pady=5)

        expense_lbl = ctk.CTkLabel(self.main_frame, text=f"Total Expenses: {total_expenses} Ksh", font=("Arial", 16))
        expense_lbl.pack(pady=5)

        balance_lbl = ctk.CTkLabel(self.main_frame, text=f"Balance: {balance} Ksh", font=("Arial", 16, "bold"))
        balance_lbl.pack(pady=5)

        debt_lbl = ctk.CTkLabel(self.main_frame, text=f"Outstanding Debts: {total_debts} Ksh", font=("Arial", 16, "bold"))
        debt_lbl.pack(pady=10)

    # ------------------ Debts ----------------------------
    def show_debts(self):
        self.clear_main()

        title = ctk.CTkLabel(self.main_frame, text="💰 Debts", font=("Arial", 20, "bold"))
        title.pack(pady=10)

        # Input fields
        name_entry = ctk.CTkEntry(self.main_frame, placeholder_text="Debt Name")
        name_entry.pack(pady=5)

        amount_entry = ctk.CTkEntry(self.main_frame, placeholder_text="Amount (Ksh)")
        amount_entry.pack(pady=5)

        interest_entry = ctk.CTkEntry(self.main_frame, placeholder_text="Interest Rate (%)")
        interest_entry.pack(pady=5)

        def add_debt():
            """Add a new debt to list"""
            try:
                name = name_entry.get()
                amount = float(amount_entry.get())
                interest = float(interest_entry.get())
                if name.strip() == "":
                    raise ValueError("Name required")

                self.debts.append({"name": name, "amount": amount, "interest": interest})
                messagebox.showinfo("Success", f"Debt '{name}' added!")
                self.show_debts()  # Refresh page
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers for amount/interest.")

        add_btn = ctk.CTkButton(self.main_frame, text="Add Debt", command=add_debt)
        add_btn.pack(pady=10)

        # Show current debts
        if self.debts:
            for d in self.debts:
                lbl = ctk.CTkLabel(self.main_frame, text=f"{d['name']} - {d['amount']} Ksh @ {d['interest']}%")
                lbl.pack()

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
            """Set monthly income"""
            try:
                self.income = float(income_entry.get())
                messagebox.showinfo("Success", f"Income set: {self.income} Ksh")
                self.show_dashboard()
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number.")

        def add_expense():
            """Add an expense"""
            try:
                amount = float(expense_entry.get())
                self.expenses.append(amount)
                messagebox.showinfo("Success", f"Expense {amount} Ksh added!")
                self.show_budget()
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number.")

        income_btn = ctk.CTkButton(self.main_frame, text="Set Income", command=set_income)
        income_btn.pack(pady=5)

        expense_btn = ctk.CTkButton(self.main_frame, text="Add Expense", command=add_expense)
        expense_btn.pack(pady=5)

        # Show list of expenses
        if self.expenses:
            for e in self.expenses:
                lbl = ctk.CTkLabel(self.main_frame, text=f"Expense: {e} Ksh")
                lbl.pack()

    # ------------------ Savings --------------------------
    def show_savings(self):
        self.clear_main()
        label = ctk.CTkLabel(self.main_frame, text="💎 Savings (Coming soon)", font=("Arial", 18))
        label.pack(pady=20)

    # ------------------ Reports --------------------------
    def show_reports(self):
        self.clear_main()
        label = ctk.CTkLabel(self.main_frame, text="📑 Reports (Coming soon)", font=("Arial", 18))
        label.pack(pady=20)

# ------------------ Run the App --------------------------
if __name__ == "__main__":
    app = DeniApp()
    app.mainloop()
