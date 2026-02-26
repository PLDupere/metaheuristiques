from zipfile import ZipFile
import requests


def generate_dictionary():
    """Fonction qui va chercher un dictionnaire sur le web et effectue un prétraitement pour 
    retourner un dictionnaire utilisable pour votre TP.
    
    ATTENTION: ne l'utilisez pas tel-quel pour vérifier l'existence d'un mot car ce sera trop lent!.

    Returns:
        list: un "dictionnaire" de mots uniques trié.
    """
    lexique_url = "http://www.lexique.org/databases/Lexique383/Lexique383.zip"

    try:
        req = requests.get(lexique_url)
    except requests.RequestException as e:
        print(e)
        exit() # ou probablement un return e serait mieux...

    try:
        open(r"lexique\Lexique383.zip", "wb").write(req.content)
    except Exception as e:
        print(e)
        exit() # ou probablement un return e serait mieux

    with ZipFile(r"lexique\Lexique383.zip") as zf:
        zf.extract("Lexique383.tsv", path=r"lexique")

    # j'aurais aimé le mettre dedans, mais c'est fastidieux niveau encodage
    with open(r"lexique\Lexique383.tsv", mode="r", encoding="utf8") as f:
        f.readline()

        dictio = sorted(list(set([l.split()[0] for l in f.readlines()])))

    return dictio

