
# Projet Python :Stratégies de gestion de flux à l’entrée 

# Table des matières
1. [Introduction](#introduction)
  - On considère un réseau de communication à commutation de paquets. Les paquets arrivant au réseau de transmission peuvent provenir de plusieurs sources en entrée de ce réseau (voir Figure 1). Si le taux d’arrivée (en bits/s) de ces paquets au réseau dépasse le taux de transmission du lien, alors les paquets sont stockés dans un buffer (ou file d’attente) noté B, avant d’être transmis sur le lien. Comme ce buffer est de capacité finie, notée C, si à l’arrivée d’un paquet le buffer est plein, ce paquet sera rejeté, c’est-à-dire perdu. On suppose que les paquets arrivent selon un processus de Poisson de paramètre λ.
  - L’objectif principal de ce projet est de développer une application qui permet de comparer les stratégies de gestion de flux à l’entrée d’un réseau de communication. Ce projet comporte deux parties.
2. [Contact](#paragraph1)
  - Chargé de TD: perla.hajjar@sqy.fr
  - Chargé du Github: hugoassis.crh@protonmail.com

## Screenshots  

![Figure 1](/embed/Figure 1.png)
