#  Les expressions 
temps approximatif : 45min <br>
```{admonition} Objectifs
:class: hint
A l'issue de ce chapître, vous serez capable de :
- reconnaître le type d'une expression
- évaluer une expression comme le ferait Python en appliquant les règles de priorité
- traduire une expression mathématique relativement simple en une expression Python
```

## Qu'est ce qu'une expression Python ?
Une expression est un morceau de code qui est évalué par Python et dont l'interprétation donne une **valeur**. On parle d'expressions simples lorsqu'elles sont uniquement constituées d'une valeur. Les expressions complexes quant à elles combinent des valeurs, des opérateurs ou des fonctions (nous aborderons les fonctions plus tard dans le cours). 

## Affichage d'une expression
Lorsque Python interprète un code (ou une cellule d'un notebook), il affiche le resultat de la dernière expression du code. Dans la majorité des exemples de ce chapitre nous utilisons cette propriété pour visualiser le résultat de chaque expression en ne mettant qu'une seule expression par cellule. Dans le cas où l'on voudrait afficher le contenu de plusieurs expressions d'un même code ou cellule, on est obligé de passer par une fonction Python qui "imprime vers l'écran" (*print* en anglais) une valeur. Cette fonction est la fonction `print()`. Les 4 exemples à suivre illustrent ces subtilités à propos de l'affichage des valeurs issues d'une expression.


```python
123.456
```




    123.456




```python
print(123.456)
```

    123.456
    


```python
123.456
789
```




    789




```python
print(123.456)
print(789)
```

    123.456
    789
    

## Types de valeurs
### Les types de base
On peut distinguer plusieurs types de valeurs :

- Des nombres entiers (*integers* en anglais, `int` pour Python)


```python
1789
```




    1789



- Des nombres à virgule (`float` pour Python). Ces nombres sont appelés communément **flottants**.


```python
3.14159
```




    3.14159



```{admonition} Attention
:class: caution
En Python le séparateur décimal est un point (`.`) et non une virgule (`,`)
```

```{admonition} Remarque
:class: note
Python lors de l'évaluation d'une expression ce ramenant à une valeur de type `float` (nombre à virgule), indiquera toujours au moins une décimale même si le nombre est un entier. C'est d'ailleurs de cette façon que l'on peut simplement déduire le type d'un nombre (`int` ou `float`)
```


```python
1789.0000000000
```




    1789.0



On peut utiliser la notation scientifique :


```python
12.345e-6
```




    1.2345e-05



- Du texte qu'on appellera chaine de caractères (*strings* en anglais, `str` pour Python)

```{note}
Les caractères qui forment une chaîne de caractères sont entourrés par des apostrophes (`'`) ou des guillemets (`"`). Ceci est nécessaire à Python pour que l'interpréteur reconnaisse l'expression comme une chaine.
```


```python
'Hello !'
```




    'Hello !'




```python
"Hello !"
```




    'Hello !'



Lorsqu'une chaine de catactères contient un `'` ou un `"`, Il suffit d'utiliser l'autre symbole pour encadrer l'expression.


```python
'Il a dit "Bonjour!".'
```




    'Il a dit "Bonjour!".'




```python
"C'est moi"
```




    "C'est moi"



Ou encore "protéger" le symbole en le faisant précéder d'un `\`


```python
'C\'est toi'
```




    "C'est toi"



- Une valeur booléenne (*boolean* en anglais et `bool` en Python)


```python
True
```




    True



Les valeurs booléennes ne peuvent prendre que 2 valeurs : 
- vrai : `True`
- faux : `False`
. Nous reviendrons plus tard sur ce type de valeur.
```{admonition} Attention
:class: caution
Pour que Python reconnaisse bien les valeurs booléennes `True` et `False`, il ne faut pas oublier qu'elles commencent par une majuscule (C'est à dire que `true` est incorrect)
```

### Récupérer le type d'une valeur
Il est possible de connaître le type de la valeur issue d'une expression en utilisant la fonction `type`. Nous reviendrons plus tard dans le cours sur la notion de fonction.


```python
type('Coucou. Comment ça va ?')
```




    str




```python
type(1789.0000)
```




    float



### Conversion de type
Il est possible de changer le type d'une valeur en utilisant les fonctions `int()` `float()` `bool()` `str()`.


```python
int(-34.56)
```




    -34




```python
float(1789)
```




    1789.0




```python
bool(0)
```




    False




```python
str(12.3)
```




    '12.3'



## Les expressions complexes
Dans tous les exemples ci-dessus, nous avions à faire à des expressions simples mais il est aussi possible de construire des expressions plus complexes qui contiennent des opérations. Ces opérations s'appuient en général sur 2 valeurs (on parle d'opérateurs binaires) ou parfois un seule valeur (opérateur unaire). Les valeurs sur lesquelles s'appuie l'opérateur pour calculer l'opération, s'appellent des opérandes.

