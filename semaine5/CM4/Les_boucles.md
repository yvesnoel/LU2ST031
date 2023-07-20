# Les boucles

Un des intérêts majeurs des languages informatiques tels que Python est de réaliser des tâches répétitives et fastidieuses pour les humains.

On appelle **boucler** une action la répéter plusieurs fois. L'objectif de ce cours est de se familiariser avec les différents moyens pour réaliser des boucles en python.

## Boucle While

**A DISCUTER : 
Problème, ce cours devrait être après les branchements: en commun, bloc instruction + conditions.
Ne pas oublier de parler des 4 espaces vs tabulation
break plus facile a expliquer si if est déjà introduit**

Commençons par une opération très répétitive à faire à la main. Nous allons afficher tous les nombres pairs de 0 à 20:

```
x = 1
print(x*0)
print(x*1)
print(x*2)
print(x*3)
print(x*4)
print(x*5)
print(x*6)
print(x*7)
print(x*8)
print(x*9)
print(x*10)
```

Ce code est valide mais il n'est pas pratique. Il est répétitif et difficile à modifier. Le mot clé `while` ("tant que" en anglais) est le premier mot clé que nous allons apprendre pour répéter une action en boucle. `while` permet de répéter une action tant qu'une condition n'est pas remplie. La syntaxe est la suivante:

```
while condition:
    # instruction 1
    # instruction 2
```

On commence par le mot clé while suivi d'une condition à remplir, généralement un test **(cf. branchement? ou Les expressions booléennes)**, puis de deux points, obligatoires (s'ils manquent, une erreur est renvoyée). 

Voici un exemple d'utilisation du while pour résoudre le problème ci dessus:

```
x = 0  # On créé une variable x qui vaut 0

while x =! 20:  # tant que x est différent de 20, répéter le bloc ci-dessous
    print(x)
    x += 2  # ajouter 2 à x
```

Les instructions sont répétées tant que `x =! 20` est vrai. Le résultat est exactement le même, mais le code est modifiable très aisément, et beaucoup plus court. Voici l'explication de ce code ligne par ligne:
1. On créé la variable x qui vaut 0.
2. On créé une boucle while: tant que x est différent de 20, on répète le bloc instruction.
3. Bloc d'instructions. C'est l'indentation qui permet d'indiquer le bloc. Ici le bloc consiste à afficher x, puis à lui ajouter 2. C'est cette instruction qui va "boucler", c'est à dire être répétée, jusqu'à ce que x soit égal à 20.

⚠️ L'indentation est le seul signe du bloc d'instructions. Dès que l'on veut sortir du bloc à répéter, il suffit d'écrire la ligne suivante sans indentation. Celle-ci n'est donc pas cosmétique: elle fait partie de la syntaxe. Par exemple, si on veut réinitialiser x à la fin:

```
x = 0

while x =! 20
    print(x)
    x = x + 2
    
x = 0 # x est remis à zéro après le bloc.
```

Le résultat est une répétition de la procédure: 20 fois, x va être affiché puis incrémenté (sa valeur va augmenter) de 2.

⚠️ Si la condition ne devient jamais fausse, on génère alors une boucle infinie. Il faut alors manuellement arrêter le script. C'est toujours au programmeur de vérifier que la condition va finir par devenir fausse. Ce type de bug ne provoque même pas de message d'erreur et peut être difficile à détecter.

💻 Essayez maintenant de modifier ce code pour afficher tous les multiples de 7 à la place.

## Boucles For

Une autre tâche répétitive est de parcourir tous les éléments d'une séquence et d'y appliquer la même action. Un objet est dit **itérable** s'il comporte plusieurs éléments et que l'on peut réaliser des actions sur chacun de ces élements. Nous avons vu précédemment les listes, qui sont des objets itérables. Mettons que l'on veuille réaliser une action sur chaque élement d'une' liste. Pour cela, un nouveau mot clé est indispensable: `for`.

Dans l'exemple ci-dessous, on a une liste de valeurs correspondant à des tailles d'ammonites en centimètres. Nous devons convertir ces valeurs en millimètres: 

```
liste_cm = [1.54,5.87,9.45,4.25]  # liste des valeurs en cm
liste_mm = []  # nouvelle liste à remplir

for i in liste_cm: # pour chaque élément de liste_cm appelé i
    liste_mm.append(i*10)  # on multiplie par 10 i et on l'ajoute à la nouvelle liste. Cette action se répéte pour chaque valeur i de liste_cm

print(liste_mm)  #affiche la nouvelle liste
```

