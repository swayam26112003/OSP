-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 10, 2023 at 08:52 PM
-- Server version: 10.4.27-MariaDB
-- PHP Version: 8.0.25

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `osp_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `cart`
--

CREATE TABLE `cart` (
  `Cartid` int(11) NOT NULL,
  `Pid` int(11) NOT NULL,
  `userid` int(11) NOT NULL,
  `quantity` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `cart`
--

INSERT INTO `cart` (`Cartid`, `Pid`, `userid`, `quantity`) VALUES
(37, 20, 31, 4);

-- --------------------------------------------------------

--
-- Table structure for table `manager`
--

CREATE TABLE `manager` (
  `manager_id` int(11) NOT NULL,
  `name` text NOT NULL,
  `phone_num` varchar(20) NOT NULL,
  `email` varchar(100) NOT NULL,
  `DOB` date NOT NULL,
  `Gender` varchar(20) NOT NULL,
  `street` text NOT NULL,
  `city` text NOT NULL,
  `state` text NOT NULL,
  `pin` text NOT NULL,
  `password` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `manager`
--

INSERT INTO `manager` (`manager_id`, `name`, `phone_num`, `email`, `DOB`, `Gender`, `street`, `city`, `state`, `pin`, `password`) VALUES
(7, 'Aseem', '9988998898', 'aseem.anand.0609@gmail.com', '2002-09-06', 'Male', 'Shivaji Park', 'Delhi', 'Delhi', '110026', '$2b$12$GJ2KeWoipP4HCah5OTOLqeKFSRUOYTRbXgroPmk9jOwJf5C4Twp/W');

-- --------------------------------------------------------

--
-- Table structure for table `negotiations`
--

CREATE TABLE `negotiations` (
  `id` int(11) NOT NULL,
  `Pid` int(11) NOT NULL,
  `seller_id` int(11) NOT NULL,
  `buyer_id` int(11) NOT NULL,
  `Message` text NOT NULL,
  `price` int(11) NOT NULL DEFAULT -1,
  `sender_id` int(11) NOT NULL,
  `ismanager` int(11) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `negotiations`
--

INSERT INTO `negotiations` (`id`, `Pid`, `seller_id`, `buyer_id`, `Message`, `price`, `sender_id`, `ismanager`) VALUES
(48, 25, 30, 31, 'Hello, How old is the car?', -1, 31, 0),
(49, 25, 30, 31, '1 year', -1, 30, 0),
(50, 25, 30, 31, 'Since it\'s old, make it Rs 70,00,000', -1, 31, 0),
(51, 25, 30, 31, 'No the best I can do is Rs 80,00,000', -1, 30, 0),
(53, 25, 30, 31, 'I recommend Hrushikesh to make it Rs 78,00,000', -1, 7, 1),
(54, 25, 30, 31, 'Ok, I can do that', -1, 30, 0),
(55, 25, 30, 31, 'Final Price per product is 7800000\n Conversation ends here', 7800000, 30, 0);

-- --------------------------------------------------------

--
-- Table structure for table `orderdetails`
--

CREATE TABLE `orderdetails` (
  `oid` int(11) NOT NULL,
  `pid` int(11) NOT NULL,
  `cid` int(11) NOT NULL,
  `date` timestamp NOT NULL DEFAULT current_timestamp(),
  `quantity` int(11) NOT NULL,
  `Status` tinyint(1) NOT NULL,
  `Price` int(11) NOT NULL DEFAULT -1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `orderdetails`
--

INSERT INTO `orderdetails` (`oid`, `pid`, `cid`, `date`, `quantity`, `Status`, `Price`) VALUES
(75, 24, 31, '2023-04-10 17:51:06', 5, 0, -1),
(76, 25, 31, '2023-04-10 18:02:22', 1, 0, 7800000);

-- --------------------------------------------------------

--
-- Table structure for table `products`
--

CREATE TABLE `products` (
  `Pid` int(11) NOT NULL,
  `Name` text NOT NULL,
  `Sellerid` int(11) NOT NULL,
  `Price` int(11) NOT NULL,
  `Image_url` varchar(100) NOT NULL,
  `mfgdate` date NOT NULL,
  `mfgcompany` text NOT NULL,
  `sellercity` text NOT NULL,
  `quantity` int(11) NOT NULL,
  `Weight` double NOT NULL,
  `status` tinyint(1) NOT NULL,
  `Description` text NOT NULL,
  `Category` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`Pid`, `Name`, `Sellerid`, `Price`, `Image_url`, `mfgdate`, `mfgcompany`, `sellercity`, `quantity`, `Weight`, `status`, `Description`, `Category`) VALUES
(20, 'HP Laptop', 29, 60000, 'laptop.jpg', '2022-11-15', 'HP Limited', 'Kolkata', 10, 2.5, 1, 'Brand new Laptop with i7 processor,16 gb RAM and much more', 'Electronics'),
(21, 'Suit', 29, 1500, 'cloth.jpg', '2023-04-01', 'Raymond', 'Kolkata', 100, 1, 1, 'A stylish and comfortable suit for men', 'Fashion'),
(22, 'Intro to algorithms', 29, 900, 'algorithm.jpg', '2022-08-16', 'PHI', 'Kolkata', 50, 1.5, 1, 'A very good for software developers', 'Books'),
(23, 'Sofa', 30, 15000, 'sofa.jpg', '2023-01-31', 'Godrej', 'Hyderabad', 30, 150, 1, 'A very comfortable and soft sofa', 'Lifestyle'),
(24, 'Cosmetics', 30, 500, 'cosmetics.jpg', '2023-02-22', 'Ponds', 'Hyderabad', 65, 1, 1, 'Good quality cosmetics', 'Beauty'),
(25, 'Porche', 30, 9000000, 'porshe.jpg', '2023-03-14', 'Porche', 'Hyderabad', 19, 500, 1, 'A very fast car', 'Automobiles'),
(26, 'Parker Pen', 30, 50, 'pen.jpg', '2023-01-26', 'Parker', 'Hyderabad', 150, 0.1, 1, 'A very smooth writing pen', 'Education');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `User_Id` int(11) NOT NULL,
  `Name` text NOT NULL,
  `Email` varchar(50) NOT NULL,
  `Password` varchar(100) NOT NULL,
  `Phone_num` varchar(15) NOT NULL,
  `Street` varchar(100) NOT NULL,
  `City` varchar(100) NOT NULL,
  `State` varchar(100) NOT NULL,
  `PIN` text NOT NULL,
  `IsBuyer` tinyint(1) NOT NULL,
  `IsSeller` tinyint(1) NOT NULL,
  `Balance` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`User_Id`, `Name`, `Email`, `Password`, `Phone_num`, `Street`, `City`, `State`, `PIN`, `IsBuyer`, `IsSeller`, `Balance`) VALUES
(29, 'Shivang', 'agrawalshivang29@gmail.com', '$2b$12$66FEQgi7SVY1sJSNV7uou.LnDPkxnG4IQhfvevrVjjxD0cbQOVGPe', '6307778300', 'Park Street', 'Kolkata', 'West Bengal', '700001', 1, 1, 0),
(30, 'Hrushikesh', 'hrushikeshkalikiri@gmail.com', '$2b$12$Lpudo2jnTQzmiT7UYwQ0muajswysil0klhb7qjDDmQPUtXmuPUdo.', '9988998898', 'Mallampet', 'Hyderabad', 'Telangana', '500001', 1, 1, 0),
(31, 'Hari Krishna', 'agrawalshivang07@gmail.com', '$2b$12$Vap.MjtF81.T02OHqA4sL.NMBOkGLiYGiXxkreMKVnvdUYj9PH2WS', '4567891230', 'Kukatpally', 'Hyderabad', 'Telangana', '500001', 1, 1, 11197500);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `cart`
--
ALTER TABLE `cart`
  ADD PRIMARY KEY (`Cartid`);

--
-- Indexes for table `manager`
--
ALTER TABLE `manager`
  ADD PRIMARY KEY (`manager_id`);

--
-- Indexes for table `negotiations`
--
ALTER TABLE `negotiations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `orderdetails`
--
ALTER TABLE `orderdetails`
  ADD PRIMARY KEY (`oid`);

--
-- Indexes for table `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`Pid`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`User_Id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `cart`
--
ALTER TABLE `cart`
  MODIFY `Cartid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=38;

--
-- AUTO_INCREMENT for table `manager`
--
ALTER TABLE `manager`
  MODIFY `manager_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `negotiations`
--
ALTER TABLE `negotiations`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=56;

--
-- AUTO_INCREMENT for table `orderdetails`
--
ALTER TABLE `orderdetails`
  MODIFY `oid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=77;

--
-- AUTO_INCREMENT for table `products`
--
ALTER TABLE `products`
  MODIFY `Pid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `User_Id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=32;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
