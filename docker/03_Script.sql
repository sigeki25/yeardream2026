# 캐릭터셋 확인
SHOW VARIABLES LIKE "character_set%";
SHOW VARIABLES LIKE "collation%";

# 유저 생성 및 권한 부여
CREATE USER "web_user"@"%" IDENTIFIED BY "admin@pass";
SELECT * FROM mysql.user;

# 권한 부여
GRANT ALL PRIVILEGES ON *.* TO 'web_user';

# 데이터베이스 생성
CREATE DATABASE mydb;
SHOW DATABASES;

# 테이블 생성
USE mydb;  # 사용할 데이터베이스 선택(사용)
CREATE TABLE member(
	id VARCHAR(50) PRIMARY KEY,
	pw VARCHAR(100),
	name VARCHAR(50),
	gender VARCHAR(4),
	age INT(3),
	email VARCHAR(50)
);
DES

# 데이터 추가
INSERT INTO member(id, pw, name, age, gender, email) 
	VALUES("admin", "pass", "관리자", 33, "남", "admin@email.com");
SELECT * FROM member;