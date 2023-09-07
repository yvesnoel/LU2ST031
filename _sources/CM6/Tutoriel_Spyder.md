# L'environnement de développement Spyder

```{admonition} Objectifs
:class: hint
A l'issue de ce chapitre, vous serez capable de : 
- installer Spyder quel que soit le système d'exploitation.

Vous serez également capable dans Spyder de :
- créer un script
- le sauvegarder
- l'exécuter ligne par ligne
- l'exécuter en entier
- lire et interpréter les informations de la console
- lire et interpréter les informations de l'explorateur de variables
```

### Spyder, qu'est-ce que c'est?

![](https://github.com/yvesnoel/LU2ST031/blob/master/docs/assets/css/upload_e406c51b9b8b63e00a4a99747902ebd6.png?raw=true)

Jusqu'à présent, nous avons écrit des scripts directement dans Moodle. Nous allons voir maintenant comment créer des scripts python (reconnaissables par leur extension en `.py`) pour vos futurs projets. On peut écrire un script Python de manière très simple en utilisant un logiciel de traitement de texte classique comme notepad, sublimetext, etc. puis de changer l'extension `.txt` en `.py`. Cependant, il existe des programmes puissants qui fournissent une assistance précieuse pour la programmation. Nous allons apprendre au cours des prochaines semaines à nous servir du programme **Spyder** pour aller plus loin, plus vite, et en évitant de nombreuses erreurs.

Spyder est ce qu'on appelle classiquement un environnement de développement intégré (ou IDE pour integrated development environment). Il s'agit d'un programme rassemblant un ensemble d'outils afin de faciliter l'écriture de code, notamment en simplifiant certaines tâches, en donnant un accès plus facile à la documentation, en affichant des alertes, en affichant un graphique directement après l'avoir appelé, etc. Un IDE se révèle rapidement indispensable pour toutes ces tâches. Spyder est un IDE open source spécifiquement concu pour Python et pour le domaine scientifique.

### Installation

Pour nous servir de Spyder, nous allons tout d'abord installer **Anaconda**, qui contient tout un ensemble d'outils pour programmer. Anaconda est gratuit, open source et contient directement Python (mais aussi le [langage R](https://fr.wikipedia.org/wiki/R_(langage))), Spyder, et permet de gérer librairies et dépendances plus facilement. 

Anaconda s'installe facilement sur Windows, MacOS et Linux. La procédure d'installation est décrite ci-dessous.


#### Pour Windows et MacOS

Télécharger l'installeur Anaconda disponible sur le site https://www.anaconda.com/.

![](https://github.com/yvesnoel/LU2ST031/blob/master/docs/assets/css/upload_daafe3904718621d360e937261984a3b.png?raw=true)

Cliquez sur le bouton `download` pour télécharger automatiquement l'installeur qui correspond à votre système d'exploitation (dans le cas contraire, cliquer sur `get additional Installers` en dessous du bouton `download` et choisissez la version qui correspond à votre système). Il suffit ensuite de lancer l'installeur téléchargé pour démarrer l'installation. 

Une fois l'installation terminée, l'application `Anaconda navigator` peut être executée comme n'importe quel autre programme (une icône est maintenant présente dans votre espace de travail ou dans un menu démarrer). Lancez `Anaconda navigator`. Lorsque le programme est ouvert, vous verrez l'icone de Spyder comme ci-dessous: 

![](https://github.com/yvesnoel/LU2ST031/blob/master/docs/assets/css/upload_407f7a64149e7ca4086d28ff5505bcbf.png?raw=true)

Cliquez sur le bouton `launch` sous l'icone Spyder pour le démarrer.

![](https://github.com/yvesnoel/LU2ST031/blob/master/docs/assets/css/upload_4c44144b84f5d31a3ade7da9a8060bc3.png?raw=true)

#### Pour Linux

Télécharger l'installeur Anaconda disponible sur le site https://www.anaconda.com/.

![](https://github.com/yvesnoel/LU2ST031/blob/master/docs/assets/css/upload_daafe3904718621d360e937261984a3b.png?raw=true)

Cliquez sur le bouton `download` pour télécharger automatiquement l'installeur qui correspond à votre système d'exploitation (dans le cas contraire, cliquer sur `get additional Installers` en dessous du bouton `download` et choisissez la version qui correspond à votre système).

Une fois téléchargé le fichier (celui-ci comporte l'extension `.sh`), vous devrez ouvrir le [terminal](https://doc.ubuntu-fr.org/terminal). Le terminal est une fenêtre dans laquelle il est possible de tapper des commandes puis de les exécuter avec Entrée. Pour ouvrir le terminal sur Ubuntu, vous pouvez:

* cliquer sur l'icone terminal (visible dans `Afficher les applications`):

![](https://github.com/yvesnoel/LU2ST031/blob/master/docs/assets/css/upload_bcaac57e555ef55d3669661e8e00cd55.png?raw=true)

* presser Ctrl+Alt+T en même temps.

et entrer l'instruction suivante:

`bash ~/Téléchargements/Anaconda3-2023.03-1-Linux-x86_64.sh`

(en remplaçant `Anaconda3-2023.03-1-Linux-x86_64.sh` par le nom du fichier `.sh` que vous venez de télécharger).

Au message `In order to continue the installation process, please review the license agreement` vous devez descendre tout en bas du texte à l'aide de la molette de la souris puis répondre `yes`. Vous devrez ensuite taper en toutes lettres `yes` et presser `Entrée` à la question suivante :

> Do you wish the installer to prepend the Anaconda3 install location
> to PATH in your /home/ec2-user/.bashrc ? [yes|no]

Une fois ceci fait, et après avoir redémarré l'ordinateur, il suffit d'ouvrir le terminal, de taper la commande `anaconda-navigator` et de la lancer en appuyant sur `Entrée`. Lorsque le programme est ouvert, vous verrez l'icone de Spyder comme ci-dessous: 

![](https://github.com/yvesnoel/LU2ST031/blob/master/docs/assets/css/upload_407f7a64149e7ca4086d28ff5505bcbf.png?raw=true)

Cliquez sur le bouton `launch` sous l'icone Spyder pour le démarrer.

![](https://github.com/yvesnoel/LU2ST031/blob/master/docs/assets/css/upload_4c44144b84f5d31a3ade7da9a8060bc3.png?raw=true)

### L'interface pas à pas

Vous devriez maintenant avoir Spyder sous les yeux. Vous remarquez immédiatement que l'interface graphique est assez complexe avec plusieurs panneaux : 

![](https://github.com/yvesnoel/LU2ST031/blob/master/docs/assets/css/upload_4ecc9dddfb4d3d064ed8b4062dda1673.png?raw=true)

La suite de cette partie va vous permettre de faire le tour de l'interface afin de commencer à prendre vos marques.

#### L'éditeur

Le panneau de gauche contient un éditeur de texte. Celui-ci sert à écrire du code, tout comme notepad ou n'importe quel autre éditeur. Ci-dessous, vous voyez que Spyder a généré un fichier temporaire temp.py dans lequel vous pouvez commencer a écrire. Vous pouvez également constater que le fichier n'est pas vide, il y a déjà des lignes:

![](https://github.com/yvesnoel/LU2ST031/blob/master/docs/assets/css/upload_0400d1184e92b5a45de26149ec9cd786.png?raw=true) 

La première ligne est la suivante:

```
# -*- coding: utf-8 -*-
```

Cette ligne est systématiquement ajoutée par défaut à n'importe quel script Spyder. Il s'agit d'une ligne spécifiant le type d'encodage (l'alphabet) utilisé pour coder. Spyder spécifie systématiquement l'encodage Utf-8 pour `Universal Character Set Transformation Format - 8 bits` qui est le standard actuel et qui inclus tous les caractères que vous pourriez utiliser. Je vous conseille de mettre cette ligne dans tous les scripts que vous produirez.

La seconde ligne est une chaîne de caractères:

```
"""
Spyder-Editor

This is a temporary script file
"""
```

Il s'agit tout simplement du "titre" de votre script, qu'il est utile de renseigner afin de donner des informations sur la fonction du script, la date, ou encore l'auteur. Tout ce qui est entre les deux triplets guillemets sera considéré comme faisant partie du titre.

Nous allons maintenant voir comment utiliser l'éditeur qui va se réveler beaucoup plus puissant qu'un éditeur classique. Commencez par créer un nouveau fichier en cliquant sur l'icone ![](https://github.com/yvesnoel/LU2ST031/blob/master/docs/assets/css/upload_5ad18019eb1f666020c32f6b622532e0.png?raw=true)

Maintenant, copiez le code suivant et collez le a la place du code généré automatiquement:

```
# -*- coding: utf-8 -*-
"""
Circulation thermohaline
"""

S2 = 34.8 # salinité dans l’Atlantique Nord en psu

V2 = 70*10^6 # # volume d'eau de l’Atlantique Nord en km

V2_apres = V2 + 0.5 # volume dans l'Atlantique Nord après décharge 
                    # d’un iceberg de 0.5 millions de km^3

# équilibre : S2 * V2 = S2_apres * V2_apres

S2_apres = (S2 * V2) / V2_apres # salinité dans l’Atlantique N. après décharge

print(S2_apres)
```

Ensuite, sauvegardez ce nouveau fichier à l'emplacement de votre choix en utilisant l'icone ![](https://github.com/yvesnoel/LU2ST031/blob/master/docs/assets/css/upload_3cea8e73159109370ee0f152ccf4eeff.png?raw=true) (vous pouvez également cliquer en haut à gauche sur l'onglet `File` puis `Save as`)


![](https://github.com/yvesnoel/LU2ST031/blob/master/docs/assets/css/upload_5a4903db6d036fc3edfda5b2f655d57e.png?raw=true)

Une fois le fichier sauvegardé, regardons le résultat:

![](https://github.com/yvesnoel/LU2ST031/blob/master/docs/assets/css/upload_2f1d15911027cb7dc65a90453f1b7a5a.png?raw=true)

Vous pouvez constater que certains mots sont dans une couleur particulière:
* en vert, les chaînes de caractères
* en jaune, les nombres
* en orange, les fonctions telles que `print`
* en grisé, les commentaires

Maintenant, essayez de supprimer la variable `V2_apres` de la ligne 12. Vous devriez voir apparaître ceci:

![](https://github.com/yvesnoel/LU2ST031/blob/master/docs/assets/css/upload_26e9a0bdc078f5ac86b46eabdefe3c17.png?raw=true)

Voila une première raison importante de l'utilité de Spyder. Celui-ci réalise une analyse de votre code en temps réel. Ici, ils vous indique avec un point rouge qu'il y a une erreur. Lorsque vous placez le curseur sur le point rouge, il vous indique le type d'erreur: ici, il s'agit d'une erreur de syntaxe. Normal, étant donné que la ligne se termine par le signe `/`.

Maintenant, après le signe `/`, ajoutez `V2_apres2`. 

![](https://github.com/yvesnoel/LU2ST031/blob/master/docs/assets/css/upload_66b3c08f25a106ace2406ea2b1c69ad9.png?raw=true)

Ici, Spyder vous alerte encore une fois. Nous avons oublié de définir `V2_apres2` avant de l'utiliser! Les points rouges ou les signes attention jaunes vous indiquent qu'il y a des erreurs dans votre script avant même de le lancer, ce qui fait gagner beaucoup de temps.

Corrigez l'erreur afin qu'il n'y ait plus de point rouge affiché. Maintenant qu'il n'y a plus d'erreur, nous voulons lancer notre script. Pour lancer le script entier, il suffit de cliquer sur ![](https://github.com/yvesnoel/LU2ST031/blob/master/docs/assets/css/upload_1060a5cddc2dd1577853aab597f3a81c.png?raw=true). Essayez.

Et voila! Le script a été exécuté. Maintenant, vous constatez qu'il faut que vous relanciez une ligne particulière. Cliquez sur la ligne de votre choix, par exemple la 8, puis cliquez sur ![](https://github.com/yvesnoel/LU2ST031/blob/master/docs/assets/css/upload_cfd9b64cd7e2af2fc2595120407d52ec.png?raw=true). Cette fois-ci, seule la ligne 8 a été exécutée.


#### Fenêtre d'aide et explorateur de variables


La fenêtre en haut à droite donne plusieurs informations utiles. Vous pouvez voir que cette fenêtre dispose de quatre onglets. Nous allons pour l'instant en voir deux, `Help` et `Variable Explorer`. 

##### Aide

Commencons par cliquer sur Help. Vous arrivez sur une page dans laquelle pouvez consulter l'aide concernant n'importe quel objet. Il suffit de taper un mot dans le champ à droite de `Object`. Essayez avec `print`: 

![](https://github.com/yvesnoel/LU2ST031/blob/master/docs/assets/css/upload_5e6071121a64d71accec38d823ca5a1a.png?raw=true)

Le champ Definition vous indique les arguments possibles. Type vous indique qu'il s'agit d'une fonction de base. Le texte en dessous indique à quoi sert cette fonction. Vous pouvez également voir l'aide directement dans l'interpréteur lorsque vous tapez un mot. Tapez `print()` dans l'éditeur de texte pour voir une infobulle apparaître.

##### Variable explorer

Cliquez maintenant sur Variable Explorer. Vous avez maintenant sous les yeux un tableau:

![](https://github.com/yvesnoel/LU2ST031/blob/master/docs/assets/css/upload_bc46a190bcfa139f92c74f85c20bec6b.png?raw=true)

Il s'agit de l'ensemble des variables actives. Au démarrage de Spyder, l'explorateur est vide. Puis, lorsque vous lancez des scripts, vous créez des variables avec une valeur. En lançant le script juste avant, vous avez notamment généré `S2` grâce à la ligne 6 `S2 = 34.8`. Vous constatez que cette variable est bien présente ici. Spyder vous indique qu'il s'agit d'une variable de type `float`, de taille 1 (pour les listes, la taille correspond par exemple au nombre d'éléments de la liste), et ayant pour valeur 34,8.

##### Files

Le troisième onglet que nous allons voir est Files. Il s'agit tout simplement de l'arborescence de vos fichiers.

![](https://github.com/yvesnoel/LU2ST031/blob/master/docs/assets/css/upload_a13c1ef4c9ed12904fdbebaa33b265a7.png?raw=true)

Vous pouvez cliquer sur les noms des fichiers pour les ouvrir directement dans l'éditeur de texte.

#### La console  

La dernière fenêtre que nous allons voir dans ce cours est la console, en bas à droite.

![](https://github.com/yvesnoel/LU2ST031/blob/master/docs/assets/css/upload_8eb574b119c4862a58f97893c04f7c4a.png?raw=true)

Il s'agit tout simplement de la console ou s'affichent les résultats du script. La ligne runfile indique que vous avez cliqué sur ![](https://github.com/yvesnoel/LU2ST031/blob/master/docs/assets/css/upload_1060a5cddc2dd1577853aab597f3a81c.png?raw=true) et écrit le nom du fichier exécuté. Vous pouvez voir en dessous un chiffre. Il s'agit du résultat du `print(S2_apres)` de la ligne 18 qui s'affiche ici.

Vous pouvez voir en haut à droite de cette fenêtre une icone poubelle ![](https://github.com/yvesnoel/LU2ST031/blob/master/docs/assets/css/upload_23016232041f42a3429416d5353f0b7f.png?raw=true). En cliquant dessus, vous remettez à zéro l'espace de travail en effaçant toutes les variables actives. Essayez de cliquer dessus, puis retournez à l'onglet `Variable Explorer` pour constater qu'il n'y a plus rien.

Vous pouvez également voir l'historique de tout ce que vous avez exécuté en cliquant sur l'onglet `History` en bas à droite:

![](https://github.com/yvesnoel/LU2ST031/blob/master/docs/assets/css/upload_6e30a19680ec0495fd34c1e18cf67d67.png?raw=true)