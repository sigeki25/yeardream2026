-- test_data 를 서버에 이동(filezilla 활용)
-- dump 복원 작업 (dump 란? DB 데이터 전체를 저장해 놓은 것을 말함)
-- dump 는 최소 월 1회정도는 권장
-- 이 덤프는 어떤 데이터베이스를 가지고 있는가? employees
CREATE DATABASE employees; -- database 를 먼저 만들어 주자
-- DB 가 있는 곳에서 복구 명령어 실행
-- putty 를 통해 서버에 접근
-- [mysql|mariadb] -u root -p [넣을 데이터 베이스] < [실행할 sql 경로]
mysql -u root -p employees < test_data/employees.sql

USE employees;
SHOW tables;
-- 데이터 파악
SELECT * FROM current_dept_emp limit 5; -- 현재 사원별 소속 팀
DESC current_dept_emp;

SELECT * FROM departments limit 5; -- 팀 정보
SELECT * FROM dept_emp; -- 사원별 소속 팀(현재뿐 아니라 과거정보도 있나?)
SELECT * FROM dept_emp_latest_date limit 5; -- 부서별 사원 최신(current_dept_emp 와 비슷?)
SELECT * FROM dept_manager limit 5; -- 부서별 매니저(담당자)
SELECT * FROM employees limit 5; -- 사원
SELECT * FROM salaries limit 5; -- 급여
SELECT * FROM titles limit 5; -- 직책


-- 문제 1번 : 사원들의 이름(성과 이름을 합쳐서)과 입사일, 직책을 입사일이 빠른 순으로 보여주시오
SELECT 
	e.emp_no,
	CONCAT(e.first_name,', ',e.last_name) as name,
	t.title,
	e.hire_date 
FROM employees e JOIN titles t ON e.emp_no = t.emp_no 
	ORDER BY e.hire_date ASC;

-- 직책은 기간이 지남에 따라 변경될수 있기에 titles 에 히스토리처럼 쌓인다.
-- 최신의 title 만 나오도록 수정
SELECT * FROM titles t WHERE t.to_date = '9999-01-01';

-- 이걸 위에서 작성한 쿼리문에 적용 해 보자!
SELECT 
	e.emp_no,
	CONCAT(e.first_name,', ',e.last_name) as name,
	t.title,
	e.hire_date,
	t.to_date 
FROM employees e JOIN titles t ON e.emp_no = t.emp_no 
	WHERE t.to_date = '9999-01-01'
	ORDER BY e.hire_date ASC;

-- dept_emp 를 보면 사원이 여러 팀을 옮겨다닌 경우가 있다는것을 알 수 있다.
SELECT COUNT(emp_no) FROM employees; -- 300,024
SELECT COUNT(emp_no) FROM dept_emp; -- 331,603


-- 문제 2 : 팀 이동이 있었던 사원의 이름을 가져오세요
-- 1 단계 : 부서이동이 있는 사람의 사원번호 추출
SELECT 
	de.emp_no, 
	COUNT(de.emp_no) as cnt 
FROM dept_emp de GROUP BY emp_no HAVING cnt > 1;

-- 2 단계 : 이렇게 추출한 emp_no 로 employees 에서 이름 가져오기
-- 서브쿼리를 조건으로
SELECT 
	e.emp_no,
	CONCAT(e.first_name,', ',e.last_name) as name 
FROM employees e WHERE e.emp_no IN (
	SELECT de.emp_no FROM dept_emp de GROUP BY emp_no HAVING COUNT(de.emp_no) > 1
); -- 0.176 S

-- 서브쿼리를 상하관계 쿼리로 활용하여 조인
SELECT 
	e.emp_no,
	CONCAT(e.first_name,', ',e.last_name) as name 
FROM employees e JOIN 
(SELECT de.emp_no, COUNT(de.emp_no) as cnt 
	FROM dept_emp de GROUP BY emp_no HAVING cnt > 1) d
ON e.emp_no = d.emp_no; -- 0.237 S


