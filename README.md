# Apprentissage de Représentations Audio par Auto-Supervision (IRCAM)

Ce projet de recherche explore l'utilisation du Self-Supervised Learning (SSL) pour l'analyse de paysages sonores. L'objectif est d'apprendre des représentations sémantiques riches à partir de larges bases de données non étiquetées, telles que des enregistrements continus en forêt tropicale guyanaise.

## Répartition des tâches et Collaboration

Le projet a été structuré pour maximiser l'efficacité de la recherche en IA :

### Pôle IA et Apprentissage Auto-Supervisé (Ghiles et Sébastien)
Nous avons géré le cœur algorithmique et l'entraînement des modèles :
- **État de l'art SSL** : Étude comparative des modèles de tokenisation audio comme Wav2Vec ou HuBERT et sélection de l'architecture WavTokenizer.
- **Ingénierie des données** : Mise en place d'un pipeline complet comprenant la segmentation des fichiers audio, la conversion de formats et le nettoyage des données massives.
- **Entraînement et Inférence** : Configuration et adaptation du modèle WavTokenizer sur des données naturelles malgré les contraintes matérielles.
- **Analyse de l'espace latent** : Utilisation d'algorithmes de clustering (K-means) pour regrouper les représentations apprises et identifier des structures sonores sans annotations préalables.

### Pôle Interface et Visualisation (Amine Nait)
- Développement des outils d'affichage et de la partie dédiée à la présentation finale des résultats.

## Expertise Technique en IA
- **Modèles de Fondation** : Compréhension des architectures de tokenisation neuronale pour transformer les signaux audio en jetons discrets.
- **SSL (Self-Supervised Learning)** : Capacité à exploiter des archives sonores sur plusieurs années sans étiquetage manuel.
- **Frameworks et Outils** : Implémentation sous PyTorch et gestion de pipelines de données complexes.
