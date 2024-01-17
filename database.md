# Database Documentation
Certainly! Here's the structured representation of the tables:

### Table: `apply_csp`

| Column Name   | Data Type    | Constraints  |
| ------------- | ------------ | ------------ |
| id            | int(11)      | NOT NULL     |
| name          | varchar(255) | NOT NULL     |
| email         | varchar(255) | NOT NULL     |
| phonenumber   | varchar(255) | NOT NULL     |
| link          | varchar(255) | NOT NULL     |
| CAIQ_link     | varchar(255) | NOT NULL     |

### Table: `choices`

| Column Name   | Data Type    | Constraints  |
| ------------- | ------------ | ------------ |
| choices       | varchar(255) | DEFAULT NULL  |
| sub_id        | int(11)      | DEFAULT NULL  |

### Table: `cloud_provider`

| Column Name       | Data Type    | Constraints  |
| ----------------- | ------------ | ------------ |
| csp_id            | int(11)      | NOT NULL     |
| csp_name          | varchar(255) | NOT NULL     |
| website           | varchar(255) | DEFAULT NULL |
| performance_score | varchar(255) | DEFAULT NULL |

### Table: `contact`

| Column Name   | Data Type    | Constraints  |
| ------------- | ------------ | ------------ |
| id            | int(11)      | NOT NULL     |
| name          | varchar(255) | NOT NULL     |
| email         | varchar(255) | NOT NULL     |
| subject       | varchar(255) | NOT NULL     |
| message       | text         | NOT NULL     |

### Table: `controls`

| Column Name           | Data Type    | Constraints  |
| --------------------- | ------------ | ------------ |
| control_id            | int(11)      | NOT NULL     |
| control_name          | varchar(255) | NOT NULL     |
| control_description   | text         | DEFAULT NULL |

### Table: `history`

| Column Name   | Data Type    | Constraints  |
| ------------- | ------------ | ------------ |
| id            | int(11)      | NOT NULL     |
| user_id       | int(11)      | NOT NULL     |
| ranking       | varchar(255) | NOT NULL     |

### Table: `level1`

| Column Name       | Data Type    | Constraints  |
| ----------------- | ------------ | ------------ |
| csp_id            | int(11)      | NOT NULL     |
| csp_name          | varchar(255) | NOT NULL     |
| website           | varchar(255) | DEFAULT NULL |
| performance_score | varchar(255) | DEFAULT NULL |

### Table: `level2`

| Column Name       | Data Type    | Constraints  |
| ----------------- | ------------ | ------------ |
| csp_id            | int(11)      | NOT NULL     |
| csp_name          | varchar(255) | NOT NULL     |
| website           | varchar(255) | DEFAULT NULL |
| performance_score | varchar(255) | DEFAULT NULL |

### Table: `levels`

| Column Name   | Data Type    | Constraints  |
| ------------- | ------------ | ------------ |
| Id            | int(255)     | NOT NULL     |
| level_name    | varchar(255) | NOT NULL     |

### Table: `subcontrols`

| Column Name     | Data Type    | Constraints  |
| --------------- | ------------ | ------------ |
| subcontrol_id   | int(11)      | NOT NULL     |
| subcontrol_name | varchar(255) | DEFAULT NULL |
| control_id      | int(11)      | DEFAULT NULL |

