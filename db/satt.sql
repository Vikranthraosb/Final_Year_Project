-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               5.0.17-nt - MySQL Community Edition (GPL)
-- Server OS:                    Win32
-- HeidiSQL Version:             9.4.0.5174
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- Dumping database structure for stattendance
CREATE DATABASE IF NOT EXISTS `stattendance` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `stattendance`;

-- Dumping structure for table stattendance.admin
CREATE TABLE IF NOT EXISTS `admin` (
  `id` int(11) NOT NULL auto_increment,
  `email` varchar(150) NOT NULL default '0',
  `pass` varchar(150) NOT NULL default '0',
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping data for table stattendance.admin: ~1 rows (approximately)
/*!40000 ALTER TABLE `admin` DISABLE KEYS */;
INSERT INTO `admin` (`id`, `email`, `pass`) VALUES
	(1, 'admin@gmail.com', '123');
/*!40000 ALTER TABLE `admin` ENABLE KEYS */;

-- Dumping structure for table stattendance.attendance
CREATE TABLE IF NOT EXISTS `attendance` (
  `id` int(11) NOT NULL auto_increment,
  `eid` int(11) NOT NULL default '0',
  `date` varchar(150) NOT NULL default '0',
  `time` varchar(150) NOT NULL default '0',
  PRIMARY KEY  (`id`),
  KEY `FK_attendance_employees` (`eid`),
  CONSTRAINT `FK_attendance_employees` FOREIGN KEY (`eid`) REFERENCES `students` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping data for table stattendance.attendance: ~0 rows (approximately)
/*!40000 ALTER TABLE `attendance` DISABLE KEYS */;
/*!40000 ALTER TABLE `attendance` ENABLE KEYS */;

-- Dumping structure for table stattendance.staff
CREATE TABLE IF NOT EXISTS `staff` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(150) NOT NULL default '0',
  `email` varchar(150) NOT NULL default '0',
  `phone` varchar(150) NOT NULL default '0',
  `sid` int(11) NOT NULL default '0',
  `password` varchar(150) NOT NULL default '0',
  PRIMARY KEY  (`id`),
  KEY `FK_staff_subject` (`sid`),
  CONSTRAINT `FK_staff_subject` FOREIGN KEY (`sid`) REFERENCES `subject` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping data for table stattendance.staff: ~1 rows (approximately)
/*!40000 ALTER TABLE `staff` DISABLE KEYS */;
INSERT INTO `staff` (`id`, `name`, `email`, `phone`, `sid`, `password`) VALUES
	(1, 'VARUN', 'varun@gmail.com', '7418529632', 1, '123');
/*!40000 ALTER TABLE `staff` ENABLE KEYS */;

-- Dumping structure for table stattendance.students
CREATE TABLE IF NOT EXISTS `students` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(150) NOT NULL default '0',
  `usn` varchar(150) NOT NULL default '0',
  `email` varchar(150) NOT NULL default '0',
  `phone` varchar(150) NOT NULL default '0',
  `gender` varchar(150) NOT NULL default '0',
  `address` varchar(150) NOT NULL default '0',
  `mid` int(11) NOT NULL default '0',
  `password` varchar(150) NOT NULL default '0',
  PRIMARY KEY  (`id`),
  KEY `FK_students_staff` (`mid`),
  CONSTRAINT `FK_students_staff` FOREIGN KEY (`mid`) REFERENCES `staff` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping data for table stattendance.students: ~1 rows (approximately)
/*!40000 ALTER TABLE `students` DISABLE KEYS */;
INSERT INTO `students` (`id`, `name`, `usn`, `email`, `phone`, `gender`, `address`, `mid`, `password`) VALUES
	(1, 'abhi', '1nc12ec418', 'abhi@gmail.com', '9876789089', 'Male', 'mysore', 1, '123');
/*!40000 ALTER TABLE `students` ENABLE KEYS */;

-- Dumping structure for table stattendance.subject
CREATE TABLE IF NOT EXISTS `subject` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(150) NOT NULL default '0',
  `sem` varchar(150) NOT NULL default '0',
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping data for table stattendance.subject: ~1 rows (approximately)
/*!40000 ALTER TABLE `subject` DISABLE KEYS */;
INSERT INTO `subject` (`id`, `name`, `sem`) VALUES
	(1, 'DATA SCIENCE', '4th');
/*!40000 ALTER TABLE `subject` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
