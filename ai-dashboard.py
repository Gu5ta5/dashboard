import json
from pathlib import Path

import matplotlib

# Use a non-interactive backend since we embed figures in Tk
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import ttkbootstrap as tb
from ttkbootstrap.constants import *

def load_grade_data(file_path: Path) -> dict:
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def render_subject_chart(frame, subject: str, grades: dict, color: str) -> None:
    labels = list(grades.keys())
    values = list(grades.values())

    fig, ax = plt.subplots(figsize=(3.4, 2.2), dpi=100)
    ax.bar(labels, values, color=color, alpha=0.85)
    ax.set_title(subject, fontsize=11, pad=8)
    ax.set_ylim(0, 12)
    ax.set_ylabel("Karakter")
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    fig.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=BOTH, expand=True)


def main() -> None:
    data_file = Path(__file__).with_name("peter_jensen_grades.json")
    data = load_grade_data(data_file)

    app = tb.Window(title="Elevdashboard", themename="flatly")
    app.columnconfigure(0, weight=1)
    app.rowconfigure(1, weight=1)

    header = tb.Frame(app, padding=10, bootstyle="dark")
    header.grid(row=0, column=0, sticky="ew")
    tb.Label(
        header,
        text=f"Karakterer · {data.get('student', 'Elev')}",
        bootstyle="inverse-dark",
        font=("Helvetica", 12, "bold"),
    ).pack(side=LEFT)
    tb.Button(
        header,
        text="Skift tema",
        command=lambda: app.style.theme_use("cosmo"),
        bootstyle="light",
    ).pack(side=RIGHT, padx=5)

    main = tb.Frame(app, padding=12)
    main.grid(row=1, column=0, sticky="nsew")
    main.columnconfigure((0, 1, 2), weight=1, uniform="chart")

    colors = ["#4CB5F5", "#7BC043", "#FFA500"]
    for idx, (subject, grades) in enumerate(data["subjects"].items()):
        card = tb.Labelframe(
            main,
            text=f"{subject}",
            padding=10,
            bootstyle="info",
        )
        card.grid(row=0, column=idx, sticky="nsew", padx=6, pady=6)

        avg = sum(grades.values()) / len(grades)
        tb.Label(
            card,
            text=f"Gennemsnit: {avg:.1f}",
            font=("Helvetica", 11, "bold"),
        ).pack(anchor=W, pady=(0, 6))

        render_subject_chart(card, subject, grades, colors[idx % len(colors)])

    app.mainloop()


if __name__ == "__main__":
    main()
