-- MySQL dump 10.13  Distrib 8.0.36, for Linux (x86_64)
--
-- Host: localhost    Database: test
-- ------------------------------------------------------
-- Server version	8.0.36-0ubuntu0.22.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `packages`
--

DROP TABLE IF EXISTS `packages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `packages` (
  `package_id` int NOT NULL AUTO_INCREMENT,
  `package_title` varchar(100) NOT NULL,
  `package_price` int NOT NULL,
  `package_occupancy` enum('Single','Double') NOT NULL,
  `package_duration` enum('One-day','Two-day','Non-Residential') NOT NULL DEFAULT 'Non-Residential',
  PRIMARY KEY (`package_id`),
  KEY `ix_packages_package_id` (`package_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `packages`
--

LOCK TABLES `packages` WRITE;
/*!40000 ALTER TABLE `packages` DISABLE KEYS */;
INSERT INTO `packages` VALUES (1,'Non-Residential Package',14000,'Single','Non-Residential'),(2,'Non-Residential Package',26000,'Double','Non-Residential'),(3,'Residential Package',27000,'Single','One-day'),(4,'Residential Package',39000,'Single','Two-day'),(5,'Residential Package',23000,'Double','One-day'),(6,'Residential Package',31000,'Double','Two-day');
/*!40000 ALTER TABLE `packages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sessions`
--

DROP TABLE IF EXISTS `sessions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sessions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_phone` varchar(10) DEFAULT NULL,
  `session_number` int DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_sessions_user_phone` (`user_phone`),
  KEY `ix_sessions_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sessions`
--

LOCK TABLES `sessions` WRITE;
/*!40000 ALTER TABLE `sessions` DISABLE KEYS */;
INSERT INTO `sessions` VALUES (12,'9353676794',3),(13,'9538755459',3);
/*!40000 ALTER TABLE `sessions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `user_honorific` enum('Dr','Mr','Mrs','Ms') NOT NULL,
  `user_first_name` varchar(100) DEFAULT NULL,
  `user_middle_name` varchar(100) DEFAULT NULL,
  `user_last_name` varchar(100) DEFAULT NULL,
  `user_email` varchar(255) NOT NULL,
  `user_phone` varchar(10) NOT NULL,
  `user_med_council_number` varchar(14) NOT NULL,
  `user_category` enum('Delegate','Faculty') NOT NULL,
  `user_type` varchar(100) NOT NULL,
  `user_package_id` int DEFAULT NULL,
  `user_city` varchar(100) NOT NULL,
  `user_state_of_practice` varchar(100) NOT NULL,
  `user_payment_id` varchar(20) NOT NULL DEFAULT 'MOJO',
  `user_payment_status` enum('SUCCESS','FAILED','PENDING') DEFAULT 'PENDING',
  `user_registration_type` varchar(10) NOT NULL DEFAULT 'DEFAULT',
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `user_phone` (`user_phone`),
  KEY `ix_users_user_last_name` (`user_last_name`),
  KEY `ix_users_user_first_name` (`user_first_name`),
  KEY `ix_users_user_middle_name` (`user_middle_name`),
  KEY `ix_users_user_id` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=58 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (56,'Dr','Mohammed ','','Faisal','mohammedfaisal3366@gmail.com','9353676794','NA','Delegate','Embryologist',2,'Tumkur','Haryana','MOJO4321H05A03946299','SUCCESS','DEFAULT'),(57,'Mr','Mohammed','Ahmed ','Pasha ','ahmedgiti@gmail.com','9538755459','Lm123','Delegate','Embryologist',1,'Bengaluru ','Karnataka','MOJO4321A05A03946300','SUCCESS','DEFAULT');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-04-23 19:44:42
