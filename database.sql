CREATE DATABASE IF NOT EXISTS school_db;
USE school_db;

CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    roll_no INT UNIQUE,
    name VARCHAR(100),
    class VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS attendance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    date DATE,
    status VARCHAR(10),
    FOREIGN KEY (student_id) REFERENCES students(id)
);

CREATE TABLE IF NOT EXISTS marks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    subject VARCHAR(100),
    marks INT,
    FOREIGN KEY (student_id) REFERENCES students(id)
);