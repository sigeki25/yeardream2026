/* 문자열 캐릭터셋 변경 (latin1 -> utf8mb4)
sudo vim /etc/my.cnf

[mysqld]
character-set-server = utf8mb4
collation-server = utf8mb4_unicode_ci
추가 후 :wq

sudo systemctl restart mariadb
systemctl status matiadb
*/

SHOW VARIABLES LIKE 'character_set%'

-- 캐릭터셋이 바뀌기 전에 만들어져버린 database 와 table 에 대해서 변경
ALTER DATABASE mydb CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
ALTER TABLE employees CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;


USE mydb;
-- INSERT
-- INSERT INTO [테이블명]([컬럼명,...])VALUES([값들,...]);
INSERT INTO employees(
	emp_no, first_name, family_name, email, mobile, salary, depart_no, commission
) VALUES(
	111, "이름1", "성", "test1@gmail.com", "01011111111", "90000000", "dev001", 90
);

INSERT INTO employees(
	emp_no, first_name, family_name, email, mobile, salary
) VALUES(
	112, "이름2", "성", "test2@gmail.com", "01022222222", "90000000"
);

INSERT INTO employees(
	emp_no, family_name, email, mobile, salary
) VALUES(
	113, "성", "test3@gmail.com", "01033333333", "90000000"
);


SELECT * FROM employees e;

-- UPDATE
-- UPDATE [테이블] SET [컬럼]=[값] WHERE [조건]
UPDATE employees SET depart_no = "dev002" WHERE depart_no IS NULL;
UPDATE employees SET commission = 10 WHERE commission IS NULL;


-- DELETE
-- DELETE FROM [테이블명] WHERE [조건]
DELETE FROM employees WHERE first_name IS NULL;
SELECT * FROM employees e;

-- UPSERT(나중에 자세하게...)
-- 키가 중복되면 UPDATE, 중복되지 않으면 INSERT
-- 키가 없으면 실행할 수 없다.
INSERT INTO employees(emp_no, first_name, family_name, email, mobile, salary)
	VALUES(112, "이름2", "성", "test2@gmail.com", "01022222222", 50000000)
	ON DUPLICATE KEY UPDATE first_name="이름2";

desc employees;