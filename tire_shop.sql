-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3307
-- Generation Time: Aug 16, 2025 at 12:32 PM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.0.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `tire_shop`
--

-- --------------------------------------------------------

--
-- Table structure for table `addresses`
--

CREATE TABLE `addresses` (
  `address_id` int(11) NOT NULL,
  `customer_id` int(11) DEFAULT NULL,
  `address_no` varchar(50) DEFAULT NULL,
  `village` varchar(100) DEFAULT NULL,
  `road` varchar(100) DEFAULT NULL,
  `subdistrict` varchar(100) DEFAULT NULL,
  `district` varchar(100) DEFAULT NULL,
  `province` varchar(100) DEFAULT NULL,
  `zipcode` varchar(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `addresses`
--

INSERT INTO `addresses` (`address_id`, `customer_id`, `address_no`, `village`, `road`, `subdistrict`, `district`, `province`, `zipcode`) VALUES
(1, 1, '99/1', 'หมู่บ้านแสนสุข', 'สุขุมวิท 101', 'บางนา', 'บางนา', 'กรุงเทพมหานคร', '10260'),
(2, 2, '55', 'None', 'ลาดพร้าว', 'จตุจักร', 'จตุจักร', 'กรุงเทพมหานคร', '10900'),
(3, 3, '123', 'หมู่บ้านหรรษา', 'เชียงใหม่-ลำพูน', 'หนองหอย', 'เมือง', 'เชียงใหม่', '50000'),
(4, 4, '7/9', 'None', 'ชลบุรี-บ้านบึง', 'บ้านบึง', 'ชลบุรี', 'ชลบุรี', '20170'),
(5, 5, '12', 'หมู่ 3', 'โรจนะ', 'คลองจิก', 'บางปะอิน', 'พระนครศรีอยุธยา', '13160'),
(7, 9, '37 M.5', 'โนนสวรรค์', '', 'บ้านด่าน', 'บ้านด่าน', 'บุรีรัมย์', '31000');

-- --------------------------------------------------------

--
-- Table structure for table `bookings`
--

CREATE TABLE `bookings` (
  `booking_id` int(11) NOT NULL,
  `customer_id` int(11) DEFAULT NULL,
  `vehicle_id` int(11) DEFAULT NULL,
  `booking_date` datetime DEFAULT NULL,
  `service_date` date DEFAULT NULL,
  `status` enum('รอดำเนินการ','สำเร็จ','ยกเลิก') DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `bookings`
--

INSERT INTO `bookings` (`booking_id`, `customer_id`, `vehicle_id`, `booking_date`, `service_date`, `status`) VALUES
(1, 1, 1, '2025-07-09 00:00:00', '2025-06-23', 'รอดำเนินการ'),
(2, 2, 2, '2025-07-26 00:00:00', '2025-06-21', 'สำเร็จ'),
(3, 3, 3, '2025-07-11 00:00:00', '2025-06-22', 'สำเร็จ'),
(4, 4, 4, '2025-06-19 13:00:00', '2025-06-24', 'รอดำเนินการ'),
(5, 5, 5, '2025-06-18 11:00:00', '2025-06-25', 'รอดำเนินการ');

-- --------------------------------------------------------

--
-- Table structure for table `booking_items`
--

CREATE TABLE `booking_items` (
  `item_id` int(11) NOT NULL,
  `booking_id` int(11) NOT NULL,
  `service_id` int(11) DEFAULT NULL,
  `quantity` int(11) DEFAULT 1,
  `note` text DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  `updated_at` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `tire_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `booking_items`
--

INSERT INTO `booking_items` (`item_id`, `booking_id`, `service_id`, `quantity`, `note`, `created_at`, `updated_at`, `tire_id`) VALUES
(222, 3, 3, 1, NULL, '2025-07-16 18:28:36', '2025-07-16 18:28:36', NULL),
(223, 3, 6, 1, NULL, '2025-07-16 18:28:36', '2025-07-16 18:28:36', NULL),
(224, 3, 13, 1, NULL, '2025-07-16 18:28:36', '2025-07-16 18:28:36', NULL),
(225, 3, 16, 1, NULL, '2025-07-16 18:28:36', '2025-07-16 18:28:36', NULL),
(226, 3, 20, 1, NULL, '2025-07-16 18:28:36', '2025-07-16 18:28:36', NULL),
(227, 3, 23, 1, NULL, '2025-07-16 18:28:36', '2025-07-16 18:28:36', NULL),
(228, 3, 26, 1, NULL, '2025-07-16 18:28:36', '2025-07-16 18:28:36', NULL),
(229, 2, 3, 1, NULL, '2025-07-16 18:41:58', '2025-07-16 18:41:58', NULL),
(230, 2, 4, 1, NULL, '2025-07-16 18:41:58', '2025-07-16 18:41:58', NULL),
(231, 2, 5, 1, NULL, '2025-07-16 18:41:58', '2025-07-16 18:41:58', NULL),
(232, 2, 6, 1, NULL, '2025-07-16 18:41:58', '2025-07-16 18:41:58', NULL),
(233, 2, 7, 1, NULL, '2025-07-16 18:41:58', '2025-07-16 18:41:58', NULL),
(234, 2, 8, 1, NULL, '2025-07-16 18:41:58', '2025-07-16 18:41:58', NULL),
(235, 2, 2, 1, NULL, '2025-07-16 18:41:58', '2025-07-16 18:41:58', NULL),
(236, 2, 9, 1, NULL, '2025-07-16 18:41:58', '2025-07-16 18:41:58', NULL),
(237, 2, 10, 1, NULL, '2025-07-16 18:41:58', '2025-07-16 18:41:58', NULL),
(238, 2, 11, 1, NULL, '2025-07-16 18:41:58', '2025-07-16 18:41:58', NULL),
(239, 2, 16, 1, NULL, '2025-07-16 18:41:58', '2025-07-16 18:41:58', NULL),
(240, 2, 17, 1, NULL, '2025-07-16 18:41:58', '2025-07-16 18:41:58', NULL),
(241, 2, 18, 1, NULL, '2025-07-16 18:41:58', '2025-07-16 18:41:58', NULL),
(242, 2, 19, 1, NULL, '2025-07-16 18:41:58', '2025-07-16 18:41:58', NULL),
(243, 2, 21, 1, NULL, '2025-07-16 18:41:58', '2025-07-16 18:41:58', NULL),
(244, 2, 20, 1, NULL, '2025-07-16 18:41:58', '2025-07-16 18:41:58', NULL),
(245, 2, 22, 1, NULL, '2025-07-16 18:41:58', '2025-07-16 18:41:58', NULL),
(246, 2, 23, 1, NULL, '2025-07-16 18:41:58', '2025-07-16 18:41:58', NULL),
(247, 2, 26, 1, NULL, '2025-07-16 18:41:58', '2025-07-16 18:41:58', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `booking_item_options`
--

CREATE TABLE `booking_item_options` (
  `id` int(11) NOT NULL,
  `item_id` int(11) NOT NULL,
  `option_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `booking_item_options`
--

INSERT INTO `booking_item_options` (`id`, `item_id`, `option_id`) VALUES
(31, 222, 5),
(32, 223, 10),
(33, 226, 20),
(34, 229, 5),
(35, 231, 7),
(36, 232, 10),
(37, 233, 13),
(38, 234, 16),
(39, 235, 2),
(40, 235, 3),
(41, 241, 17),
(42, 242, 18),
(43, 244, 20);

-- --------------------------------------------------------

--
-- Table structure for table `brands`
--

CREATE TABLE `brands` (
  `brand_id` int(11) NOT NULL,
  `brand_name` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `brands`
--

INSERT INTO `brands` (`brand_id`, `brand_name`) VALUES
(1, 'Michelin'),
(2, 'BFgoodrich'),
(3, 'Maxxis');

-- --------------------------------------------------------

--
-- Table structure for table `customers`
--

CREATE TABLE `customers` (
  `customer_id` int(11) NOT NULL,
  `first_name` varchar(100) DEFAULT NULL,
  `last_name` varchar(100) DEFAULT NULL,
  `gender` enum('ชาย','หญิง','ไม่ระบุ') DEFAULT NULL,
  `birthdate` date DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `customers`
--

INSERT INTO `customers` (`customer_id`, `first_name`, `last_name`, `gender`, `birthdate`, `phone`, `email`) VALUES
(1, 'สมชาย', 'ใจดี', 'ไม่ระบุ', '1985-06-15', '0812345679', 'somchai@example.com'),
(2, 'สมหญิง', 'สุขใจ', 'หญิง', '1990-10-01', '0899998888', 'somying@example.com'),
(3, 'เจน', 'โสภา', 'หญิง', '1995-02-20', '0866667777', 'jane@example.com'),
(4, 'เด่น', 'เกรียงไกร', 'ชาย', '1982-12-05', '0855554444', 'den@example.com'),
(5, 'ธนา', 'รุ่งเรือง', 'ชาย', '2000-01-01', '0841231234', 'thana@example.com'),
(9, 'พลอย', 'ณัฐ', 'หญิง', '2003-11-16', '0610903262', 'ploynatthanicha11@gmail.com');

-- --------------------------------------------------------

--
-- Table structure for table `page_views`
--

CREATE TABLE `page_views` (
  `page_id` varchar(100) NOT NULL,
  `views` int(11) DEFAULT 0,
  `last_viewed_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `promotions`
--

CREATE TABLE `promotions` (
  `promotion_id` int(11) NOT NULL,
  `title` varchar(100) DEFAULT NULL,
  `description` text DEFAULT NULL,
  `image_url` varchar(255) DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `promotions`
--

INSERT INTO `promotions` (`promotion_id`, `title`, `description`, `image_url`, `start_date`, `end_date`) VALUES
(5, 'ยางรถยนต์ ราคาสุทธิชุดละ 5,399.-', 'ยางรถยนต์ ราคาสุทธิชุดละ 5,399 ขนาดยาง 185/60R15 จำนวน 4 เส้น บริการติดตั้งฟรี 1-31 กรกฎาคม 2568 ที่ไทร์พลัสบุรีรัมย์ 2 สาขาเท่านั้น ** เงื่อนไขเป็นไปตามที่บริษัทฯ กำหนด', 'pro1.jpg', '2025-07-01', '2025-07-31'),
(6, 'น้ำมันเครื่องฟรีไส้กรอง 950.-', 'น้ำมันเครื่องฟรีไส้กรอง 950.- 1-31 กรกฎาคม 2568 ที่ไทร์พลัสบุรีรัมย์ 2 สาขาเท่านั้น ** เงื่อนไขเป็นไปตามที่บริษัทฯ กำหนด', 'pro2.jpg', '2025-07-01', '2025-07-31'),
(7, 'อะไหล่ช่วงล่าง ลดสูงสุด 40%', 'อะไหล่ช่วงล่าง ลดสูงสุด 40% 1-31 กรกฎาคม 2568 ที่ไทร์พลัสบุรีรัมย์ 2 สาขาเท่านั้น ** เงื่อนไขเป็นไปตามที่บริษัทฯ กำหนด', 'pro3.jpg', '2025-07-01', '2025-07-31'),
(8, 'ผ่อนบัตรเครดิต นาน 10 เดือน 0%', 'ผ่อนบัตรเครดิต นาน 10 เดือน 0% 1-31 กรกฎาคม 2568 ที่ไทร์พลัสบุรีรัมย์ 2 สาขาเท่านั้น ** เงื่อนไขเป็นไปตามที่บริษัทฯ กำหนด', 'pro4.jpg', '2025-07-01', '2025-07-31');

-- --------------------------------------------------------

--
-- Table structure for table `roles`
--

CREATE TABLE `roles` (
  `role_id` int(11) NOT NULL,
  `role_name` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `roles`
--

INSERT INTO `roles` (`role_id`, `role_name`) VALUES
(1, 'admin'),
(2, 'staff'),
(3, 'owner');

-- --------------------------------------------------------

--
-- Table structure for table `services`
--

CREATE TABLE `services` (
  `service_id` int(11) NOT NULL,
  `category` varchar(100) NOT NULL,
  `service_name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `services`
--

INSERT INTO `services` (`service_id`, `category`, `service_name`) VALUES
(1, 'ยาง', 'สลับยาง'),
(2, 'ยาง', 'ถ่วงล้อ'),
(3, 'ยาง', 'ตั้งศูนย์'),
(4, 'ยาง', 'ถอดใส่ยาง'),
(5, 'ยาง', 'ปะยาง'),
(6, 'ยาง', 'จุ๊บ'),
(7, 'ยาง', 'ยางเก่า'),
(8, 'ยาง', 'เติมลม'),
(9, 'ยาง', 'ขับปอนด์ล้อ'),
(10, 'บำรุงรักษา', 'น้ำมันเครื่อง'),
(11, 'บำรุงรักษา', 'ไส้กรองน้ำมันเครื่อง'),
(12, 'บำรุงรักษา', 'ไส้กรองอากาศ'),
(13, 'บำรุงรักษา', 'ไส้กรองแอร์'),
(14, 'บำรุงรักษา', 'น้ำมันเกียร์'),
(15, 'บำรุงรักษา', 'น้ำมันเฟืองท้าย'),
(16, 'ระบบเบรก', 'ผ้าเบรกหน้า'),
(17, 'ระบบเบรก', 'ผ้าเบรกหลัง'),
(18, 'ระบบเบรก', 'ตรวจเช็กทำความสะอาดเบรก'),
(19, 'ระบบเบรก', 'เจียรจาน'),
(20, 'ระบบเบรก', 'เปลี่ยนจาน'),
(21, 'ระบบเบรก', 'น้ำมันเบรก DOT'),
(22, 'ไฟฟ้า', 'แบตเตอรี่'),
(23, 'ไฟฟ้า', 'น้ำกลั่น'),
(24, 'ไฟฟ้า', 'หลอดไฟ'),
(25, 'ไฟฟ้า', 'ใบปัดน้ำฝน'),
(26, 'ช่วงล่าง', 'โช้คอัพหน้า'),
(27, 'ช่วงล่าง', 'โช้คอัพหลัง');

-- --------------------------------------------------------

--
-- Table structure for table `service_options`
--

CREATE TABLE `service_options` (
  `option_id` int(11) NOT NULL,
  `service_id` int(11) NOT NULL,
  `option_name` varchar(255) NOT NULL,
  `note` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `service_options`
--

INSERT INTO `service_options` (`option_id`, `service_id`, `option_name`, `note`) VALUES
(1, 2, 'แม็ก', ' '),
(2, 2, 'กระทะ', ' '),
(3, 2, '2 ล้อ', ' '),
(4, 2, '4 ล้อ', ' '),
(5, 3, '2 ล้อ', ' '),
(6, 3, '4 ล้อ', ' '),
(7, 5, 'ดอกเห็ด PRP', ' '),
(8, 5, 'แผ่นปะ', ' '),
(9, 5, 'ใยไหม', ' '),
(10, 6, 'เหล็ก', ' '),
(11, 6, 'ยาง', ' '),
(12, 6, 'เซ็นเซอร์', ' '),
(13, 7, 'นำกลับ', ' '),
(14, 7, 'ทิ้งไว้ที่ร้าน', ' '),
(15, 8, 'ธรรมดา', 'ไม่มีค่าบริการ'),
(16, 8, 'ไนโตรเจน', 'มีค่าบริการเพิ่ม'),
(17, 18, 'น้ำยาล้างเบรก', ' '),
(18, 19, 'หน้า', ' '),
(19, 19, 'หลัง', ' '),
(20, 20, 'หน้า', ' '),
(21, 20, 'หลัง', ' ');

-- --------------------------------------------------------

--
-- Table structure for table `service_tires`
--

CREATE TABLE `service_tires` (
  `id` int(11) NOT NULL,
  `booking_id` int(11) NOT NULL,
  `position` enum('front_left','front_right','rear_left','rear_right') NOT NULL,
  `tire_id` int(11) DEFAULT NULL,
  `brand` varchar(100) DEFAULT NULL,
  `model` varchar(100) DEFAULT NULL,
  `size` varchar(50) DEFAULT NULL,
  `dot` varchar(20) DEFAULT NULL,
  `notes` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tires`
--

CREATE TABLE `tires` (
  `tire_id` int(11) NOT NULL,
  `model_id` int(11) NOT NULL,
  `width` int(11) DEFAULT NULL,
  `aspect_ratio` int(11) DEFAULT NULL,
  `construction` char(1) DEFAULT NULL,
  `rim_diameter` int(11) DEFAULT NULL,
  `service_description` enum('XL') DEFAULT NULL,
  `full_size` varchar(50) DEFAULT NULL,
  `load_index` varchar(10) DEFAULT NULL,
  `speed_symbol` varchar(5) DEFAULT NULL,
  `ply_rating` varchar(10) DEFAULT NULL,
  `tubeless_type` varchar(20) DEFAULT NULL,
  `tire_load_type` enum('C','LT') DEFAULT NULL,
  `product_date` varchar(20) DEFAULT NULL,
  `price_each` decimal(10,2) DEFAULT NULL,
  `price_set` decimal(10,2) DEFAULT NULL,
  `promotion_price` decimal(10,2) DEFAULT NULL,
  `tire_image_url` text DEFAULT NULL,
  `notes` text DEFAULT NULL,
  `high_speed_rating` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `tires`
--

INSERT INTO `tires` (`tire_id`, `model_id`, `width`, `aspect_ratio`, `construction`, `rim_diameter`, `service_description`, `full_size`, `load_index`, `speed_symbol`, `ply_rating`, `tubeless_type`, `tire_load_type`, `product_date`, `price_each`, `price_set`, `promotion_price`, `tire_image_url`, `notes`, `high_speed_rating`) VALUES
(25, 8, 175, 70, 'R', 13, 'XL', '175/70 R13 86T XL TL', '86', 'T', NULL, 'TL', NULL, NULL, 1950.00, 7800.00, NULL, 'BFGoodrich ADVANTAGE TOURING.png', NULL, 0),
(26, 8, 165, 70, 'R', 14, 'XL', '165/70 R14 85T XL TL', '85', 'T', NULL, 'TL', NULL, NULL, 2050.00, 8200.00, NULL, 'BFGoodrich ADVANTAGE TOURING.png', NULL, 0),
(27, 8, 175, 65, 'R', 14, 'XL', '175/65 R14 86H XL TL', '86', 'H', NULL, 'TL', NULL, NULL, 2050.00, 8200.00, NULL, 'BFGoodrich ADVANTAGE TOURING.png', NULL, 0),
(28, 8, 175, 70, 'R', 14, 'XL', '175/70 R14 88T XL TL', '88', 'T', NULL, 'TL', NULL, NULL, 2050.00, 8200.00, NULL, 'BFGoodrich ADVANTAGE TOURING.png', NULL, 0),
(29, 8, 185, 60, 'R', 14, 'XL', '185/60 R14 86H XL TL', '86', 'H', NULL, 'TL', NULL, NULL, 2050.00, 8200.00, NULL, 'BFGoodrich ADVANTAGE TOURING.png', NULL, 0),
(30, 8, 185, 65, 'R', 14, 'XL', '185/65 R14 90H XL TL', '90', 'H', NULL, 'TL', NULL, NULL, 2400.00, 7200.00, NULL, 'BFGoodrich ADVANTAGE TOURING.png', NULL, 0),
(31, 9, 215, 65, 'R', 16, NULL, '215/65 R16 98T TL', '98', 'T', NULL, 'TL', NULL, NULL, 5350.00, 21400.00, NULL, 'BFGoodrich TRAIL-TERRAIN.png', NULL, 0),
(32, 9, 245, 70, 'R', 16, 'XL', '245/70 R16 111T XL TL', '111', 'T', NULL, 'TL', NULL, NULL, 6000.00, 24000.00, NULL, 'BFGoodrich TRAIL-TERRAIN.png', NULL, 0),
(33, 9, 255, 70, 'R', 16, 'XL', '255/70 R16 115T XL TL', '115', 'T', NULL, 'TL', NULL, NULL, 6400.00, 15600.00, NULL, 'BFGoodrich TRAIL-TERRAIN.png', NULL, 0),
(34, 9, 265, 70, 'R', 16, NULL, '265/70 R16 112T TL', '112', 'T', NULL, 'TL', NULL, NULL, 6500.00, 26000.00, NULL, 'BFGoodrich TRAIL-TERRAIN.png', NULL, 0),
(35, 9, 265, 75, 'R', 16, NULL, '265/75 R16 116T TL', '116', 'T', NULL, 'TL', NULL, NULL, 6600.00, 26400.00, NULL, 'BFGoodrich TRAIL-TERRAIN.png', NULL, 0),
(36, 9, 215, 60, 'R', 17, NULL, '215/60 R17 96H TL', '96', 'H', NULL, 'TL', NULL, NULL, 6050.00, 24200.00, NULL, 'BFGoodrich TRAIL-TERRAIN.png', NULL, 0),
(37, 10, 195, 80, 'R', 15, NULL, 'LT195/80 R15 107S TL', '107', 'S', NULL, 'TL', NULL, NULL, 6850.00, 27400.00, NULL, 'BFGoodrich KO3.jpg', NULL, 0),
(38, 10, 225, 70, 'R', 16, NULL, 'LT225/70R16 102/995S TL', '102/995', 'S', NULL, 'TL', NULL, NULL, 6550.00, 26200.00, NULL, 'BFGoodrich KO3.jpg', NULL, 0),
(39, 10, 225, 75, 'R', 16, NULL, 'LT225/75R16 115/112S TL', '115/112', 'S', NULL, 'TL', NULL, NULL, 7350.00, 29400.00, NULL, 'BFGoodrich KO3.jpg', NULL, 0),
(40, 10, 235, 70, 'R', 16, NULL, 'LT235/70R16 110/107S TL', '110/107', 'S', NULL, 'TL', NULL, NULL, 7650.00, 29400.00, NULL, 'BFGoodrich KO3.jpg', NULL, 0),
(41, 10, 235, 85, 'R', 16, NULL, 'LT235/85R16 120/116S TL', '120/116', 'S', NULL, 'TL', NULL, NULL, 7190.00, 28760.00, NULL, 'BFGoodrich KO3.jpg', NULL, 0),
(42, 1, 175, 70, 'R', 13, NULL, '175/70 82T R13 TL', '82', 'T', NULL, 'TL', NULL, NULL, 2750.00, 11000.00, NULL, 'Michelin ENERGY XM2 +_EXM2+.png', NULL, 0),
(43, 1, 185, 70, 'R', 13, NULL, '185/70 R13 86T TL', '86', 'T', NULL, 'TL', NULL, NULL, 2850.00, 11400.00, NULL, 'Michelin ENERGY XM2 +_EXM2+.png', NULL, 0),
(44, 1, 165, 65, 'R', 14, NULL, '165/65 R14 79H TL', '79', 'H', NULL, 'TL', NULL, NULL, 2850.00, 11400.00, NULL, 'Michelin ENERGY XM2 +_EXM2+.png', NULL, 0),
(45, 1, 165, 70, 'R', 14, NULL, '165/70 R14 81T TL', '81', 'T', NULL, 'TL', NULL, NULL, 2950.00, 11800.00, NULL, 'Michelin ENERGY XM2 +_EXM2+.png', NULL, 0),
(46, 1, 175, 65, 'R', 14, '', '175/65 R14 82H', '82', 'H', NULL, 'TL', NULL, '47/23', 2950.00, 11800.00, NULL, 'Michelin ENERGY XM2 +_EXM2+.png', NULL, 0),
(47, 1, 175, 70, 'R', 14, 'XL', '175/70 R14 88T XL TL', '88', 'T', NULL, 'TL', NULL, NULL, 3250.00, 13000.00, NULL, 'Michelin ENERGY XM2 +_EXM2+.png', NULL, 0),
(48, 1, 185, 60, 'R', 14, NULL, '185/60 R14 82H TL', '82', 'H', NULL, 'TL', NULL, NULL, 3300.00, 13200.00, NULL, 'Michelin ENERGY XM2 +_EXM2+.png', NULL, 0),
(49, 1, 185, 65, 'R', 14, NULL, '185/65 R14 86H TL', '86', 'H', NULL, 'TL', NULL, '46/23,13/24', 3100.00, 12400.00, NULL, 'Michelin ENERGY XM2 +_EXM2+.png', NULL, 0),
(50, 1, 185, 70, 'R', 14, NULL, '185/70 R14 88H TL', '88', 'H', NULL, 'TL', NULL, NULL, 3300.00, 13200.00, NULL, 'Michelin ENERGY XM2 +_EXM2+.png', NULL, 0),
(51, 1, 195, 60, 'R', 14, NULL, '195/60 R14 86H TL', '86', 'H', NULL, 'TL', NULL, NULL, 3600.00, 14400.00, NULL, 'Michelin ENERGY XM2 +_EXM2+.png', NULL, 0),
(52, 1, 195, 70, 'R', 14, NULL, '195/70 R14 91H TL', '91', 'H', NULL, 'TL', NULL, NULL, 3650.00, 14600.00, NULL, 'Michelin ENERGY XM2 +_EXM2+.png', NULL, 0),
(53, 2, 175, 65, 'R', 15, NULL, '175/65 R15 84H TL', '84', 'H', NULL, 'TL', NULL, NULL, 2650.00, 10600.00, NULL, 'Michelin ENERGY XM2 +_EXM2+.png', NULL, 0),
(54, 2, 185, 60, 'R', 15, NULL, '185/60 R15 84H', '84', 'H', NULL, NULL, NULL, NULL, 2650.00, 10600.00, NULL, 'Michelin ENERGY XM2 +_EXM2+.png', NULL, 0),
(55, 3, 195, 80, 'R', 14, NULL, '195/80 R14 106/104R', '106/104', 'R', NULL, 'TL', 'C', '39/24', 2700.00, 10800.00, NULL, 'Michelin_AGILIS_3.png', NULL, NULL),
(56, 3, 205, 75, 'R', 14, NULL, '205/75 R14C 109/107R TL', '109/107', 'R', NULL, 'TL', 'C', NULL, 3300.00, 13200.00, NULL, 'Michelin AGILIS 3.png', NULL, 0),
(57, 3, 195, 80, 'R', 15, NULL, '195/80 R15C 108/106S TL', '108/106', 'S', NULL, 'TL', 'C', NULL, NULL, NULL, NULL, 'Michelin AGILIS 3.png', NULL, 0),
(58, 3, 205, 70, 'R', 15, NULL, '205/70 R15C 106/104S TL', '106/104', 'S', NULL, 'TL', 'C', '44/24', 3270.00, 11445.00, NULL, 'Michelin AGILIS 3.png', NULL, 0),
(59, 3, 215, 70, 'R', 15, NULL, '215/70 R15C 109/107S TL', '109/107', 'S', NULL, 'TL', 'C', '02/25', 3360.00, 11760.00, NULL, 'Michelin AGILIS 3.png', NULL, 0),
(60, 3, 215, 65, 'R', 16, NULL, '215/65 R16C 109/107T TL', '109/107', 'T', NULL, 'TL', 'C', '42/24', 3820.00, 13370.00, NULL, 'Michelin AGILIS 3.png', NULL, 0),
(61, 3, 215, 70, 'R', 16, '', '215/70 R16 108/106T', '108/106', 'T', NULL, 'TL', 'C', '32/23,06/24', 3450.00, 13800.00, NULL, 'Michelin AGILIS 3.png', NULL, 0),
(62, 3, 215, 75, 'R', 16, '', '215/75 R16 113/111T', '113/111', 'T', NULL, 'TL', 'C', '07/24,41/24,03/25', 4550.00, 18200.00, NULL, 'Michelin AGILIS 3.png', NULL, 0),
(63, 3, 235, 65, 'R', 16, '', '235/65 R16 115/113T', '115/113', 'T', NULL, 'TL', 'C', '06/23,35/24', 3400.00, 13600.00, NULL, 'Michelin AGILIS 3.png', NULL, 0),
(64, 3, 235, 60, 'R', 17, '', '235/60 R17 117/115T', '117/115', 'T', NULL, 'TL', 'C', '47/23,10/24', 3600.00, 14400.00, NULL, 'Michelin AGILIS 3.png', NULL, 0),
(65, 4, 205, 75, 'R', 14, NULL, '205/75 R14C 109/107P TL PR8', '109/107', 'P', 'PR8', 'TL', 'C', NULL, 3450.00, 13800.00, NULL, 'Michelin XCD 2.png', NULL, 0),
(66, 4, 215, 75, 'R', 14, NULL, '215/75 R14C 112/110P TL PR8', '112/110', 'P', 'PR8', 'TL', 'C', NULL, 3850.00, 15400.00, NULL, 'Michelin XCD 2.png', NULL, 0),
(67, 4, 225, 75, 'R', 14, NULL, '225/75 R14C 115/113P TL PR8', '115/113', 'P', 'PR8', 'TL', 'C', NULL, 4650.00, 18600.00, NULL, 'Michelin XCD 2.png', NULL, 0),
(68, 4, 205, 70, 'R', 15, NULL, '205/70 R15C 106/104S TL PR8', '106/104', 'S', 'PR8', 'TL', 'C', NULL, 3900.00, 15600.00, NULL, 'Michelin XCD 2.png', NULL, 0),
(69, 4, 225, 75, 'R', 15, NULL, '225/75 R15C 116/114Q TL PR8', '116/114', 'Q', 'PR8', 'TL', 'C', NULL, 4950.00, 19800.00, NULL, 'Michelin XCD 2.png', NULL, 0),
(70, 5, 205, 70, 'R', 15, NULL, '205/70 R15 96H TL', '96', 'H', NULL, 'TL', NULL, NULL, 4650.00, 18600.00, NULL, 'Michelin PRIMACRY SUV+.png', NULL, 0),
(71, 5, 215, 70, 'R', 16, NULL, '215/70 R16 100H TL', '100', 'H', NULL, 'TL', NULL, NULL, 5750.00, 23000.00, NULL, 'Michelin PRIMACRY SUV+.png', NULL, 0),
(72, 5, 215, 65, 'R', 16, NULL, '215/65 R16 102H TL', '102', 'H', NULL, 'TL', NULL, NULL, 5000.00, 20000.00, NULL, 'Michelin PRIMACRY SUV+.png', NULL, 0),
(73, 5, 235, 70, 'R', 16, NULL, '235/70 R16 106T TL', '106', 'H', NULL, 'TL', NULL, NULL, 6800.00, 27200.00, NULL, 'Michelin PRIMACRY SUV+.png', NULL, 0),
(74, 5, 245, 70, 'R', 16, 'XL', '245/70 R16 111H Extra Load TL', '111', 'H', NULL, 'TL', NULL, '06/24,10/24', 5450.00, 21800.00, NULL, 'Michelin PRIMACRY SUV+.png', NULL, 0),
(75, 5, 265, 70, 'R', 16, NULL, '265/70 R16 106H TL', '112', 'H', NULL, 'TL', NULL, '42/23,12/24', 5450.00, 21800.00, NULL, 'Michelin PRIMACRY SUV+.png', NULL, 0),
(76, 5, 225, 65, 'R', 17, 'XL', '225/65 R17 106H Extra Load TL', '106', 'H', NULL, 'TL', NULL, '08/24,19/24', 5850.00, 23400.00, NULL, 'Michelin PRIMACRY SUV+.png', NULL, 0),
(77, 5, 235, 60, 'R', 17, NULL, '235/60 R17 102V TL', '102', 'V', NULL, 'TL', NULL, '07/24', 7550.00, 30200.00, NULL, 'Michelin PRIMACRY SUV+.png', NULL, 0),
(78, 5, 235, 65, 'R', 17, 'XL', '235/65 R17 102V Extra Load TL', '108', 'V', NULL, 'TL', NULL, '08/23', 6750.00, 27000.00, NULL, 'Michelin PRIMACRY SUV+.png', NULL, 0),
(79, 5, 265, 65, 'R', 17, NULL, '265/65 R17 112H TL', '112', 'H', NULL, 'TL', NULL, '11/24', 5950.00, 23800.00, NULL, 'Michelin PRIMACRY SUV+.png', NULL, 0),
(80, 5, 275, 65, 'R', 17, NULL, '275/65 R17 115H TL', '115', 'H', NULL, 'TL', NULL, NULL, 8550.00, 34200.00, NULL, 'Michelin PRIMACRY SUV+.png', NULL, 0),
(81, 5, 215, 50, 'R', 18, NULL, '215/50 R18 92V TL', '92', 'V', NULL, 'TL', NULL, NULL, 6250.00, 25000.00, NULL, 'Michelin PRIMACRY SUV+.png', NULL, 0),
(82, 5, 225, 55, 'R', 18, NULL, '225/55 R18 98V TL', '98', 'V', NULL, 'TL', NULL, '07/23', 6800.00, 27200.00, NULL, 'Michelin PRIMACRY SUV+.png', NULL, 0),
(83, 5, 235, 55, 'R', 18, 'XL', '235/55 R18 104V EXTRA LOAD TL', '104', 'V', NULL, 'TL', NULL, '09/23,24/24', 7300.00, 29200.00, NULL, 'Michelin PRIMACRY SUV+.png', NULL, 0),
(84, 5, 235, 60, 'R', 18, NULL, '235/60 R18 103V TL', '103', 'V', NULL, 'TL', NULL, '23/23,24/24', 7200.00, 28800.00, NULL, 'Michelin PRIMACRY SUV+.png', NULL, 0),
(85, 5, 235, 65, 'R', 18, NULL, '235/65 R18 106H TL', '106', 'H', NULL, 'TL', NULL, NULL, 7300.00, 29200.00, NULL, 'Michelin PRIMACRY SUV+.png', NULL, 0),
(86, 11, 195, NULL, 'R', 14, '', '195 R14C 106/104R 8PR', '106/104', 'R', '8PR', NULL, 'C', NULL, 2300.00, NULL, 3000.00, 'Maxxis MCV5.jpg', NULL, 0),
(87, 11, 225, 75, 'R', 14, NULL, '225/75 R14 8PR', NULL, NULL, '8PR', NULL, NULL, NULL, 2950.00, NULL, NULL, 'Maxxis MCV5.jpg', NULL, 0),
(88, 11, 205, 70, 'R', 15, '', '205/70 R15C 106/104R 8PR', '106/104', 'R', '8PR', NULL, 'C', NULL, 2450.00, NULL, 3200.00, 'Maxxis MCV5.jpg', NULL, 0),
(89, 11, 215, 70, 'R', 15, '', '215/70 R15C 109/107S 8PR', '109/107', 'S', '8PR', NULL, 'C', NULL, 2500.00, NULL, 3250.00, 'Maxxis MCV5.jpg', NULL, 0),
(90, 11, 215, 65, 'R', 16, '', '215/65 R16C 109/107T', '109/107', 'T', NULL, NULL, 'C', NULL, 3000.00, NULL, 3900.00, 'Maxxis MCV5.jpg', NULL, 0),
(91, 11, 215, 70, 'R', 16, '', '215/70 R16C 108/106T 25/22', '108/106', 'T', NULL, NULL, 'C', '25/22', 2950.00, NULL, 3850.00, 'Maxxis MCV5.jpg', NULL, 0),
(92, 11, 215, 75, 'R', 16, '', '215/75 R16C 113/111S 8PR 04/24', '113/111', 'S', '8PR', NULL, 'C', '04/24', 3200.00, NULL, 4200.00, 'Maxxis MCV5.jpg', NULL, 0),
(93, 11, 225, 70, 'R', 15, '', '225/70 R15C 112/100S 8PR 23/23', '112/100', 'S', '8PR', NULL, 'C', '23/23', 3100.00, NULL, 4050.00, 'Maxxis MCV5.jpg', NULL, 0),
(94, 11, 225, 75, 'R', 15, NULL, '225/75 R15 8PR 06/24', NULL, NULL, '8PR', NULL, NULL, '06/24', 3100.00, NULL, NULL, 'Maxxis MCV5.jpg', NULL, 0),
(95, 11, 235, 65, 'R', 16, '', '235/65 R16C 115/113T 8PR', '115/113', 'T', '8PR', NULL, 'C', NULL, 3250.00, NULL, 4250.00, 'Maxxis MCV5.jpg', NULL, 0),
(96, 13, 155, 80, 'R', 12, NULL, '155/80 R12 77H', '77', 'H', NULL, NULL, NULL, NULL, 1000.00, NULL, NULL, 'MAXXIS MA-P3.png', NULL, 0),
(97, 13, 185, 70, 'R', 13, NULL, '185/70 R13 86H', '86', 'H', NULL, NULL, NULL, NULL, 1000.00, NULL, NULL, 'MAXXIS MA-P3.png', NULL, 0),
(98, 13, 185, 65, 'R', 14, NULL, '185/65 R14 86H', '86', 'H', NULL, NULL, NULL, NULL, 1000.00, NULL, NULL, 'MAXXIS MA-P3.png', NULL, 0),
(99, 13, 165, 80, 'R', 15, NULL, '165/80 R15 83T', '83', 'T', NULL, NULL, NULL, NULL, 1200.00, NULL, NULL, 'MAXXIS MA-P3.png', NULL, 0),
(100, 13, 185, 60, 'R', 15, NULL, '185/60 R15 88H', '88', 'H', NULL, NULL, NULL, '21/24', 1450.00, NULL, 1800.00, 'MAXXIS MA-P3.png', NULL, 0),
(101, 13, 185, 65, 'R', 15, NULL, '185/65 R15 88H', '88', 'H', NULL, NULL, NULL, NULL, 1000.00, NULL, NULL, 'MAXXIS MA-P3.png', NULL, 0),
(102, 13, 205, 55, 'R', 16, NULL, '205/55 R16 91V', '91', 'V', NULL, NULL, NULL, NULL, 1500.00, NULL, NULL, 'MAXXIS MA-P3.png', NULL, 0),
(103, 13, 225, 75, 'R', 15, NULL, '225/75 R15', NULL, NULL, NULL, NULL, NULL, NULL, 1200.00, NULL, NULL, 'MAXXIS MA-P3.png', NULL, 0),
(104, 13, 225, 70, 'R', 15, NULL, '225/70 R15', NULL, NULL, NULL, NULL, NULL, NULL, 1200.00, NULL, NULL, 'MAXXIS MA-P3.png', NULL, 0),
(105, 14, 175, 65, 'R', 15, NULL, '175/65 R15 84T', '84', 'T', NULL, NULL, NULL, NULL, 2200.00, NULL, 2850.00, 'Maxxis MA307.jpg', NULL, 0),
(106, 14, 165, 70, 'R', 14, NULL, '165/70 R14 81S', '81', 'S', NULL, NULL, NULL, NULL, 2050.00, NULL, 2650.00, 'Maxxis MA307.jpg', NULL, 0),
(107, 15, 195, NULL, 'R', 14, NULL, '195 R14 8PR', NULL, NULL, 'PR8', NULL, NULL, NULL, 1950.00, NULL, NULL, 'Maxxis MA-579.jpg', NULL, 0),
(108, 15, 205, 70, 'R', 15, NULL, '205/70 R15 8PR', NULL, NULL, 'PR8', NULL, NULL, '18/24', 220.00, NULL, 2850.00, 'Maxxis MA-579.jpg', NULL, 0),
(109, 15, 215, 70, 'R', 15, NULL, '215/70 R15 8PR', NULL, NULL, 'PR8', NULL, NULL, NULL, 2350.00, NULL, 3050.00, 'Maxxis MA-579.jpg', NULL, 0),
(110, 15, 215, 65, 'R', 16, NULL, '215/65 R16 8PR', NULL, NULL, 'PR8', NULL, NULL, '34/23,09/24', 2850.00, NULL, 3700.00, 'Maxxis MA-579.jpg', NULL, 0),
(113, 16, 165, NULL, 'R', 14, '', '165 R14C 97/95N 8PR', '97/95', 'N', '8PR', NULL, NULL, NULL, 2900.00, NULL, 3700.00, 'Maxxis UE-168.jpg', NULL, 0),
(114, 16, 185, NULL, 'R', 14, '', '185 R14C 99/97N 6PR 13/22', '99/97', 'N', '6PR', NULL, NULL, '13/22', 3050.00, NULL, 3900.00, 'Maxxis UE-168.jpg', NULL, 0),
(135, 17, 195, 50, 'R', 15, NULL, '195/50 R15 86V', '86', 'V', NULL, NULL, NULL, NULL, 2050.00, NULL, 2050.00, 'Maxxis i-PRO.jpg', NULL, 0),
(136, 17, 195, 55, 'R', 15, NULL, '195/55 R15 85V', '85', 'V', NULL, NULL, NULL, NULL, 2050.00, NULL, 2050.00, 'Maxxis i-PRO.jpg', NULL, 0),
(137, 17, 215, 65, 'R', 15, NULL, '215/65 R15 100V', '100', 'V', NULL, NULL, NULL, NULL, 2400.00, NULL, 2400.00, 'Maxxis i-PRO.jpg', NULL, 0),
(138, 17, 205, 45, 'R', 16, NULL, '205/45 ZR16 87W', '87', 'W', NULL, NULL, NULL, NULL, 2450.00, NULL, 2450.00, 'Maxxis i-PRO.jpg', NULL, 1),
(139, 17, 205, 55, 'R', 16, 'XL', '205/55 ZR16 94W', '94', 'W', NULL, NULL, NULL, NULL, 2450.00, NULL, 2450.00, 'Maxxis i-PRO.jpg', NULL, 1),
(140, 17, 205, 40, 'R', 17, NULL, '205/40 ZR17 84W', '84', 'W', NULL, NULL, NULL, NULL, 2550.00, NULL, 2550.00, 'Maxxis i-PRO.jpg', NULL, 1),
(141, 17, 205, 45, 'R', 17, NULL, '205/45 ZR17 88W', '88', 'W', NULL, NULL, NULL, NULL, 2450.00, NULL, 2450.00, 'Maxxis i-PRO.jpg', NULL, 1),
(142, 17, 215, 45, 'R', 17, NULL, '215/45 ZR17 91W', '91', 'W', NULL, NULL, NULL, NULL, 2550.00, NULL, 2550.00, 'Maxxis i-PRO.jpg', NULL, 1),
(143, 17, 215, 50, 'R', 17, NULL, '215/50 ZR17', '95', 'W', NULL, NULL, NULL, NULL, 2600.00, NULL, 2600.00, 'Maxxis i-PRO.jpg', NULL, 1),
(144, 17, 215, 55, 'R', 17, NULL, '215/55 ZR17 98W', '98', 'W', NULL, NULL, NULL, NULL, 2650.00, NULL, 2650.00, 'Maxxis i-PRO.jpg', NULL, 1),
(145, 17, 225, 45, 'R', 17, NULL, '225/45 ZR17 94W', '94', 'W', NULL, NULL, NULL, NULL, 3000.00, NULL, 3000.00, 'Maxxis i-PRO.jpg', NULL, 1),
(146, 17, 225, 50, 'R', 17, NULL, '225/50 ZR17 98W', '98', 'W', NULL, NULL, NULL, NULL, 2800.00, NULL, 2800.00, 'Maxxis i-PRO.jpg', NULL, 1),
(147, 17, 225, 55, 'R', 17, NULL, '225/55 ZR17 101W', '101', 'W', NULL, NULL, NULL, NULL, 2850.00, NULL, 2850.00, 'Maxxis i-PRO.jpg', NULL, 1),
(148, 17, 235, 45, 'R', 17, NULL, '235/45 ZR17 97W', '97', 'W', NULL, NULL, NULL, NULL, 3450.00, NULL, 3450.00, 'Maxxis i-PRO.jpg', NULL, 1),
(149, 17, 225, 40, 'R', 18, 'XL', '225/40 ZR18 92W XL', '92', 'W', NULL, NULL, NULL, NULL, 3150.00, NULL, 3150.00, 'Maxxis i-PRO.jpg', NULL, 1),
(150, 17, 225, 45, 'R', 18, 'XL', '225/45 ZR18 95W XL', '95', 'W', NULL, NULL, NULL, NULL, 3300.00, NULL, 3300.00, 'Maxxis i-PRO.jpg', NULL, 1),
(151, 17, 235, 40, 'R', 18, 'XL', '235/40 ZR18 95W XL', '95', 'W', NULL, NULL, NULL, NULL, 3300.00, NULL, 3300.00, 'Maxxis i-PRO.jpg', NULL, 1),
(152, 17, 235, 45, 'R', 18, 'XL', '235/45 ZR18 98W XL', '98', 'W', NULL, NULL, NULL, NULL, 3500.00, NULL, 3500.00, 'Maxxis i-PRO.jpg', NULL, 1),
(153, 17, 235, 50, 'R', 18, 'XL', '235/50 ZR18 101W XL', '101', 'W', NULL, NULL, NULL, NULL, 3450.00, NULL, 3450.00, 'Maxxis i-PRO.jpg', NULL, 1),
(154, 17, 255, 45, 'R', 18, 'XL', '255/45 ZR18 103W XL', '103', 'W', NULL, NULL, NULL, NULL, 3600.00, NULL, 3600.00, 'Maxxis i-PRO.jpg', NULL, 1),
(155, 19, 235, 55, 'R', 18, NULL, '235/55 R18 104V', '104', 'V', NULL, NULL, NULL, NULL, 2950.00, NULL, 3800.00, 'MAXXIS MA-S2.png', NULL, 0),
(156, 19, 265, 60, 'R', 18, NULL, '265/60 R18 110H', '110', 'H', NULL, NULL, NULL, NULL, 3950.00, NULL, 5100.00, 'MAXXIS MA-S2.png', NULL, 0),
(157, 19, 265, 50, 'R', 20, NULL, '265/50 R20 112V', '112', 'V', NULL, NULL, NULL, NULL, 4250.00, NULL, 5500.00, 'MAXXIS MA-S2.png', NULL, 0),
(158, 18, 205, 55, 'R', 16, NULL, '205/55 R16 91V', '91', 'V', NULL, NULL, NULL, NULL, 2600.00, NULL, 3400.00, 'Maxxis MS2.jpg', NULL, 0),
(159, 18, 215, 55, 'R', 16, 'XL', '215/55 R16 97W XL', '97', 'W', NULL, NULL, NULL, NULL, 2600.00, NULL, 3400.00, 'Maxxis MS2.jpg', NULL, 0),
(160, 18, 215, 60, 'R', 16, NULL, '215/60 R16 95V', '95', 'V', NULL, NULL, NULL, NULL, 2650.00, NULL, 3450.00, 'Maxxis MS2.jpg', NULL, 0),
(161, 18, 215, 45, 'R', 17, 'XL', '215/45 R17 91V XL', '91', 'V', NULL, NULL, NULL, NULL, 2800.00, NULL, 3650.00, 'Maxxis MS2.jpg', NULL, 0),
(162, 18, 215, 50, 'R', 17, 'XL', '215/50 R17 95W XL', '95', 'W', NULL, NULL, NULL, NULL, 3000.00, NULL, 3900.00, 'Maxxis MS2.jpg', NULL, 0),
(163, 18, 215, 55, 'R', 17, NULL, '215/55 R17 94V', '94', 'V', NULL, NULL, NULL, NULL, 3100.00, NULL, 4000.00, 'Maxxis MS2.jpg', NULL, 0),
(164, 18, 225, 50, 'R', 17, 'XL', '225/50 R17 98V XL', '98', 'V', NULL, NULL, NULL, NULL, 3150.00, NULL, 4100.00, 'Maxxis MS2.jpg', NULL, 0),
(165, 20, 225, 70, 'R', 15, NULL, '225/70 R15 100T', '100', 'T', NULL, NULL, NULL, NULL, 3100.00, NULL, 4050.00, 'Maxxis HT770.jpg', NULL, 0),
(166, 20, 245, 70, 'R', 16, NULL, '245/70 R16 111T', '111', 'T', NULL, NULL, NULL, '19/22', 3250.00, NULL, 4250.00, 'Maxxis HT770.jpg', NULL, 0),
(167, 20, 265, 70, 'R', 16, NULL, '265/70 R16 112T', '112', 'T', NULL, NULL, NULL, '11/23', 3500.00, NULL, 4600.00, 'Maxxis HT770.jpg', NULL, 0),
(168, 20, 225, 65, 'R', 17, NULL, '225/65 R17 102H', '102', 'H', NULL, NULL, NULL, NULL, 3850.00, NULL, 5050.00, 'Maxxis HT770.jpg', NULL, 0),
(169, 20, 265, 65, 'R', 17, NULL, '265/65 R17 112S', '112', 'S', NULL, NULL, NULL, '15/22', 3700.00, NULL, 4850.00, 'Maxxis HT770.jpg', NULL, 0),
(170, 20, 265, 60, 'R', 18, NULL, '265/60 R18 114H', '114', 'H', NULL, NULL, NULL, '22/22', 4200.00, NULL, 5500.00, 'Maxxis HT770.jpg', NULL, 0),
(171, 21, 225, 75, 'R', 15, NULL, '225/75 R15 6PR', NULL, NULL, '6PR', NULL, NULL, NULL, 3300.00, NULL, 4300.00, 'Maxxis AT700.jpg', NULL, 0),
(172, 21, 235, 70, 'R', 15, NULL, '235/70 R15 6PR', NULL, NULL, '6PR', NULL, NULL, NULL, 3300.00, NULL, 4300.00, 'Maxxis AT700.jpg', NULL, 0),
(173, 21, 235, 75, 'R', 15, NULL, '235/75 R15 6PR', NULL, NULL, '6PR', NULL, NULL, NULL, 3500.00, NULL, 4600.00, 'Maxxis AT700.jpg', NULL, 0),
(174, 21, 255, 70, 'R', 15, NULL, '255/70 R15 108T', '108', 'T', NULL, NULL, NULL, '46/23 /24', 3600.00, NULL, 4700.00, 'Maxxis AT700.jpg', NULL, NULL),
(175, 21, 245, 70, 'R', 16, NULL, '245/70 R16 111S', '111', 'S', NULL, NULL, NULL, '37/23', 3350.00, NULL, 4400.00, 'Maxxis AT700.jpg', NULL, 0),
(176, 21, 265, 70, 'R', 16, NULL, '265/70 R16 112S', '112', 'S', NULL, NULL, NULL, '14/23', 3450.00, NULL, 4500.00, 'Maxxis AT700.jpg', NULL, 0),
(177, 21, 265, 75, 'R', 16, NULL, '265/75 R16 116S', '116', 'S', NULL, NULL, NULL, NULL, 4150.00, NULL, 5450.00, 'Maxxis AT700.jpg', NULL, 0),
(178, 21, 265, 65, 'R', 17, NULL, '265/65 R17 112S', '112', 'S', NULL, NULL, NULL, '02/24', 4000.00, NULL, 5250.00, 'Maxxis AT700.jpg', NULL, 0),
(179, 21, 265, 60, 'R', 18, NULL, '265/60 R18 110S', '110', 'S', NULL, NULL, NULL, NULL, 4150.00, NULL, 5450.00, 'Maxxis AT700.jpg', NULL, 0),
(180, 21, 265, 50, 'R', 20, NULL, '265/50 R20 112V', '112', 'V', NULL, NULL, NULL, NULL, 4550.00, NULL, 6000.00, 'Maxxis AT700.jpg', NULL, 0),
(181, 21, 265, 55, 'R', 20, NULL, '265/55 R20 113H', '113', 'H', NULL, NULL, NULL, NULL, 5150.00, NULL, 6800.00, 'Maxxis AT700.jpg', NULL, 0),
(182, 22, 245, 70, 'R', 16, NULL, '245/70 R16 10PR', NULL, NULL, '10PR', NULL, NULL, NULL, 4550.00, NULL, 6000.00, 'Maxxis AT811.jpg', NULL, 0),
(183, 22, 265, 70, 'R', 16, NULL, '265/70 R16 10PR', NULL, NULL, '10PR', NULL, NULL, NULL, 4850.00, NULL, 6400.00, 'Maxxis AT811.jpg', NULL, 0),
(184, 22, 265, 75, 'R', 16, NULL, '265/75 R16 8PR', NULL, NULL, '8PR', NULL, NULL, NULL, 5200.00, NULL, 6850.00, 'Maxxis AT811.jpg', NULL, 0),
(185, 22, 285, 75, 'R', 16, NULL, '285/75 R16 6PR', NULL, NULL, '6PR', NULL, NULL, NULL, 5500.00, NULL, 7250.00, 'Maxxis AT811.jpg', NULL, 0),
(186, 22, 265, 65, 'R', 17, NULL, '265/65 R17 10PR', NULL, NULL, '10PR', NULL, NULL, NULL, 5350.00, NULL, 7050.00, 'Maxxis AT811.jpg', NULL, 0),
(187, 22, 265, 70, 'R', 17, NULL, '265/70 R17 10PR', NULL, NULL, '10PR', NULL, NULL, NULL, 5400.00, NULL, 7100.00, 'Maxxis AT811.jpg', NULL, 0),
(188, 22, 285, 70, 'R', 17, NULL, '285/70 R17 10PR', NULL, NULL, '10PR', NULL, NULL, NULL, 6000.00, NULL, 7900.00, 'Maxxis AT811.jpg', NULL, 0),
(189, 22, 265, 60, 'R', 18, NULL, '265/60 R18 10PR', NULL, NULL, '10PR', NULL, NULL, NULL, 5600.00, NULL, 7400.00, 'Maxxis AT811.jpg', NULL, 0),
(196, 7, 205, 55, 'R', 16, 'XL', '205/55 ZR16 XL TL', '94', 'W', NULL, 'TL', NULL, NULL, 4550.00, 18200.00, NULL, 'BFGoodrich G-FORCE PHENOM.png', NULL, 1),
(197, 7, 205, 50, 'R', 17, 'XL', '205/50 ZR17 XL TL', '93', 'W', NULL, 'TL', NULL, NULL, 4850.00, 19400.00, NULL, 'BFGoodrich G-FORCE PHENOM.png', NULL, 1),
(198, 7, 215, 45, 'R', 17, 'XL', '215/45 ZR17 XL TL', '91', 'W', NULL, 'TL', NULL, NULL, 4650.00, 18600.00, NULL, 'BFGoodrich G-FORCE PHENOM.png', NULL, 1),
(199, 7, 215, 50, 'R', 17, 'XL', '215/50 ZR17 XL TL', '95', 'Y', NULL, 'TL', NULL, NULL, 4950.00, 19800.00, NULL, 'BFGoodrich G-FORCE PHENOM.png', NULL, 1),
(200, 7, 215, 55, 'R', 17, 'XL', '215/55 ZR17 XL TL', '98', 'W', NULL, 'TL', NULL, NULL, 4950.00, 19800.00, NULL, 'BFGoodrich G-FORCE PHENOM.png', NULL, 1),
(201, 7, 225, 55, 'R', 17, 'XL', '225/55 ZRR17 101W XL', '101', 'W', NULL, NULL, NULL, NULL, 4950.00, 19800.00, NULL, 'BFGoodrich G-FORCE PHENOM.png', NULL, 1),
(202, 12, 195, 55, 'R', 16, NULL, '195/55 R16', NULL, NULL, NULL, NULL, NULL, '02/24', 2500.00, NULL, 3200.00, 'MAXXIS PRO-R1.png', 'ฮิตมาก', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `tire_models`
--

CREATE TABLE `tire_models` (
  `model_id` int(11) NOT NULL,
  `brand_id` int(11) DEFAULT NULL,
  `model_name` varchar(100) DEFAULT NULL,
  `tire_category` varchar(50) DEFAULT NULL,
  `description` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `tire_models`
--

INSERT INTO `tire_models` (`model_id`, `brand_id`, `model_name`, `tire_category`, `description`) VALUES
(1, 1, 'EXM2+', 'Comfort', NULL),
(2, 1, 'ENERGY XM2+', 'Comfort', NULL),
(3, 1, 'AGILIS3', 'Commercial / Van', NULL),
(4, 1, 'XCD2', 'Commercial / Van', NULL),
(5, 1, 'PRIMACRY SUV+', 'Comfort / SUV', NULL),
(7, 2, 'G-FORCE PHENOM', 'Performance', NULL),
(8, 2, 'ADVANTAGE TOURING', 'Comfort', NULL),
(9, 2, 'TRAIL TERRAIN', 'All-Terrain (AT)', NULL),
(10, 2, 'KO3', 'All-Terrain (AT)', NULL),
(11, 3, 'MCV5', 'Commercial / Van', NULL),
(12, 3, 'PRO-R1', 'Comfort', NULL),
(13, 3, 'MAP3', 'Standard / Economy', NULL),
(14, 3, 'MA-307', 'Standard / Economy', NULL),
(15, 3, 'MA-579', 'Standard / Economy', NULL),
(16, 3, 'UE-168', 'Commercial / Van', NULL),
(17, 3, 'i-PRO', 'Performance', NULL),
(18, 3, 'MS2', 'Comfort / SUV', NULL),
(19, 3, 'MA-S2', 'Comfort / SUV', NULL),
(20, 3, 'HT-770', 'Highway / SUV', NULL),
(21, 3, 'AT700', 'All-Terrain (AT)', NULL),
(22, 3, 'AT-811', 'All-Terrain (AT)', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `tire_model_targets`
--

CREATE TABLE `tire_model_targets` (
  `model_id` int(11) NOT NULL,
  `usage_type_id` int(11) NOT NULL,
  `vehicle_type_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `tire_model_targets`
--

INSERT INTO `tire_model_targets` (`model_id`, `usage_type_id`, `vehicle_type_id`) VALUES
(1, 1, 1),
(1, 7, 1),
(1, 9, 1),
(1, 13, 1),
(2, 1, 1),
(2, 7, 1),
(2, 9, 1),
(2, 13, 1),
(3, 5, 3),
(3, 6, 3),
(3, 15, 3),
(4, 5, 3),
(4, 6, 3),
(4, 15, 3),
(5, 5, 2),
(5, 12, 2),
(5, 13, 2),
(7, 2, 1),
(7, 14, 1),
(8, 1, 1),
(8, 9, 1),
(8, 13, 1),
(9, 3, 2),
(9, 4, 2),
(9, 5, 2),
(9, 8, 2),
(10, 3, 2),
(10, 4, 2),
(10, 5, 2),
(10, 8, 2),
(11, 1, 3),
(11, 5, 3),
(11, 6, 3),
(11, 15, 3),
(11, 16, 3),
(12, 1, 1),
(12, 13, 1),
(13, 1, 1),
(13, 10, 1),
(13, 11, 1),
(14, 1, 1),
(14, 10, 1),
(14, 11, 1),
(15, 1, 1),
(15, 10, 1),
(15, 11, 1),
(16, 5, 3),
(16, 6, 3),
(16, 15, 3),
(17, 2, 1),
(17, 14, 1),
(18, 1, 2),
(18, 13, 2),
(19, 1, 2),
(19, 13, 2),
(20, 5, 2),
(20, 12, 2),
(21, 3, 2),
(21, 4, 2),
(21, 5, 2),
(21, 8, 2),
(22, 3, 2),
(22, 4, 2),
(22, 5, 2),
(22, 8, 2);

-- --------------------------------------------------------

--
-- Table structure for table `usage_types`
--

CREATE TABLE `usage_types` (
  `usage_type_id` int(11) NOT NULL,
  `usage_type_name` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `usage_types`
--

INSERT INTO `usage_types` (`usage_type_id`, `usage_type_name`) VALUES
(1, 'ขับในเมือง'),
(2, 'ขับเร็ว'),
(3, 'ลุยฝน'),
(4, 'ออฟโรด'),
(5, 'เดินทางไกล'),
(6, 'ใช้งานหนัก'),
(7, 'ขับทางชัน / โค้งเยอะ'),
(8, 'ขับในหิมะ / โคลนลึก'),
(9, 'ขับกลางคืน / แสงน้อยบ่อย'),
(10, 'รถ Eco-Car'),
(11, 'รถไฟฟ้า (EV)'),
(12, 'รถ SUV / PPV'),
(13, 'ต้องการความนุ่มเงียบ'),
(14, 'สมรรถนะสูง (High Performance)'),
(15, 'รถติดประจำ / ขับช้า'),
(16, 'ยางใช้งานทั่วไป');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `user_id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `role` enum('admin','staff','owner','customer') NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `customer_id` int(11) DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_id`, `username`, `password_hash`, `role`, `name`, `customer_id`, `created_at`) VALUES
(1, 'admin01', '1234', 'admin', 'แอดมินระบบ', NULL, '2025-06-23 17:38:39'),
(2, 'staff01', '1234', 'staff', 'คุณพนักงาน', NULL, '2025-06-23 17:38:39'),
(3, 'owner01', '1234', 'owner', 'เจ้าของกิจการ', NULL, '2025-06-23 17:38:39'),
(4, 'somchai12', '1234', 'customer', 'สมชาย ใจดี', 1, '2025-06-23 17:44:54');

-- --------------------------------------------------------

--
-- Table structure for table `vehicles`
--

CREATE TABLE `vehicles` (
  `vehicle_id` int(11) NOT NULL,
  `customer_id` int(11) DEFAULT NULL,
  `vehicle_type_id` int(11) DEFAULT NULL,
  `color` varchar(50) DEFAULT NULL,
  `license_plate` varchar(20) DEFAULT NULL,
  `license_province` varchar(100) DEFAULT NULL,
  `engine_type_name` varchar(50) DEFAULT NULL,
  `production_year` year(4) DEFAULT NULL,
  `brand_name` varchar(100) DEFAULT NULL,
  `model_name` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `vehicles`
--

INSERT INTO `vehicles` (`vehicle_id`, `customer_id`, `vehicle_type_id`, `color`, `license_plate`, `license_province`, `engine_type_name`, `production_year`, `brand_name`, `model_name`) VALUES
(1, 1, 1, 'ขาว', 'กข 1234', 'สมุทรปราการ', 'ดีเซล', '2024', 'Mitsubishi', 'Mirage'),
(2, 2, 2, 'ดำ', 'ขย 5678', 'ลพบุรี', 'เบนซิน', '1990', 'BMW', 'iX3'),
(3, 3, 3, 'น้ำเงิน', 'งท 9012', 'ชลบุรี', 'ไฮบริด', '2022', 'Ford', 'Everest'),
(4, 4, 1, 'แดง', 'ฉพ 3456', 'ชลบุรี', 'เบนซิน', '1990', 'Honda', 'Civic'),
(5, 5, 2, 'เทา', 'ตค 7890', 'พระนครศรีอยุธยา', 'ดีเซล', '1988', 'Nissan', 'Note'),
(6, 9, 1, 'ดำ', '1กฮ 6734', 'บุรีรัมย์', 'ดีเซล', '2022', 'BMW', 'X1'),
(7, 9, 3, 'บลอน', 'บษ 9990', 'กรุงเทพมหานคร', 'เบนซิน', '2016', 'Isuzu', 'D-Max');

-- --------------------------------------------------------

--
-- Table structure for table `vehicle_types`
--

CREATE TABLE `vehicle_types` (
  `vehicle_type_id` int(11) NOT NULL,
  `vehicle_type_name` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `vehicle_types`
--

INSERT INTO `vehicle_types` (`vehicle_type_id`, `vehicle_type_name`) VALUES
(1, 'รถเก๋ง'),
(2, 'SUV'),
(3, 'กระบะ/รถตู้');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `addresses`
--
ALTER TABLE `addresses`
  ADD PRIMARY KEY (`address_id`),
  ADD KEY `customer_id` (`customer_id`);

--
-- Indexes for table `bookings`
--
ALTER TABLE `bookings`
  ADD PRIMARY KEY (`booking_id`),
  ADD KEY `customer_id` (`customer_id`),
  ADD KEY `vehicle_id` (`vehicle_id`);

--
-- Indexes for table `booking_items`
--
ALTER TABLE `booking_items`
  ADD PRIMARY KEY (`item_id`),
  ADD KEY `booking_id` (`booking_id`),
  ADD KEY `service_id` (`service_id`),
  ADD KEY `tire_id` (`tire_id`);

--
-- Indexes for table `booking_item_options`
--
ALTER TABLE `booking_item_options`
  ADD PRIMARY KEY (`id`),
  ADD KEY `item_id` (`item_id`),
  ADD KEY `option_id` (`option_id`);

--
-- Indexes for table `brands`
--
ALTER TABLE `brands`
  ADD PRIMARY KEY (`brand_id`);

--
-- Indexes for table `customers`
--
ALTER TABLE `customers`
  ADD PRIMARY KEY (`customer_id`);

--
-- Indexes for table `page_views`
--
ALTER TABLE `page_views`
  ADD PRIMARY KEY (`page_id`);

--
-- Indexes for table `promotions`
--
ALTER TABLE `promotions`
  ADD PRIMARY KEY (`promotion_id`);

--
-- Indexes for table `roles`
--
ALTER TABLE `roles`
  ADD PRIMARY KEY (`role_id`);

--
-- Indexes for table `services`
--
ALTER TABLE `services`
  ADD PRIMARY KEY (`service_id`);

--
-- Indexes for table `service_options`
--
ALTER TABLE `service_options`
  ADD PRIMARY KEY (`option_id`),
  ADD KEY `fk_options_services` (`service_id`);

--
-- Indexes for table `service_tires`
--
ALTER TABLE `service_tires`
  ADD PRIMARY KEY (`id`),
  ADD KEY `booking_id` (`booking_id`),
  ADD KEY `tire_id` (`tire_id`);

--
-- Indexes for table `tires`
--
ALTER TABLE `tires`
  ADD PRIMARY KEY (`tire_id`),
  ADD KEY `fk_tires_model` (`model_id`);

--
-- Indexes for table `tire_models`
--
ALTER TABLE `tire_models`
  ADD PRIMARY KEY (`model_id`),
  ADD KEY `brand_id` (`brand_id`);

--
-- Indexes for table `tire_model_targets`
--
ALTER TABLE `tire_model_targets`
  ADD PRIMARY KEY (`model_id`,`usage_type_id`,`vehicle_type_id`),
  ADD KEY `usage_type_id` (`usage_type_id`),
  ADD KEY `vehicle_type_id` (`vehicle_type_id`);

--
-- Indexes for table `usage_types`
--
ALTER TABLE `usage_types`
  ADD PRIMARY KEY (`usage_type_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD KEY `customer_id` (`customer_id`);

--
-- Indexes for table `vehicles`
--
ALTER TABLE `vehicles`
  ADD PRIMARY KEY (`vehicle_id`),
  ADD KEY `customer_id` (`customer_id`),
  ADD KEY `vehicle_type_id` (`vehicle_type_id`);

--
-- Indexes for table `vehicle_types`
--
ALTER TABLE `vehicle_types`
  ADD PRIMARY KEY (`vehicle_type_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `addresses`
--
ALTER TABLE `addresses`
  MODIFY `address_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `bookings`
--
ALTER TABLE `bookings`
  MODIFY `booking_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `booking_items`
--
ALTER TABLE `booking_items`
  MODIFY `item_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=248;

--
-- AUTO_INCREMENT for table `booking_item_options`
--
ALTER TABLE `booking_item_options`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=44;

--
-- AUTO_INCREMENT for table `brands`
--
ALTER TABLE `brands`
  MODIFY `brand_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `customers`
--
ALTER TABLE `customers`
  MODIFY `customer_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `promotions`
--
ALTER TABLE `promotions`
  MODIFY `promotion_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `roles`
--
ALTER TABLE `roles`
  MODIFY `role_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `services`
--
ALTER TABLE `services`
  MODIFY `service_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=28;

--
-- AUTO_INCREMENT for table `service_options`
--
ALTER TABLE `service_options`
  MODIFY `option_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT for table `service_tires`
--
ALTER TABLE `service_tires`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `tires`
--
ALTER TABLE `tires`
  MODIFY `tire_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=204;

--
-- AUTO_INCREMENT for table `usage_types`
--
ALTER TABLE `usage_types`
  MODIFY `usage_type_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `vehicles`
--
ALTER TABLE `vehicles`
  MODIFY `vehicle_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `vehicle_types`
--
ALTER TABLE `vehicle_types`
  MODIFY `vehicle_type_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `addresses`
--
ALTER TABLE `addresses`
  ADD CONSTRAINT `addresses_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`customer_id`);

--
-- Constraints for table `bookings`
--
ALTER TABLE `bookings`
  ADD CONSTRAINT `bookings_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`customer_id`),
  ADD CONSTRAINT `bookings_ibfk_2` FOREIGN KEY (`vehicle_id`) REFERENCES `vehicles` (`vehicle_id`);

--
-- Constraints for table `booking_items`
--
ALTER TABLE `booking_items`
  ADD CONSTRAINT `booking_items_ibfk_1` FOREIGN KEY (`booking_id`) REFERENCES `bookings` (`booking_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `booking_items_ibfk_2` FOREIGN KEY (`service_id`) REFERENCES `services` (`service_id`) ON DELETE SET NULL,
  ADD CONSTRAINT `booking_items_ibfk_4` FOREIGN KEY (`tire_id`) REFERENCES `tires` (`tire_id`) ON DELETE SET NULL;

--
-- Constraints for table `booking_item_options`
--
ALTER TABLE `booking_item_options`
  ADD CONSTRAINT `booking_item_options_ibfk_1` FOREIGN KEY (`item_id`) REFERENCES `booking_items` (`item_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `booking_item_options_ibfk_2` FOREIGN KEY (`option_id`) REFERENCES `service_options` (`option_id`) ON DELETE CASCADE;

--
-- Constraints for table `service_options`
--
ALTER TABLE `service_options`
  ADD CONSTRAINT `fk_options_services` FOREIGN KEY (`service_id`) REFERENCES `services` (`service_id`),
  ADD CONSTRAINT `service_options_ibfk_1` FOREIGN KEY (`service_id`) REFERENCES `services` (`service_id`);

--
-- Constraints for table `service_tires`
--
ALTER TABLE `service_tires`
  ADD CONSTRAINT `service_tires_ibfk_1` FOREIGN KEY (`booking_id`) REFERENCES `bookings` (`booking_id`),
  ADD CONSTRAINT `service_tires_ibfk_2` FOREIGN KEY (`tire_id`) REFERENCES `tires` (`tire_id`);

--
-- Constraints for table `tires`
--
ALTER TABLE `tires`
  ADD CONSTRAINT `fk_tires_model` FOREIGN KEY (`model_id`) REFERENCES `tire_models` (`model_id`),
  ADD CONSTRAINT `tires_ibfk_1` FOREIGN KEY (`model_id`) REFERENCES `tire_models` (`model_id`);

--
-- Constraints for table `tire_models`
--
ALTER TABLE `tire_models`
  ADD CONSTRAINT `tire_models_ibfk_1` FOREIGN KEY (`brand_id`) REFERENCES `brands` (`brand_id`);

--
-- Constraints for table `tire_model_targets`
--
ALTER TABLE `tire_model_targets`
  ADD CONSTRAINT `tire_model_targets_ibfk_1` FOREIGN KEY (`model_id`) REFERENCES `tire_models` (`model_id`),
  ADD CONSTRAINT `tire_model_targets_ibfk_2` FOREIGN KEY (`usage_type_id`) REFERENCES `usage_types` (`usage_type_id`),
  ADD CONSTRAINT `tire_model_targets_ibfk_3` FOREIGN KEY (`vehicle_type_id`) REFERENCES `vehicle_types` (`vehicle_type_id`);

--
-- Constraints for table `users`
--
ALTER TABLE `users`
  ADD CONSTRAINT `users_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`customer_id`);

--
-- Constraints for table `vehicles`
--
ALTER TABLE `vehicles`
  ADD CONSTRAINT `vehicles_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`customer_id`),
  ADD CONSTRAINT `vehicles_ibfk_2` FOREIGN KEY (`vehicle_type_id`) REFERENCES `vehicle_types` (`vehicle_type_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
