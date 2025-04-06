import planetterp
import csv

professors = ["Dmitry Dolgopyat", "Larry Herman", "Clyde Kruskal", "Liyi Li", "Anwar Mamat", "Leonidas Lampropoulos"]

with open("data.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile, delimiter="|")
    writer.writerow(["review", "rating"])

    for prof_name in professors:
        
        prof = planetterp.professor(name=prof_name, reviews=True)
        
        for x in prof["reviews"]:
            review = x.get("review", "").strip().replace('"', '""')  # escape internal quotes
            rating = x.get("rating", 0)

            if review:
                writer.writerow([f'"{review}"', rating])

            if review:
                writer.writerow([review, rating])