-- 문제 3 : 각 인원들이 어느팀에서 어느팀으로 이동했는지 알아보기
-- 이름, 팀명, from_date, to_date
-- 이름 팀명은 모르지만, 이동 순서대로 정렬
-- 서브쿼리
SELECT 
	-- 이후 emp_no 와 dept_no 를 통해 서브쿼리로 원하는 데이터 추출
	(SELECT CONCAT(first_name,',',last_name) FROM employees WHERE emp_no = de.emp_no) AS name,
	(SELECT dept_name FROM departments WHERE dept_no = de.dept_no)AS team_name,
	de.from_date,
	de.to_date
FROM dept_emp de WHERE de.emp_no 
IN (SELECT de.emp_no FROM dept_emp de GROUP BY emp_no HAVING COUNT(de.emp_no) > 1)
ORDER BY emp_no, from_date; -- 0.25S

-- JOIN 이용
-- 1) departements 와 dept_emp JOIN
SELECT 
	d.dept_name,
	de.emp_no,
	de.from_date,
	de.to_date
FROM departments d JOIN dept_emp de ON d.dept_no = de.dept_no;

-- 2) employees 와 JOIN
SELECT 
	de.emp_no,
	d.dept_name,
	CONCAT(e.first_name,', ',e.last_name) AS name, 
	de.from_date,
	de.to_date
FROM departments d JOIN dept_emp de ON d.dept_no = de.dept_no
JOIN employees e ON de.emp_no = e.emp_no 
-- 부서 이동이 있는 사람들만 추려서...
WHERE de.emp_no 
IN (SELECT de.emp_no FROM dept_emp de GROUP BY emp_no HAVING COUNT(de.emp_no) > 1)
-- 이후 emp_no 와 to_date 순으로 정렬
ORDER BY de.emp_no, de.to_date; -- 0.802 S


-- 문제 4. 현재 MANAGER 들의 이름, 성별, 입사일, 소속팀명
-- 현재 팀장들의 사원번호와 팀번호
SELECT dm.emp_no, dm.dept_no FROM dept_manager dm WHERE dm.to_date = '9999-01-01';
-- 사원정보
SELECT e.first_name, e.last_name, e.gender, e.hire_date FROM employees e WHERE emp_no = '110039';
-- 팀 이름
SELECT d.dept_name FROM departments d WHERE d.dept_no = 'd001';

-- JOIN?(1개이상 컬럼을 가져올때) 서브쿼리?(1개컬럼 가져올 경우) 어느게 좋은가?
-- 1단계 : dept_manager 와 employees 를 JOIN
-- 2단계 : dept_name 에 대해서만 서브쿼리로 가져온다.
SELECT 
	CONCAT(e.first_name,', ',e.last_name) AS name,
	e.gender,
	e.hire_date,
	(SELECT dept_name FROM departments WHERE dept_no = dm.dept_no) AS team_name
FROM dept_manager dm NATURAL JOIN employees e 
ORDER BY e.hire_date;


-- 문제 5. 현재 직원들의 사번, 이름, 직책, 급여
SELECT e.emp_no, e.first_name, e.last_name FROM employees e;
SELECT t.emp_no, t.title FROM titles t WHERE t.to_date = '9999-01-01';
SELECT s.emp_no, s.salary FROM salaries s WHERE s.to_date = '9999-01-01';
-- 조합
-- NULL 이 나타나는 데이터 발생(알고보니 employees 는 퇴사자의 데이터도 모두 가지고 있음)
-- 그리고 그사람이 퇴사상태인지 알수 있는 방법도 없음
SELECT 
	e.emp_no,
	CONCAT(e.first_name,', ',e.last_name) AS name,
	(SELECT s.salary FROM salaries s 
		WHERE s.to_date = '9999-01-01' AND s.emp_no = e.emp_no)AS 급여,
	(SELECT t.title FROM titles t 
		WHERE t.to_date = '9999-01-01' AND t.emp_no = e.emp_no) AS 팀명
FROM employees e;

SELECT * FROM titles t WHERE t.emp_no = 10008;

-- 그래서 기본 데이터를 titles 에서 시작한다.
SELECT 
	t.emp_no,
	(SELECT 
		CONCAT(first_name,',',last_name) FROM employees WHERE emp_no = t.emp_no) AS 이름,
	(SELECT salary FROM salaries WHERE emp_no = t.emp_no AND to_date = '9999-01-01') AS 급여,
	t.title AS 직급
FROM titles t WHERE t.to_date = '9999-01-01';













