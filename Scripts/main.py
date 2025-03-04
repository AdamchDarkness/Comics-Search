import os
import zipfile
import rarfile  # pip install rarfile
import fitz     # pip install PyMuPDF
from elasticsearch import Elasticsearch

# Configuration pour rarfile : Spécifiez le chemin vers UnRAR.exe sur Windows
rarfile.UNRAR_TOOL = r'UnRAR.exe'  # Mettez à jour ce chemin selon votre installation

# --- Fonctions d'extraction d'images ---
def extract_pdf_first_page(pdf_path, output_path):
    """Extrait la première page d'un PDF et la sauvegarde en PNG."""
    try:
        doc = fitz.open(pdf_path)
        if doc.page_count < 1:
            print(f"PDF sans pages : {pdf_path}")
            return False
        page = doc.load_page(0)
        pix = page.get_pixmap()
        pix.save(output_path)
        print(f"Image extraite de {pdf_path} sauvegardée sous {output_path}")
        return True
    except Exception as e:
        print(f"Erreur lors de l'extraction de {pdf_path} : {e}")
        return False

def extract_cbz_first_image(cbz_path, output_path):
    """Extrait la première image d'une archive CBZ et la sauvegarde."""
    try:
        with zipfile.ZipFile(cbz_path, 'r') as z:
            image_files = [f for f in z.namelist() if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            if not image_files:
                print(f"Aucune image trouvée dans {cbz_path}")
                return False
            image_files.sort()
            first_image = image_files[0]
            data = z.read(first_image)
            with open(output_path, 'wb') as f:
                f.write(data)
            print(f"Image extraite de {cbz_path} ({first_image}) sauvegardée sous {output_path}")
            return True
    except Exception as e:
        print(f"Erreur lors de l'extraction de {cbz_path} : {e}")
        return False

def extract_cbr_first_image(cbr_path, output_path):
    """Extrait la première image d'une archive CBR (RAR) et la sauvegarde."""
    try:
        with rarfile.RarFile(cbr_path, 'r') as r:
            image_files = [f for f in r.namelist() if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            if not image_files:
                print(f"Aucune image trouvée dans {cbr_path}")
                return False
            image_files.sort()
            first_image = image_files[0]
            data = r.read(first_image)
            with open(output_path, 'wb') as f:
                f.write(data)
            print(f"Image extraite de {cbr_path} ({first_image}) sauvegardée sous {output_path}")
            return True
    except Exception as e:
        print(f"Erreur lors de l'extraction de {cbr_path} : {e}")
        return False

# --- Fonction d'extraction des champs à partir du chemin ---
def get_fields_from_path(root_path, base_path):
    """
    Déduit à partir du chemin (root_path) relatif au dossier base_path :
      - maison_d_edition : premier sous-dossier,
      - saga             : deuxième sous-dossier,
      - run              : concaténation des troisième niveaux et suivants ou, s'il n'existe pas, la saga.
    """
    relative_dir = os.path.relpath(root_path, base_path)
    if relative_dir == ".":
        return "", "", ""
    
    subfolders = relative_dir.split(os.sep)
    
    if len(subfolders) >= 2:
        maison_d_edition = subfolders[0]
        saga = subfolders[1]
        run = "_".join(subfolders[2:]) if len(subfolders) >= 3 else saga
    elif len(subfolders) == 1:
        maison_d_edition = subfolders[0]
        saga = subfolders[0]
        run = subfolders[0]
    else:
        maison_d_edition = ""
        saga = ""
        run = ""
    
    return maison_d_edition, saga, run

# --- Connexion à Elasticsearch ---
username = "elastic"
password = "lOf0*vttz9GwK3yUJhU="

es = Elasticsearch(
    "https://localhost:9200",
    basic_auth=(username, password),
    verify_certs=False  # Pour tests uniquement; activez la vérification en production
)

index_name = "comics"

# --- Paramètres et dossier de travail ---
comics_dir = r"\\lord_of_adam\Comics Mangas Livre\Comics"
output_dir = os.path.join(comics_dir, "extracted_covers")
os.makedirs(output_dir, exist_ok=True)
valid_ext = {".pdf", ".cbz", ".cbr"}

def main():
    doc_count = 0

    # Parcours récursif du dossier comics (en excluant le dossier extracted_covers)
    for root, dirs, files in os.walk(comics_dir):
        if os.path.abspath(root) == os.path.abspath(output_dir):
            continue
        for file in files:
            name, ext = os.path.splitext(file)
            ext = ext.lower()
            if ext not in valid_ext:
                print(f"Format non supporté pour {file}")
                continue

            file_path = os.path.join(root, file)
            # Chemin relatif pour indexer le champ "path"
            relative_file_path = os.path.relpath(file_path, comics_dir)
            
            # Chemin de sortie pour l'image extraite
            cover_filename = f"{name}.png"
            cover_path = os.path.join(output_dir, cover_filename)
            
            if os.path.exists(cover_path):
                print(f"L'image {cover_path} existe déjà, extraction ignorée.")
            else:
                success = False
                if ext == ".pdf":
                    print(f"Traitement PDF : {file_path}")
                    success = extract_pdf_first_page(file_path, cover_path)
                elif ext == ".cbz":
                    print(f"Traitement CBZ : {file_path}")
                    success = extract_cbz_first_image(file_path, cover_path)
                elif ext == ".cbr":
                    print(f"Traitement CBR : {file_path}")
                    success = extract_cbr_first_image(file_path, cover_path)
                
                if not success or not os.path.exists(cover_path):
                    print(f"Échec de l'extraction de l'image pour {file_path}, document non indexé.")
                    continue
            
            maison_d_edition, saga, run_field = get_fields_from_path(root, comics_dir)
            if not run_field:
                run_field = saga
            
            doc = {
                "nom": name,
                "path": relative_file_path,
                "extention": ext[1:],
                "maison_d_edition": maison_d_edition,
                "saga": saga,
                "run": run_field,
                "cover_path": cover_path
            }
            
            try:
                res = es.index(index=index_name, document=doc)
                print(f"Document indexé: {doc} (ID: {res['_id']})")
                doc_count += 1
            except Exception as e:
                print(f"Erreur lors de l'indexation de {file_path} : {e}")

    print(f"Nombre total de documents indexés: {doc_count}")

if __name__ == "__main__":
    main()