Evidemment, la ou les opérandes peuvent être de types variés. La valeur du résultat de l'opération peut aussi être de type variés.

### Les expressions numériques 
Vous avez déjà l'habitude d'utiliser votre calculatrice pour effectuer des opérations sur des nombres, voici la liste des opérations connues de python :

|Symbole | Description   |
| :----: | :-----------: |
| \+     | addition      |
| \-     | soustraction  |
| \*     |multiplicaction|
| \/     |division       |
| \/\/   |division entière|
| % | modulo|
| ** | puissance |

```{admonition} Remarque
:class: note
Dans tous les cas (sauf pour la division) si les deux opérandes sont de type entier (`int`), alors le résultat sera de type entier mais si l'un des deux opérandes est de type flottant (`float`) alors le résultat sera de type flottant. La division (`/`) est une exception : même si les deux opérandes sont des entiers, le résultat sera toujours de type flottant.
```

##### Exemples d'expressions utilisant des opérateurs numériques
- une addition avec 2 entiers donne un entier


```python
2 + 3
```




    5



- une division simple avec 2 entiers donne quand même un flottant


```python
8 / 4
```




    2.0



- une division entière avec 2 entiers donne un entier


```python
8 // 4
```




    2



- une division entière avec au moins un flottant donne un flottant (même si ce nombre est une valeur entière il est codé comme étant de type flottant)


```python
8.4 // 4
```




    2.0



- une opération avec un entier et un flottant donne un flotant (sauf pour la division simple).


```python
4 * 3.0
```




    12.0



- une opération avec un entier et un flottant donne un flotant (sauf pour la division simple).


```python
4**0.5
```




    2.0



- le modulo avec des entiers peut être vu comme le reste de la division entière.


```python
23 % 5
```




    3



- l'exemple ci-dessous qui fait appel à la division entière et au modulo et peut s'expliquer de la manière suivante : $$5,55 = 4 \times 1,2 + 0,75 $$



```python
print(5.55 // 1.20)
print(5.55 % 1.20)
```

    4.0
    0.75
    

On pourrait l'illustrer par la situation suivante : "Je dispose de 5,55€, combien de croissants à 1,20 € l'unité, puis je acheter ? combien me restera-t-il ?". La réponse est : "Je peux acheter 4 croissants et il me restera 0,75€".

#### Les règles de priorité

Dans une expression num￩rique sans parenth￨se, la priorit￩ va d'abord sur les puissances puis sur multiplications et divisons, et enfin sur les additions et soustractions. Le parenth￨ses permettent d'indiquer pr￩cis￩ment comment une expression doit ￪tre calcul￩e.


```python
2 + 3 * 5
```




    17




```python
3 + 7 // 2
```




    6




```python
(3 + 7) // 2
```




    5




```python
2 * 3 ** 2 * 2
```




    36




```python
2 * (3 ** 2) * 2
```




    36



```{admonition} À vous de jouer
:class: seealso
Ecrire une expression sans parenthèse pour calculer $4^3+\frac{2}{4\times 3}$
```


```python
### SOLUTION
4**3 + 2/4/3
```




    64.16666666666667



```{admonition} Remarque
:class: note
Python n'intègre pas dans ses commandes de base les constantes et fonction mathématiques usuelles (à part `abs` pour la valeur absolue). Pour les utiliser il faut importer un module spécifique : le module math. Nous reviendrons plus loin dans ce cours sur les modules et la façon de les importer mais l'exemple ci-dessous vous permet d'ores et déjà de les utiliser.
```


