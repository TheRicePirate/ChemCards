import os
from rdkit import Chem
from rdkit.Chem import Draw
from PIL import Image

def generate_2d_diagram(molecule_smile):
    mol = Chem.MolFromSmiles(molecule_smile)
    if mol:
        directory = os.path.join("Diagrams", "Temp")
        os.makedirs(directory, exist_ok=True)


        image_path = os.path.join(directory, "tempimg.png")
        image = Draw.MolToImage(mol)
        image.save(image_path)
        
        return image_path
    else:
        print(f"Invalid SMILES string: {molecule_smile}")
        return False
