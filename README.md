# Manuel utilisateur

## Description du projet

Ce projet a été fait dans le cadre de l'EC IHME (Interaction Homme-Machines Evoluées) qui est un cours de 5ème année de département ITI (Informatique et Technologie de l'Information) de l'INSA Rouen Normandie.

Le projet consiste en la conception d'un jeu du "Pierre Feuille Ciseaux" contre l'ordinateur dans lequel l'utilisateur interagit avec le programme via des gestes et des postures (pas besoin du clavier).

## Installation

Mettre à jour pip si besoin : `curl https://bootstrap.pypa.io/get-pip.py | python`

Installer virtualenv si besoin : `sudo pip3 install virtualenv`

Se placer à la racine du dépôt, et créer un environnement virtuel : `python3 -m venv venv`

Activer l'environnement virtuel : `source venv/bin/activate`

Installer les librairies nécessaires : `pip3 install -r requirements.txt`

Désactiver l'environnement virtuel : `deactivate`

Mettre à jour les librairies nécessaires : `pip freeze > requirements.txt`

## Lancer le programme

**Prérequis :**
- Vous devez posséder une webcam (si vous possédez plusieurs webcam, la webcam par défaut sera utilisée). 
- La webcam ne doit pas déjà être utilisée au lancement du programme.

Activer l'environnement virtuel : `source venv/bin/activate`

Pour lancer le programme à la racine du projet faire : `python3 run.py`

Le pseudo du joueur est demandé : entrez le pseudo via le clavier. Vous n'aurez désormais plus besoin du clavier.

Au lancement du programme, l'écran principal contenant la webcam s'affiche et vous invite à faire un geste de la main (gauche ou droite). 

Plusieurs options s'offrent à vous :

- **Lancer une partie :** Swipe de la gauche de l'écran vers la droite de l'écran.
- **Accéder aux statistiques :** Swipe du haut de l'écran vers le bas.
- **Quitter le programme :** Fermer la main.

**Remarque : **

Vous pouvez à tout moment :
- Appuyer sur la touche `d` pour activer ou désactiver l'affichage du squelette de la main.
- Appuyer sur la touche `q` pour quitter le programme.
  
## Fonctionnalités

### 1. Lancement d'une partie

Pour lancer une partie, effectuez un swipe de la gauche de l'écran vers la droite de l'écran.

Le programme demande le **nombre de rounds** de la partie : indiquez le nombre désiré (entre 1 et 5) à l'aide de vos doigts.

La partie se lance alors avec le 1er round.

Faites alors le **symbole** que vous souhaitez jouer (Pierre, Feuille ou Ciseaux) à l'aide d'une de vos mains.

Un symbole aléatoire est choisi par l'ordinateur : le vainqueur du round marque 1 point.

À la fin des rounds, celui qui a marqué le plus de points a gagné.

Les informations de la partie (coups joués, victoire/défaite, ...) sont enregistrées dans les statistiques.

### 2. Accès aux statistiques

Pour accéder aux statistiques, effectuez un swipe depuis l'écran principal du haut de l'écran vers le bas de l'écran.

Les statistiques s'affichent :
- 1ère colonne : **statistiques du joueur** ayant entré son pseudo au lancement du programme (nb de victoires, symboles les plus joués, ...)
- 2ème colonne : **statistiques du programme** (nb de parties, ...)
- 3ème colonne : **statistiques de l'ordinateur**  (nb de victoires, symboles les plus joués, ...)
  

Les statistiques restent affichées pendant une dizaines de secondes, puis disparaissent pour laisser de nouveau place à l'écran principal.

### 3. Fermeture du programme

Depuis l'écran principal il est possible de fermer le programme. Pour cela ouvrez grand l'une de vos mains, puis refermez-là.

## Troubleshooting

Il peut arriver que le programme ne détecte pas correctement vos gestes et postures. Le plus souvent, c'est que votre main n'est pas correctement détectée. 
Vous pouvez vérifier si votre main est correctement détectée en activant l'affichage du squelette de la main (touche `d`) :  les marqueurs doivent correctement se superposer à votre main, sans quoi il est normal que la reconnaissance ne fonctionne pas.

Si les marqueurs sont correctement placés mais que la reconnaissance ne fonctionne tout de même pas, suivez ces conseils :

- Ne montrez **qu'une seule main** à la caméra ;
- Placez-vous ni trop proche, ni trop loin de votre caméra ;
- Placez-vous dans des conditions de luminosité suffisante ;
- Limitez la complexité de l'arrière plan ;
- Votre main doit être de préférence paume face à la caméra.

Si toutefois les problèmes persistent, reportez-vous aux sections suivantes.

### Mauvaise reconnaissance du geste

Votre main (gauche ou droite) doit être de préférence paume face à la caméra.

Pour les swipes, essayez les conseils suivants :
- Votre main doit être de préférence ouverte ;
- Votre main ne doit pas sortir du cadre ;
- Le bas de votre paume doit être visible à tout instant ;
- Pour lancer la partie :
  - Partez bien du bord gauche vers le bord droit
  - Si le swipe de gauche à droite ne fonctionne vraiment pas, votre caméra est peut-être inversée : essayez de swiper de la droite vers la gauche.
- Pour accéder aux statistiques :
  - Ne partez pas trop proche du bord supérieur (votre main ne doit pas trop sortir du cadre pour être détectée)
  - Essayez de vous éloigner un peu

Pour quitter le programme, essayez le conseil suivant:
- Approchez-vous pour faire le geste


### Mauvaise reconnaissance du nombre de rounds

Essayez les conseils suivants :
- Votre main (gauche ou droite) doit être de préférence paume face à la caméra.
- Votre main doit être orientée doigts vers le haut.
- Le nombre de rounds ne peut-être compris qu'entre 1 inclus et 5 inclus 

*Remarque : pour les nombres inférieurs ou égaux à 4, ils peuvent être indiqués avec n'importe quelle combinaison de doigts.*

### Mauvaise reconnaissance du symbole

Conseils généraux :
- Votre main (gauche ou droite) doit être de préférence paume face à la caméra.
- Votre main doit être orientée de préférence doigts vers le haut.
  

Pour le symbole "Pierre", essayez le conseil suivant :
- Votre pouce ne doit de préférence pas être caché par vos autres doigts : placez-le sur votre index.

Pour le symbole "Ciseaux", essayez le conseil suivant :
- Votre annulaire et auriculaire doivent être correctement baissés (en revanche la position du pouce est libre)

Pour le symbole "Feuille", essayez le conseil suivant :
- Vos doigts ne doivent pas être écartés (à l'exception du pouce qui peut être collé ou non aux autres doigts)