-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Máy chủ: 127.0.0.1
-- Thời gian đã tạo: Th3 18, 2026 lúc 02:51 PM
-- Phiên bản máy phục vụ: 10.4.32-MariaDB
-- Phiên bản PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Cơ sở dữ liệu: `nckh`
--

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `ingredients`
--

CREATE TABLE `ingredients` (
  `id` varchar(36) NOT NULL,
  `name` varchar(100) NOT NULL,
  `icon` varchar(10) NOT NULL,
  `category_id` varchar(36) NOT NULL,
  `image_url` text DEFAULT NULL,
  `is_popular` tinyint(1) DEFAULT NULL,
  `aliases` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`aliases`)),
  `created_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `ingredients`
--

INSERT INTO `ingredients` (`id`, `name`, `icon`, `category_id`, `image_url`, `is_popular`, `aliases`, `created_at`) VALUES
('1', 'Thịt gà', '🍗', 'c1', 'images/thit_ga.jpg', 1, '[\"gà\",\"ức gà\"]', '2026-03-17 20:12:55'),
('10', 'Hành tây', '🧅', 'c3', 'images/hanh_tay.jpg', 1, '[\"onion\"]', '2026-03-17 20:12:55'),
('11', 'Tỏi', '🧄', 'c3', 'images/toi.jpg', 1, '[\"garlic\"]', '2026-03-17 20:12:55'),
('12', 'Rau muống', '🥬', 'c3', 'images/rau_muong.jpg', 0, '[\"rau\"]', '2026-03-17 20:12:55'),
('13', 'Bún', '🍜', 'c4', 'images/bun.jpg', 1, '[\"bún tươi\"]', '2026-03-17 20:12:55'),
('14', 'Phở', '🍜', 'c4', 'images/pho.jpg', 1, '[\"bánh phở\"]', '2026-03-17 20:12:55'),
('15', 'Mì gói', '🍝', 'c4', 'images/mi.jpg', 1, '[\"mì ăn liền\"]', '2026-03-17 20:12:55'),
('16', 'Gạo', '🍚', 'c4', 'images/gao.jpg', 1, '[\"cơm\"]', '2026-03-17 20:12:55'),
('17', 'Nước mắm', '🧂', 'c5', 'images/nuoc_mam.jpg', 1, '[\"mắm\"]', '2026-03-17 20:12:55'),
('18', 'Đường', '🍬', 'c5', 'images/duong.jpg', 1, '[\"đường cát\"]', '2026-03-17 20:12:55'),
('19', 'Muối', '🧂', 'c5', 'images/muoi.jpg', 1, '[\"muối biển\"]', '2026-03-17 20:12:55'),
('2', 'Thịt bò', '🥩', 'c1', 'images/thit_bo.jpg', 1, '[\"bò\"]', '2026-03-17 20:12:55'),
('20', 'Tiêu', '🌶️', 'c5', 'images/tieu.jpg', 0, '[\"hạt tiêu\"]', '2026-03-17 20:12:55'),
('3', 'Cá hồi', '🐟', 'c1', 'images/ca_hoi.jpg', 1, '[\"salmon\"]', '2026-03-17 20:12:55'),
('4', 'Tôm', '🦐', 'c1', 'images/tom.jpg', 1, '[\"tôm tươi\"]', '2026-03-17 20:12:55'),
('5', 'Trứng gà', '🥚', 'c2', 'images/trung.jpg', 1, '[\"trứng\"]', '2026-03-17 20:12:55'),
('6', 'Sữa tươi', '🥛', 'c2', 'images/sua.jpg', 0, '[\"sữa\"]', '2026-03-17 20:12:55'),
('7', 'Cà chua', '🍅', 'c3', 'images/ca_chua.jpg', 1, '[\"tomato\"]', '2026-03-17 20:12:55'),
('8', 'Khoai tây', '🥔', 'c3', 'images/khoai_tay.jpg', 1, '[\"potato\"]', '2026-03-17 20:12:55'),
('9', 'Cà rốt', '🥕', 'c3', 'images/ca_rot.jpg', 1, '[\"carrot\"]', '2026-03-17 20:12:55'),
('ing-seed-0001', 'Rau cần', '🥬', 'c3', 'images/rau_can.jpg', 0, '[]', '2026-03-18 20:16:29'),
('ing-seed-0002', 'Rong mứt', '🥬', 'c3', 'images/rong_mut.jpg', 0, '[]', '2026-03-18 20:16:30'),
('ing-seed-0003', 'Bạc hà', '🥬', 'c3', 'images/bac_ha.jpg', 0, '[]', '2026-03-18 20:16:30'),
('ing-seed-0004', 'Nước mắm chay', '🧂', 'c5', 'images/nuoc_mam_chay.jpg', 0, '[]', '2026-03-18 20:16:30'),
('ing-seed-0005', 'Hạt nêm', '🧂', 'c5', 'images/hat_nem.jpg', 0, '[]', '2026-03-18 20:16:30'),
('ing-seed-0006', 'Cơm mẻ', '🧂', 'c5', 'images/com_me.jpg', 0, '[]', '2026-03-18 20:16:30'),
('ing-seed-0007', 'Rau thì là', '🥬', 'c3', 'images/rau_thi_la.jpg', 0, '[]', '2026-03-18 20:16:30'),
('ing-seed-0008', 'Rau ngò om', '🥬', 'c3', 'images/rau_ngo_om.jpg', 0, '[]', '2026-03-18 20:16:30'),
('ing-seed-0009', 'Cá lóc', '🐟', 'c1', 'images/ca_loc.jpg', 0, '[]', '2026-03-18 20:16:31'),
('ing-seed-0010', 'Xương cá lóc', '🐟', 'c1', 'images/xuong_ca_loc.jpg', 0, '[]', '2026-03-18 20:16:31'),
('ing-seed-0011', 'Chả cá Nha Trang', '🐟', 'c1', 'images/cha_ca_nha_trang.jpg', 0, '[]', '2026-03-18 20:16:31'),
('ing-seed-0012', 'Bánh canh bột gạo', '🍜', 'c4', 'images/banh_canh_bot_gao.jpg', 0, '[]', '2026-03-18 20:16:31'),
('ing-seed-0013', 'Hành tím', '🧅', 'c5', 'images/hanh_tim.jpg', 0, '[]', '2026-03-18 20:16:31'),
('ing-seed-0014', 'Bột ngọt', '🧂', 'c5', 'images/bot_ngot.jpg', 0, '[]', '2026-03-18 20:16:31'),
('ing-seed-0015', 'Hành ngò', '🧂', 'c5', 'images/hanh_ngo.jpg', 0, '[]', '2026-03-18 20:16:31'),
('ing-seed-0016', 'Cá bớp', '🐟', 'c1', 'images/ca_bop.jpg', 0, '[]', '2026-03-18 20:16:31'),
('ing-seed-0017', 'Nước dừa', '🥥', 'c3', 'images/nuoc_dua.jpg', 0, '[]', '2026-03-18 20:16:31'),
('ing-seed-0018', 'Dưa cà', '🍗', 'c1', 'images/dua_ca.jpg', 0, '[]', '2026-03-18 20:16:31'),
('ing-seed-0019', 'Thịt ba rọi', '🥩', 'c1', 'images/thit_ba_roi.jpg', 0, '[]', '2026-03-18 20:16:31'),
('ing-seed-0020', 'Đầu cá bông lau', '🍗', 'c1', 'images/au_ca_bong_lau.jpg', 0, '[]', '2026-03-18 20:16:31'),
('ing-seed-0021', 'Đầu cá mú đen', '🍗', 'c1', 'images/au_ca_mu_en.jpg', 0, '[]', '2026-03-18 20:16:31'),
('ing-seed-0022', 'Rau tần dày', '🥬', 'c3', 'images/rau_tan_day.jpg', 0, '[]', '2026-03-18 20:16:31'),
('ing-seed-0023', 'Húng quế', '🌿', 'c3', 'images/hung_que.jpg', 0, '[]', '2026-03-18 20:16:31'),
('ing-seed-0024', 'Hành lá', '🌿', 'c5', 'images/hanh_la.jpg', 0, '[]', '2026-03-18 20:16:31'),
('ing-seed-0025', 'Ngò gai', '🌿', 'c3', 'images/ngo_gai.jpg', 0, '[]', '2026-03-18 20:16:31'),
('ing-seed-0026', 'Ngò om', '🥬', 'c3', 'images/ngo_om.jpg', 0, '[]', '2026-03-18 20:16:31'),
('ing-seed-0027', 'Ớt xiêm xanh', '🌶️', 'c5', 'images/ot_xiem_xanh.jpg', 0, '[]', '2026-03-18 20:16:31'),
('ing-seed-0028', 'Lá me non', '🧂', 'c5', 'images/la_me_non.jpg', 0, '[]', '2026-03-18 20:16:31'),
('ing-seed-0029', 'Giá đỗ', '🧂', 'c5', 'images/gia_o.jpg', 0, '[]', '2026-03-18 20:16:31'),
('ing-seed-0030', 'Cá dứa', '🐟', 'c1', 'images/ca_dua.jpg', 0, '[]', '2026-03-18 20:16:31'),
('ing-seed-0031', 'Ớt', '🌶️', 'c5', 'images/ot.jpg', 0, '[]', '2026-03-18 20:16:31'),
('ing-seed-0032', 'Gia vị', '🧂', 'c5', 'images/gia_vi.jpg', 0, '[]', '2026-03-18 20:16:31'),
('ing-seed-0033', 'Thịt vai bò', '🥩', 'c1', 'images/thit_vai_bo.jpg', 0, '[]', '2026-03-18 20:16:31'),
('ing-seed-0034', 'Cải chua', '🥬', 'c3', 'images/cai_chua.jpg', 0, '[]', '2026-03-18 20:16:31'),
('ing-seed-0035', 'Rau răm', '🌿', 'c3', 'images/rau_ram.jpg', 0, '[]', '2026-03-18 20:16:31'),
('ing-seed-0036', 'Ngò rí', '🌿', 'c3', 'images/ngo_ri.jpg', 0, '[]', '2026-03-18 20:16:31'),
('ing-seed-0037', 'Muối biển', '🧂', 'c5', 'images/muoi_bien.jpg', 0, '[]', '2026-03-18 20:16:31'),
('ing-seed-0038', 'Đường trắng', '🍬', 'c3', 'images/uong_trang.jpg', 0, '[]', '2026-03-18 20:16:31'),
('ing-seed-0039', 'Dầu ăn', '🧴', 'c3', 'images/dau_an.jpg', 0, '[]', '2026-03-18 20:16:31'),
('ing-seed-0040', 'Ớt bột', '🌶️', 'c5', 'images/ot_bot.jpg', 0, '[]', '2026-03-18 20:16:31'),
('ing-seed-0041', 'Cá hú', '🐟', 'c1', 'images/ca_hu.jpg', 0, '[]', '2026-03-18 20:16:31'),
('ing-seed-0042', 'Nước màu', '🧴', 'c5', 'images/nuoc_mau.jpg', 0, '[]', '2026-03-18 20:16:31'),
('ing-seed-0043', 'Cá rô đồng', '🍗', 'c1', 'images/ca_ro_ong.jpg', 0, '[]', '2026-03-18 20:16:31'),
('ing-seed-0044', 'Nghệ', '🌿', 'c3', 'images/nghe.jpg', 0, '[]', '2026-03-18 20:16:31'),
('ing-seed-0045', 'Gừng', '🌿', 'c5', 'images/gung.jpg', 0, '[]', '2026-03-18 20:16:31'),
('ing-seed-0046', 'Hành tăm', '🧂', 'c5', 'images/hanh_tam.jpg', 0, '[]', '2026-03-18 20:16:31'),
('ing-seed-0047', 'Sấu', '🥬', 'c3', 'images/sau.jpg', 0, '[]', '2026-03-18 20:16:31'),
('ing-seed-0048', 'Thịt nạc', '🥩', 'c1', 'images/thit_nac.jpg', 0, '[]', '2026-03-18 20:16:31'),
('ing-seed-0049', 'Bột canh', '🧂', 'c5', 'images/bot_canh.jpg', 0, '[]', '2026-03-18 20:16:31'),
('ing-seed-0050', 'Mùi tàu', '🌿', 'c3', 'images/mui_tau.jpg', 0, '[]', '2026-03-18 20:16:31'),
('ing-seed-0051', 'Hành khô', '🧅', 'c5', 'images/hanh_kho.jpg', 0, '[]', '2026-03-18 20:16:31'),
('ing-seed-0052', 'Cải xanh', '🥬', 'c3', 'images/cai_xanh.jpg', 0, '[]', '2026-03-18 20:16:31'),
('ing-seed-0053', 'Bột nêm', '🧂', 'c5', 'images/bot_nem.jpg', 0, '[]', '2026-03-18 20:16:31'),
('ing-seed-0054', 'Cá lóc bông', '🍗', 'c1', 'images/ca_loc_bong.jpg', 0, '[]', '2026-03-18 20:16:31'),
('ing-seed-0055', 'Tương ớt', '🧴', 'c5', 'images/tuong_ot.jpg', 0, '[]', '2026-03-18 20:16:31'),
('ing-seed-0056', 'Bầu', '🥒', 'c3', 'images/bau.jpg', 0, '[]', '2026-03-18 20:16:31'),
('ing-seed-0057', 'Giấm', '🧴', 'c5', 'images/giam.jpg', 0, '[]', '2026-03-18 20:16:31'),
('ing-seed-0058', 'Tóp mỡ', '🥬', 'c3', 'images/top_mo.jpg', 0, '[]', '2026-03-18 20:16:31'),
('ing-seed-0059', 'Ớt xiêm', '🌶️', 'c5', 'images/ot_xiem.jpg', 0, '[]', '2026-03-18 20:16:31'),
('ing-seed-0060', 'Nước cốt chanh', '🍋', 'c5', 'images/nuoc_cot_chanh.jpg', 0, '[]', '2026-03-18 20:16:31'),
('ing-seed-0061', 'Đường phèn', '🍬', 'c3', 'images/uong_phen.jpg', 0, '[]', '2026-03-18 20:16:31'),
('ing-seed-0062', 'Thơm', '🍍', 'c3', 'images/thom.jpg', 0, '[]', '2026-03-18 20:16:31'),
('ing-seed-0063', 'Ớt sừng', '🌶️', 'c5', 'images/ot_sung.jpg', 0, '[]', '2026-03-18 20:16:31'),
('ing-seed-0064', 'Nước màu dừa', '🧴', 'c5', 'images/nuoc_mau_dua.jpg', 0, '[]', '2026-03-18 20:16:31'),
('ing-seed-0065', 'Dứa', '🍍', 'c3', 'images/dua.jpg', 0, '[]', '2026-03-18 20:16:31'),
('ing-seed-0066', 'Rong biển', '🥬', 'c3', 'images/rong_bien.jpg', 0, '[]', '2026-03-18 20:16:31'),
('ing-seed-0067', 'Cá rô', '🐟', 'c1', 'images/ca_ro.jpg', 0, '[]', '2026-03-18 20:16:31'),
('ing-seed-0068', 'Cá', '🐟', 'c1', 'images/ca.jpg', 0, '[]', '2026-03-18 20:16:31'),
('ing-seed-0069', 'Riềng', '🌿', 'c5', 'images/rieng.jpg', 0, '[]', '2026-03-18 20:16:31'),
('ing-seed-0070', 'Sả', '🌿', 'c5', 'images/sa.jpg', 0, '[]', '2026-03-18 20:16:31'),
('ing-seed-0071', 'Thịt ba chỉ', '🥩', 'c1', 'images/thit_ba_chi.jpg', 0, '[]', '2026-03-18 20:16:31'),
('ing-seed-0072', 'Mỡ lợn', '🥓', 'c1', 'images/mo_lon.jpg', 0, '[]', '2026-03-18 20:16:31'),
('ing-seed-0073', 'Đường thốt nốt', '🍬', 'c3', 'images/uong_thot_not.jpg', 0, '[]', '2026-03-18 20:16:31'),
('ing-seed-0074', 'Bắp bò', '🥩', 'c1', 'images/bap_bo.jpg', 0, '[]', '2026-03-18 20:16:31'),
('ing-seed-0075', 'Đậu hũ', '🍱', 'c3', 'images/au_hu.jpg', 0, '[]', '2026-03-18 20:16:31'),
('ing-seed-0076', 'Giá', '🧂', 'c5', 'images/gia.jpg', 0, '[]', '2026-03-18 20:16:31'),
('ing-seed-0077', 'Bắp chuối', '🥬', 'c3', 'images/bap_chuoi.jpg', 0, '[]', '2026-03-18 20:16:31'),
('ing-seed-0078', 'Me', '🧂', 'c5', 'images/me.jpg', 0, '[]', '2026-03-18 20:16:31'),
('ing-seed-0079', 'Rau om', '🥬', 'c3', 'images/rau_om.jpg', 0, '[]', '2026-03-18 20:16:31'),
('ing-seed-0080', 'Bột mì', '🍞', 'c4', 'images/bot_mi.jpg', 0, '[]', '2026-03-18 20:16:31'),
('ing-seed-0081', 'Bột chiên giòn', '🍞', 'c4', 'images/bot_chien_gion.jpg', 0, '[]', '2026-03-18 20:16:31');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `ingredient_categories`
--

CREATE TABLE `ingredient_categories` (
  `id` varchar(36) NOT NULL,
  `slug` varchar(50) NOT NULL,
  `name` varchar(100) NOT NULL,
  `icon` varchar(10) DEFAULT NULL,
  `sort_order` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `ingredient_categories`
--

INSERT INTO `ingredient_categories` (`id`, `slug`, `name`, `icon`, `sort_order`) VALUES
('c1', 'thit-ca', 'Thịt cá', '🍗', 1),
('c2', 'trung-sua', 'Trứng sữa', '🥚', 2),
('c3', 'rau-cu', 'Rau củ', '🥬', 3),
('c4', 'tinh-bot', 'Tinh bột', '🍚', 4),
('c5', 'gia-vi', 'Gia vị', '🧂', 5);

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `pantry_items`
--

CREATE TABLE `pantry_items` (
  `id` varchar(36) NOT NULL,
  `user_id` varchar(64) NOT NULL,
  `ingredient_id` varchar(36) NOT NULL,
  `quantity` varchar(50) NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `pantry_items`
--

INSERT INTO `pantry_items` (`id`, `user_id`, `ingredient_id`, `quantity`, `created_at`, `updated_at`) VALUES
('254e52b4-2974-4a89-829d-833fa4fc567c', 'mobile-demo-user', '11', '1', '2026-03-17 15:03:47', '2026-03-17 15:03:47'),
('34d07ea4-de93-4eed-8b0a-a52afcd80777', 'mobile-demo-user', '10', '1', '2026-03-17 15:03:47', '2026-03-17 15:03:47'),
('561fbc3b-2428-4908-843f-f80d296352e6', 'mobile-demo-user', '5', '1', '2026-03-17 15:03:47', '2026-03-17 15:03:47'),
('cb56eb00-8420-47c4-a215-82b31f2303bb', 'mobile-demo-user', '7', '1', '2026-03-17 15:03:47', '2026-03-17 15:03:47');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `recipes`
--

CREATE TABLE `recipes` (
  `id` varchar(36) NOT NULL,
  `name` varchar(200) NOT NULL,
  `description` text NOT NULL,
  `image_url` text NOT NULL,
  `cook_time_minutes` int(11) NOT NULL,
  `difficulty` varchar(20) NOT NULL,
  `servings` int(11) NOT NULL,
  `cuisine_type` varchar(50) DEFAULT NULL,
  `diet_tags` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`diet_tags`)),
  `is_featured` tinyint(1) DEFAULT NULL,
  `total_favorites` int(11) DEFAULT NULL,
  `total_views` int(11) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `recipes`
--

INSERT INTO `recipes` (`id`, `name`, `description`, `image_url`, `cook_time_minutes`, `difficulty`, `servings`, `cuisine_type`, `diet_tags`, `is_featured`, `total_favorites`, `total_views`, `created_at`, `updated_at`) VALUES
('recipe-seed-0001', 'Canh chua rau cần rong biển', 'Cách làm món Canh chua rau cần rong biển ngon tuyệt của nhà mình ;) Ngày trước tôi nghĩ canh chua phải là những món theo truyền thống, theo vùng miền này nọ Sau này tôi mới phát hiện ra rằng cứ canh có vị chua thì được gọi là canh chua, còn nấu theo cách nào thì mình cứ nấu theo cách mà mình...', 'https://img-global.cpcdn.com/recipes/523c431c8781f6f8/1200x630cq80/photo.jpg', 35, 'medium', 4, 'Vietnamese', '[]', 0, 0, 0, '2026-03-18 20:16:31', '2026-03-18 20:16:31'),
('recipe-seed-0002', 'Bánh canh chả cá, cá lóc', 'Cách làm món Bánh canh chả cá, cá lóc ngon tuyệt của nhà mình ;) Nước dùng bánh canh được hầm từ xương cá ngọt thanh rất ngon. #TapDeVang23', 'https://og-image.cookpad.com/global/vn/recipe/16118781?t=1701745481', 35, 'medium', 4, 'Vietnamese', '[]', 0, 0, 0, '2026-03-18 20:16:31', '2026-03-18 20:16:31'),
('recipe-seed-0003', 'Canh chua cá kho đậm vị cơm nhà', 'Cách làm món Canh chua cá kho đậm vị cơm nhà ngon tuyệt của nhà mình ;) #Cookpadapron2025 Combo canh chua và cá kho luôn là những món ăn hấp dẫn khó quên với khẩu vị người Việt, thêm dĩa đồ xào nhiều màu sắc tạo nên vị cơm nhà đậm đà khó quên', 'https://img-global.cpcdn.com/recipes/74834ec931494638/1200x630cq80/photo.jpg', 35, 'medium', 4, 'Vietnamese', '[]', 0, 0, 0, '2026-03-18 20:16:31', '2026-03-18 20:16:31'),
('recipe-seed-0004', 'Canh Chua Đầu Cá Mú Đen', 'Cách làm món Canh Chua Đầu Cá Mú Đen ngon tuyệt của nhà mình ;) #10nam1hanhtrinh Tháng 9', 'https://img-global.cpcdn.com/recipes/f07c30c15d2c211b/1200x630cq80/photo.jpg', 35, 'medium', 4, 'Vietnamese', '[]', 0, 0, 0, '2026-03-18 20:16:31', '2026-03-18 20:16:31'),
('recipe-seed-0005', 'Cá dứa kho tộ', 'Cách làm món Cá dứa (cá basa, cá hú, cá lăng) kho tộ (kho tiêu) ngon tuyệt của nhà mình ;) Đây là những loại cá da trơn, nếu không biết sơ chế và chế biến thì sẽ bị tanh. Tuy nhiên, cá có độ béo nên ăn thịt rất mềm ngậy, cùng mình làm nhen! #coginaudo', 'https://img-global.cpcdn.com/recipes/d02d8cb5fadc9b01/1200x630cq80/photo.jpg', 45, 'medium', 3, 'Vietnamese', '[]', 0, 0, 0, '2026-03-18 20:16:31', '2026-03-18 20:16:31'),
('recipe-seed-0006', 'Canh Thịt Bò Nấu Cải Chua', 'Cách làm món Canh Thịt Bò Nấu Cải Chua ngon tuyệt của nhà mình ;) #10nam1hanhtrinh Tháng 7', 'https://img-global.cpcdn.com/recipes/50ccb4ef8b262bd1/1200x630cq80/photo.jpg', 35, 'medium', 4, 'Vietnamese', '[]', 0, 0, 0, '2026-03-18 20:16:31', '2026-03-18 20:16:31'),
('recipe-seed-0007', 'Cá Bớp kho tộ', 'Cách làm món Cá Bớp kho tộ ngon tuyệt của nhà mình ;) Cá kho tộ là 1 trong những món xuất hiện thường xuyên trong bữa cơm của dân miền Tây cũng như mọi miền đất nước. Nó đậm đà đưa cơm, ăn kèm rau luộc, rau gém, chuối chát....Và không thể bỏ qua được khi nó xuất hiện cùng canh chua, bộ đôi món ăn...', 'https://img-global.cpcdn.com/recipes/f8af5fc08a2e36df/1200x630cq80/photo.jpg', 45, 'medium', 3, 'Vietnamese', '[]', 0, 0, 0, '2026-03-18 20:16:31', '2026-03-18 20:16:31'),
('recipe-seed-0008', 'Cá Hú Kho Tộ', 'Cách làm món Cá Hú Kho Tộ ngon tuyệt của nhà mình ;) Cá mềm béo thơm ngon...đậm đà, bén cơm', 'https://img-global.cpcdn.com/recipes/b9a8a36be3d43c70/1200x630cq80/photo.jpg', 45, 'hard', 3, 'Vietnamese', '[]', 0, 0, 0, '2026-03-18 20:16:31', '2026-03-18 20:16:31'),
('recipe-seed-0009', 'Cá rô đồng kho tộ', 'Cách làm món Cá rô đồng kho tộ ngon tuyệt của nhà mình ;)', 'https://og-image.cookpad.com/global/vn/recipe/15033071?t=1621483863', 45, 'easy', 3, 'Vietnamese', '[]', 0, 0, 0, '2026-03-18 20:16:31', '2026-03-18 20:16:31'),
('recipe-seed-0010', 'Thịt thăn thuôn sấu', 'Cách làm món Thịt thăn thuôn sấu (canh chua sấu thịt thăn) ngon tuyệt của nhà mình ;) #10nam1hanhtrinh Tìm kiếm phổ biến:canh chua Mình khá tò mò khi tìm hiểu trong món canh chua sấu thịt thăn thì có 1 tên khác ít biết là \"thịt thăn thuôn sấu\" thì hóa ra từ \"Thuôn\" không phải chỉ hình dáng mà 1...', 'https://img-global.cpcdn.com/recipes/5f4dd5a6453ffc3b/1200x630cq80/photo.jpg', 30, 'medium', 3, 'Vietnamese', '[]', 0, 0, 0, '2026-03-18 20:16:31', '2026-03-18 20:16:31'),
('recipe-seed-0011', 'Canh cải xanh nấu cá lóc', 'Cách làm món Canh cải xanh nấu cá lóc ngon tuyệt của nhà mình ;) #ancathang4 #globalapron2024', 'https://og-image.cookpad.com/global/vn/recipe/17308151?t=1711941514', 35, 'medium', 4, 'Vietnamese', '[]', 0, 0, 0, '2026-03-18 20:16:31', '2026-03-18 20:16:31'),
('recipe-seed-0012', 'Cá Lóc Bông Kho Nước Dừa Xiêm', 'Cách làm món Cá Lóc Bông Kho Nước Dừa Xiêm ngon tuyệt của nhà mình ;) #GlobalApron2024 #AnCaThang4 Cá Lóc Bông thịt chắc, ngọt, lại lành tính hơn nhiều loại cá khác. Vì vậy, khi dùng làm nguyên liệu cho món kho nước dừa sẽ rất hợp lý, vì cá sẽ không bị nhừ khi nấu lâu. #CaLocBongKhoNuocDua...', 'https://img-global.cpcdn.com/recipes/2b433704617555db/1200x630cq80/photo.jpg', 45, 'medium', 3, 'Vietnamese', '[]', 0, 0, 0, '2026-03-18 20:16:31', '2026-03-18 20:16:31'),
('recipe-seed-0013', 'Cá lóc hấp bầu', 'Cách làm món Cá lóc hấp bầu ngon tuyệt của nhà mình ;) #TapDeVang23 Món ăn nổi tiếng với phần cá lóc hấp chín cùng phần bầu ngọt ngọt thấm vị cá rất ngon. Mình dùng phần phile cá cho đỡ xương', 'https://img-global.cpcdn.com/recipes/6bbc5aacfe3627d7/1200x630cq80/photo.jpg', 30, 'medium', 3, 'Vietnamese', '[]', 0, 0, 0, '2026-03-18 20:16:31', '2026-03-18 20:16:31'),
('recipe-seed-0014', 'Cá rô kho tộ', 'Cách làm món Cá rô kho tộ ngon tuyệt của nhà mình ;) #bepvang', 'https://img-global.cpcdn.com/recipes/5fc1453e393c4c76/1200x630cq80/photo.jpg', 45, 'medium', 3, 'Vietnamese', '[]', 0, 0, 0, '2026-03-18 20:16:31', '2026-03-18 20:16:31'),
('recipe-seed-0015', 'Canh Chua Thịt Bò', 'Cách làm món Canh Chua Thịt Bò ngon tuyệt của nhà mình ;) #CookpadApron2025 Tuần 14', 'https://img-global.cpcdn.com/recipes/59b593df2860c828/1200x630cq80/photo.jpg', 35, 'medium', 4, 'Vietnamese', '[]', 0, 0, 0, '2026-03-18 20:16:31', '2026-03-18 20:16:31'),
('recipe-seed-0016', 'Phi lê Cá Lóc Bông Kho Thơm', 'Cách làm món Filet Cá Lóc Bông Kho Thơm ngon tuyệt của nhà mình ;) #GlobalCookpadGames2024 #VeTuLa Nhà ít người nên đi chợ về, lúc nào nấu xong cũng còn sót lại mỗi thứ một chút… Lục tủ lạnh, thấy còn sót lại 3 khoanh cá lóc bông từ khá lâu với nửa trái thơm (đồ ăn tráng miệng còn sót lại). Thế...', 'https://img-global.cpcdn.com/recipes/10ed99a647567016/1200x630cq80/photo.jpg', 45, 'medium', 3, 'Vietnamese', '[]', 0, 0, 0, '2026-03-18 20:16:31', '2026-03-18 20:16:31'),
('recipe-seed-0017', 'Canh chua rau cần bạc hà', 'Cách làm món Canh chua rau cần bạc hà ngon tuyệt của nhà mình ;) Nếu bạn đang cần 1 tô canh chua nhẹ, thanh vị, đủ chất, không cần ăn với cơm thì đây là một gợi ý', 'https://img-global.cpcdn.com/recipes/4a4ea86ca0bcc1b3/1200x630cq80/photo.jpg', 35, 'medium', 4, 'Vietnamese', '[]', 0, 0, 0, '2026-03-18 20:16:31', '2026-03-18 20:16:31'),
('recipe-seed-0018', 'Cá rô kho tộ', 'Cách làm món CƠM NHÀ | CÁ RÔ KHO TỘ ngon tuyệt của nhà mình ;) Cá rô mà mang đi kho tộ, ăn kèm với rau luộc hoặc ít rau sống thì đúng là không chê vào đâu được. Mấy con cá rô hôm nay cũng khá đặc biệt mọi người ạ. Đây là loại cá rô suối, Ric mua được trong chuyến công tác về khu Suối Giai- Bình...', 'https://img-global.cpcdn.com/recipes/3306396d07b2b24c/1200x630cq80/photo.jpg', 45, 'medium', 3, 'Vietnamese', '[]', 0, 0, 0, '2026-03-18 20:16:31', '2026-03-18 20:16:31'),
('recipe-seed-0019', 'Cá Kho Tộ', 'Cách làm món Cá Kho Tộ ngon tuyệt của nhà mình ;) Cá Kho Tộ- Xin chào các anh chị A/c, em yêu quí em Vào trang page cty Công ty CPDP Thiên Thảo tìm sản phẩm của em like=1 đ và share = 3 đ. Trân trọng cảm ơn cả nhà !...', 'https://img-global.cpcdn.com/recipes/4721cb98c78f1719/1200x630cq80/photo.jpg', 45, 'hard', 3, 'Vietnamese', '[]', 0, 0, 0, '2026-03-18 20:16:31', '2026-03-18 20:16:31'),
('recipe-seed-0020', 'Canh chua thịt bò đậu hũ', 'Cách làm món Canh chua thịt bò đậu hũ ngon tuyệt của nhà mình ;) #Cookpadapron2025 Tuần 14: Canh chua', 'https://img-global.cpcdn.com/recipes/166565f2ed5e1185/1200x630cq80/photo.jpg', 35, 'hard', 4, 'Vietnamese', '[]', 0, 0, 0, '2026-03-18 20:16:31', '2026-03-18 20:16:31'),
('recipe-seed-0021', 'Cá lóc fillet lăn bột chiên dòn', 'Cách làm món Cá lóc fillet lăn bột chiên dòn ngon tuyệt của nhà mình ;) #tapdevang23 Món cá chiên dòn tan, không xương dễ ăn cho bữa ăn kèm salad chiều nay!', 'https://img-global.cpcdn.com/recipes/2229538ef5364f91/1200x630cq80/photo.jpg', 25, 'medium', 3, 'Vietnamese', '[]', 0, 0, 0, '2026-03-18 20:16:31', '2026-03-18 20:16:31');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `recipe_ingredients`
--

CREATE TABLE `recipe_ingredients` (
  `id` varchar(36) NOT NULL,
  `recipe_id` varchar(36) NOT NULL,
  `ingredient_id` varchar(36) DEFAULT NULL,
  `amount` varchar(50) NOT NULL,
  `is_optional` tinyint(1) DEFAULT NULL,
  `sort_order` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `recipe_ingredients`
--

INSERT INTO `recipe_ingredients` (`id`, `recipe_id`, `ingredient_id`, `amount`, `is_optional`, `sort_order`) VALUES
('rig-seed-00001', 'recipe-seed-0001', '7', 'to taste', 0, 1),
('rig-seed-00002', 'recipe-seed-0001', 'ing-seed-0001', 'to taste', 0, 2),
('rig-seed-00003', 'recipe-seed-0001', 'ing-seed-0002', 'to taste', 0, 3),
('rig-seed-00004', 'recipe-seed-0001', 'ing-seed-0003', 'to taste', 0, 4),
('rig-seed-00005', 'recipe-seed-0001', 'ing-seed-0004', 'to taste', 0, 5),
('rig-seed-00006', 'recipe-seed-0001', 'ing-seed-0005', 'to taste', 0, 6),
('rig-seed-00007', 'recipe-seed-0001', 'ing-seed-0006', 'to taste', 0, 7),
('rig-seed-00008', 'recipe-seed-0001', 'ing-seed-0007', 'to taste', 0, 8),
('rig-seed-00009', 'recipe-seed-0001', 'ing-seed-0008', 'to taste', 0, 9),
('rig-seed-00010', 'recipe-seed-0002', 'ing-seed-0009', 'to taste', 0, 1),
('rig-seed-00011', 'recipe-seed-0002', 'ing-seed-0010', 'to taste', 0, 2),
('rig-seed-00012', 'recipe-seed-0002', 'ing-seed-0011', 'to taste', 0, 3),
('rig-seed-00013', 'recipe-seed-0002', 'ing-seed-0012', 'to taste', 0, 4),
('rig-seed-00014', 'recipe-seed-0002', '10', 'to taste', 0, 5),
('rig-seed-00015', 'recipe-seed-0002', 'ing-seed-0013', 'to taste', 0, 6),
('rig-seed-00016', 'recipe-seed-0002', '17', 'to taste', 0, 7),
('rig-seed-00017', 'recipe-seed-0002', '19', 'to taste', 0, 8),
('rig-seed-00018', 'recipe-seed-0002', 'ing-seed-0014', 'to taste', 0, 9),
('rig-seed-00019', 'recipe-seed-0002', 'ing-seed-0005', 'to taste', 0, 10),
('rig-seed-00020', 'recipe-seed-0002', '20', 'to taste', 0, 11),
('rig-seed-00021', 'recipe-seed-0002', 'ing-seed-0015', 'to taste', 0, 12),
('rig-seed-00022', 'recipe-seed-0003', 'ing-seed-0016', 'to taste', 0, 1),
('rig-seed-00023', 'recipe-seed-0003', 'ing-seed-0017', 'to taste', 0, 2),
('rig-seed-00024', 'recipe-seed-0003', 'ing-seed-0018', 'to taste', 0, 3),
('rig-seed-00025', 'recipe-seed-0003', 'ing-seed-0019', 'to taste', 0, 4),
('rig-seed-00026', 'recipe-seed-0003', 'ing-seed-0020', 'to taste', 0, 5),
('rig-seed-00027', 'recipe-seed-0004', 'ing-seed-0021', 'to taste', 0, 1),
('rig-seed-00028', 'recipe-seed-0004', 'ing-seed-0003', 'to taste', 0, 2),
('rig-seed-00029', 'recipe-seed-0004', 'ing-seed-0022', 'to taste', 0, 3),
('rig-seed-00030', 'recipe-seed-0004', 'ing-seed-0023', 'to taste', 0, 4),
('rig-seed-00031', 'recipe-seed-0004', 'ing-seed-0024', 'to taste', 0, 5),
('rig-seed-00032', 'recipe-seed-0004', 'ing-seed-0025', 'to taste', 0, 6),
('rig-seed-00033', 'recipe-seed-0004', 'ing-seed-0026', 'to taste', 0, 7),
('rig-seed-00034', 'recipe-seed-0004', 'ing-seed-0027', 'to taste', 0, 8),
('rig-seed-00035', 'recipe-seed-0004', 'ing-seed-0028', 'to taste', 0, 9),
('rig-seed-00036', 'recipe-seed-0004', 'ing-seed-0029', 'to taste', 0, 10),
('rig-seed-00037', 'recipe-seed-0005', 'ing-seed-0030', 'to taste', 0, 1),
('rig-seed-00038', 'recipe-seed-0005', 'ing-seed-0031', 'to taste', 0, 2),
('rig-seed-00039', 'recipe-seed-0005', '20', 'to taste', 0, 3),
('rig-seed-00040', 'recipe-seed-0005', 'ing-seed-0024', 'to taste', 0, 4),
('rig-seed-00041', 'recipe-seed-0005', 'ing-seed-0032', 'to taste', 0, 5),
('rig-seed-00042', 'recipe-seed-0005', 'ing-seed-0017', 'to taste', 0, 6),
('rig-seed-00043', 'recipe-seed-0006', 'ing-seed-0033', 'to taste', 0, 1),
('rig-seed-00044', 'recipe-seed-0006', '7', 'to taste', 0, 2),
('rig-seed-00045', 'recipe-seed-0006', '11', 'to taste', 0, 3),
('rig-seed-00046', 'recipe-seed-0006', 'ing-seed-0034', 'to taste', 0, 4),
('rig-seed-00047', 'recipe-seed-0006', 'ing-seed-0026', 'to taste', 0, 5),
('rig-seed-00048', 'recipe-seed-0006', 'ing-seed-0035', 'to taste', 0, 6),
('rig-seed-00049', 'recipe-seed-0006', 'ing-seed-0025', 'to taste', 0, 7),
('rig-seed-00050', 'recipe-seed-0006', 'ing-seed-0036', 'to taste', 0, 8),
('rig-seed-00051', 'recipe-seed-0007', 'ing-seed-0016', 'to taste', 0, 1),
('rig-seed-00052', 'recipe-seed-0007', 'ing-seed-0037', 'to taste', 0, 2),
('rig-seed-00053', 'recipe-seed-0007', 'ing-seed-0005', 'to taste', 0, 3),
('rig-seed-00054', 'recipe-seed-0007', '17', 'to taste', 0, 4),
('rig-seed-00055', 'recipe-seed-0007', 'ing-seed-0038', 'to taste', 0, 5),
('rig-seed-00056', 'recipe-seed-0007', '11', 'to taste', 0, 6),
('rig-seed-00057', 'recipe-seed-0007', 'ing-seed-0039', 'to taste', 0, 7),
('rig-seed-00058', 'recipe-seed-0007', '20', 'to taste', 0, 8),
('rig-seed-00059', 'recipe-seed-0007', 'ing-seed-0040', 'to taste', 0, 9),
('rig-seed-00060', 'recipe-seed-0007', 'ing-seed-0024', 'to taste', 0, 10),
('rig-seed-00061', 'recipe-seed-0008', 'ing-seed-0041', 'to taste', 0, 1),
('rig-seed-00062', 'recipe-seed-0008', 'ing-seed-0013', 'to taste', 0, 2),
('rig-seed-00063', 'recipe-seed-0008', '11', 'to taste', 0, 3),
('rig-seed-00064', 'recipe-seed-0008', 'ing-seed-0042', 'to taste', 0, 4),
('rig-seed-00065', 'recipe-seed-0008', '17', 'to taste', 0, 5),
('rig-seed-00066', 'recipe-seed-0008', '18', 'to taste', 0, 6),
('rig-seed-00067', 'recipe-seed-0008', 'ing-seed-0014', 'to taste', 0, 7),
('rig-seed-00068', 'recipe-seed-0008', '20', 'to taste', 0, 8),
('rig-seed-00069', 'recipe-seed-0008', 'ing-seed-0031', 'to taste', 0, 9),
('rig-seed-00070', 'recipe-seed-0008', 'ing-seed-0024', 'to taste', 0, 10),
('rig-seed-00071', 'recipe-seed-0009', 'ing-seed-0043', 'to taste', 0, 1),
('rig-seed-00072', 'recipe-seed-0009', 'ing-seed-0044', 'to taste', 0, 2),
('rig-seed-00073', 'recipe-seed-0009', 'ing-seed-0045', 'to taste', 0, 3),
('rig-seed-00074', 'recipe-seed-0009', 'ing-seed-0046', 'to taste', 0, 4),
('rig-seed-00075', 'recipe-seed-0009', '18', 'to taste', 0, 5),
('rig-seed-00076', 'recipe-seed-0009', '17', 'to taste', 0, 6),
('rig-seed-00077', 'recipe-seed-0009', 'ing-seed-0031', 'to taste', 0, 7),
('rig-seed-00078', 'recipe-seed-0010', '7', 'to taste', 0, 1),
('rig-seed-00079', 'recipe-seed-0010', 'ing-seed-0047', 'to taste', 0, 2),
('rig-seed-00080', 'recipe-seed-0010', 'ing-seed-0048', 'to taste', 0, 3),
('rig-seed-00081', 'recipe-seed-0010', '17', 'to taste', 0, 4),
('rig-seed-00082', 'recipe-seed-0010', 'ing-seed-0049', 'to taste', 0, 5),
('rig-seed-00083', 'recipe-seed-0010', 'ing-seed-0024', 'to taste', 0, 6),
('rig-seed-00084', 'recipe-seed-0010', 'ing-seed-0050', 'to taste', 0, 7),
('rig-seed-00085', 'recipe-seed-0010', 'ing-seed-0039', 'to taste', 0, 8),
('rig-seed-00086', 'recipe-seed-0010', 'ing-seed-0051', 'to taste', 0, 9),
('rig-seed-00087', 'recipe-seed-0011', 'ing-seed-0052', 'to taste', 0, 1),
('rig-seed-00088', 'recipe-seed-0011', 'ing-seed-0009', 'to taste', 0, 2),
('rig-seed-00089', 'recipe-seed-0011', 'ing-seed-0053', 'to taste', 0, 3),
('rig-seed-00090', 'recipe-seed-0011', '20', 'to taste', 0, 4),
('rig-seed-00091', 'recipe-seed-0011', 'ing-seed-0045', 'to taste', 0, 5),
('rig-seed-00092', 'recipe-seed-0011', '11', 'to taste', 0, 6),
('rig-seed-00093', 'recipe-seed-0012', 'ing-seed-0054', 'to taste', 0, 1),
('rig-seed-00094', 'recipe-seed-0012', 'ing-seed-0017', 'to taste', 0, 2),
('rig-seed-00095', 'recipe-seed-0012', 'ing-seed-0013', 'to taste', 0, 3),
('rig-seed-00096', 'recipe-seed-0012', '11', 'to taste', 0, 4),
('rig-seed-00097', 'recipe-seed-0012', 'ing-seed-0024', 'to taste', 0, 5),
('rig-seed-00098', 'recipe-seed-0012', '18', 'to taste', 0, 6),
('rig-seed-00099', 'recipe-seed-0012', 'ing-seed-0055', 'to taste', 0, 7),
('rig-seed-00100', 'recipe-seed-0012', 'ing-seed-0005', 'to taste', 0, 8),
('rig-seed-00101', 'recipe-seed-0012', 'ing-seed-0014', 'to taste', 0, 9),
('rig-seed-00102', 'recipe-seed-0012', '20', 'to taste', 0, 10),
('rig-seed-00103', 'recipe-seed-0012', '17', 'to taste', 0, 11),
('rig-seed-00104', 'recipe-seed-0012', 'ing-seed-0039', 'to taste', 0, 12),
('rig-seed-00105', 'recipe-seed-0013', 'ing-seed-0009', 'to taste', 0, 1),
('rig-seed-00106', 'recipe-seed-0013', 'ing-seed-0056', 'to taste', 0, 2),
('rig-seed-00107', 'recipe-seed-0013', 'ing-seed-0045', 'to taste', 0, 3),
('rig-seed-00108', 'recipe-seed-0013', 'ing-seed-0015', 'to taste', 0, 4),
('rig-seed-00109', 'recipe-seed-0013', '19', 'to taste', 0, 5),
('rig-seed-00110', 'recipe-seed-0013', '20', 'to taste', 0, 6),
('rig-seed-00111', 'recipe-seed-0013', 'ing-seed-0005', 'to taste', 0, 7),
('rig-seed-00112', 'recipe-seed-0014', 'ing-seed-0043', 'to taste', 0, 1),
('rig-seed-00113', 'recipe-seed-0014', '17', 'to taste', 0, 2),
('rig-seed-00114', 'recipe-seed-0014', '18', 'to taste', 0, 3),
('rig-seed-00115', 'recipe-seed-0014', 'ing-seed-0014', 'to taste', 0, 4),
('rig-seed-00116', 'recipe-seed-0014', '11', 'to taste', 0, 5),
('rig-seed-00117', 'recipe-seed-0014', 'ing-seed-0031', 'to taste', 0, 6),
('rig-seed-00118', 'recipe-seed-0014', '20', 'to taste', 0, 7),
('rig-seed-00119', 'recipe-seed-0014', 'ing-seed-0057', 'to taste', 0, 8),
('rig-seed-00120', 'recipe-seed-0014', 'ing-seed-0058', 'to taste', 0, 9),
('rig-seed-00121', 'recipe-seed-0015', 'ing-seed-0033', 'to taste', 0, 1),
('rig-seed-00122', 'recipe-seed-0015', 'ing-seed-0029', 'to taste', 0, 2),
('rig-seed-00123', 'recipe-seed-0015', '7', 'to taste', 0, 3),
('rig-seed-00124', 'recipe-seed-0015', 'ing-seed-0023', 'to taste', 0, 4),
('rig-seed-00125', 'recipe-seed-0015', 'ing-seed-0025', 'to taste', 0, 5),
('rig-seed-00126', 'recipe-seed-0015', 'ing-seed-0026', 'to taste', 0, 6),
('rig-seed-00127', 'recipe-seed-0015', 'ing-seed-0024', 'to taste', 0, 7),
('rig-seed-00128', 'recipe-seed-0015', 'ing-seed-0036', 'to taste', 0, 8),
('rig-seed-00129', 'recipe-seed-0015', 'ing-seed-0035', 'to taste', 0, 9),
('rig-seed-00130', 'recipe-seed-0015', 'ing-seed-0059', 'to taste', 0, 10),
('rig-seed-00131', 'recipe-seed-0015', '20', 'to taste', 0, 11),
('rig-seed-00132', 'recipe-seed-0015', 'ing-seed-0060', 'to taste', 0, 12),
('rig-seed-00133', 'recipe-seed-0015', 'ing-seed-0061', 'to taste', 0, 13),
('rig-seed-00134', 'recipe-seed-0015', '19', 'to taste', 0, 14),
('rig-seed-00135', 'recipe-seed-0015', 'ing-seed-0014', 'to taste', 0, 15),
('rig-seed-00136', 'recipe-seed-0016', 'ing-seed-0054', 'to taste', 0, 1),
('rig-seed-00137', 'recipe-seed-0016', 'ing-seed-0062', 'to taste', 0, 2),
('rig-seed-00138', 'recipe-seed-0016', 'ing-seed-0063', 'to taste', 0, 3),
('rig-seed-00139', 'recipe-seed-0016', 'ing-seed-0024', 'to taste', 0, 4),
('rig-seed-00140', 'recipe-seed-0016', 'ing-seed-0005', 'to taste', 0, 5),
('rig-seed-00141', 'recipe-seed-0016', '18', 'to taste', 0, 6),
('rig-seed-00142', 'recipe-seed-0016', '19', 'to taste', 0, 7),
('rig-seed-00143', 'recipe-seed-0016', 'ing-seed-0055', 'to taste', 0, 8),
('rig-seed-00144', 'recipe-seed-0016', 'ing-seed-0014', 'to taste', 0, 9),
('rig-seed-00145', 'recipe-seed-0016', '20', 'to taste', 0, 10),
('rig-seed-00146', 'recipe-seed-0016', 'ing-seed-0064', 'to taste', 0, 11),
('rig-seed-00147', 'recipe-seed-0016', '17', 'to taste', 0, 12),
('rig-seed-00148', 'recipe-seed-0016', 'ing-seed-0039', 'to taste', 0, 13),
('rig-seed-00149', 'recipe-seed-0017', '7', 'to taste', 0, 1),
('rig-seed-00150', 'recipe-seed-0017', 'ing-seed-0065', 'to taste', 0, 2),
('rig-seed-00151', 'recipe-seed-0017', 'ing-seed-0066', 'to taste', 0, 3),
('rig-seed-00152', 'recipe-seed-0017', 'ing-seed-0001', 'to taste', 0, 4),
('rig-seed-00153', 'recipe-seed-0017', 'ing-seed-0003', 'to taste', 0, 5),
('rig-seed-00154', 'recipe-seed-0017', 'ing-seed-0005', 'to taste', 0, 6),
('rig-seed-00155', 'recipe-seed-0017', '19', 'to taste', 0, 7),
('rig-seed-00156', 'recipe-seed-0018', 'ing-seed-0067', 'to taste', 0, 1),
('rig-seed-00157', 'recipe-seed-0018', '17', 'to taste', 0, 2),
('rig-seed-00158', 'recipe-seed-0018', '19', 'to taste', 0, 3),
('rig-seed-00159', 'recipe-seed-0018', '18', 'to taste', 0, 4),
('rig-seed-00160', 'recipe-seed-0018', 'ing-seed-0014', 'to taste', 0, 5),
('rig-seed-00161', 'recipe-seed-0018', 'ing-seed-0039', 'to taste', 0, 6),
('rig-seed-00162', 'recipe-seed-0018', 'ing-seed-0042', 'to taste', 0, 7),
('rig-seed-00163', 'recipe-seed-0018', 'ing-seed-0013', 'to taste', 0, 8),
('rig-seed-00164', 'recipe-seed-0018', 'ing-seed-0024', 'to taste', 0, 9),
('rig-seed-00165', 'recipe-seed-0018', '11', 'to taste', 0, 10),
('rig-seed-00166', 'recipe-seed-0018', 'ing-seed-0044', 'to taste', 0, 11),
('rig-seed-00167', 'recipe-seed-0018', '20', 'to taste', 0, 12),
('rig-seed-00168', 'recipe-seed-0018', 'ing-seed-0031', 'to taste', 0, 13),
('rig-seed-00169', 'recipe-seed-0019', 'ing-seed-0068', 'to taste', 0, 1),
('rig-seed-00170', 'recipe-seed-0019', '20', 'to taste', 0, 2),
('rig-seed-00171', 'recipe-seed-0019', 'ing-seed-0069', 'to taste', 0, 3),
('rig-seed-00172', 'recipe-seed-0019', 'ing-seed-0070', 'to taste', 0, 4),
('rig-seed-00173', 'recipe-seed-0019', '17', 'to taste', 0, 5),
('rig-seed-00174', 'recipe-seed-0019', '19', 'to taste', 0, 6),
('rig-seed-00175', 'recipe-seed-0019', 'ing-seed-0045', 'to taste', 0, 7),
('rig-seed-00176', 'recipe-seed-0019', 'ing-seed-0051', 'to taste', 0, 8),
('rig-seed-00177', 'recipe-seed-0019', 'ing-seed-0071', 'to taste', 0, 9),
('rig-seed-00178', 'recipe-seed-0019', 'ing-seed-0072', 'to taste', 0, 10),
('rig-seed-00179', 'recipe-seed-0019', 'ing-seed-0073', 'to taste', 0, 11),
('rig-seed-00180', 'recipe-seed-0020', 'ing-seed-0074', 'to taste', 0, 1),
('rig-seed-00181', 'recipe-seed-0020', 'ing-seed-0075', 'to taste', 0, 2),
('rig-seed-00182', 'recipe-seed-0020', '7', 'to taste', 0, 3),
('rig-seed-00183', 'recipe-seed-0020', 'ing-seed-0076', 'to taste', 0, 4),
('rig-seed-00184', 'recipe-seed-0020', '12', 'to taste', 0, 5),
('rig-seed-00185', 'recipe-seed-0020', 'ing-seed-0077', 'to taste', 0, 6),
('rig-seed-00186', 'recipe-seed-0020', 'ing-seed-0078', 'to taste', 0, 7),
('rig-seed-00187', 'recipe-seed-0020', 'ing-seed-0079', 'to taste', 0, 8),
('rig-seed-00188', 'recipe-seed-0020', '11', 'to taste', 0, 9),
('rig-seed-00189', 'recipe-seed-0020', 'ing-seed-0032', 'to taste', 0, 10),
('rig-seed-00190', 'recipe-seed-0021', 'ing-seed-0009', 'to taste', 0, 1),
('rig-seed-00191', 'recipe-seed-0021', '5', 'to taste', 0, 2),
('rig-seed-00192', 'recipe-seed-0021', 'ing-seed-0080', 'to taste', 0, 3),
('rig-seed-00193', 'recipe-seed-0021', 'ing-seed-0081', 'to taste', 0, 4),
('rig-seed-00194', 'recipe-seed-0021', 'ing-seed-0039', 'to taste', 0, 5),
('rig-seed-00195', 'recipe-seed-0021', 'ing-seed-0024', 'to taste', 0, 6),
('rig-seed-00196', 'recipe-seed-0021', '19', 'to taste', 0, 7);

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `recipe_steps`
--

CREATE TABLE `recipe_steps` (
  `id` varchar(36) NOT NULL,
  `recipe_id` varchar(36) NOT NULL,
  `step_number` int(11) NOT NULL,
  `title` varchar(200) DEFAULT NULL,
  `description` text NOT NULL,
  `image_url` text DEFAULT NULL,
  `duration_minutes` int(11) DEFAULT NULL,
  `tip` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `recipe_steps`
--

INSERT INTO `recipe_steps` (`id`, `recipe_id`, `step_number`, `title`, `description`, `image_url`, `duration_minutes`, `tip`) VALUES
('rst-seed-00001', 'recipe-seed-0001', 1, 'Step 1', 'Bước 1: Sơ chế nguyên liệu. Rau cần cắt khúc dài 5 cm. Bạc hà tước vỏ, cắt lát mỏng.', NULL, NULL, NULL),
('rst-seed-00002', 'recipe-seed-0001', 2, 'Step 2', 'Bước 2: Nấu nước dùng. Cà chua cắt nhỏ, xào thật mềm. Đổ lượng nước vừa đủ vào nồi đun sôi vài phút. Nêm nước mắm chay và hạt nêm cho vừa ăn.', NULL, NULL, NULL),
('rst-seed-00003', 'recipe-seed-0001', 3, 'Step 3', 'Bước 3: Nấu canh. Cho bạc hà vào nồi nấu trước 1-2 phút, sau đó cho tiếp rau cần và rong mứt vào nấu chung.', NULL, NULL, NULL),
('rst-seed-00004', 'recipe-seed-0001', 4, 'Step 4', 'Bước 4: Hoàn thiện. Khi canh vừa sôi, nêm thêm mẻ chua cho vừa khẩu vị. Cho rau thì là hoặc ngò om vào, sau đó tắt bếp.', NULL, NULL, NULL),
('rst-seed-00005', 'recipe-seed-0002', 1, 'Step 1', 'Bước 1: Sơ chế nguyên liệu. Cá lóc làm sạch, lọc lấy phần phi lê và cắt lát mỏng. Ướp phi lê cá với hạt nêm, tiêu, nước mắm cho thấm gia vị. Phần xương cá rửa sạch.', NULL, NULL, NULL),
('rst-seed-00006', 'recipe-seed-0002', 2, 'Step 2', 'Bước 2: Nấu nước dùng. Cho xương cá lóc vào nồi hầm cùng 2 lít nước, 1 củ hành tây và vài củ hành tím để lấy nước ngọt. Hầm lửa nhỏ khoảng 30 phút, sau đó lọc bỏ xương. Nêm nếm nước mắm, muối, bột ngọt cho vừa ăn.', NULL, NULL, NULL),
('rst-seed-00007', 'recipe-seed-0002', 3, 'Step 3', 'Bước 3: Chế biến cá. Phi thơm dầu hành, cho phần phi lê cá lóc đã ướp vào xào săn lại. Cho cá đã xào vào nồi nước dùng.', NULL, NULL, NULL),
('rst-seed-00008', 'recipe-seed-0002', 4, 'Step 4', 'Bước 4: Hoàn thiện. Cho sợi bánh canh và chả cá vào nồi nấu sôi, nêm nếm lại lần cuối. Múc bánh canh ra tô, rắc thêm hành ngò và tiêu trước khi thưởng thức.', NULL, NULL, NULL),
('rst-seed-00009', 'recipe-seed-0003', 1, 'Step 1', 'Bước 1: Chế biến món mặn. Làm món cá bớp kho nước dừa theo công thức tiêu chuẩn.', NULL, NULL, NULL),
('rst-seed-00010', 'recipe-seed-0003', 2, 'Step 2', 'Bước 2: Chế biến món xào. Dưa cà đem xào chín cùng với thịt ba rọi.', NULL, NULL, NULL),
('rst-seed-00011', 'recipe-seed-0003', 3, 'Step 3', 'Bước 3: Chế biến món canh. Nấu canh chua sử dụng nguyên liệu chính là đầu cá bông lau.', NULL, NULL, NULL),
('rst-seed-00012', 'recipe-seed-0003', 4, 'Step 4', 'Bước 4: Trình bày. Dọn các món ăn ra mâm, chấm kèm nước mắm cá kho.', NULL, NULL, NULL),
('rst-seed-00013', 'recipe-seed-0004', 1, 'Step 1', 'Bước 1: Sơ chế. Rửa sạch tất cả các nguyên liệu và để ráo nước. Ớt xiêm xanh giã dập, đầu hành lá đập dập.', NULL, NULL, NULL),
('rst-seed-00014', 'recipe-seed-0004', 2, 'Step 2', 'Bước 2: Nấu canh. Đun sôi nước, cho đầu cá, ớt xiêm xanh và đầu hành lá vào nấu. Đợi nước sôi lại thì vớt thật sạch bọt.', NULL, NULL, NULL),
('rst-seed-00015', 'recipe-seed-0004', 3, 'Step 3', 'Bước 3: Nêm nếm. Khi cá đã chín, cho lá me non, bạc hà và giá đỗ vào nấu thêm 2 phút. Nêm nếm gia vị cho vừa khẩu vị.', NULL, NULL, NULL),
('rst-seed-00016', 'recipe-seed-0004', 4, 'Step 4', 'Bước 4: Hoàn thiện. Cắt nhỏ các loại rau nêm (rau tần dày, húng quế, hành lá, ngò gai, ngò om) cho vào nồi rồi tắt bếp. Múc canh ra tô, ăn kèm với nước mắm mặn dầm ớt xanh.', NULL, NULL, NULL),
('rst-seed-00017', 'recipe-seed-0005', 1, 'Step 1', 'Bước 1: Sơ chế cá. Cá rửa sạch bằng muối và giấm. Dùng dao cạo da cá cho bớt nhớt tanh rồi rửa sạch lại. Ướp cá với hành, tỏi băm, nước mắm và tiêu trong 30 phút cho ngấm.', NULL, NULL, NULL),
('rst-seed-00018', 'recipe-seed-0005', 2, 'Step 2', 'Bước 2: Chế biến. Phi thơm hành tỏi băm, cho nước màu (nước hàng) vào chảo rồi thả cá vào lật đều hai mặt cho săn lại.', NULL, NULL, NULL),
('rst-seed-00019', 'recipe-seed-0005', 3, 'Step 3', 'Bước 3: Kho cá. Đổ nước dừa ngập mặt cá. Khi nước sôi, nêm nếm lại gia vị, thả 2-3 quả ớt vào rồi đậy vung. Kho lửa nhỏ đến khi nước sệt lại và cá thấm vị.', NULL, NULL, NULL),
('rst-seed-00020', 'recipe-seed-0005', 4, 'Step 4', 'Bước 4: Hoàn thiện. Khi nước kho còn sền sệt thì tắt bếp, rắc thêm tiêu và đầu hành lá lên trên. Gắp cá ra đĩa và thưởng thức cùng cơm nóng.', NULL, NULL, NULL),
('rst-seed-00021', 'recipe-seed-0006', 1, 'Step 1', 'Bước 1: Sơ chế. Rửa sạch tất cả các nguyên liệu và để ráo nước. Tỏi đem băm nhỏ và phi thơm.', NULL, NULL, NULL),
('rst-seed-00022', 'recipe-seed-0006', 2, 'Step 2', 'Bước 2: Xào nguyên liệu. Làm nóng nồi, cho mỡ và tỏi vào phi thơm rồi vớt tỏi ra để riêng. Cho cà chua vào xào chín mềm, sau đó thêm cải chua và thịt bò vào xào cùng.', NULL, NULL, NULL),
('rst-seed-00023', 'recipe-seed-0006', 3, 'Step 3', 'Bước 3: Nấu canh. Đổ nước sôi vào nồi đun lên. Khi nước sôi, nêm nếm lại gia vị cho vừa khẩu vị.', NULL, NULL, NULL),
('rst-seed-00024', 'recipe-seed-0006', 4, 'Step 4', 'Bước 4: Hoàn thiện. Thả ngò om, rau răm, ngò gai, ngò rí vào nồi. Múc canh ra tô, trang trí thêm rau thơm và rắc tỏi phi lên trên.', NULL, NULL, NULL),
('rst-seed-00025', 'recipe-seed-0007', 1, 'Step 1', 'Bước 1: Sơ chế. Cá rửa sạch, để ráo. Ướp cá với muối, hạt nêm, 1 muỗng nước mắm và tỏi băm trong khoảng 15 phút.', NULL, NULL, NULL),
('rst-seed-00026', 'recipe-seed-0007', 2, 'Step 2', 'Bước 2: Thắng nước màu. Bắc chảo hoặc nồi kho lên bếp. Cho dầu ăn và 1 muỗng đường vào, đun lửa nhỏ, lắc nhẹ chảo cho đường tan. Khi đường chuyển màu cánh gián thì cho tiếp 1 muỗng nước mắm vào.', NULL, NULL, NULL),
('rst-seed-00027', 'recipe-seed-0007', 3, 'Step 3', 'Bước 3: Kho cá. Cho cá đã ướp vào chảo, trở nhẹ tay để cá thấm đều màu và gia vị. Thêm khoảng 2 muỗng nước lọc vào nồi, để lửa liu riu kho trong khoảng 7-10 phút cho cá chín. Nêm nếm lại theo khẩu vị.', NULL, NULL, NULL),
('rst-seed-00028', 'recipe-seed-0007', 4, 'Step 4', 'Bước 4: Trình bày. Chỉnh lượng nước kho tùy sở thích. Tắt bếp, rắc thêm tiêu, ớt bột và hành lá lên trên.', NULL, NULL, NULL),
('rst-seed-00029', 'recipe-seed-0008', 1, 'Step 1', 'Bước 1: Sơ chế. Cá hú rửa sạch với muối, rượu và nước ấm, cạo sạch nhớt, cắt khúc vừa ăn.', NULL, NULL, NULL),
('rst-seed-00030', 'recipe-seed-0008', 2, 'Step 2', 'Bước 2: Ướp cá. Hành, tỏi băm nhỏ. Ướp cá cùng hành tỏi băm và tất cả các gia vị (nước màu, nước mắm, đường, bột ngọt, tiêu, ớt). Để cá ngấm gia vị khoảng 30 phút.', NULL, NULL, NULL),
('rst-seed-00031', 'recipe-seed-0008', 3, 'Step 3', 'Bước 3: Áp chảo. Cho ít dầu vào nồi, phi thơm hành tỏi. Cho cá vào áp chảo cho săn lại cả hai mặt.', NULL, NULL, NULL),
('rst-seed-00032', 'recipe-seed-0008', 4, 'Step 4', 'Bước 4: Kho cá. Cho phần nước ướp cá vào nồi. Châm thêm một ít nước nóng và ớt nguyên quả (tùy thích). Kho với lửa nhỏ, nêm nếm lại cho vừa khẩu vị.', NULL, NULL, NULL),
('rst-seed-00033', 'recipe-seed-0008', 5, 'Step 5', 'Bước 5: Hoàn thành. Khi nước kho cạn sánh lại, thêm hành lá cắt khúc rồi tắt bếp.', NULL, NULL, NULL),
('rst-seed-00034', 'recipe-seed-0009', 1, 'Step 1', 'Bước 1: Sơ chế. Cá rô đồng làm sạch, để ráo. Gừng, nghệ, hành tăm sơ chế sạch, giã nhỏ hoặc cắt lát.', NULL, NULL, NULL),
('rst-seed-00035', 'recipe-seed-0009', 2, 'Step 2', 'Bước 2: Ướp cá. Ướp cá rô đồng cùng với đường, nước mắm, ớt, gừng, hành tăm và nghệ trong một lúc cho thấm gia vị.', NULL, NULL, NULL),
('rst-seed-00036', 'recipe-seed-0009', 3, 'Step 3', 'Bước 3: Kho cá. Đặt nồi cá lên bếp nấu với lửa nhỏ. Kho cho đến khi cá chín mềm và nước kho hơi cạn keo lại là hoàn thành.', NULL, NULL, NULL),
('rst-seed-00037', 'recipe-seed-0010', 1, 'Step 1', 'Bước 1: Sơ chế thịt. Thịt lợn thái bản to, mỏng (nếu bản dày thì dùng búa dần thịt cho mềm). Ướp thịt với một chút bột nêm.', NULL, NULL, NULL),
('rst-seed-00038', 'recipe-seed-0010', 2, 'Step 2', 'Bước 2: Nấu nước dùng. Phi thơm hành khô đập dập (hoặc đầu hành trắng) với chút dầu ăn. Cho cà chua cắt nhỏ vào xào nhừ để tạo màu. Thêm sấu và đổ một bát nước lọc vào nồi. Nêm nếm nước mắm, muối, bột canh cho vừa khẩu vị.', NULL, NULL, NULL),
('rst-seed-00039', 'recipe-seed-0010', 3, 'Step 3', 'Bước 3: Dầm sấu. Khi nước sôi khoảng 1-2 phút cho sấu mềm, dùng thìa dầm nát sấu để tạo độ chua (gia giảm lượng sấu tùy khẩu vị).', NULL, NULL, NULL),
('rst-seed-00040', 'recipe-seed-0010', 4, 'Step 4', 'Bước 4: Nấu thịt. Mở lửa to cho nước sôi bùng lên. Thả thịt vào quậy đều để thịt nhúng vừa chín tới nhằm giữ độ ngọt mềm. Tắt bếp, rắc hành lá và mùi tàu thái nhỏ lên trên.', NULL, NULL, NULL),
('rst-seed-00041', 'recipe-seed-0011', 1, 'Step 1', 'Bước 1: Sơ chế cá. Cá lóc làm sạch. Lấy phần đuôi thái miếng mỏng để nấu canh (phần đầu và giữa để dành kho). Ướp cá với bột nêm và tiêu.', NULL, NULL, NULL),
('rst-seed-00042', 'recipe-seed-0011', 2, 'Step 2', 'Bước 2: Sơ chế rau củ. Gừng thái sợi, tỏi đập dập. Cải xanh rửa sạch, cắt khúc vừa ăn.', NULL, NULL, NULL),
('rst-seed-00043', 'recipe-seed-0011', 3, 'Step 3', 'Bước 3: Nấu nước dùng. Bắc nồi lên bếp, cho dầu ăn vào phi thơm tỏi và gừng. Đổ lượng nước vừa đủ vào nồi và đun sôi.', NULL, NULL, NULL),
('rst-seed-00044', 'recipe-seed-0011', 4, 'Step 4', 'Bước 4: Nấu canh. Khi nước sôi, cho rau cải xanh vào đảo đều một vòng. Tiếp tục cho cá lóc đã ướp vào nồi. Khi nước sôi lại và cá chín, nêm nếm gia vị cho vừa miệng rồi tắt bếp. Múc canh ra tô, rắc thêm tiêu lên trên.', NULL, NULL, NULL),
('rst-seed-00045', 'recipe-seed-0012', 1, 'Step 1', 'Bước 1: Sơ chế và ướp cá. Cá lóc bông làm sạch, cắt khoanh dày khoảng 2.5cm. Ướp cá với hành tím băm, tỏi băm, đường, tương ớt, hạt nêm, bột ngọt, tiêu, dầu ăn và nước mắm. Trộn đều và để khoảng 10 phút cho cá thấm gia vị.', NULL, NULL, NULL),
('rst-seed-00046', 'recipe-seed-0012', 2, 'Step 2', 'Bước 2: Chiên cá. Bắc chảo sâu lòng lên bếp, cho dầu ăn vào. Khi dầu nóng, lần lượt thả các khoanh cá đã ướp vào chiên trên lửa vừa cho săn đều hai mặt.', NULL, NULL, NULL),
('rst-seed-00047', 'recipe-seed-0012', 3, 'Step 3', 'Bước 3: Kho cá. Đổ nước dừa xiêm vào chảo cho ngập cá. Nấu đến khi nước dừa sôi thì hạ nhỏ lửa. Để nước sôi liu riu, hớt bọt thường xuyên để nước kho trong. Thỉnh thoảng trở mặt cá để thấm đều gia vị và tránh bị khét.', NULL, NULL, NULL),
('rst-seed-00048', 'recipe-seed-0012', 4, 'Step 4', 'Bước 4: Hoàn thành. Khi nước dừa cạn bớt và lên màu vàng đẹp mắt, nêm thêm một chút nước mắm cho vừa ăn (món này không cần quá mặn). Cho hành lá cắt khúc và tiêu vào, tắt bếp. Dùng nóng với rau sống và cơm.', NULL, NULL, NULL),
('rst-seed-00049', 'recipe-seed-0013', 1, 'Step 1', 'Bước 1: Sơ chế. Phi lê cá lóc bóp với muối, rửa sạch. Ướp cá với muối, hạt nêm, tiêu xay và đầu hành lá trong khoảng 30 phút. Gừng thái sợi.', NULL, NULL, NULL),
('rst-seed-00050', 'recipe-seed-0013', 2, 'Step 2', 'Bước 2: Chuẩn bị bầu. Bầu rửa sạch, dùng dao cắt rời 2/3 theo chiều dọc để tạo thành hình chiếc nắp đậy (khoét bỏ một phần ruột nếu cần).', NULL, NULL, NULL),
('rst-seed-00051', 'recipe-seed-0013', 3, 'Step 3', 'Bước 3: Hấp cá. Cho phần cá lóc đã ướp vào bên trong quả bầu, rắc thêm hành lá và gừng lên trên. Đậy nắp quả bầu lại.', NULL, NULL, NULL),
('rst-seed-00052', 'recipe-seed-0013', 4, 'Step 4', 'Bước 4: Hoàn thiện. Đưa quả bầu vào xửng hấp khoảng 15 phút cho đến khi cá chín và bầu mềm. Lấy ra và thưởng thức.', NULL, NULL, NULL),
('rst-seed-00053', 'recipe-seed-0014', 1, 'Step 1', 'Bước 1: Sơ chế. Cá rô cạo vảy, chẻ bụng bỏ ruột. Rửa cá qua nước giấm để khử nhớt và mùi tanh, xả lại bằng nước sạch, để ráo.', NULL, NULL, NULL),
('rst-seed-00054', 'recipe-seed-0014', 2, 'Step 2', 'Bước 2: Thắng nước màu. Đặt nồi đất lên bếp, cho một chút dầu ăn và đường vào thắng để lấy màu cánh gián. Khi màu đạt, cho tỏi và ớt băm vào phi thơm.', NULL, NULL, NULL),
('rst-seed-00055', 'recipe-seed-0014', 3, 'Step 3', 'Bước 3: Kho cá. Cho cá rô vào nồi lăn đều cho săn lại rồi tắt bếp. Nêm nước mắm, nước lọc, bột ngọt và đường vào nồi. Bật bếp trở lại và bắt đầu kho với lửa nhỏ.', NULL, NULL, NULL),
('rst-seed-00056', 'recipe-seed-0014', 4, 'Step 4', 'Bước 4: Hoàn thành. Trong lúc kho, thỉnh thoảng trở mặt cá và hớt bọt. Khi cá chín, nêm nếm lại gia vị. Để nước kho sắc lại, cho tóp mỡ vào đun sôi bùng lên để tóp mỡ thấm vị rồi tắt bếp. Rắc tiêu và ớt tươi lên trên.', NULL, NULL, NULL),
('rst-seed-00057', 'recipe-seed-0015', 1, 'Step 1', 'Bước 1: Sơ chế nguyên liệu. Rửa sạch thịt bò và thái lát mỏng. Các loại rau nêm (húng quế, ngò gai, ngò om, hành lá, ngò rí, rau răm), giá đỗ, cà chua rửa sạch và để ráo nước.', NULL, NULL, NULL),
('rst-seed-00058', 'recipe-seed-0015', 2, 'Step 2', 'Bước 2: Nấu nước dùng. Đun sôi một lượng nước vừa đủ. Cho thịt bò và cà chua vào nấu sôi. Vớt sạch bọt trên bề mặt nếu có.', NULL, NULL, NULL),
('rst-seed-00059', 'recipe-seed-0015', 3, 'Step 3', 'Bước 3: Nêm nếm. Cho nước cốt chanh (hoặc giấm), đường phèn, muối, bột ngọt vào nồi. Nêm nếm gia vị sao cho có độ chua ngọt hài hòa. Thêm ớt xiêm nếu thích ăn cay.', NULL, NULL, NULL),
('rst-seed-00060', 'recipe-seed-0015', 4, 'Step 4', 'Bước 4: Hoàn thiện. Tắt bếp, múc canh ra tô. Cho giá đỗ và các loại rau nêm cắt nhỏ vào. Rắc thêm một ít tiêu xay lên trên để tăng hương vị.', NULL, NULL, NULL),
('rst-seed-00061', 'recipe-seed-0016', 1, 'Step 1', 'Bước 1: Sơ chế. Cá lóc bông lọc bỏ xương, cắt thành khối vuông vừa ăn. Thơm xắt miếng mỏng. Gốc hành lá và ớt băm nhỏ. Phần lá hành xắt khúc.', NULL, NULL, NULL),
('rst-seed-00062', 'recipe-seed-0016', 2, 'Step 2', 'Bước 2: Ướp cá. Ướp cá lần 1 với hạt nêm, đường, muối, tương ớt, bột ngọt, tiêu. Trộn đều và để 5 phút. Ướp lần 2 với nước màu dừa, nước mắm, dầu ăn. Trộn đều và để thêm 10 phút cho cá ngấm.', NULL, NULL, NULL),
('rst-seed-00063', 'recipe-seed-0016', 3, 'Step 3', 'Bước 3: Chế biến. Bắc chảo lên bếp, làm nóng dầu ăn. Cho gốc hành và ớt băm vào phi thơm, trút cá vào đảo trên lửa lớn cho săn lại. Khi cá săn, chế nước lọc xăm xắp mặt cá và hạ lửa nhỏ.', NULL, NULL, NULL),
('rst-seed-00064', 'recipe-seed-0016', 4, 'Step 4', 'Bước 4: Hoàn thiện. Khi nước sốt sôi, cho thơm đã thái vào kho chung. Đảo nhẹ để thơm ngấm sốt. Khi thơm mềm, nêm nếm lại gia vị cho vừa miệng. Thêm hành lá xắt khúc, rắc tiêu, tắt bếp và dọn ra đĩa.', NULL, NULL, NULL),
('rst-seed-00065', 'recipe-seed-0017', 1, 'Step 1', 'Bước 1: Sơ chế. Cà chua rửa sạch, bổ múi cau. Dứa cắt nhỏ hoặc vắt lấy nước cốt để nấu cho nhanh. Rau cần cắt khúc vừa ăn. Bạc hà tước vỏ, thái vát mỏng.', NULL, NULL, NULL),
('rst-seed-00066', 'recipe-seed-0017', 2, 'Step 2', 'Bước 2: Chế biến nước dùng. Xào cà chua cho thật mềm nhừ, đổ lượng nước vừa đủ vào nồi đun sôi. (Nếu dùng dứa cắt miếng thì cho vào xào cùng cà chua từ đầu).', NULL, NULL, NULL),
('rst-seed-00067', 'recipe-seed-0017', 3, 'Step 3', 'Bước 3: Nêm nếm. Cho nước cốt dứa vào nồi (nếu dùng nước cốt). Nêm hạt nêm và muối cho vừa khẩu vị.', NULL, NULL, NULL),
('rst-seed-00068', 'recipe-seed-0017', 4, 'Step 4', 'Bước 4: Hoàn thiện. Cho rau cần, bạc hà và rong biển vào nồi nấu sôi lại. Tắt bếp và múc ra tô. (Lưu ý: Có thể nấu kèm đậu hũ hoặc chả chay nếu thích).', NULL, NULL, NULL),
('rst-seed-00069', 'recipe-seed-0018', 1, 'Step 1', 'Bước 1: Sơ chế nguyên liệu. Cá rô làm sạch. Tỏi, hành tím, ớt, đầu hành lá đập dập rồi băm nhuyễn. Nghệ non cạo vỏ, cắt lát mỏng.', NULL, NULL, NULL),
('rst-seed-00070', 'recipe-seed-0018', 2, 'Step 2', 'Bước 2: Ướp cá. Ướp cá rô với nước mắm, đường, bột ngọt, muối, tiêu, dầu ăn, nước màu (có thể dùng đường thốt nốt thắng caramel). Cho phần hành, tỏi, ớt băm và nghệ thái lát vào trộn đều. Ướp cá trong 20 phút cho thấm gia vị.', NULL, NULL, NULL),
('rst-seed-00071', 'recipe-seed-0018', 3, 'Step 3', 'Bước 3: Kho cá. Đặt nồi cá lên bếp, đổ thêm một chút nước lọc cho vừa ngập mặt cá. Đun sôi sau đó vặn lửa nhỏ, kho liu riu trong khoảng 15-20 phút cho đến khi nước cạn keo lại.', NULL, NULL, NULL),
('rst-seed-00072', 'recipe-seed-0018', 4, 'Step 4', 'Bước 4: Hoàn thành. Tắt bếp, ăn kèm với rau luộc hoặc rau sống.', NULL, NULL, NULL),
('rst-seed-00073', 'recipe-seed-0019', 1, 'Step 1', 'Bước 1: Sơ chế. Rửa cá với nước muối pha loãng, làm sạch máu và tủy ở xương sống để loại bỏ hoàn toàn mùi tanh (không dùng giấm hay rượu để giữ độ tươi). Cắt cá thành khúc vừa ăn.', NULL, NULL, NULL),
('rst-seed-00074', 'recipe-seed-0019', 2, 'Step 2', 'Bước 2: Ướp cá. Ướp cá với sả, gừng, hành khô băm nhỏ, tiêu, muối và một chút nước mắm. Đợi 30 phút cho cá ngấm gia vị và săn chắc lại.', NULL, NULL, NULL),
('rst-seed-00075', 'recipe-seed-0019', 3, 'Step 3', 'Bước 3: Chế biến thịt. Thịt ba chỉ thái miếng, đảo xém cạnh trên chảo rồi vớt ra lót dưới đáy nồi kho. Dùng mỡ lợn phi thơm một phần hành khô, sả, gừng.', NULL, NULL, NULL),
('rst-seed-00076', 'recipe-seed-0019', 4, 'Step 4', 'Bước 4: Kho cá. Xếp cá lên trên lớp thịt ba chỉ. Thắng đường thốt nốt tạo màu cánh gián rồi đổ nước (hoặc nước dừa) vào đun sôi. Rót nước màu ngập mặt cá. Đun vừa lửa trong 20 phút, sau đó giảm lửa liu riu kho thêm 1 giờ.', NULL, NULL, NULL),
('rst-seed-00077', 'recipe-seed-0019', 5, 'Step 5', 'Bước 5: Hoàn thiện. Tắt bếp. (Bí quyết: Cá đun lại lần 2 sẽ ngấm gia vị và thịt keo lại ngon hơn).', NULL, NULL, NULL),
('rst-seed-00078', 'recipe-seed-0020', 1, 'Step 1', 'Bước 1: Sơ chế nguyên liệu. Rau giá, rau muống, bắp chuối bào rửa sạch, để ráo. Cà chua cắt múi cau. Đậu hũ cắt miếng vuông, chiên vàng. Rau om cắt nhỏ. Thịt bắp bò thái mỏng.', NULL, NULL, NULL),
('rst-seed-00079', 'recipe-seed-0020', 2, 'Step 2', 'Bước 2: Xào thịt bò. Phi thơm tỏi băm, cho thịt bò vào xào sơ cho săn lại rồi gắp ra đĩa để riêng.', NULL, NULL, NULL),
('rst-seed-00080', 'recipe-seed-0020', 3, 'Step 3', 'Bước 3: Nấu nước dùng. Tiếp tục dùng nồi xào thịt bò, cho cà chua vào xào để tạo màu. Đổ nước lượng vừa đủ vào nồi đun sôi. Lấy nước cốt me hòa vào nồi.', NULL, NULL, NULL),
('rst-seed-00081', 'recipe-seed-0020', 4, 'Step 4', 'Bước 4: Nấu canh. Nước sôi, thả đậu hũ và các loại rau (rau muống, bắp chuối) vào. Nêm nếm muối, đường cho vừa vị chua ngọt. Khi nước sôi lại, cho thịt bò và giá vào, tắt bếp ngay để thịt không bị dai.', NULL, NULL, NULL),
('rst-seed-00082', 'recipe-seed-0020', 5, 'Step 5', 'Bước 5: Hoàn thiện. Nêm thêm chút nước mắm cho dậy mùi. Múc canh ra tô, rắc rau om, tỏi phi và tiêu xay lên trên.', NULL, NULL, NULL),
('rst-seed-00083', 'recipe-seed-0021', 1, 'Step 1', 'Bước 1: Sơ chế. Cá lóc phi lê rửa sạch, dùng giấy thấm thật khô nước, cắt thành miếng vừa ăn. Hành lá cắt nhuyễn.', NULL, NULL, NULL),
('rst-seed-00084', 'recipe-seed-0021', 2, 'Step 2', 'Bước 2: Pha bột. Cho vào tô lòng đỏ trứng gà, bột mì, một ít muối, dầu ăn và hành lá. Trộn đều, từ từ chế thêm nước lọc vào khuấy đến khi hỗn hợp bột có độ sánh sền sệt vừa phải.', NULL, NULL, NULL),
('rst-seed-00085', 'recipe-seed-0021', 3, 'Step 3', 'Bước 3: Tẩm bột chiên. Thả từng miếng cá vào tô bột ướt, sau đó lăn qua một lớp bột chiên giòn khô. Đun nóng chảo dầu, thả cá vào chiên cho đến khi vàng giòn đều hai mặt.', NULL, NULL, NULL),
('rst-seed-00086', 'recipe-seed-0021', 4, 'Step 4', 'Bước 4: Hoàn thành. Vớt cá ra giấy thấm dầu để ráo. Dùng nóng kèm với salad và tương ớt chua ngọt.', NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `scan_sessions`
--

CREATE TABLE `scan_sessions` (
  `id` varchar(36) NOT NULL,
  `user_id` varchar(64) NOT NULL,
  `image_name` varchar(255) NOT NULL,
  `vision_provider` varchar(50) NOT NULL,
  `raw_detections` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`raw_detections`)),
  `matched_ingredients` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`matched_ingredients`)),
  `created_at` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `scan_sessions`
--

INSERT INTO `scan_sessions` (`id`, `user_id`, `image_name`, `vision_provider`, `raw_detections`, `matched_ingredients`, `created_at`) VALUES
('51573087-9813-4c13-a3be-018690d6c738', 'mobile-demo-user', 'scaled_8415bbdd-a486-4276-a7be-6b77a0132e25629526932087736803.jpg', 'service_demo', '[{\"name\": \"ca chua\", \"confidence\": 0.96}, {\"name\": \"hanh tay\", \"confidence\": 0.9}, {\"name\": \"trung ga\", \"confidence\": 0.87}, {\"name\": \"toi\", \"confidence\": 0.73}]', '[{\"detected_name\": \"ca chua\", \"normalized_name\": \"ca chua\", \"confidence\": 0.96, \"matched\": true, \"ingredient\": {\"id\": \"7\", \"name\": \"C\\u00e0 chua\", \"icon\": \"\\ud83c\\udf45\", \"category_id\": \"c3\", \"image_url\": \"images/ca_chua.jpg\", \"is_popular\": true, \"aliases\": [\"tomato\"], \"created_at\": \"2026-03-17T20:12:55\", \"category\": {\"id\": \"c3\", \"slug\": \"rau-cu\", \"name\": \"Rau c\\u1ee7\", \"icon\": \"\\ud83e\\udd6c\", \"sort_order\": 3}}}, {\"detected_name\": \"hanh tay\", \"normalized_name\": \"hanh tay\", \"confidence\": 0.9, \"matched\": true, \"ingredient\": {\"id\": \"10\", \"name\": \"H\\u00e0nh t\\u00e2y\", \"icon\": \"\\ud83e\\uddc5\", \"category_id\": \"c3\", \"image_url\": \"images/hanh_tay.jpg\", \"is_popular\": true, \"aliases\": [\"onion\"], \"created_at\": \"2026-03-17T20:12:55\", \"category\": {\"id\": \"c3\", \"slug\": \"rau-cu\", \"name\": \"Rau c\\u1ee7\", \"icon\": \"\\ud83e\\udd6c\", \"sort_order\": 3}}}, {\"detected_name\": \"trung ga\", \"normalized_name\": \"trung ga\", \"confidence\": 0.87, \"matched\": true, \"ingredient\": {\"id\": \"5\", \"name\": \"Tr\\u1ee9ng g\\u00e0\", \"icon\": \"\\ud83e\\udd5a\", \"category_id\": \"c2\", \"image_url\": \"images/trung.jpg\", \"is_popular\": true, \"aliases\": [\"tr\\u1ee9ng\"], \"created_at\": \"2026-03-17T20:12:55\", \"category\": {\"id\": \"c2\", \"slug\": \"trung-sua\", \"name\": \"Tr\\u1ee9ng s\\u1eefa\", \"icon\": \"\\ud83e\\udd5a\", \"sort_order\": 2}}}, {\"detected_name\": \"toi\", \"normalized_name\": \"toi\", \"confidence\": 0.73, \"matched\": true, \"ingredient\": {\"id\": \"11\", \"name\": \"T\\u1ecfi\", \"icon\": \"\\ud83e\\uddc4\", \"category_id\": \"c3\", \"image_url\": \"images/toi.jpg\", \"is_popular\": true, \"aliases\": [\"garlic\"], \"created_at\": \"2026-03-17T20:12:55\", \"category\": {\"id\": \"c3\", \"slug\": \"rau-cu\", \"name\": \"Rau c\\u1ee7\", \"icon\": \"\\ud83e\\udd6c\", \"sort_order\": 3}}}]', '2026-03-17 14:52:38'),
('68e48ed9-be10-4678-8351-ee72aa482702', 'mobile-demo-user', 'scaled_f6a3d218-4c60-459c-8b21-72dd57c78baa3242634136507544555.jpg', 'service_demo', '[{\"name\": \"ca chua\", \"confidence\": 0.96}, {\"name\": \"hanh tay\", \"confidence\": 0.9}, {\"name\": \"trung ga\", \"confidence\": 0.87}, {\"name\": \"toi\", \"confidence\": 0.73}]', '[{\"detected_name\": \"ca chua\", \"normalized_name\": \"ca chua\", \"confidence\": 0.96, \"matched\": true, \"ingredient\": {\"id\": \"7\", \"name\": \"C\\u00e0 chua\", \"icon\": \"\\ud83c\\udf45\", \"category_id\": \"c3\", \"image_url\": \"images/ca_chua.jpg\", \"is_popular\": true, \"aliases\": [\"tomato\"], \"created_at\": \"2026-03-17T20:12:55\", \"category\": {\"id\": \"c3\", \"slug\": \"rau-cu\", \"name\": \"Rau c\\u1ee7\", \"icon\": \"\\ud83e\\udd6c\", \"sort_order\": 3}}}, {\"detected_name\": \"hanh tay\", \"normalized_name\": \"hanh tay\", \"confidence\": 0.9, \"matched\": true, \"ingredient\": {\"id\": \"10\", \"name\": \"H\\u00e0nh t\\u00e2y\", \"icon\": \"\\ud83e\\uddc5\", \"category_id\": \"c3\", \"image_url\": \"images/hanh_tay.jpg\", \"is_popular\": true, \"aliases\": [\"onion\"], \"created_at\": \"2026-03-17T20:12:55\", \"category\": {\"id\": \"c3\", \"slug\": \"rau-cu\", \"name\": \"Rau c\\u1ee7\", \"icon\": \"\\ud83e\\udd6c\", \"sort_order\": 3}}}, {\"detected_name\": \"trung ga\", \"normalized_name\": \"trung ga\", \"confidence\": 0.87, \"matched\": true, \"ingredient\": {\"id\": \"5\", \"name\": \"Tr\\u1ee9ng g\\u00e0\", \"icon\": \"\\ud83e\\udd5a\", \"category_id\": \"c2\", \"image_url\": \"images/trung.jpg\", \"is_popular\": true, \"aliases\": [\"tr\\u1ee9ng\"], \"created_at\": \"2026-03-17T20:12:55\", \"category\": {\"id\": \"c2\", \"slug\": \"trung-sua\", \"name\": \"Tr\\u1ee9ng s\\u1eefa\", \"icon\": \"\\ud83e\\udd5a\", \"sort_order\": 2}}}, {\"detected_name\": \"toi\", \"normalized_name\": \"toi\", \"confidence\": 0.73, \"matched\": true, \"ingredient\": {\"id\": \"11\", \"name\": \"T\\u1ecfi\", \"icon\": \"\\ud83e\\uddc4\", \"category_id\": \"c3\", \"image_url\": \"images/toi.jpg\", \"is_popular\": true, \"aliases\": [\"garlic\"], \"created_at\": \"2026-03-17T20:12:55\", \"category\": {\"id\": \"c3\", \"slug\": \"rau-cu\", \"name\": \"Rau c\\u1ee7\", \"icon\": \"\\ud83e\\udd6c\", \"sort_order\": 3}}}]', '2026-03-18 12:37:02'),
('771dbb0d-0e80-48a9-a672-4cc1c2bc4832', 'mobile-demo-user', 'scan_mock.jpg', 'service_demo', '[{\"name\": \"ca chua\", \"confidence\": 0.96}, {\"name\": \"hanh tay\", \"confidence\": 0.9}, {\"name\": \"trung ga\", \"confidence\": 0.87}, {\"name\": \"toi\", \"confidence\": 0.73}]', '[{\"detected_name\": \"ca chua\", \"normalized_name\": \"ca chua\", \"confidence\": 0.96, \"matched\": true, \"ingredient\": {\"id\": \"7\", \"name\": \"C\\u00e0 chua\", \"icon\": \"\\ud83c\\udf45\", \"category_id\": \"c3\", \"image_url\": \"images/ca_chua.jpg\", \"is_popular\": true, \"aliases\": [\"tomato\"], \"created_at\": \"2026-03-17T20:12:55\", \"category\": {\"id\": \"c3\", \"slug\": \"rau-cu\", \"name\": \"Rau c\\u1ee7\", \"icon\": \"\\ud83e\\udd6c\", \"sort_order\": 3}}}, {\"detected_name\": \"hanh tay\", \"normalized_name\": \"hanh tay\", \"confidence\": 0.9, \"matched\": true, \"ingredient\": {\"id\": \"10\", \"name\": \"H\\u00e0nh t\\u00e2y\", \"icon\": \"\\ud83e\\uddc5\", \"category_id\": \"c3\", \"image_url\": \"images/hanh_tay.jpg\", \"is_popular\": true, \"aliases\": [\"onion\"], \"created_at\": \"2026-03-17T20:12:55\", \"category\": {\"id\": \"c3\", \"slug\": \"rau-cu\", \"name\": \"Rau c\\u1ee7\", \"icon\": \"\\ud83e\\udd6c\", \"sort_order\": 3}}}, {\"detected_name\": \"trung ga\", \"normalized_name\": \"trung ga\", \"confidence\": 0.87, \"matched\": true, \"ingredient\": {\"id\": \"5\", \"name\": \"Tr\\u1ee9ng g\\u00e0\", \"icon\": \"\\ud83e\\udd5a\", \"category_id\": \"c2\", \"image_url\": \"images/trung.jpg\", \"is_popular\": true, \"aliases\": [\"tr\\u1ee9ng\"], \"created_at\": \"2026-03-17T20:12:55\", \"category\": {\"id\": \"c2\", \"slug\": \"trung-sua\", \"name\": \"Tr\\u1ee9ng s\\u1eefa\", \"icon\": \"\\ud83e\\udd5a\", \"sort_order\": 2}}}, {\"detected_name\": \"toi\", \"normalized_name\": \"toi\", \"confidence\": 0.73, \"matched\": true, \"ingredient\": {\"id\": \"11\", \"name\": \"T\\u1ecfi\", \"icon\": \"\\ud83e\\uddc4\", \"category_id\": \"c3\", \"image_url\": \"images/toi.jpg\", \"is_popular\": true, \"aliases\": [\"garlic\"], \"created_at\": \"2026-03-17T20:12:55\", \"category\": {\"id\": \"c3\", \"slug\": \"rau-cu\", \"name\": \"Rau c\\u1ee7\", \"icon\": \"\\ud83e\\udd6c\", \"sort_order\": 3}}}]', '2026-03-17 14:51:43'),
('f77da26c-910a-4a6a-a891-5b60dd2c2018', 'mobile-demo-user', 'scaled_e6175817-02c6-4115-a20b-3fde3ed750dd1224525859799777941.jpg', 'service_demo', '[{\"name\": \"ca chua\", \"confidence\": 0.96}, {\"name\": \"hanh tay\", \"confidence\": 0.9}, {\"name\": \"trung ga\", \"confidence\": 0.87}, {\"name\": \"toi\", \"confidence\": 0.73}]', '[{\"detected_name\": \"ca chua\", \"normalized_name\": \"ca chua\", \"confidence\": 0.96, \"matched\": true, \"ingredient\": {\"id\": \"7\", \"name\": \"C\\u00e0 chua\", \"icon\": \"\\ud83c\\udf45\", \"category_id\": \"c3\", \"image_url\": \"images/ca_chua.jpg\", \"is_popular\": true, \"aliases\": [\"tomato\"], \"created_at\": \"2026-03-17T20:12:55\", \"category\": {\"id\": \"c3\", \"slug\": \"rau-cu\", \"name\": \"Rau c\\u1ee7\", \"icon\": \"\\ud83e\\udd6c\", \"sort_order\": 3}}}, {\"detected_name\": \"hanh tay\", \"normalized_name\": \"hanh tay\", \"confidence\": 0.9, \"matched\": true, \"ingredient\": {\"id\": \"10\", \"name\": \"H\\u00e0nh t\\u00e2y\", \"icon\": \"\\ud83e\\uddc5\", \"category_id\": \"c3\", \"image_url\": \"images/hanh_tay.jpg\", \"is_popular\": true, \"aliases\": [\"onion\"], \"created_at\": \"2026-03-17T20:12:55\", \"category\": {\"id\": \"c3\", \"slug\": \"rau-cu\", \"name\": \"Rau c\\u1ee7\", \"icon\": \"\\ud83e\\udd6c\", \"sort_order\": 3}}}, {\"detected_name\": \"trung ga\", \"normalized_name\": \"trung ga\", \"confidence\": 0.87, \"matched\": true, \"ingredient\": {\"id\": \"5\", \"name\": \"Tr\\u1ee9ng g\\u00e0\", \"icon\": \"\\ud83e\\udd5a\", \"category_id\": \"c2\", \"image_url\": \"images/trung.jpg\", \"is_popular\": true, \"aliases\": [\"tr\\u1ee9ng\"], \"created_at\": \"2026-03-17T20:12:55\", \"category\": {\"id\": \"c2\", \"slug\": \"trung-sua\", \"name\": \"Tr\\u1ee9ng s\\u1eefa\", \"icon\": \"\\ud83e\\udd5a\", \"sort_order\": 2}}}, {\"detected_name\": \"toi\", \"normalized_name\": \"toi\", \"confidence\": 0.73, \"matched\": true, \"ingredient\": {\"id\": \"11\", \"name\": \"T\\u1ecfi\", \"icon\": \"\\ud83e\\uddc4\", \"category_id\": \"c3\", \"image_url\": \"images/toi.jpg\", \"is_popular\": true, \"aliases\": [\"garlic\"], \"created_at\": \"2026-03-17T20:12:55\", \"category\": {\"id\": \"c3\", \"slug\": \"rau-cu\", \"name\": \"Rau c\\u1ee7\", \"icon\": \"\\ud83e\\udd6c\", \"sort_order\": 3}}}]', '2026-03-17 15:03:44');

--
-- Chỉ mục cho các bảng đã đổ
--

--
-- Chỉ mục cho bảng `ingredients`
--
ALTER TABLE `ingredients`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `ix_ingredients_name` (`name`),
  ADD KEY `ix_ingredients_is_popular` (`is_popular`),
  ADD KEY `ix_ingredients_category_id` (`category_id`);

--
-- Chỉ mục cho bảng `ingredient_categories`
--
ALTER TABLE `ingredient_categories`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `ix_ingredient_categories_slug` (`slug`);

--
-- Chỉ mục cho bảng `pantry_items`
--
ALTER TABLE `pantry_items`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uq_pantry_user_ingredient` (`user_id`,`ingredient_id`),
  ADD KEY `ix_pantry_items_created_at` (`created_at`),
  ADD KEY `ix_pantry_items_user_id` (`user_id`),
  ADD KEY `ix_pantry_items_ingredient_id` (`ingredient_id`);

