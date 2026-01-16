import json
import matplotlib
from pathlib import Path


# Use a non-interactive backend since we embed figures in Tk
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import ttkbootstrap as tb
from ttkbootstrap.constants import *

def load_grade_data(file_path: Path) -> dict:
    """
    Indlæser karakterdata fra en JSON-fil.
    
    Args:
        file_path (Path): Stien til JSON-filen som indeholder elevens karakterer.
    
    Returns:
        dict: Et ordbog med elevens data, typisk med nøglerne 'student' og 'subjects'.
              Eksempel: {'student': 'Peter Jensen', 'subjects': {'Dansk': {}, ...}}
    
    Raises:
        FileNotFoundError: Hvis filen ikke findes på den angivne sti.
        json.JSONDecodeError: Hvis JSON-filen er ugyldigt formateret.
    """
    # Åbner filen i læsetilstand med UTF-8 encoding for at læse danske tegn korrekt
    with open(file_path, "r", encoding="utf-8") as f:
        # json.load() parser JSON-teksten og konverterer den til et Python-ordbog
        return json.load(f)

def render_average_chart(frame, data: dict) -> None:
    """
    Tegner et søjlediagram med gennemsnitlige karakterer pr. fag plus et samlet gennemsnit.
    
    Funktionen:
    1. Udtrækker alle fag og beregner deres gennemsnit
    2. Beregner det samlede gennemsnit blandt alle fag
    3. Tilføjer det samlede gennemsnit som en ekstra søjle
    4. Viser alle søjler i forskellige farver med værdier på toppen
    5. Indlejrer grafen i det givne Tk-frame
    
    Args:
        frame (tk.Frame): Tk-frame hvor grafen skal tegnes.
        data (dict): Ordbog med elevens karakterdata. Skal indeholde 'subjects' nøgle
                     med fagene og deres karakterer, f.eks.:
                     {'subjects': {'Dansk': {'test1': 7, 'test2': 10}, ...}}
    
    Returns:
        None: Funktionen tegner blot i det givne frame.
    """
    subjects = []
    averages = []
    
    # Beregn gennemsnit for hvert fag
    for subject, grades in data["subjects"].items():
        subjects.append(subject)
        # sum() adderer alle karakterer, len() tæller hvor mange der er
        avg = sum(grades.values()) / len(grades)
        averages.append(avg)
    
    # Beregn det samlede gennemsnit blandt alle fag
    # Ved at summere alle gennemsnit og dele med antal fag får vi det samlede gennemsnit
    overall_average = sum(averages) / len(averages) if averages else 0
    
    # Tilføj det samlede gennemsnit til listen
    subjects.append("Samlet gennemsnit")
    averages.append(overall_average)
    
    # Farver til søjlerne - de gentages hvis der er flere fag end farver
    colors = ["#4CB5F5", "#7BC043", "#FFA500"]
    # Sørg for at den sidste søjle (samlet gennemsnit) får en anden farve
    bar_colors = [colors[i % len(colors)] for i in range(len(subjects) - 1)]
    bar_colors.append("#E74C3C")  # Rød farve for det samlede gennemsnit
    
    # Opret figuren og aksen - figsize er bredde x højde i inches, dpi er opløsning
    fig, ax = plt.subplots(figsize=(8, 5), dpi=100)
    
    # Tegn søjlerne med indstillinger for farver, gennemsigtighed og kanter
    ax.bar(subjects, averages, color=bar_colors, alpha=0.85, edgecolor="black", linewidth=1.2)
    
    # Indstil titlen, størrelse og afstand fra grafen
    ax.set_title("Gennemsnitlige karakterer pr. fag", fontsize=14, fontweight="bold", pad=15)
    
    # Indstil y-aksen til at gå fra 0-12 (dansk karakterskala)
    ax.set_ylim(0, 12)
    
    # Navngiv akserne
    ax.set_ylabel("Gennemsnitlig karakter", fontsize=11)
    ax.set_xlabel("Fag", fontsize=11)
    
    # Tilføj stiplede gitterlinjer for at gøre det nemmere at læse værdier
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    
    # Tilføj værdier på toppen af hver søjle
    for i, (subject, avg) in enumerate(zip(subjects, averages)):
        # ha="center" betyder vandret centreret, va="bottom" betyder lodret under toppen
        ax.text(i, avg + 0.3, f"{avg:.1f}", ha="center", va="bottom", fontweight="bold")
    
    # Sørg for at alle elementer passer inden for figuren
    fig.tight_layout()
    
    # Indlejr matplotlib-figuren i Tk-vinduet ved hjælp af FigureCanvasTkAgg
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=BOTH, expand=True)


def main() -> None:
    """
    Hovedfunktion der initialiserer og kører Tk-applikationen.
    
    Funktionen:
    1. Indlæser karakterdata fra JSON-filen
    2. Opretter Tk-vinduet med ttkbootstrap tema
    3. Opbygger headerbar med titel og tema-skift knap
    4. Opbygger hovedindhold med karakteroversigt-kort
    5. Starter applikationen (mainloop)
    
    Tk-gride-systemet bruges til at placere elementer:
    - grid() placerer widgets i rækker og kolonner
    - weight=1 gør at elementet udvider sig når vinduet ændrer størrelse
    - sticky="nsew" betyder at elementet fylder hele sin celle
    """
    # Find JSON-filen i samme mappe som dette script
    data_file = Path(__file__).with_name("peter_jensen_grades.json")
    data = load_grade_data(data_file)

    # Opret hovedvinduet med "flatly" tema fra ttkbootstrap
    app = tb.Window(title="Elevdashboard", themename="flatly")
    app.columnconfigure(0, weight=1)
    app.rowconfigure(1, weight=1)

    # Opret header (øverste bar med titel og knapper)
    header = tb.Frame(app, padding=10, bootstyle="dark")
    header.grid(row=0, column=0, sticky="ew")
    
    # Tilføj titellabel med elevens navn
    tb.Label(
        header,
        text=f"Karakterer · {data.get('student', 'Elev')}",
        bootstyle="inverse-dark",
        font=("Helvetica", 12, "bold"),
    ).pack(side=LEFT)
    
    # Tilføj tema-skift knap
    tb.Button(
        header,
        text="Skift tema",
        command=lambda: app.style.theme_use("cosmo"),
        bootstyle="light",
    ).pack(side=RIGHT, padx=5)

    # Opret hovedindhold-frame som udvider sig med vinduet
    main = tb.Frame(app, padding=12)
    main.grid(row=1, column=0, sticky="nsew")
    main.columnconfigure(0, weight=1)
    main.rowconfigure(0, weight=1)

    # Opret kort (card) med karakteroversigten
    card = tb.Labelframe(
        main,
        text="Oversigt",
        padding=10,
        bootstyle="info",
    )
    card.grid(row=0, column=0, sticky="nsew", padx=6, pady=6)
    card.columnconfigure(0, weight=1)
    card.rowconfigure(0, weight=1)

    # Tegn grafen i kortet
    render_average_chart(card, data)

    # Start applikationen (venter på brugerinteraktion)
    app.mainloop()


if __name__ == "__main__":
    main()
