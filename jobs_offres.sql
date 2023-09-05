-- Créer la base de données jobs_offres
CREATE DATABASE IF NOT EXISTS jobs_offres;

-- Utiliser la base de données jobs_offres
USE jobs_offres;

-- Créer la table annonce
CREATE TABLE IF NOT EXISTS annonce (
    `id` int NOT NULL AUTO_INCREMENT,
  `titre` varchar(255) NOT NULL,
  `metier` varchar(100) DEFAULT NULL,
  `pays` varchar(50) DEFAULT NULL,
  `ville` varchar(100) DEFAULT NULL,
  `type_contrat` varchar(50) DEFAULT NULL,
  `experience` int DEFAULT NULL,
  `diplome` varchar(100) DEFAULT NULL,
  `nom_entreprise` varchar(255) DEFAULT NULL,
  `skills` text,
  `description` text,
  `url` varchar(255) DEFAULT NULL,
  `date_offre` date DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;