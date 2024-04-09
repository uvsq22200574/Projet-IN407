
# Projet Python: Stratégies de gestion de flux à l'entrée 

# Table des matières
  ## Partie 1
1. [Sujet](#sujet)
  - On considère un réseau de communication à commutation de paquets. Les paquets arrivant au réseau de transmission peuvent provenir de plusieurs sources en entrée de ce réseau (voir Figure 1). Si le taux d'arrivée (en bits/s) de ces paquets au réseau dépasse le taux de transmission du lien, alors les paquets sont stockés dans un buffer (ou file d'attente) noté B, avant d'être transmis sur le lien. Comme ce buffer est de capacité finie, notée C, si à l'arrivée d'un paquet le buffer est plein, ce paquet sera rejeté, c'est-à-dire perdu. On suppose que les paquets arrivent selon un processus de Poisson de paramètre λ.
  - ![Figure1](embed/Figure_1.png)
  - L'objectif principal de ce projet est de développer une application qui permet de comparer les stratégies de gestion de flux à l'entrée d'un réseau de communication. Ce projet comporte deux parties.
  ## Partie 2
  - Pour limiter le nombre de paquets perdus, on associe à chaque source Si , i = 1, . . . N, un buffer Bi de capacité Ci dans lequel tous les paquets émis par la source Si sont préalablement stockés avant d'être acheminés vers la file d'attente B (voir Figure 2). On suppose que les paquets d'une source Si arrivent au buffer Bi selon un processus de Poisson de paramètre λi.
  - ![Figure2](embed/Figure_2.png)
  - L'objectif de cette seconde partie du projet est de comparer les performances de plusieurs stratégies de traitement des paquets des différentes files d'attente. En effet, plusieurs stratégies peuvent être considérées, en terme du choix et de l'ordre de traitement des paquets des différentes files d'attente.
    - La file d'attente choisie est celle contenant le plus grand nombre de paquets.
    - Un paquet est pris de chaque file d'attente, à tour de rôle.
    - La file d'attente est choisie de manière aléatoire
2. [Questions](#questions)
    1. [Partie 1](#P1)
        1. [Question1](#Q1P1) ![](https://img.shields.io/badge/Status-completed-green)
        2. [Question2](#Q2P1) ![](https://img.shields.io/badge/Status-completed-green)
        3. [Question3](#Q3P1) ![](https://img.shields.io/badge/Status-completed-green)
        4. [Question4](#Q4P1) ![](https://img.shields.io/badge/Status-completed-red)
        5. [Question5](#Q5P1) ![](https://img.shields.io/badge/Status-completed-red)
    2. [Partie 2](#P2)
        1. [Question1](#Q1P2) ![](https://img.shields.io/badge/Status-completed-red)
        2. [Question2](#Q2P2) ![](https://img.shields.io/badge/Status-completed-red)
        3. [Question3](#Q3P2) ![](https://img.shields.io/badge/Status-completed-red)
        4. [Question4](#Q4P2) ![](https://img.shields.io/badge/Status-completed-red)

# Contacts
  - Chargé de TD: perla.hajjar@sqy.fr
  - Chargé du Github: hugoassis.crh@protonmail.com
  - Collaborateurs : N/A
