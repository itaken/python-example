CREATE TABLE `goods_info_tbl` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `goods_id` int(11) DEFAULT '0',
  `user_id` int(11) DEFAULT '0',
  `title` varchar(45) DEFAULT NULL,
  `ubb_detail` mediumtext,
  `html_detail` mediumtext,
  `ratio` float DEFAULT '0'
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

