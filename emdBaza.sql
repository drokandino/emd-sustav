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
-- Table structure for table `alat`
--

DROP TABLE IF EXISTS `alat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alat` (
  `ime` varchar(100) COLLATE utf8_croatian_ci NOT NULL,
  PRIMARY KEY (`ime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_croatian_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alat`
--

LOCK TABLES `alat` WRITE;
/*!40000 ALTER TABLE `alat` DISABLE KEYS */;
INSERT INTO `alat` VALUES ('M5'),('M56'),('M6'),('M8'),('nema'),('Ø7h9');
/*!40000 ALTER TABLE `alat` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `alatPozicija`
--

DROP TABLE IF EXISTS `alatPozicija`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alatPozicija` (
  `nacrt` varchar(100) COLLATE utf8_croatian_ci NOT NULL,
  `alat` varchar(100) COLLATE utf8_croatian_ci NOT NULL,
  `mjestoNavoja` varchar(100) COLLATE utf8_croatian_ci NOT NULL,
  PRIMARY KEY (`nacrt`,`alat`),
  KEY `alatPozicija_FK` (`alat`),
  CONSTRAINT `alatPozicija_FK` FOREIGN KEY (`alat`) REFERENCES `alat` (`ime`),
  CONSTRAINT `alatPozicija_FK_1` FOREIGN KEY (`nacrt`) REFERENCES `pozicija` (`nacrt`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_croatian_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alatPozicija`
--

LOCK TABLES `alatPozicija` WRITE;
/*!40000 ALTER TABLE `alatPozicija` DISABLE KEYS */;
INSERT INTO `alatPozicija` VALUES ('10160936','M5','unutarnji'),('10160936','Ø7h9','vanjski'),('10160963','nema','unutarnji'),('10232608','M6','vanjski'),('10232608','M8','unutarnji'),('10531548','M6','vanjski'),('10531548','M8','unutarnji'),('10594613','nema','unutarnji'),('108-19-016','nema','unutarnji'),('11219725','nema','unutarnji'),('11226820','M6','vanjski'),('11226820','M8','unutarnji'),('11263788','M6','vanjski'),('11263788','nema','unutarnji'),('11331097','M8','unutarnji'),('11331097','nema','vanjski'),('11344228','nema','unutarnji'),('11430378','M6','vanjski'),('11430378','M8','unutarnji'),('11460132','M6','vanjski'),('11460132','nema','unutarnji'),('IM-NRV-1-3','M56','vanjski'),('IM-NRV-1-3','nema','unutarnji'),('IM-NRV-1-4','M56','unutarnji'),('IM-NRV-1-4','nema','vanjski');
/*!40000 ALTER TABLE `alatPozicija` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dobavljac`
--

DROP TABLE IF EXISTS `dobavljac`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dobavljac` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ime` varchar(100) COLLATE utf8_croatian_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_croatian_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dobavljac`
--

LOCK TABLES `dobavljac` WRITE;
/*!40000 ALTER TABLE `dobavljac` DISABLE KEYS */;
/*!40000 ALTER TABLE `dobavljac` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dobavljacAlat`
--

DROP TABLE IF EXISTS `dobavljacAlat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dobavljacAlat` (
  `id` int(11) NOT NULL,
  `ime` varchar(100) COLLATE utf8_croatian_ci NOT NULL,
  PRIMARY KEY (`id`,`ime`),
  KEY `dobavljacAlat_FK` (`ime`),
  CONSTRAINT `dobavljacAlat_FK` FOREIGN KEY (`ime`) REFERENCES `alat` (`ime`),
  CONSTRAINT `dobavljacAlat_FK_1` FOREIGN KEY (`id`) REFERENCES `dobavljac` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_croatian_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dobavljacAlat`
--

LOCK TABLES `dobavljacAlat` WRITE;
/*!40000 ALTER TABLE `dobavljacAlat` DISABLE KEYS */;
/*!40000 ALTER TABLE `dobavljacAlat` ENABLE KEYS */;
UNLOCK TABLES;

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
  `nacrt` varchar(100) COLLATE utf8_croatian_ci NOT NULL DEFAULT '0',
  `idMaterijal` varchar(100) COLLATE utf8_croatian_ci DEFAULT NULL,
  `redniBr` int(11) DEFAULT NULL,
  `dimenzija` varchar(100) COLLATE utf8_croatian_ci DEFAULT NULL,
  `duljina` float DEFAULT NULL,
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
INSERT INTO `pozicija` VALUES ('Klemmbolzen M5','10160936','AISI 304',169,'Ø7',7),('Spannbolzen','10160963','AISI 304',162,'Ø7',8),('Bolzen M6_25 KRATKI NOVO!','10232608','AISI 316',15,'Ø20',40),('Bolzen M6_22 KRATKI NOVO!','10531548','AISI 316',17,'Ø20',35),('Bolt  poliranje/novo','10594613','AISI 316',168,'Ø15',20),('Priključak plovka (06-11)','108-19-016','AISI 316',170,'Ø12',15),('Nut (kvadrat 15 - novo!)','11219725','AISI 304',0,'Ø18',15),('Bolzen M8_19,5 KRATKI','11226820','AISI 316',16,'Ø20',35),('Stopper screw M6','11263788','AISI 304',71,'SW19',38.5),('Hexagon nut M8x1','11331097','AISI 304',138,'SW11',4),('Zentrierpin SW8','11344228','AISI 316',75,'Ø10',15),('Bolzen M6_18 KRATKI NOVO!','11430378','AISI 316',18,'Ø20',29),('Gewindebolzen M6','11460132','AISI 304',113,'Ø12',44),('IM-NRV-01: Čep gornji Ø60','IM-NRV-1-3','AISI 316',34,'Ø60',20),('IM-NRV-01: Cijev Ø60','IM-NRV-1-4','AISI 316',33,'Ø60x3',84),('Dugi bolzeni  6vrsta 304/316','nema','nema',0,'Ø20',75);
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
  `komada` int(11) DEFAULT NULL,
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
INSERT INTO `pozicijaNarudzba` VALUES ('10160936',2702.2,100),('10160963',2856.4,100),('10232608',0,30),('10531548',2856.3,10),('10594613',2701.2,20),('108-19-016',657,600),('11219725',2618.2,150),('11226820',1,200),('11263788',2702.4,30),('11331097',2921,150),('11344228',2702.3,24),('11430378',2856.1,5),('11460132',2522.7,150),('IM-NRV-1-3',279,300),('IM-NRV-1-4',279,300);
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
  `generiran` tinyint(1) DEFAULT NULL,
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
INSERT INTO `radniNalog` VALUES (166,NULL,1),(170,NULL,1),(174,NULL,1),(175,NULL,1),(176,NULL,1),(177,NULL,1),(178,NULL,1),(179,NULL,1),(180,NULL,1),(181,NULL,1);
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

-- Dump completed on 2020-02-27 16:01:18
