# Auteur : Ju-Heon HWANG 

# Date : 06/10/2025

## Tâches réalisées : 

On a repris les scénarios d’utilisation, et là j’ai vraiment senti que ça avançait.
Le fait de devoir détailler “pas à pas” comment l’utilisateur et le système interagissent m’a obligé à réfléchir à des aspects auxquels je ne pensais pas au début :

que faire si l’IA OCR échoue ?
comment gérer les doublons ?

En même temps, je réalisais à quel point Git pouvait devenir lent si on l’utilisait comme une vraie base de données.
Ça m’a fait réfléchir à la performance, et j’ai commencé à noter dans un coin les endroits où on pourrait se retrouver bloqués :

recherches dans des centaines (voire des milliers) d’œuvres, mises à jour répétées de dépôts,

vérification des métadonnées.

J’ai commencé à comprendre que le système devait être rapide, même si Git n’est pas fait pour ça.
C’est cette séance qui a posé les bases du choix d’un module d’indexation, pour éviter des parcours de dépôt trop fréquents.