-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 05, 2025 at 06:17 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `appointtrack`
--

-- --------------------------------------------------------

--
-- Table structure for table `appointments`
--

CREATE TABLE `appointments` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `provider_name` varchar(100) NOT NULL,
  `date_time` datetime NOT NULL,
  `reason` text DEFAULT NULL,
  `status` enum('Upcoming','Completed','Cancelled') DEFAULT 'Upcoming',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `appointments`
--

INSERT INTO `appointments` (`id`, `user_id`, `provider_name`, `date_time`, `reason`, `status`, `created_at`, `updated_at`) VALUES
(1, 1, 'apollo', '2025-04-02 21:07:00', 'fever reduced\r\n', 'Cancelled', '2025-04-05 15:38:09', '2025-04-05 15:40:20'),
(2, 1, 'vijaya diagnostics', '2025-04-04 10:10:00', 'scan and blood test', 'Completed', '2025-04-05 15:38:56', '2025-04-05 15:38:56'),
(3, 1, 'vijaya diagnostics', '2025-04-08 09:30:00', 'second blood test', 'Upcoming', '2025-04-05 15:41:27', '2025-04-05 15:41:27'),
(4, 1, 'vijaya diagnostics', '2025-04-17 09:30:00', 'third blood test\r\n', 'Upcoming', '2025-04-05 15:42:02', '2025-04-05 15:42:22'),
(5, 2, 'apollo', '2025-04-02 21:23:00', 'scan', 'Completed', '2025-04-05 15:53:56', '2025-04-05 15:54:10');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `password`, `created_at`) VALUES
(1, 'skanuri03', 'pbkdf2:sha256:260000$HohvifrDeOblIW7Q$a26afc406a38e9cda8dd5f1c26fac6229a0beae4669782b424c70007ae095e02', '2025-04-05 15:37:04'),
(2, 'akhilesh', 'pbkdf2:sha256:260000$sWQtdnYOfD17j72A$7df284af07f0167a501f5b266c3c81dffd65ec01a5e417847e5f8d976689e2e5', '2025-04-05 15:53:26');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `appointments`
--
ALTER TABLE `appointments`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `appointments`
--
ALTER TABLE `appointments`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `appointments`
--
ALTER TABLE `appointments`
  ADD CONSTRAINT `appointments_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
