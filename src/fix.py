with open("src/predict.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if 'label = "POSITIVE" if probas[1] > 0.5 else "NEGATIVE"' in line or "label = 'POSITIVE' if probas[1] > 0.5 else 'NEGATIVE'" in line:
        indent = len(line) - len(line.lstrip())
        new_lines.append(" " * indent + "if score < 0.65:\n")
        new_lines.append(" " * (indent + 4) + "label = \"INDETERMINE\"\n")
        new_lines.append(" " * indent + "else:\n")
        new_lines.append(" " * (indent + 4) + line.lstrip())
    else:
        new_lines.append(line)

with open("src/predict.py", "w", encoding="utf-8") as f:
    f.writelines(new_lines)
print("Succes : src/predict.py mis a jour avec le seuil de 0.65 !")