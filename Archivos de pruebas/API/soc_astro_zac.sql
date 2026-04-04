/*
Navicat MySQL Data Transfer

Source Server         : SociedadAstronomicaZac
Source Server Version : 50505
Source Host           : idawis-uaz.ddns.net:3306
Source Database       : soc_astro_zac

Target Server Type    : MYSQL
Target Server Version : 50505
File Encoding         : 65001

Date: 2025-08-07 23:11:32
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `data_radob`
-- ----------------------------
DROP TABLE IF EXISTS `data_radob`;
CREATE TABLE `data_radob` (
  `datetime_utc` datetime NOT NULL,
  `ua` decimal(22,10) NOT NULL,
  `sended` enum('N','Y') NOT NULL DEFAULT 'N'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of data_radob
-- ----------------------------

-- ----------------------------
-- Table structure for `data_ray_gpt`
-- ----------------------------
DROP TABLE IF EXISTS `data_ray_gpt`;
CREATE TABLE `data_ray_gpt` (
  `datetime_utc` datetime NOT NULL,
  `intensidad` decimal(6,2) NOT NULL,
  `campo_kVm` decimal(6,2) NOT NULL,
  `temp_C` decimal(6,2) NOT NULL,
  `humedad_rh` decimal(6,2) NOT NULL,
  `presion_hPa` decimal(6,2) NOT NULL,
  `cpm_escalado` decimal(6,2) NOT NULL,
  `avg_cpm_reciente` decimal(6,2) NOT NULL,
  `sended` enum('N','Y') NOT NULL DEFAULT 'N'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of data_ray_gpt
-- ----------------------------
