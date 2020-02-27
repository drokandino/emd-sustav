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
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-02-27 16:33:11