```python
import math
print(math.sqrt(4))
print(math.factorial(4))
print(math.exp(-12.1))
print(math.log(23))
math.sin(math.pi/2)
```

    2.0
    24
    5.559513241650146e-06
    3.1354942159291497
    




    1.0



(L_expressionsBooleennes)=
### Les expressions booléennes 

#### Les opérateurs ayant pour résultat une valeur booléenne
| Symbole | Description |
| :---:| :--- |
| \> | strictement supérieur à|
| \>=|  supérieur ou égal à|
| <| strictement inférieur à|
| <=|  inférieur ou égal à|
| ==| égal à |
| !=| différent de |


```python
4 > 10
```




    False




```python
3 // 2 != 2 + 6 - 7
```




    False




```python
2*2 == 16**0.5
```




    True




```python
-3.5 / 1.3 <= 2.1 *3
```




    True



```{admonition} Remarque
:class: note
Les nombres flottants ne sont pas mémorisés avec une précision infinie. Ils sont mémorisés avec un certain nombre de décimales. Dans l'exemple ci-dessous, on peut s'en apercevoir.
```


```python
3.0 - 2.7
```




    0.2999999999999998



Du coup si on effectue la comparaison suivante le résultat ne sera pas celui auquel on aurait pu s'attendre :


```python
(3.0 - 2.7) == 0.3
```




    False



Ceci peut être généralisé pour tous les flottants : Il ne faut pas tester l'égalité stricte entre deux nombres flottants. Il faut tester leur égalité, à une certaine précision de la manière suivante :\
**`abs(flottant_1 - flottant_2) < precision`** \
Par exemple, si je veux tester si 3.0 -2.7 est égal à 0.3 à 10{sup}`-6` près il faut écrire :


```python
abs((3.0 - 2.7) -0.3) < 1e-6
```




    True



3.0 - 2.7 et 0.3 sont donc égaux à 10{sup}`-6` près

#### Les principaux opérateurs booléennes
Il existe plusieurs opérateurs, voici les principaux :
- `not` : `not` est un opérateur unaire. Le résultat de cet opérateur sur une valeur booléenne est le contraire de cette valeur. Le contraire de `True` est `False` et le contraire de `False` est `True`.
- `and` : fait un ET logique des booléens à gauche et droite du `and`
- `or` : fait un OU logique des booléens à gauche et droite du `or`

Soient a et b deux booléens. On peut résumer le comportement des ET et OU logiques dans le tableau suivant (appelé Table de vérité):
|   a   |   b   | a and b | a or b |
| :---  | ---   | ---     |   ---: |
| True  | True  |  True   |  True  |
| True  | False |  False  |  True  |
| False | True  |  False  |  True  |
| False | False |  False  |  False |


- une opération unaire sur une seule valeur booléenne (l'opérateur `not` donne le booléen contraire à celui de l'opérande)


```python
not False
```




    True



- Le "et logique" fait appel à deux valeurs booléennes et son résultat est une valeur booléenne. Nous verrons plus loin 


```python
True and False
```




    False



### Les chaînes de caractères

Les chaînes de caractères acceptent quelques opérateurs.
- `len` : Cette fonction donne la longueur, c'est à dire le nombre de caractères d'une chaîne


```python
len("Lorem ipsum")
```




    11



- `+` : Opérateur de concaténation. Il permet de "coller" 2 chaînes. 


```python
"Bonjour" + " à toutes et tous"
```




    'Bonjour à toutes et tous'



- `*` : Opérateur de répétition. Il permet de répéter la chaine qui le précède le nombre de fois qui sui l'étoile (nécessairement entier)


```python
print("hop" * 3)
print("Pom " * (3 + 2))
```

    hophophop
    Pom Pom Pom Pom Pom 
    

- `in` : Indique si une chaîne est incluse dans une autre. Il existe aussi `not in`.


```python
print("tout" in "Bonjour à toutes et tous")
print( "ph" in "hop"*3)
print("sorbonne" not in "Sorbonne Université")
```

    True
    True
    True
    

```{admonition} À vous de jouer
:class: seealso
Ecrire le code le plus court possible permettant d'afficher *hip hip hip hourra !*
```


```python
### SOLUTION
print('hip ' * 3 + 'hourra !')
```

    hip hip hip hourra !
    


```python

```
