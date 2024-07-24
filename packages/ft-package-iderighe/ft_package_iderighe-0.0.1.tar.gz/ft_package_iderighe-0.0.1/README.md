# GENERAL

README.md Contient des informations sur le package. Il sera affiché comme documentation
sur la page de notre package sur PyPI. On peut écrire n’importe quoi dans ce fichier.

# FT_PACKAGE_IDERIGHE

Ce package est un test de création de package. Pour ce test, ce package aura comme 
fonction de compter le nombre de lignes dans un texte.txt

# AU PREALABLE : CONSTRUIRE LE PACKAGE

 - pip install --upgrade build
 (- python3 -m build --sdist => NON : ne crée que ft_package-0.0.1.tar.gz)
 - python -m build -> crée ft_package-0.0.1.tar.gz ET ft_package-0.0.1-py3-none-any.whl
=> build installe le builder spécifié dans le fichier.toml
et l'utilisera ensuite pour construire une distribution sdist et wheel (fichier.whl)

Après ces deux commandes, on a ft_package-0.0.1.tar.gz ET ft_package-0.0.1-py3-none-any.whl

# AU PREALABLE : CREER UN COMPTE PERSO SUR PyPI

Récupérer un token pour l'API PyPI

# AU PREALABLE : PUBLIER LE PACKAGE SUR LA BIBLIO PYTHON PyPI

 - python3 -m pip install twine => installe twine
 - ajouter export PATH="$HOME/.local/bin:$PATH" dans le fichier .zshrc
 - source ~/.zshrc => recharge le fichier de config
 - twine upload dist/* => cancel le wallet KDE, puis entrer le token de l'API

A ce stade, notre package est dans la biblio online PyPI (Python Package Index)

# TELECHARGER LE PACKAGE

 - pip install ./dist/ft_package-0.0.1.tar.gz
 - pip install ./dist/ft_package-0.0.1-py3-none-any.whl
ATTENTION : les deux commandes doivent fonctionner

# VERIFICATION

 - pip list : pour voir si le package apparait dans les packages installés
 - pip show -v ft_package : display les caractéristique du package
