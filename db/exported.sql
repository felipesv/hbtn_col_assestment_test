-- MySQL dump 10.13  Distrib 5.7.34, for Linux (x86_64)
--
-- Host: localhost    Database: orders
-- ------------------------------------------------------
-- Server version	5.7.34-0ubuntu0.18.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `orders` (
  `order_id` varchar(36) NOT NULL,
  `orders_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `orders_subtotal` int(11) NOT NULL,
  `orders_taxes` int(11) NOT NULL,
  `orders_total` int(11) NOT NULL,
  `orders_paid` tinyint(1) NOT NULL,
  `user_id` varchar(36) NOT NULL,
  PRIMARY KEY (`order_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders`
--

LOCK TABLES `orders` WRITE;
/*!40000 ALTER TABLE `orders` DISABLE KEYS */;
INSERT INTO `orders` VALUES ('2277265d-b37a-4535-bfee-9e408c34af09','2021-05-27 02:44:52',305,71,376,0,'4ada8124-9abd-4b3d-afbf-4a76c6165c8b'),('95bc4589-a1a5-4ab4-8f6d-57b39460a8ae','2021-05-27 02:44:57',500,92,592,0,'a1e62758-5690-43be-8b93-574c79babdb3'),('c9e8a8ce-11d6-4671-9919-caba0fe01ea6','2021-05-27 02:37:54',220,98,318,0,'9c596bdc-ff00-424e-b750-6e71a2e4211c'),('d4dc9fc4-3c30-4c7a-862c-9ce90aa7797f','2021-05-27 02:37:48',120,46,166,0,'dd0d5285-d116-4a2e-a62a-5e9c6ccf072c');
/*!40000 ALTER TABLE `orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payment`
--

DROP TABLE IF EXISTS `payment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `payment` (
  `payment_id` varchar(36) NOT NULL,
  `payment_type` enum('cash','credit card','bank check') NOT NULL,
  `payment_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `payment_txn_id` int(11) NOT NULL,
  `payment_total` int(11) NOT NULL,
  `payment_status` enum('ok','failed','process') NOT NULL,
  `order_id` varchar(36) NOT NULL,
  PRIMARY KEY (`payment_id`),
  KEY `order_id` (`order_id`),
  CONSTRAINT `payment_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`order_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payment`
--

LOCK TABLES `payment` WRITE;
/*!40000 ALTER TABLE `payment` DISABLE KEYS */;
INSERT INTO `payment` VALUES ('a2e9b491-54c6-441a-88fb-ac14ac75d017','bank check','2021-05-27 02:37:54',75878,383,'ok','c9e8a8ce-11d6-4671-9919-caba0fe01ea6'),('b1047d92-de12-439d-97b1-b723481446a9','credit card','2021-05-27 02:44:52',17507,507,'ok','2277265d-b37a-4535-bfee-9e408c34af09'),('d8ca4245-d6bf-420b-9deb-1008fd4400a5','cash','2021-05-27 02:37:48',84421,331,'ok','d4dc9fc4-3c30-4c7a-862c-9ce90aa7797f'),('f4efb051-036e-403a-9dd4-455c252cbf9e','credit card','2021-05-27 02:44:57',35845,661,'ok','95bc4589-a1a5-4ab4-8f6d-57b39460a8ae');
/*!40000 ALTER TABLE `payment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `shipping`
--

DROP TABLE IF EXISTS `shipping`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `shipping` (
  `shipping_id` varchar(36) NOT NULL,
  `shipping_address` varchar(60) NOT NULL,
  `shipping_city` varchar(15) NOT NULL,
  `shipping_state` varchar(15) NOT NULL,
  `shipping_country` varchar(20) NOT NULL,
  `shipping_cost` int(11) NOT NULL,
  `order_id` varchar(36) NOT NULL,
  PRIMARY KEY (`shipping_id`),
  KEY `order_id` (`order_id`),
  CONSTRAINT `shipping_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`order_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shipping`
--

LOCK TABLES `shipping` WRITE;
/*!40000 ALTER TABLE `shipping` DISABLE KEYS */;
INSERT INTO `shipping` VALUES ('203281cb-b42a-4d97-9043-65cf5e71aea2','Tvr 100 No. 12093742','New York','New York','United States',131,'2277265d-b37a-4535-bfee-9e408c34af09'),('58a58b3c-26e3-443f-a7e5-eb34d401ea35','Avenue 12 No. 011020127','San Francisco','California','United States',65,'c9e8a8ce-11d6-4671-9919-caba0fe01ea6'),('8689652f-55d2-4566-8b7f-1b0a232ef57d','St 45 No. 12243434233','Los Angeles','California','United States',165,'d4dc9fc4-3c30-4c7a-862c-9ce90aa7797f'),('ec399c0a-1fc7-413a-bb12-c909c5518ffb','St 62 No. 1292361','Boston','Massachusetts','United States',69,'95bc4589-a1a5-4ab4-8f6d-57b39460a8ae');
/*!40000 ALTER TABLE `shipping` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `user_id` varchar(36) NOT NULL,
  `user_name` varchar(50) NOT NULL,
  `user_last_name` varchar(50) NOT NULL,
  `user_gov_id` varchar(20) NOT NULL,
  `user_email` varchar(30) NOT NULL,
  `user_password` varchar(30) NOT NULL,
  `user_company` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `user_email` (`user_email`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES ('4ada8124-9abd-4b3d-afbf-4a76c6165c8b','Maxi','Tyler','8R7B3N3I5P7','max.tyler@xmail.com','123','Tesla'),('9c596bdc-ff00-424e-b750-6e71a2e4211c','Sara','Bush','5T3Y4U5H4I6','sara.bsh@xmail.com','123','Facebook'),('a1e62758-5690-43be-8b93-574c79babdb3','Jordan','Caicedo','4D391K3M49M','jordan.c@xmail.com','123','Tesla'),('dd0d5285-d116-4a2e-a62a-5e9c6ccf072c','Jhon','Doe','1F2G45J8K2','jhon.doe@xmail.com','123','Apple');
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

-- Dump completed on 2021-05-26 22:03:39
