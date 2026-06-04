-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema it_project_management
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `it_project_management` ;

-- -----------------------------------------------------
-- Schema it_project_management
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `it_project_management` ;
USE `it_project_management` ;

-- -----------------------------------------------------
-- Table `it_project_management`.`clients`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `it_project_management`.`clients` ;

CREATE TABLE IF NOT EXISTS `it_project_management`.`clients` (
  `client_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `client_name` VARCHAR(150) NOT NULL,
  `industry` VARCHAR(100) NULL,
  `country` VARCHAR(100) NULL,
  `contact_person` VARCHAR(150) NULL,
  `contact_email` VARCHAR(150) NULL,
  `phone` VARCHAR(30) NULL,
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`client_id`),
  UNIQUE INDEX `client_name_UNIQUE` (`client_name` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `it_project_management`.`project_statuses`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `it_project_management`.`project_statuses` ;

CREATE TABLE IF NOT EXISTS `it_project_management`.`project_statuses` (
  `project_status_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `status_name` VARCHAR(50) NOT NULL,
  `is_final` TINYINT(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (`project_status_id`),
  UNIQUE INDEX `status_name_UNIQUE` (`status_name` ASC) VISIBLE,
  CONSTRAINT `chk_project_statuses_is_final`
    CHECK (`is_final` IN (0, 1)))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `it_project_management`.`projects`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `it_project_management`.`projects` ;

CREATE TABLE IF NOT EXISTS `it_project_management`.`projects` (
  `project_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `client_id` INT UNSIGNED NOT NULL,
  `project_status_id` INT UNSIGNED NOT NULL,
  `project_name` VARCHAR(150) NOT NULL,
  `description` TEXT NULL,
  `start_date` DATE NOT NULL,
  `planned_end_date` DATE NULL,
  `actual_end_date` DATE NULL,
  `total_budget` DECIMAL(12,2) NOT NULL DEFAULT 0.00,
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`project_id`),
  INDEX `fk_projects_clients_idx` (`client_id` ASC) VISIBLE,
  INDEX `fk_projects_project_statuses1_idx` (`project_status_id` ASC) VISIBLE,
  UNIQUE INDEX `projects_client_project_name_UNIQUE` (`client_id` ASC, `project_name` ASC) INVISIBLE,
  CONSTRAINT `fk_projects_clients`
    FOREIGN KEY (`client_id`)
    REFERENCES `it_project_management`.`clients` (`client_id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_projects_project_statuses1`
    FOREIGN KEY (`project_status_id`)
    REFERENCES `it_project_management`.`project_statuses` (`project_status_id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `chk_projects_total_budget`
    CHECK (`total_budget` >= 0),
  CONSTRAINT `chk_projects_planned_end_date`
    CHECK (`planned_end_date` IS NULL OR `planned_end_date` >= `start_date`),
  CONSTRAINT `chk_projects_actual_end_date`
    CHECK (`actual_end_date` IS NULL OR `actual_end_date` >= `start_date`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `it_project_management`.`employee_roles`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `it_project_management`.`employee_roles` ;

CREATE TABLE IF NOT EXISTS `it_project_management`.`employee_roles` (
  `role_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `role_title` VARCHAR(100) NOT NULL,
  `base_hourly_rate` DECIMAL(10,2) NOT NULL DEFAULT 0.00,
  `description` TEXT NULL,
  PRIMARY KEY (`role_id`),
  UNIQUE INDEX `role_title_UNIQUE` (`role_title` ASC) VISIBLE,
  CONSTRAINT `chk_employee_roles_base_hourly_rate`
    CHECK (`base_hourly_rate` >= 0))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `it_project_management`.`employees`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `it_project_management`.`employees` ;

CREATE TABLE IF NOT EXISTS `it_project_management`.`employees` (
  `employee_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(100) NOT NULL,
  `last_name` VARCHAR(100) NOT NULL,
  `email` VARCHAR(150) NOT NULL,
  `phone` VARCHAR(30) NULL,
  `hire_date` DATE NOT NULL,
  `role_id` INT UNSIGNED NOT NULL,
  `dept_id` INT UNSIGNED NOT NULL,
  `is_active` TINYINT(1) NOT NULL DEFAULT 1,
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`employee_id`),
  INDEX `fk_employees_employee_roles1_idx` (`role_id` ASC) VISIBLE,
  INDEX `fk_employees_departments1_idx` (`dept_id` ASC) VISIBLE,
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE,
  CONSTRAINT `fk_employees_employee_roles1`
    FOREIGN KEY (`role_id`)
    REFERENCES `it_project_management`.`employee_roles` (`role_id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_employees_departments1`
    FOREIGN KEY (`dept_id`)
    REFERENCES `it_project_management`.`departments` (`dept_id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `it_project_management`.`departments`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `it_project_management`.`departments` ;

CREATE TABLE IF NOT EXISTS `it_project_management`.`departments` (
  `dept_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `dept_name` VARCHAR(100) NOT NULL,
  `manager_id` INT UNSIGNED NULL,
  PRIMARY KEY (`dept_id`),
  UNIQUE INDEX `dept_name_UNIQUE` (`dept_name` ASC) VISIBLE,
  INDEX `fk_departments_employees1_idx` (`manager_id` ASC) VISIBLE,
  CONSTRAINT `fk_departments_employees1`
    FOREIGN KEY (`manager_id`)
    REFERENCES `it_project_management`.`employees` (`employee_id`)
    ON DELETE SET NULL
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `it_project_management`.`skills`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `it_project_management`.`skills` ;

CREATE TABLE IF NOT EXISTS `it_project_management`.`skills` (
  `skill_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `skill_name` VARCHAR(100) NOT NULL,
  `category` ENUM('Programming', 'Database', 'DevOps', 'QA', 'Design', 'Management', 'Soft Skills', 'Other') NOT NULL DEFAULT 'Other',
  `description` TEXT NULL,
  PRIMARY KEY (`skill_id`),
  UNIQUE INDEX `skill_name_UNIQUE` (`skill_name` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `it_project_management`.`employee_skills`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `it_project_management`.`employee_skills` ;

CREATE TABLE IF NOT EXISTS `it_project_management`.`employee_skills` (
  `employee_id` INT UNSIGNED NOT NULL,
  `skill_id` INT UNSIGNED NOT NULL,
  `proficiency_level` TINYINT NOT NULL DEFAULT 1,
  `confirmed_at` DATE NULL,
  PRIMARY KEY (`employee_id`, `skill_id`),
  INDEX `fk_skills_has_employees_employees1_idx` (`employee_id` ASC) VISIBLE,
  INDEX `fk_skills_has_employees_skills1_idx` (`skill_id` ASC) VISIBLE,
  CONSTRAINT `fk_skills_has_employees_skills1`
    FOREIGN KEY (`skill_id`)
    REFERENCES `it_project_management`.`skills` (`skill_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_skills_has_employees_employees1`
    FOREIGN KEY (`employee_id`)
    REFERENCES `it_project_management`.`employees` (`employee_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `chk_employee_skills_proficiency`
    CHECK (`proficiency_level` BETWEEN 1 AND 5))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `it_project_management`.`project_members`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `it_project_management`.`project_members` ;

CREATE TABLE IF NOT EXISTS `it_project_management`.`project_members` (
  `project_id` INT UNSIGNED NOT NULL,
  `employee_id` INT UNSIGNED NOT NULL,
  `project_role` VARCHAR(100) NOT NULL,
  `allocation_percentage` DECIMAL(5,2) NOT NULL DEFAULT 100.00,
  `joined_at` DATE NOT NULL,
  `left_at` DATE NULL,
  PRIMARY KEY (`project_id`, `employee_id`),
  INDEX `fk_projects_has_employees_employees1_idx` (`employee_id` ASC) VISIBLE,
  INDEX `fk_projects_has_employees_projects1_idx` (`project_id` ASC) VISIBLE,
  CONSTRAINT `fk_projects_has_employees_projects1`
    FOREIGN KEY (`project_id`)
    REFERENCES `it_project_management`.`projects` (`project_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_projects_has_employees_employees1`
    FOREIGN KEY (`employee_id`)
    REFERENCES `it_project_management`.`employees` (`employee_id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `chk_project_members_allocation`
    CHECK (`allocation_percentage` > 0 AND `allocation_percentage` <= 100),
  CONSTRAINT `chk_project_members_dates`
    CHECK (`left_at` IS NULL OR `left_at` >= `joined_at`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `it_project_management`.`sprints`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `it_project_management`.`sprints` ;

CREATE TABLE IF NOT EXISTS `it_project_management`.`sprints` (
  `sprint_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `project_id` INT UNSIGNED NOT NULL,
  `sprint_number` INT UNSIGNED NOT NULL,
  `sprint_goal` VARCHAR(255) NULL,
  `start_date` DATE NOT NULL,
  `end_date` DATE NOT NULL,
  `velocity_goal` INT UNSIGNED NOT NULL DEFAULT 0,
  PRIMARY KEY (`sprint_id`),
  INDEX `fk_sprints_projects1_idx` (`project_id` ASC) INVISIBLE,
  UNIQUE INDEX `project_id_UNIQUE` (`project_id` ASC, `sprint_id` ASC) VISIBLE,
  CONSTRAINT `fk_sprints_projects1`
    FOREIGN KEY (`project_id`)
    REFERENCES `it_project_management`.`projects` (`project_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `chk_sprints_dates`
    CHECK (`end_date` >= `start_date`),
  CONSTRAINT `chk_sprints_velocity`
	CHECK (`velocity_goal` >= 0))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `it_project_management`.`task_statuses`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `it_project_management`.`task_statuses` ;

CREATE TABLE IF NOT EXISTS `it_project_management`.`task_statuses` (
  `status_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `status_name` VARCHAR(50) NOT NULL,
  `is_final` TINYINT(1) NOT NULL DEFAULT 0,
  `sort_order` INT UNSIGNED NOT NULL DEFAULT 0,
  PRIMARY KEY (`status_id`),
  UNIQUE INDEX `status_name_UNIQUE` (`status_name` ASC) VISIBLE,
  CONSTRAINT `chk_task_statuses_is_final`
    CHECK (`is_final` IN (0, 1)))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `it_project_management`.`task_priorities`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `it_project_management`.`task_priorities` ;

CREATE TABLE IF NOT EXISTS `it_project_management`.`task_priorities` (
  `priority_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `priority_label` VARCHAR(50) NOT NULL,
  `response_time_sla_hours` INT UNSIGNED NOT NULL DEFAULT 24,
  PRIMARY KEY (`priority_id`),
  UNIQUE INDEX `priority_label_UNIQUE` (`priority_label` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `it_project_management`.`task_types`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `it_project_management`.`task_types` ;

CREATE TABLE IF NOT EXISTS `it_project_management`.`task_types` (
  `type_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `type_name` VARCHAR(50) NOT NULL,
  `description` TEXT NULL,
  PRIMARY KEY (`type_id`),
  UNIQUE INDEX `type_name_UNIQUE` (`type_name` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `it_project_management`.`tasks`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `it_project_management`.`tasks` ;

CREATE TABLE IF NOT EXISTS `it_project_management`.`tasks` (
  `task_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `project_id` INT UNSIGNED NOT NULL,
  `sprint_id` INT UNSIGNED NULL,
  `assignee_id` INT UNSIGNED NULL,
  `reporter_id` INT UNSIGNED NOT NULL,
  `type_id` INT UNSIGNED NOT NULL,
  `status_id` INT UNSIGNED NOT NULL,
  `priority_id` INT UNSIGNED NOT NULL,
  `task_title` VARCHAR(200) NOT NULL,
  `description` TEXT NULL,
  `story_points` DECIMAL(4,1) NOT NULL DEFAULT 0.0,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `due_date` DATE NULL,
  `completed_at` DATETIME NULL,
  PRIMARY KEY (`task_id`),
  INDEX `fk_tasks_sprints1_idx` (`sprint_id` ASC) VISIBLE,
  INDEX `fk_tasks_employees1_idx` (`assignee_id` ASC) INVISIBLE,
  INDEX `fk_tasks_employees2_idx` (`reporter_id` ASC) VISIBLE,
  INDEX `fk_tasks_task_types1_idx` (`type_id` ASC) VISIBLE,
  INDEX `fk_tasks_task_statuses1_idx` (`status_id` ASC) VISIBLE,
  INDEX `fk_tasks_task_priorities1_idx` (`priority_id` ASC) VISIBLE,
  INDEX `fk_tasks_projects1_idx` (`project_id` ASC) VISIBLE,
  CONSTRAINT `fk_tasks_sprints1`
    FOREIGN KEY (`sprint_id`)
    REFERENCES `it_project_management`.`sprints` (`sprint_id`)
    ON DELETE SET NULL
    ON UPDATE CASCADE,
  CONSTRAINT `fk_tasks_employees1`
    FOREIGN KEY (`assignee_id`)
    REFERENCES `it_project_management`.`employees` (`employee_id`)
    ON DELETE SET NULL
    ON UPDATE CASCADE,
  CONSTRAINT `fk_tasks_employees2`
    FOREIGN KEY (`reporter_id`)
    REFERENCES `it_project_management`.`employees` (`employee_id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_tasks_task_types1`
    FOREIGN KEY (`type_id`)
    REFERENCES `it_project_management`.`task_types` (`type_id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_tasks_task_statuses1`
    FOREIGN KEY (`status_id`)
    REFERENCES `it_project_management`.`task_statuses` (`status_id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_tasks_task_priorities1`
    FOREIGN KEY (`priority_id`)
    REFERENCES `it_project_management`.`task_priorities` (`priority_id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_tasks_projects1`
    FOREIGN KEY (`project_id`)
    REFERENCES `it_project_management`.`projects` (`project_id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `chk_tasks_story_points`
    CHECK (`story_points` >= 0),
  CONSTRAINT `chk_tasks_due_date`
    CHECK (`due_date` IS NULL OR `due_date` >= DATE(`created_at`)),
  CONSTRAINT `chk_tasks_completed_at`
    CHECK (`completed_at` IS NULL OR `completed_at` >= `created_at`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `it_project_management`.`time_logs`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `it_project_management`.`time_logs` ;

CREATE TABLE IF NOT EXISTS `it_project_management`.`time_logs` (
  `log_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `task_id` INT UNSIGNED NOT NULL,
  `employee_id` INT UNSIGNED NOT NULL,
  `hours_spent` DECIMAL(5,2) NOT NULL,
  `log_date` DATE NOT NULL,
  `description` TEXT NULL,
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`log_id`),
  INDEX `fk_time_logs_tasks1_idx` (`task_id` ASC) VISIBLE,
  INDEX `fk_time_logs_employees1_idx` (`employee_id` ASC) VISIBLE,
  CONSTRAINT `fk_time_logs_tasks1`
    FOREIGN KEY (`task_id`)
    REFERENCES `it_project_management`.`tasks` (`task_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_time_logs_employees1`
    FOREIGN KEY (`employee_id`)
    REFERENCES `it_project_management`.`employees` (`employee_id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `chk_time_logs_hours`
    CHECK (`hours_spent` > 0 AND `hours_spent` <= 24))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `it_project_management`.`task_comments`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `it_project_management`.`task_comments` ;

CREATE TABLE IF NOT EXISTS `it_project_management`.`task_comments` (
  `comment_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `task_id` INT UNSIGNED NOT NULL,
  `author_id` INT UNSIGNED NOT NULL,
  `content` TEXT NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`comment_id`),
  INDEX `fk_task_comments_tasks1_idx` (`task_id` ASC) VISIBLE,
  INDEX `fk_task_comments_employees1_idx` (`author_id` ASC) VISIBLE,
  CONSTRAINT `fk_task_comments_tasks1`
    FOREIGN KEY (`task_id`)
    REFERENCES `it_project_management`.`tasks` (`task_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_task_comments_employees1`
    FOREIGN KEY (`author_id`)
    REFERENCES `it_project_management`.`employees` (`employee_id`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
