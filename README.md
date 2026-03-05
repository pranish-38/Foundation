# Database Normalization and SQL JOIN using Docker & MySQL

## Database management Overview
This part demonstrates **database normalization (1NF, 2NF, 3NF)** and **SQL JOIN operations** using **MySQL running inside a Docker container**.

The goal is to design a structured database for **students joining clubs** while reducing redundancy and maintaining data integrity.

---

# Technologies Used
- Docker
- MySQL 8.0
- SQL
- GitHub

---

# 1. Running MySQL in Docker

Run a MySQL container:

```bash
docker run -d -p 3306:3306 \
-e MYSQL_ROOT_PASSWORD=root \
--name mysql-container \
mysql:8.0
```

Check running containers:

```bash
docker ps
```

Enter the container:

```bash
docker exec -it mysql-container bash
```

Start MySQL:

```bash
mysql -u root -p
```

Password:

```
root
```

---

# 2. Create Database

```sql
CREATE DATABASE school;
USE school;
```

---

# 3. First Normal Form (1NF)

Rules:
- Each column contains **atomic values**
- Each row has a **unique identifier**

Create table:

```sql
CREATE TABLE StudentClubs (
StudentID INT,
StudentName VARCHAR(50),
Email VARCHAR(100),
ClubName VARCHAR(50),
ClubRoom VARCHAR(20),
ClubMentor VARCHAR(50),
JoinDate DATE,
PRIMARY KEY (StudentID, ClubName)
);
```

Insert data:

```sql
INSERT INTO StudentClubs VALUES
(1,'Asha','asha@email.com','Music Club','R101','Mr. Raman','2024-01-10'),
(2,'Bikash','bikash@email.com','Sports Club','R202','Ms. Sita','2024-01-12'),
(1,'Asha','asha@email.com','Sports Club','R202','Ms. Sita','2024-01-15'),
(3,'Nisha','nisha@email.com','Music Club','R101','Mr. Raman','2024-01-20'),
(4,'Rohan','rohan@email.com','Drama Club','R303','Mr. Kiran','2024-01-18'),
(5,'Suman','suman@email.com','Music Club','R101','Mr. Raman','2024-01-22'),
(2,'Bikash','bikash@email.com','Drama Club','R303','Mr. Kiran','2024-01-25'),
(6,'Pooja','pooja@email.com','Sports Club','R202','Ms. Sita','2024-01-27'),
(3,'Nisha','nisha@email.com','Coding Club','Lab1','Mr. Anil','2024-01-28'),
(7,'Aman','aman@email.com','Coding Club','Lab1','Mr. Anil','2024-01-30');
```

View table:

```sql
SELECT * FROM StudentClubs;
```

---

# 4. Second Normal Form (2NF)

Remove **partial dependencies**.

## Student Table

```sql
CREATE TABLE Student (
StudentID INT PRIMARY KEY,
StudentName VARCHAR(50),
Email VARCHAR(100)
);
```

Insert students:

```sql
INSERT INTO Student VALUES
(1,'Asha','asha@email.com'),
(2,'Bikash','bikash@email.com'),
(3,'Nisha','nisha@email.com'),
(4,'Rohan','rohan@email.com'),
(5,'Suman','suman@email.com'),
(6,'Pooja','pooja@email.com'),
(7,'Aman','aman@email.com');
```

---

## Club Table

```sql
CREATE TABLE Club (
ClubName VARCHAR(50) PRIMARY KEY,
ClubRoom VARCHAR(20),
ClubMentor VARCHAR(50)
);
```

Insert clubs:

```sql
INSERT INTO Club VALUES
('Music Club','R101','Mr. Raman'),
('Sports Club','R202','Ms. Sita'),
('Drama Club','R303','Mr. Kiran'),
('Coding Club','Lab1','Mr. Anil');
```

---

## Membership Table

```sql
CREATE TABLE Membership (
StudentID INT,
ClubName VARCHAR(50),
JoinDate DATE,
PRIMARY KEY (StudentID, ClubName),
FOREIGN KEY (StudentID) REFERENCES Student(StudentID),
FOREIGN KEY (ClubName) REFERENCES Club(ClubName)
);
```

Insert memberships:

```sql
INSERT INTO Membership VALUES
(1,'Music Club','2024-01-10'),
(2,'Sports Club','2024-01-12'),
(1,'Sports Club','2024-01-15'),
(3,'Music Club','2024-01-20'),
(4,'Drama Club','2024-01-18'),
(5,'Music Club','2024-01-22'),
(2,'Drama Club','2024-01-25'),
(6,'Sports Club','2024-01-27'),
(3,'Coding Club','2024-01-28'),
(7,'Coding Club','2024-01-30');
```

---

# 5. Third Normal Form (3NF)

Remove **transitive dependencies**.

## Student3NF Table

```sql
CREATE TABLE Student3NF (
StudentID INT PRIMARY KEY,
StudentName VARCHAR(50),
Email VARCHAR(100)
);
```

```sql
INSERT INTO Student3NF VALUES
(1,'Asha','asha@email.com'),
(2,'Bikash','bikash@email.com'),
(3,'Nisha','nisha@email.com'),
(4,'Rohan','rohan@email.com'),
(5,'Suman','suman@email.com'),
(6,'Pooja','pooja@email.com'),
(7,'Aman','aman@email.com');
```

---

## Club3NF Table

```sql
CREATE TABLE Club3NF (
ClubID INT PRIMARY KEY,
ClubName VARCHAR(50),
ClubRoom VARCHAR(20),
ClubMentor VARCHAR(50)
);
```

```sql
INSERT INTO Club3NF VALUES
(101,'Music Club','R101','Mr. Raman'),
(102,'Sports Club','R202','Ms. Sita'),
(103,'Drama Club','R303','Mr. Kiran'),
(104,'Coding Club','Lab1','Mr. Anil');
```

---

## Membership3NF Table

```sql
CREATE TABLE Membership3NF (
StudentID INT,
ClubID INT,
JoinDate DATE,
PRIMARY KEY (StudentID, ClubID),
FOREIGN KEY (StudentID) REFERENCES Student3NF(StudentID),
FOREIGN KEY (ClubID) REFERENCES Club3NF(ClubID)
);
```

```sql
INSERT INTO Membership3NF VALUES
(1,101,'2024-01-10'),
(2,102,'2024-01-12'),
(1,102,'2024-01-15'),
(3,101,'2024-01-20'),
(4,103,'2024-01-18'),
(5,101,'2024-01-22'),
(2,103,'2024-01-25'),
(6,102,'2024-01-27'),
(3,104,'2024-01-28'),
(7,104,'2024-01-30');
```

---

# 6. SQL JOIN Operation

Display:
- Student Name
- Club Name
- Join Date

```sql
SELECT 
s.StudentName,
c.ClubName,
m.JoinDate
FROM Membership3NF m
JOIN Student3NF s
ON m.StudentID = s.StudentID
JOIN Club3NF c
ON m.ClubID = c.ClubID;
```

---

# Author

Pranish Khawas
