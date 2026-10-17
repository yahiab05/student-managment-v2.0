-- MySQL dump 10.13  Distrib 8.0.36, for Linux (x86_64)
--
-- Host: localhost    Database: darcoran
-- ------------------------------------------------------
-- Server version	8.0.46-0ubuntu0.24.04.4

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `classeleve`
--
-- Create the database and use it
--
create database if not exists `darcoran` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */;
use `darcoran`;

DROP TABLE IF EXISTS `classeleve`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `classeleve` (
  `id` int NOT NULL AUTO_INCREMENT,
  `student_id` int DEFAULT NULL,
  `class_name` varchar(255) DEFAULT NULL,
  `user` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `student_id` (`student_id`),
  KEY `class_name` (`class_name`),
  KEY `ix_classeleve_id` (`id`),
  CONSTRAINT `classeleve_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `students` (`id`) ON DELETE CASCADE,
  CONSTRAINT `classeleve_ibfk_2` FOREIGN KEY (`class_name`) REFERENCES `classes` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `classes`
--

DROP TABLE IF EXISTS `classes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `classes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `way` varchar(255) NOT NULL,
  `teacher` varchar(255) NOT NULL,
  `note` varchar(255) NOT NULL,
  `price` float NOT NULL,
  `user` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_classes_name` (`name`),
  KEY `ix_classes_id` (`id`),
  KEY `fk_classes_teacher` (`teacher`),
  KEY `fk_classes_way` (`way`),
  CONSTRAINT `fk_classes_teacher` FOREIGN KEY (`teacher`) REFERENCES `teachers` (`name`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_classes_way` FOREIGN KEY (`way`) REFERENCES `settings` (`way_teaching`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `entery`
--

DROP TABLE IF EXISTS `entery`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `entery` (
  `id` int NOT NULL AUTO_INCREMENT,
  `num_inscrit` int DEFAULT NULL,
  `name` varchar(255) NOT NULL,
  `bill_number` varchar(255) NOT NULL,
  `payment_date` date DEFAULT NULL,
  `addition_date` date NOT NULL,
  `way` varchar(255) NOT NULL,
  `type` varchar(255) NOT NULL,
  `code` int NOT NULL,
  `price` float NOT NULL,
  `note` varchar(255) DEFAULT NULL,
  `user` varchar(255) NOT NULL,
  `cheq_num` varchar(255) DEFAULT NULL,
  `classroom` varchar(255) DEFAULT NULL,
  `in_bank` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_entery_id` (`id`),
  KEY `fk_entery_code` (`code`),
  KEY `fk_entery_type` (`type`),
  KEY `fk_entery_way` (`way`),
  CONSTRAINT `fk_entery_code` FOREIGN KEY (`code`) REFERENCES `settings` (`entery_code`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_entery_type` FOREIGN KEY (`type`) REFERENCES `settings` (`entery`) ON UPDATE CASCADE,
  CONSTRAINT `fk_entery_way` FOREIGN KEY (`way`) REFERENCES `settings` (`way_payment`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `outmoney`
--

DROP TABLE IF EXISTS `outmoney`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `outmoney` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `bill_number` varchar(255) NOT NULL,
  `date` date NOT NULL,
  `price` float NOT NULL,
  `way` varchar(255) NOT NULL,
  `cheq_num` varchar(255) DEFAULT NULL,
  `note` varchar(255) NOT NULL,
  `code` int NOT NULL,
  `type` varchar(255) NOT NULL,
  `user` varchar(255) NOT NULL,
  `in_bank` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_outmoney_id` (`id`),
  KEY `fk_out_way` (`way`),
  KEY `fk_out_type` (`type`),
  KEY `fk_out_code` (`code`),
  CONSTRAINT `fk_out_code` FOREIGN KEY (`code`) REFERENCES `settings` (`out_code`),
  CONSTRAINT `fk_out_type` FOREIGN KEY (`type`) REFERENCES `settings` (`out_money`),
  CONSTRAINT `fk_out_way` FOREIGN KEY (`way`) REFERENCES `settings` (`way_payment`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `role`
--

DROP TABLE IF EXISTS `role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `role` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `classes` tinyint(1) NOT NULL,
  `students` tinyint(1) NOT NULL,
  `teachers` tinyint(1) NOT NULL,
  `payment` tinyint(1) NOT NULL,
  `money` tinyint(1) NOT NULL,
  `settings` tinyint(1) NOT NULL,
  `user` tinyint(1) NOT NULL,
  `payment_editting` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `ix_role_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `settings`
--

DROP TABLE IF EXISTS `settings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `settings` (
  `id` int NOT NULL AUTO_INCREMENT,
  `way_teaching` varchar(255) DEFAULT NULL,
  `entery` varchar(255) DEFAULT NULL,
  `entery_code` int DEFAULT NULL,
  `out_money` varchar(255) DEFAULT NULL,
  `out_code` int DEFAULT NULL,
  `way_payment` varchar(255) DEFAULT NULL,
  `fr` varchar(255) DEFAULT NULL,
  `user` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `way_teaching` (`way_teaching`),
  UNIQUE KEY `entery` (`entery`),
  UNIQUE KEY `entery_code` (`entery_code`),
  UNIQUE KEY `out_money` (`out_money`),
  UNIQUE KEY `out_code` (`out_code`),
  UNIQUE KEY `way_payment` (`way_payment`),
  UNIQUE KEY `fr` (`fr`),
  KEY `ix_settings_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `students`
--

DROP TABLE IF EXISTS `students`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `students` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `gender` varchar(255) NOT NULL,
  `birthday` date NOT NULL,
  `date_inscrit` date NOT NULL,
  `parent` varchar(255) NOT NULL,
  `cin` int NOT NULL,
  `activity` varchar(255) NOT NULL,
  `num_tel` varchar(255) NOT NULL,
  `excused` varchar(255) NOT NULL,
  `note` varchar(255) NOT NULL,
  `user` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_students_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `students_history`
--

DROP TABLE IF EXISTS `students_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `students_history` (
  `id` int NOT NULL AUTO_INCREMENT,
  `num_inscrit` int DEFAULT NULL,
  `date_inscrit` date NOT NULL,
  `user` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `num_inscrit` (`num_inscrit`),
  KEY `ix_students_history_id` (`id`),
  CONSTRAINT `students_history_ibfk_1` FOREIGN KEY (`num_inscrit`) REFERENCES `students` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `teachers`
--

DROP TABLE IF EXISTS `teachers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `teachers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `date_inscrit` date NOT NULL,
  `birthday` date NOT NULL,
  `phone` varchar(255) NOT NULL,
  `note` varchar(255) NOT NULL,
  `user` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `ix_teachers_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `teachershistory`
--

DROP TABLE IF EXISTS `teachershistory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `teachershistory` (
  `id` int NOT NULL AUTO_INCREMENT,
  `teacher_id` int DEFAULT NULL,
  `date_inscrit` date NOT NULL,
  `user` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_teachershistory_id` (`id`),
  KEY `teachershistory_ibfk_1` (`teacher_id`),
  CONSTRAINT `teachershistory_ibfk_1` FOREIGN KEY (`teacher_id`) REFERENCES `teachers` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `transfer`
--

DROP TABLE IF EXISTS `transfer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transfer` (
  `id` int NOT NULL AUTO_INCREMENT,
  `price` float NOT NULL,
  `origin` varchar(255) NOT NULL,
  `destination` varchar(255) NOT NULL,
  `date` date NOT NULL,
  `note` varchar(255) NOT NULL,
  `user` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_transfer_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role_name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  KEY `role_name` (`role_name`),
  KEY `ix_users_id` (`id`),
  CONSTRAINT `users_ibfk_1` FOREIGN KEY (`role_name`) REFERENCES `role` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-09-29 21:13:03
