
# Projet Python: Stratégies de gestion de flux à l'entrée 

# Table des matières
  ## Partie 1
  - On considère un réseau de communication à commutation de paquets. Les paquets arrivant au réseau de transmission peuvent provenir de plusieurs sources en entrée de ce réseau (voir Figure 1). Si le taux d'arrivée (en bits/s) de ces paquets au réseau dépasse le taux de transmission du lien, alors les paquets sont stockés dans un buffer (ou file d'attente) noté B, avant d'être transmis sur le lien. Comme ce buffer est de capacité finie, notée C, si à l'arrivée d'un paquet le buffer est plein, ce paquet sera rejeté, c'est-à-dire perdu. On suppose que les paquets arrivent selon un processus de Poisson de paramètre λ.
  ![Figure1](embed/Figure%201.png)
  - L'objectif principal de ce projet est de développer une application qui permet de comparer les stratégies de gestion de flux à l'entrée d'un réseau de communication. Ce projet comporte deux parties.
  - Question1 ![](https://img.shields.io/badge/Status-half_completed-yellow) Les classes évoluent constamment c'est difficile de dire qu'elle sont terminées
  - Question2 ![](https://img.shields.io/badge/Status-half_completed-yellow) La surcharge à été effectuée mais nécessite des tests (Rapide)
  - Question3 ![](https://img.shields.io/badge/Status-to_redo-purple) Puisque le code est "ancient", il faut le revoir et le tester (Rapide)
  - Question4 ![](https://img.shields.io/badge/Status-completed-green)
  - Question5 ![](https://img.shields.io/badge/Status-completed-green)
  ## Partie 2
  - Pour limiter le nombre de paquets perdus, on associe à chaque source Si , i = 1, . . . N, un buffer Bi de capacité Ci dans lequel tous les paquets émis par la source Si sont préalablement stockés avant d'être acheminés vers la file d'attente B (voir Figure 2). On suppose que les paquets d'une source Si arrivent au buffer Bi selon un processus de Poisson de paramètre λi.
  ![Figure2](embed/Figure%202.png)
  - L'objectif de cette seconde partie du projet est de comparer les performances de plusieurs stratégies de traitement des paquets des différentes files d'attente. En effet, plusieurs stratégies peuvent être considérées, en terme du choix et de l'ordre de traitement des paquets des différentes files d'attente.
    - La file d'attente choisie est celle contenant le plus grand nombre de paquets.
    - Un paquet est pris de chaque file d'attente, à tour de rôle.
    - La file d'attente est choisie de manière aléatoire
  - Question1 ![](https://img.shields.io/badge/Status-todo-red) Hugo: Je me demande encore quelle aproche prendre pour cette partie, modifer la classe Client et la rendre similaire à la classe Buffer, ou bien modifier la classe Buffer et lui intégrer un "type".
  - Question2 ![](https://img.shields.io/badge/Status-todo-red)
  - Question3 ![](https://img.shields.io/badge/Status-todo-red) Hugo: Il faudrait juste créer un Label pour afficher le packet actuel dans la Source et modifier la source du packet pour que le Buffer principal affiche cette source
  - Question4 ![](https://img.shields.io/badge/Status-todo-red) Hugo: Il faudrait récuperer le self.ratio de chaque Source et en faire une analyse sur le temps
  ## À faire
  - Separate the Client from the Buffer class
  - Rename the Buffer class to something else, as they are just containers for a progressbar and labels
  - Make Clients a custom widget that can be associated to the custom widget "Buffer"
  - Add radio buttons to choose the strategy of emptying
  - Add emptying strategy

# Contacts
  - Chargé de TD: perla.hajjar@sqy.fr
  - Chargé du Github: hugoassis.crh@protonmail.com
  - Collaborateurs : N/A
