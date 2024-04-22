
# Projet Python: Stratégies de gestion de flux à l'entrée 

# Téléchargement
  - Voici le lien de téléchargement:
  [Archive ZIP](https://github.com/uvsq22200574/Projet-IN407/raw/main/embed/Projet-IN407_2024_04_20.7z)

# Table des matières
  ## Partie 1
  - On considère un réseau de communication à commutation de paquets. Les paquets arrivant au réseau de transmission peuvent provenir de plusieurs sources en entrée de ce réseau (voir Figure 1). Si le taux d'arrivée (en bits/s) de ces paquets au réseau dépasse le taux de transmission du lien, alors les paquets sont stockés dans un buffer (ou file d'attente) noté B, avant d'être transmis sur le lien. Comme ce buffer est de capacité finie, notée C, si à l'arrivée d'un paquet le buffer est plein, ce paquet sera rejeté, c'est-à-dire perdu. On suppose que les paquets arrivent selon un processus de Poisson de paramètre λ.
  ![Figure1](embed/Figure%201.png)
  - L'objectif principal de ce projet est de développer une application qui permet de comparer les stratégies de gestion de flux à l'entrée d'un réseau de communication. Ce projet comporte deux parties.
  - Question1 ![](https://img.shields.io/badge/Status-half_completed-yellow) Les classes évoluent constamment c'est difficile de dire qu'elle sont terminées
  - Question2 ![](https://img.shields.io/badge/Status-completed-green)
  - Question3 ![](https://img.shields.io/badge/Status-completed-green) Il faut re-tester quand la classe Client sera modifiée/fusionnée.
  - Question4 ![](https://img.shields.io/badge/Status-completed-green)
  - Question5 ![](https://img.shields.io/badge/Status-completed-green)
  ## Partie 2
  - Pour limiter le nombre de paquets perdus, on associe à chaque source Si , i = 1, . . . N, un buffer Bi de capacité Ci dans lequel tous les paquets émis par la source Si sont préalablement stockés avant d'être acheminés vers la file d'attente B (voir Figure 2). On suppose que les paquets d'une source Si arrivent au buffer Bi selon un processus de Poisson de paramètre λi.
  ![Figure2](embed/Figure%202.png)
  - L'objectif de cette seconde partie du projet est de comparer les performances de plusieurs stratégies de traitement des paquets des différentes files d'attente. En effet, plusieurs stratégies peuvent être considérées, en terme du choix et de l'ordre de traitement des paquets des différentes files d'attente.
    - La file d'attente choisie est celle contenant le plus grand nombre de paquets.
    - Un paquet est pris de chaque file d'attente, à tour de rôle.
    - La file d'attente est choisie de manière aléatoire
  - Question1 ![](https://img.shields.io/badge/Status-todo-red) Hugo: Je me demande encore quelle approche prendre pour cette partie, modifer la classe Client et la rendre similaire à la classe Buffer, ou bien fusionner les classe Buffer et Client et les distinguer au sein de la classe. Il faut pouvoir créer des Clients et les associer à un Buffer. Chaque client possède son propre Buffer, donc quand on le vide, il faut envoyer les paquets. La seconde approche me parait être la plus intuitive, mais le code deviendrait lourd.
  - Question2 ![](https://img.shields.io/badge/Status-todo-red)
  - Question3 ![](https://img.shields.io/badge/Status-todo-red) Hugo: Il faudrait juste créer un Label pour afficher le packet actuel dans la Source et modifier la source du packet pour que le Buffer principal affiche cette source
  - Question4 ![](https://img.shields.io/badge/Status-todo-red) Hugo: Il faudrait récuperer le self.ratio de chaque Source et en faire une analyse sur le temps
  ## À faire
  - Ajouter des paramètres pour les fonctions de test (Rapide)
  - La classe Buffer devient la partie graphique, les classes Queue et Client représentent les classes demandées (Buffer et Source). Ces classes héritent de la partie graphique, les clients n'ont pas de pertes de packets donc pas de label associé, et le buffer principal n'a pas de packets restant à envoyer donc pas de label non plus. Il faut rajouter le packet "actuel", donc créer le label qui affiche le packet que les deux sont en train d'échanger(P2Q3).
  - Il faut les faire communiquer de sorte à ce que le buffer principal choisise le client, celui-ci envoie ses packets au buffer principal.
  - La vitesse du buffer principal détermine la vitesse de suppression des packets
  - Le choix se fait à partir des stratégies, donc le buffer principal choisit 1 client qui correspond au critère.
  - Il faut revoir les maximums des Scale, 1/8 peut devenir trop si la vitesse du lien n'est pas suffisante.
  - Il faut rajouter au Client un attribut temps d'attente, qui est augmenté de 1 à chaque cycle, et qui est remis à zéro dès qu'ils sont choisit
  - On peut faire ainsi une analyse en récupérant cet attribut pour chaque client.

# Contacts
  - Chargé de TD: perla.hajjar@sqy.fr
  - Chargé du Github: hugoassis.crh@protonmail.com
  - Collaborateurs : N/A
