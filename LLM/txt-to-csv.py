import csv
import re

def process_text_to_csv(input_file, output_file):
    headers = [
        "Year","Area","English title","Authors","Contact",
        "University by author","Keywords","Highlights","Software Used",
        "Methods Applied","Basis Set","Related Reactions",
        "Molecules or atoms used","Conclusion","Relevance","Acknowledgments"
    ]

    data_rows = []

    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()

    blocks = re.split(r'(?=category,information)', content)
    if blocks and not blocks[0].strip():
        blocks = blocks[1:]

    for block in blocks:
        row = {header: "N/A" for header in headers}
        lines = block.splitlines()
        for line in lines:
            if line.strip().lower() == "category,information":
                continue

            if "," in line:
                key, value = line.split(",", 1)
                key = key.strip()
                key_lower = key.lower()
                value = value.strip().strip('"').replace(',', ';')

                # Ordem é importante: verificar termos mais específicos antes
                if "year" in key_lower:
                    row["Year"] = value
                elif "area" in key_lower:
                    row["Area"] = value
                elif "english title" in key_lower:
                    row["English title"] = value
                elif "university by author" in key_lower:
                    row["University by author"] = value
                elif key_lower.startswith("authors"):
                    row["Authors"] = value
                elif "contact" in key_lower:
                    row["Contact"] = value
                elif "keyword" in key_lower:
                    row["Keywords"] = value
                elif "highlight" in key_lower:
                    row["Highlights"] = value
                elif "software" in key_lower:
                    row["Software Used"] = value
                elif "method" in key_lower:
                    row["Methods Applied"] = value
                elif "basis" in key_lower:
                    row["Basis Set"] = value
                elif "related reaction" in key_lower:
                    row["Related Reactions"] = value
                elif "molecule" in key_lower or "atom" in key_lower:
                    row["Molecules or atoms used"] = value
                elif "conclusion" in key_lower:
                    row["Conclusion"] = value
                elif "relevance" in key_lower:
                    row["Relevance"] = value
                elif "acknowledgment" in key_lower:
                    row["Acknowledgments"] = value

        if any(v != "N/A" for v in row.values()):
            data_rows.append(row)

    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data_rows)


# Exemplo de uso
input_file = "answers/full_csv.txt"
output_file = "SBQ_CSV.csv"
process_text_to_csv(input_file, output_file)
