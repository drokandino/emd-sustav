-- MySQL dump 10.13  Distrib 5.7.28, for Linux (x86_64)
--
-- Host: localhost    Database: emd_novi
-- ------------------------------------------------------
-- Server version	5.7.28-0ubuntu0.19.04.2

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
-- Table structure for table `materijal`
--

DROP TABLE IF EXISTS `materijal`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `materijal` (
  `idMaterijal` varchar(100) COLLATE utf8_croatian_ci NOT NULL,
  PRIMARY KEY (`idMaterijal`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_croatian_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `materijal`
--

LOCK TABLES `materijal` WRITE;
/*!40000 ALTER TABLE `materijal` DISABLE KEYS */;
INSERT INTO `materijal` VALUES ('AISI 304'),('AISI 316'),('nema');
/*!40000 ALTER TABLE `materijal` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `nalogNarudzba`
--

DROP TABLE IF EXISTS `nalogNarudzba`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `nalogNarudzba` (
  `nalog` int(11) NOT NULL,
  `narudzba` float NOT NULL,
  PRIMARY KEY (`nalog`,`narudzba`),
  KEY `nalogNarudzba_FK_1` (`narudzba`),
  CONSTRAINT `nalogNarudzba_FK` FOREIGN KEY (`nalog`) REFERENCES `radniNalog` (`brojNaloga`),
  CONSTRAINT `nalogNarudzba_FK_1` FOREIGN KEY (`narudzba`) REFERENCES `narudzba` (`narudzbenica`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_croatian_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nalogNarudzba`
--

LOCK TABLES `nalogNarudzba` WRITE;
/*!40000 ALTER TABLE `nalogNarudzba` DISABLE KEYS */;
INSERT INTO `nalogNarudzba` VALUES (166,0),(166,1),(170,279),(177,657),(175,2522.7),(180,2601),(179,2618.2),(174,2701.2),(176,2702.2),(181,2702.3),(178,2702.4),(166,2856.1),(166,2856.3),(176,2856.4),(178,2921);
/*!40000 ALTER TABLE `nalogNarudzba` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `nalogPozicija`
--

DROP TABLE IF EXISTS `nalogPozicija`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `nalogPozicija` (
  `nacrt` varchar(100) COLLATE utf8_croatian_ci NOT NULL,
  `nalog` int(11) NOT NULL,
  PRIMARY KEY (`nacrt`,`nalog`),
  KEY `nalogPozicija_FK_1` (`nalog`),
  CONSTRAINT `nalogPozicija_FK` FOREIGN KEY (`nacrt`) REFERENCES `pozicija` (`nacrt`),
  CONSTRAINT `nalogPozicija_FK_1` FOREIGN KEY (`nalog`) REFERENCES `radniNalog` (`brojNaloga`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_croatian_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nalogPozicija`
--

LOCK TABLES `nalogPozicija` WRITE;
/*!40000 ALTER TABLE `nalogPozicija` DISABLE KEYS */;
INSERT INTO `nalogPozicija` VALUES ('10232608',166),('10531548',166),('11226820',166),('11430378',166),('IM-NRV-1-3',170),('IM-NRV-1-4',170),('10594613',174),('11460132',175),('10160936',176),('10160963',176),('108-19-016',177),('11263788',178),('11331097',178),('11219725',179),('nema',180),('11344228',181);
/*!40000 ALTER TABLE `nalogPozicija` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `narudzba`
--

DROP TABLE IF EXISTS `narudzba`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `narudzba` (
  `narudzbenica` float NOT NULL,
  `rok` date DEFAULT NULL,
  PRIMARY KEY (`narudzbenica`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_croatian_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `narudzba`
--

LOCK TABLES `narudzba` WRITE;
/*!40000 ALTER TABLE `narudzba` DISABLE KEYS */;
INSERT INTO `narudzba` VALUES (0,'2019-11-26'),(1,'2019-11-26'),(279,'2019-11-27'),(657,'2019-10-30'),(2522.7,'2019-11-09'),(2601,'2019-11-15'),(2618.2,'2019-11-11'),(2701.2,'2019-11-06'),(2702.2,'2019-11-07'),(2702.3,'2019-11-11'),(2702.4,'2019-11-09'),(2856.1,'2019-11-30'),(2856.3,'2019-11-30'),(2856.4,'2019-11-30'),(2921,'2019-11-09');
/*!40000 ALTER TABLE `narudzba` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pozicija`
--

DROP TABLE IF EXISTS `pozicija`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pozicija` (
  `naziv` text COLLATE utf8_croatian_ci,
  `nacrt` varchar(100) COLLATE utf8_croatian_ci NOT NULL,
  `idMaterijal` varchar(100) COLLATE utf8_croatian_ci DEFAULT NULL,
  `redniBr` int(11) DEFAULT NULL,
  PRIMARY KEY (`nacrt`),
  KEY `pozicija_FK` (`idMaterijal`),
  CONSTRAINT `pozicija_FK` FOREIGN KEY (`idMaterijal`) REFERENCES `materijal` (`idMaterijal`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_croatian_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pozicija`
--

LOCK TABLES `pozicija` WRITE;
/*!40000 ALTER TABLE `pozicija` DISABLE KEYS */;
INSERT INTO `pozicija` VALUES ('Klemmbolzen M5','10160936','AISI 304',169),('Spannbolzen','10160963','AISI 304',162),('Bolzen M6_25 KRATKI NOVO!','10232608','AISI 316',15),('Bolzen M6_22 KRATKI NOVO!','10531548','AISI 316',17),('Bolt  poliranje/novo','10594613','AISI 316',168),('Priključak plovka (06-11)','108-19-016','AISI 316',170),('Nut (kvadrat 15 - novo!)','11219725','AISI 304',0),('Bolzen M8_19,5 KRATKI','11226820','AISI 316',16),('Stopper screw M6','11263788','AISI 304',71),('Hexagon nut M8x1','11331097','AISI 304',138),('Zentrierpin SW8','11344228','AISI 316',75),('Bolzen M6_18 KRATKI NOVO!','11430378','AISI 316',18),('Gewindebolzen M6','11460132','AISI 304',113),('IM-NRV-01: Čep gornji Ø60','IM-NRV-1-3','AISI 316',34),('IM-NRV-01: Cijev Ø60','IM-NRV-1-4','AISI 316',33),('Dugi bolzeni  6vrsta 304/316','nema','nema',0);
/*!40000 ALTER TABLE `pozicija` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pozicijaNarudzba`
--

DROP TABLE IF EXISTS `pozicijaNarudzba`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pozicijaNarudzba` (
  `nacrt` varchar(100) COLLATE utf8_croatian_ci NOT NULL,
  `narudzbenica` float NOT NULL,
  PRIMARY KEY (`nacrt`,`narudzbenica`),
  KEY `pozicijaNarudzba_FK_1` (`narudzbenica`),
  CONSTRAINT `pozicijaNarudzba_FK` FOREIGN KEY (`nacrt`) REFERENCES `pozicija` (`nacrt`),
  CONSTRAINT `pozicijaNarudzba_FK_1` FOREIGN KEY (`narudzbenica`) REFERENCES `narudzba` (`narudzbenica`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_croatian_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pozicijaNarudzba`
--

LOCK TABLES `pozicijaNarudzba` WRITE;
/*!40000 ALTER TABLE `pozicijaNarudzba` DISABLE KEYS */;
INSERT INTO `pozicijaNarudzba` VALUES ('10232608',0),('11226820',1),('IM-NRV-1-3',279),('IM-NRV-1-4',279),('108-19-016',657),('11460132',2522.7),('11219725',2618.2),('10594613',2701.2),('10160936',2702.2),('11344228',2702.3),('11263788',2702.4),('11430378',2856.1),('10531548',2856.3),('10160963',2856.4),('11331097',2921);
/*!40000 ALTER TABLE `pozicijaNarudzba` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `radniNalog`
--

DROP TABLE IF EXISTS `radniNalog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `radniNalog` (
  `brojNaloga` int(11) NOT NULL,
  `nalogVeza` int(11) DEFAULT NULL,
  PRIMARY KEY (`brojNaloga`),
  KEY `radniNalog_FK` (`nalogVeza`),
  CONSTRAINT `radniNalog_FK` FOREIGN KEY (`nalogVeza`) REFERENCES `radniNalog` (`brojNaloga`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_croatian_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `radniNalog`
--

LOCK TABLES `radniNalog` WRITE;
/*!40000 ALTER TABLE `radniNalog` DISABLE KEYS */;
INSERT INTO `radniNalog` VALUES (166,NULL),(170,NULL),(174,NULL),(175,NULL),(176,NULL),(177,NULL),(178,NULL),(179,NULL),(180,NULL),(181,NULL);
/*!40000 ALTER TABLE `radniNalog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tehnologija`
--

DROP TABLE IF EXISTS `tehnologija`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tehnologija` (
  `cnc` varchar(100) COLLATE utf8_croatian_ci NOT NULL,
  PRIMARY KEY (`cnc`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_croatian_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tehnologija`
--

LOCK TABLES `tehnologija` WRITE;
/*!40000 ALTER TABLE `tehnologija` DISABLE KEYS */;
INSERT INTO `tehnologija` VALUES ('bušilica'),('nema'),('SL'),('ST1'),('ST2'),('TNP');
/*!40000 ALTER TABLE `tehnologija` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tehnologijaPozicija`
--

DROP TABLE IF EXISTS `tehnologijaPozicija`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tehnologijaPozicija` (
  `cnc` varchar(100) COLLATE utf8_croatian_ci NOT NULL,
  `nacrt` varchar(100) COLLATE utf8_croatian_ci NOT NULL,
  PRIMARY KEY (`cnc`,`nacrt`),
  KEY `tehnologijaPozicija_FK_1` (`nacrt`),
  CONSTRAINT `tehnologijaPozicija_FK` FOREIGN KEY (`cnc`) REFERENCES `tehnologija` (`cnc`),
  CONSTRAINT `tehnologijaPozicija_FK_1` FOREIGN KEY (`nacrt`) REFERENCES `pozicija` (`nacrt`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_croatian_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tehnologijaPozicija`
--

LOCK TABLES `tehnologijaPozicija` WRITE;
/*!40000 ALTER TABLE `tehnologijaPozicija` DISABLE KEYS */;
INSERT INTO `tehnologijaPozicija` VALUES ('nema','10160936'),('ST1','10160936'),('ST1','10160963'),('TNP','10160963'),('SL','10232608'),('SL','10531548'),('nema','10594613'),('bušilica','108-19-016'),('SL','108-19-016'),('nema','11219725'),('ST1','11219725'),('SL','11226820'),('SL','11263788'),('ST2','11263788'),('nema','11331097'),('SL','11331097'),('nema','11344228'),('ST2','11344228'),('SL','11430378'),('ST1','11460132'),('ST2','11460132'),('nema','IM-NRV-1-3'),('SL','IM-NRV-1-3'),('nema','IM-NRV-1-4'),('SL','IM-NRV-1-4'),('nema','nema');
/*!40000 ALTER TABLE `tehnologijaPozicija` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-01-27 21:08:09
