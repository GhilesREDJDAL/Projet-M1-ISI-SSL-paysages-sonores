# Apprentissage de Représentations Audio par Auto-Supervision (IRCAM)

[cite_start]Ce projet de recherche explore l'utilisation du Self-Supervised Learning (SSL) pour l'analyse de paysages sonores[cite: 10, 11]. [cite_start]L'objectif est d'apprendre des représentations sémantiques riches à partir de larges bases de données non étiquetées, telles que des enregistrements continus en forêt tropicale guyanaise[cite: 10, 11].

## Répartition des tâches et Collaboration

Le projet a été structuré pour maximiser l'efficacité de la recherche en IA :

### Pôle IA et Apprentissage Auto-Supervisé (Mon rôle et Sébastien)
Nous avons géré le cœur algorithmique et l'entraînement des modèles :
- [cite_start]**État de l'art SSL** : Étude comparative des modèles de tokenisation audio comme Wav2Vec ou HuBERT et sélection de l'architecture WavTokenizer[cite: 10, 11].
- [cite_start]**Ingénierie des données** : Mise en place d'un pipeline complet comprenant la segmentation des fichiers audio, la conversion de formats et le nettoyage des données massives[cite: 10, 11].
- [cite_start]**Entraînement et Inférence** : Configuration et adaptation du modèle WavTokenizer sur des données naturelles malgré les contraintes matérielles[cite: 10, 11, 12].
- [cite_start]**Analyse de l'espace latent** : Utilisation d'algorithmes de clustering (K-means) pour regrouper les représentations apprises et identifier des structures sonores sans annotations préalables[cite: 10, 11].

### Pôle Interface et Visualisation (Amine Nait)
- [cite_start]Développement des outils d'affichage et de la partie dédiée à la présentation finale des résultats[cite: 10, 11].

## Expertise Technique en IA
- [cite_start]**Modèles de Fondation** : Compréhension des architectures de tokenisation neuronale pour transformer les signaux audio en jetons discrets[cite: 10, 11, 12].
- [cite_start]**SSL (Self-Supervised Learning)** : Capacité à exploiter des archives sonores sur plusieurs années sans étiquetage manuel[cite: 10, 11].
- [cite_start]**Frameworks et Outils** : Implémentation sous PyTorch et gestion de pipelines de données complexes[cite: 10, 11].

---
[cite_start]Note : Ce projet a été réalisé au sein du laboratoire STMS (IRCAM, CNRS, Sorbonne Université)[cite: 10, 11].