Ce code ressemble beaucoup au while, avec son indentation qui distingue le bloc d'instructions. Cependant, le fonctionnement y est ici différent. `liste_cm` est la liste sur laquelle nous itérons. `for i in liste_cm` peut être traduit en : pour chaque élément dénoté `i` de `liste_cm`, réaliser le bloc d'instructions. Le code va répéter le bloc d'instructions pour chaque élément de la liste. A chaque itération, le nouvel élément courant de la liste prendra le nom `i` (`i` va donc changer à chaque boucle). C'est un outil puissant pour automatiser des actions à répéter!

```
liste_cm = [1.54,5.87,9.45,4.25]  # liste des valeurs en cm
liste_mm = []  # nouvelle liste à remplir

for i in liste_cm: # pour chaque élément de liste_cm appelé i
    liste_mm.append(i*10)  # on multiplie par 10 i et on l'ajoute à la nouvelle liste. Cette action se répéte pour chaque valeur i de liste_cm

print(liste_mm)  #affiche la nouvelle liste
```

⚠️ Il ne faut jamais modifier une liste lorsque l'on boucle dessus, car c'est une source majeure d'erreurs. Préférez toujours créer une nouvelle liste pour que les éléments de la liste ne soient pas modifiés et puissent continuer à être itérer.

A retenir: while sert à répéter une action jusqu'à ce qu'une condition ne soit plus satisfaite. for sert à répéter une action sur chaque élément d'une liste ou d'un autre objet itérable. En général, on utilise plutôt for quand on sait combien de fois il va falloir répéter le bloc d'instructions. Si ce nombre n'est pas connu, on se reporte vers while.

On utilise souvent une variable qui va servir de **compteur** et qui est notée `i` par convention. Mettons que l'on veuille reproduire une action dix fois. Il est possible d'utiliser un compteur avec while:

```
i = 0  # en règle générale, on compte à partir de zéro en python

while i =! 10:  # tant que i ne vaut pas dix, répéter
    print('infogeol')
    i += 1  # incrémenter le compteur de 1
```

Il est également possible d'utiliser l'instruction `range` pour générer une suite de nombres, ce qui est très utile pour itérer sans avoir de liste. Cette instruction s’utilise de la manière suivante :

`range(start, stop, step)`

Ce qui créé une suite de nombres allant de start (inclus) à stop (exclu) avec un pas de step (cet argument est optionnel). `range(0,1000)` permet de générer tous les nombres de 0 à 999. Il est possible d'utiliser ce résultat directement dans une boucle `for`. Par exemple, si l'on souhaite afficher dix fois un texte:

```
for i in range(0,10): # pour chaque élément i de 0 à 9
    print('infogeol') # bloc d'instructions
```

i va prendre toutes les valeurs de 0 à 9. Il peut être utilisé mais ce n'est pas le cas ici, car on souhaite uniquement répéter le même élément à chaque fois.

💻 Essayez maintenant d'afficher tous les résultats de la table de 8 en utilisant `for` et `range`.

## 🚀 Pour aller plus loin: listes en intension

Reprenons l'exemple:


```
liste_cm = [1.54,5.87,9.45,4.25]  # liste des valeurs en cm
liste_mm = []  # nouvelle liste à remplir

for i in liste_cm: # pour chaque élément de liste_cm appelé i
    liste_mm.append(i*10)  # on multiplie par 10 i et on l'ajoute à la nouvelle liste. Cette action se répéte pour chaque valeur i de liste_cm

print(liste_mm)  #affiche la nouvelle liste
```

Les listes en intension sont une forme encore plus puissante et synthétique de créer des listes:

```
liste_mm = [i*10 for i in liste_cm]
```

Ici, plus de bloc, la création de liste tient en une ligne, sans avoir à écrire toutes les valeurs. Il s'agit d'une **liste en intension**. Les listes en intension sont un moyen très efficace de transformer toute une liste. Il est possible par exemple de jouer avec les types:

```
liste_mm = [str(i*10) for i in liste_cm]
```

Et même de filtrer des éléments d'une liste en y ajoutant, de manière très intuitive, une condition:

```
liste_mm = [i*10 for i in liste_cm if i > 5]
```

est équivalent à:

```
for i in liste_cm: 
    if i > 5:  # on filtre les valeurs supérieures à 5
        liste_mm.append(i*10) 
```

# TP 2 : les boucles

Notions à connaître

- For
- While

## Exercice 1

Créer une boucle for qui affiche les multiples de 4 compris entre 1 et 20 (inclus).

## Exercice 2 : suite de Fibonacci

En mathématiques, la suite de Fibonacci est une suite d'entiers dans laquelle chaque terme est la somme des deux termes qui le précèdent. Elle commence généralement par les termes 0 et 1 (parfois 1 et 1) et ses premiers termes sont 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, etc.

Écrivez un script qui fournit la série de Fibonacci pour obtenir les valeurs des 20 premiers éléments de la suite.

## Exercices sup.

Toutes les "gammes" sur Moodle