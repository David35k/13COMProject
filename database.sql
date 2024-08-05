-- MariaDB dump 10.19-11.3.2-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: OneBit
-- ------------------------------------------------------
-- Server version	11.3.2-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `commentLikes`
--

DROP TABLE IF EXISTS `commentLikes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `commentLikes` (
  `likeID` int(11) NOT NULL AUTO_INCREMENT,
  `commentID` int(11) DEFAULT NULL,
  `userID` int(11) DEFAULT NULL,
  PRIMARY KEY (`likeID`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `commentLikes`
--

LOCK TABLES `commentLikes` WRITE;
/*!40000 ALTER TABLE `commentLikes` DISABLE KEYS */;
INSERT INTO `commentLikes` VALUES
(5,15,28),
(7,13,28),
(9,11,28),
(12,7,28),
(16,17,28),
(17,16,28),
(19,16,25),
(20,6,25),
(21,5,25),
(23,15,25),
(24,18,28),
(25,20,28);
/*!40000 ALTER TABLE `commentLikes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comments`
--

DROP TABLE IF EXISTS `comments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `comments` (
  `commentID` int(11) NOT NULL AUTO_INCREMENT,
  `postID` int(11) DEFAULT NULL,
  `comment` text DEFAULT NULL,
  `time` datetime DEFAULT current_timestamp(),
  `userID` int(11) DEFAULT NULL,
  `likes` int(11) DEFAULT 0,
  PRIMARY KEY (`commentID`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comments`
--

LOCK TABLES `comments` WRITE;
/*!40000 ALTER TABLE `comments` DISABLE KEYS */;
INSERT INTO `comments` VALUES
(16,40,'test','2024-07-21 12:35:11',28,2),
(17,40,'yoyoyoyoyoy','2024-07-27 00:12:26',28,1),
(18,38,'yur','2024-07-27 00:31:57',28,1),
(19,40,'yur','2024-07-27 00:37:54',28,0),
(20,40,'epic comment bro','2024-07-27 00:45:13',28,1),
(21,40,'yo comment sorting works and they look epic 🔥🔥','2024-07-27 23:27:47',28,0);
/*!40000 ALTER TABLE `comments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `likes`
--

DROP TABLE IF EXISTS `likes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `likes` (
  `likeID` int(11) NOT NULL AUTO_INCREMENT,
  `userID` int(11) DEFAULT NULL,
  `postID` int(11) DEFAULT NULL,
  PRIMARY KEY (`likeID`)
) ENGINE=InnoDB AUTO_INCREMENT=142 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `likes`
--

LOCK TABLES `likes` WRITE;
/*!40000 ALTER TABLE `likes` DISABLE KEYS */;
INSERT INTO `likes` VALUES
(24,25,11),
(27,25,10),
(32,28,12),
(90,28,14),
(91,28,16),
(92,28,20),
(93,29,14),
(94,29,19),
(95,28,18),
(96,28,21),
(102,38,30),
(128,28,29),
(129,28,30),
(130,28,38),
(131,28,32),
(133,57,38),
(134,56,38),
(135,28,39),
(136,28,40),
(137,37,40),
(139,25,40),
(140,25,38),
(141,25,36);
/*!40000 ALTER TABLE `likes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `posts`
--

DROP TABLE IF EXISTS `posts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `posts` (
  `postID` int(11) NOT NULL AUTO_INCREMENT,
  `userID` int(11) DEFAULT NULL,
  `image` varchar(255) DEFAULT NULL,
  `description` text DEFAULT NULL,
  `title` varchar(40) DEFAULT NULL,
  `likes` int(11) DEFAULT 0,
  `time` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`postID`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `posts`
--

LOCK TABLES `posts` WRITE;
/*!40000 ALTER TABLE `posts` DISABLE KEYS */;
INSERT INTO `posts` VALUES
(28,28,'/static/images/postImages/84bef901-placeholder.png','epic','test',0,'2024-06-22 11:55:59'),
(30,28,'/static/images/postImages/48d6f653-epicDiagramDroneCOM.jpg','epic','test',2,'2024-06-22 12:14:47'),
(31,28,'/static/images/postImages/88e3703b-bro.jpg','ohio','sigma',0,'2024-07-02 10:27:23'),
(32,28,'/static/images/postImages/0f5507c6-placeholder.png','asdf','ohio',1,'2024-07-02 10:28:11'),
(34,28,'/static/images/postImages/9e9310f6-bro.jpg','','',0,'2024-07-06 11:36:39'),
(36,28,'/static/images/postImages/aace1f2e-placeholder.png','','asdfkadjfkasdjfkasdjfaksdsdjfaksdjfkaj',1,'2024-07-06 11:52:19'),
(38,28,'/static/images/postImages/33d63948-epicDiagramDroneCOM.jpg','epic super epic','epic post lawl',4,'2024-07-06 12:45:15'),
(40,28,'/static/images/postImages/912de48f-placeholder.png','only image i had','this is yet another test',3,'2024-07-16 09:39:14');
/*!40000 ALTER TABLE `posts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tags`
--

DROP TABLE IF EXISTS `tags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tags` (
  `tagID` int(11) NOT NULL AUTO_INCREMENT,
  `tag` varchar(25) DEFAULT NULL,
  `postID` int(11) DEFAULT NULL,
  PRIMARY KEY (`tagID`),
  KEY `postID` (`postID`)
) ENGINE=InnoDB AUTO_INCREMENT=96 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tags`
--

LOCK TABLES `tags` WRITE;
/*!40000 ALTER TABLE `tags` DISABLE KEYS */;
INSERT INTO `tags` VALUES
(33,'epic',21),
(34,'post',21),
(35,'epic',22),
(36,'post',22),
(37,'',23),
(38,'',24),
(39,'',25),
(40,'',26),
(41,'',27),
(51,'epic',28),
(52,'test',28),
(53,'post',28),
(54,'bruh',29),
(55,'sigma',30),
(56,'lawl',31),
(57,'',32),
(58,'ohio?',33),
(59,'',34),
(60,'',35),
(61,'',37),
(63,'',36),
(64,'pinkpantheress',39),
(65,'like please',39),
(66,'singer',39),
(67,'epic',39),
(77,'bruh',38),
(93,'test',40),
(94,'epic',40),
(95,'i love this website dude',40);
/*!40000 ALTER TABLE `tags` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `userID` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` char(64) DEFAULT NULL,
  `userName` varchar(30) NOT NULL,
  `image` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`userID`)
) ENGINE=InnoDB AUTO_INCREMENT=62 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES
(1,'David','davidtoman07@gmail.com','epicPassword','David35k',NULL),
(21,'Bob','bob@gma','bob123','BobIsCool123',NULL),
(22,'adsf','asdf@gmail.com','asdf','asdf',NULL),
(23,'test dude','testing@gmail.com','49a70bd1e731c8cd1f77a9b75803bad6453ea9c6bc1cbc5e32a1dd19aa5d31db','testing',NULL),
(24,'Miroslav','someone@gmail.com','9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08','Miro',NULL),
(25,'david','david@gamil.com','07d046d5fac12b3f82daf5035b9aae86db5adc8275ebfbf05ec83005a4a8ba3e','david',NULL),
(26,'Liam','balls@baller.st','0d45dbe12febe4ff7536c3736578bdef1eb3c76153dd27ed600b2906c53e0bb5','kurry',NULL),
(28,'epic name','test@gmail.com','9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08','test','/static/images/profilePictures/c21487ea-slay.jpg'),
(29,'david toman','epic@gmail.com','/static/images/profilePictures/6183b23f-bro.jpg','kay','/static/images/profilePictures/6a509ae7-seky911.png'),
(30,'not david','testing@gmail.com','cf80cd8aed482d5d1527d7dc72fceff84e6326592848447d2dc0b0e87dfc9a90','testing','/static/images/profilePictures/2364b661-ohio.png'),
(31,'another test','another@gmail.com','64320dd12e5c2caeac673b91454dac750c08ba333639d129671c2f58cb5d0ad1','another test','/static/images/profilePictures/5f41be2e-Vector.png'),
(32,'another test','another@gmail.com','64320dd12e5c2caeac673b91454dac750c08ba333639d129671c2f58cb5d0ad1','another test','/static/images/profilePictures/c3a6cdda-Vector.png'),
(33,'Pollen','test@gmail.com','63640264849a87c90356129d99ea165e37aa5fabc1fea46906df1a7ca50db492','polmarcuelo',NULL),
(36,'testing','buh@gmail.com','cf80cd8aed482d5d1527d7dc72fceff84e6326592848447d2dc0b0e87dfc9a90','testing','/static/images/profilePictures/0421d327-bro.jpg'),
(37,'bruh','bruh@gmail.com','408f31d86c6bf4a8aff4ea682ad002278f8cb39dc5f37b53d343e63a61f3cc4f','bruh','/static/images/profilePictures/492dd65b-placeholder.png'),
(38,'Pollen Marcuelo','pollywolly@gmail.com','ee4a4d2d0f10b5f8ac34888ffbb8ec1f638dff5cfdd01a6ae7e5d0e5488c46dc','pollywolly',NULL),
(39,'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa','','e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855','',NULL),
(40,'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa','aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa@gmail.com','ffe054fe7ae0cb6dc65c3af9b61d5209f439851db43d0ba5997337df154668eb','aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',NULL),
(41,'','','635361c48bb9eab14198e76ea8ab7f1a41685d6ad62aa9146d301d4f17eb0ae0','',NULL),
(42,'edging','edgind@gmail.com','635361c48bb9eab14198e76ea8ab7f1a41685d6ad62aa9146d301d4f17eb0ae0','edging',NULL),
(43,'adf','asdf@gmail.com','e5e9222b50fc559a766eb26a15088d1c4f203e43ee7ef2cfce378e9fe91b2241','asdf',NULL),
(44,'','','5fadcd7f9bca600c295e0f02e1bbc401a6ff2f4c60aac0e8e006b5f8c2b1230a','',NULL),
(45,'','','0347f2ea5ddb672b7d074a81a7d6210ba86b85b58df9e8c2511784a8f0d856dd','',NULL),
(46,'','aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa@gmail.com','e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855','',NULL),
(47,'aaaaaaaaaaaaaaaa','aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa@gmail.com','e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855','aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',NULL),
(48,'','','e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855','aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',NULL),
(49,'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa','','e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855','',NULL),
(50,'aaaaaaaaaaaaaaaaaaaaaaaaaaaaa','','d1ef49c8259ac69a50fcfd62a1188fa1ed5a61689e536b91e137aadc431349e5','','/static/images/profilePictures/4146b88e-epicDiagramDroneCOM.jpg'),
(51,'aa','aaa@gmail.com','b9151a591ca6de5de8f6c72f25dea2e36679e37a68817292560dc87dd9b9256c','aa','/static/images/profilePictures/34806183-bro.jpg'),
(52,'sigma','sigm@gmail.com','45ae2016afce607c91d180c55d776b2222844a49eb25b33d28e75e61c826a59f','sigma','/static/images/profilePictures/129f4642-bro.jpg'),
(53,'','','cb7e343a6e6437b104e25b23982eb4b6ff76dfaf610bf6a68cf0abd0b01d4821','',NULL),
(54,'','','e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855','',NULL),
(55,'','','e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855','',NULL),
(56,'David','davidtoman07@gmail.com','c01638541229aa5f6f5612627ad32bd4a108851b9402f83a29e524a6e048e757','kayyy','/static/images/profilePictures/8122393b-C771CB5A-DCD4-4604-B288-C06CC70D0D7C.jpeg'),
(57,'poop','elenatoman090@gmail.com','1cf4151f098060d5589953c4789325c04c172996bc61a181d9a96e1c1e069e5a','poop','/static/images/profilePictures/3c518a03-IMG_1667.JPG'),
(58,'legit doesnt matter what name','epic@gmail.com','c1bc9890f06a627ef11883093bee270e9bd891958e3607eb32dd8e35140530b3','test',NULL),
(59,'ohio','bruh@gmail.com','67ca751a1f5f723f719d07b3c9e027f93290d796693920cf6aa255ac2ed04754','bruh','/static/images/profilePictures/aa68233b-bro.jpg'),
(60,'ohio','ohio@mgail.com','fe36cc30a215af2280be650bea3e76c58e92f6b4df906ae9258cefe9ca574532','ohio','/static/images/profilePictures/2bbfcbec-bro.jpg'),
(61,'name','email@gmail.com','bbee9c4bff4472811b3e690ad1eb90fae727d5f1cc1ba9b0d4d138259d676c20','name','/static/images/profilePictures/3766f93e-bro.jpg');
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

-- Dump completed on 2024-08-05 12:48:28