--
-- Chỉ mục cho bảng `recipes`
--
ALTER TABLE `recipes`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ix_recipes_difficulty` (`difficulty`),
  ADD KEY `ix_recipes_is_featured` (`is_featured`),
  ADD KEY `ix_recipes_name` (`name`);

--
-- Chỉ mục cho bảng `recipe_ingredients`
--
ALTER TABLE `recipe_ingredients`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ix_recipe_ingredients_recipe_id` (`recipe_id`),
  ADD KEY `ix_recipe_ingredients_ingredient_id` (`ingredient_id`);

--
-- Chỉ mục cho bảng `recipe_steps`
--
ALTER TABLE `recipe_steps`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ix_recipe_steps_recipe_id` (`recipe_id`);

--
-- Chỉ mục cho bảng `scan_sessions`
--
ALTER TABLE `scan_sessions`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ix_scan_sessions_user_id` (`user_id`),
  ADD KEY `ix_scan_sessions_created_at` (`created_at`);

--
-- Các ràng buộc cho các bảng đã đổ
--

--
-- Các ràng buộc cho bảng `ingredients`
--
ALTER TABLE `ingredients`
  ADD CONSTRAINT `ingredients_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `ingredient_categories` (`id`);

--
-- Các ràng buộc cho bảng `pantry_items`
--
ALTER TABLE `pantry_items`
  ADD CONSTRAINT `pantry_items_ibfk_1` FOREIGN KEY (`ingredient_id`) REFERENCES `ingredients` (`id`) ON DELETE CASCADE;

--
-- Các ràng buộc cho bảng `recipe_ingredients`
--
ALTER TABLE `recipe_ingredients`
  ADD CONSTRAINT `recipe_ingredients_ibfk_1` FOREIGN KEY (`recipe_id`) REFERENCES `recipes` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `recipe_ingredients_ibfk_2` FOREIGN KEY (`ingredient_id`) REFERENCES `ingredients` (`id`) ON DELETE SET NULL;

--
-- Các ràng buộc cho bảng `recipe_steps`
--
ALTER TABLE `recipe_steps`
  ADD CONSTRAINT `recipe_steps_ibfk_1` FOREIGN KEY (`recipe_id`) REFERENCES `recipes` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
