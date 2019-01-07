DROP TABLE IF EXISTS `role`;

CREATE TABLE `role` (
  `role_id` int(11) NOT NULL AUTO_INCREMENT,
  `roleName` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`role_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO `role` (`role_id`, `roleName`)
VALUES(1,'ADMIN');


DROP TABLE IF EXISTS `user_role`;

CREATE TABLE `user_role` (
  `user_id` int(11) NOT NULL,
  `role_id` int(11) NOT NULL,
  PRIMARY KEY (`user_id`,`role_id`),
  UNIQUE KEY `UK_it77eq964jhfqtu54081ebtio` (`role_id`),
  CONSTRAINT `FK859n2jvi8ivhui0rl0esws6o` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`),
  CONSTRAINT `FKa68196081fvovjhkek5m97n3y` FOREIGN KEY (`role_id`) REFERENCES `role` (`role_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO `user_role` (`user_id`, `role_id`)
VALUES(1,1);


ALTER TABLE user
ADD password varchar(10);


ALTER TABLE user
ADD username varchar(20);


Drop table company

CREATE TABLE `company` (
  `company_id` int(11) NOT NULL AUTO_INCREMENT,
  `companyname` varchar(255) DEFAULT NULL,
  `tinnumber` int(20) NOT NULL,
  `street` varchar(255) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`company_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



CREATE TABLE `country` (
  `country_id` int(11) NOT NULL AUTO_INCREMENT,
  `country` varchar(255) NOT NULL UNIQUE,
  PRIMARY KEY (`country_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE `state` (
  `state_id` int(11) NOT NULL AUTO_INCREMENT,
  `state` varchar(255) NOT NULL UNIQUE,
  PRIMARY KEY (`state_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE `city` (
  `city_id` int(11) NOT NULL AUTO_INCREMENT,
  `city` varchar(255) NOT NULL UNIQUE,
  PRIMARY KEY (`city_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

ALTER TABLE state
    ADD country_id int(11),
    ADD CONSTRAINT FOREIGN KEY(country_id) REFERENCES country(country_id);

ALTER TABLE city
    ADD state_id int(11),
    ADD CONSTRAINT FOREIGN KEY(state_id) REFERENCES state(state_id);

  
ALTER TABLE company
    ADD state_id int(11),
    ADD CONSTRAINT FOREIGN KEY(state_id) REFERENCES state(state_id);

ALTER TABLE company
    ADD country_id int(11),
    ADD CONSTRAINT FOREIGN KEY(country_id) REFERENCES country(country_id);

ALTER TABLE company
    ADD city_id int(11),
    ADD CONSTRAINT FOREIGN KEY(city_id) REFERENCES City(city_id);

CREATE TABLE `report` (
`report_id` NOT NULL AUTO_INCREMENT,
`oppId` varchar(255),
  `campaignName` varchar(255),
 `valueItem` int(30),
  `AE` varchar(255),
  `AM` varchar(255),
  `year` int(11),
  `month` varchar(255),
  `finalTotal` int(30),
  `remaining` int (30),
  `subtotal` int(30)
  PRIMARY KEY (`report_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
    
    