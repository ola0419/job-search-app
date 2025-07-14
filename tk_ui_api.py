import tkinter as tk
from tkinter import ttk, messagebox
from adzuna_api import fetch_jobs


class JobApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Job Search App (Powered by Adzuna API)")
        self.root.geometry("750x500")

        # Labels and Entry fields
        self.keyword_label = tk.Label(root, text="Job Title:")
        self.keyword_label.pack()
        self.keyword_entry = tk.Entry(root, width=40)
        self.keyword_entry.pack(pady=5)

        self.location_label = tk.Label(root, text="Location:")
        self.location_label.pack()
        self.location_entry = tk.Entry(root, width=40)
        self.location_entry.pack(pady=5)

        self.search_button = tk.Button(root, text="Search Jobs", command=self.search_jobs)
        self.search_button.pack(pady=10)

        # Result frame
        self.result_frame = tk.Frame(root)
        self.result_frame.pack(fill="both", expand=True)

        # Styling
        style = ttk.Style()
        style.configure("Treeview", font=('Arial', 11), rowheight=30)
        style.configure("Treeview.Heading", font=('Arial', 12, 'bold'))

        # Treeview table
        self.tree = ttk.Treeview(self.result_frame, columns=("Title", "Company", "Location", "Salary"), show='headings')

        self.tree.heading("Title", text="Title")
        self.tree.heading("Company", text="Company")
        self.tree.heading("Location", text="Location")
        self.tree.heading("Salary", text="Salary")

        self.tree.column("Title", width=250)
        self.tree.column("Company", width=180)
        self.tree.column("Location", width=180)
        self.tree.column("Salary", width=120)

        self.tree.pack(fill="both", expand=True)

        # Scrollbar
        self.scrollbar = ttk.Scrollbar(self.result_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")

        # Row tags for color
        self.tree.tag_configure('evenrow', background='white')
        self.tree.tag_configure('oddrow', background='lightblue')

    def search_jobs(self):
        keyword = self.keyword_entry.get()
        location = self.location_entry.get()

        if not keyword or not location:
            messagebox.showwarning("Input Error", "Please enter both job title and location.")
            return

        self.tree.delete(*self.tree.get_children())
        jobs = fetch_jobs(keyword, location)

        if not jobs:
            messagebox.showinfo("No Results", "No jobs found.")
            return

        for i, job in enumerate(jobs):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            self.tree.insert("", "end", values=(job["title"], job["company"], job["location"], job["salary"]), tags=(tag,))


if __name__ == "__main__":
    root = tk.Tk()
    app = JobApp(root)
    root.mainloop()
