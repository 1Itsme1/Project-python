import hashlib
import chardet

def hash_file(input_file, output_file):
    try:
    
        with open(input_file, 'rb') as f:
            raw_data = f.read()
            detected_encoding = chardet.detect(raw_data)['encoding']

        print(f"Encodage détecté : {detected_encoding}")

   
        with open(input_file, 'r', encoding=detected_encoding, errors='ignore') as infile:
            with open(output_file, 'w', encoding='utf-8') as outfile:
                for line in infile:
                    line = line.strip()
                    if not line:
                        continue
                    hashed_line = hashlib.sha256(line.encode('utf-8')).hexdigest()
                    outfile.write(hashed_line + '\n')

        print(f"Le contenu du fichier {input_file} a été haché et sauvegardé dans {output_file}.")

    except FileNotFoundError:
        print(f"Erreur : Le fichier {input_file} est introuvable.")
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")


input_file = 'rockyou.txt'
output_file = 'rockyou-sha256.txt'

hash_file(input_file, output_file)
