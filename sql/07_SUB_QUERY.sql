CREATE TABLE dept(
  deptno VARCHAR(10) PRIMARY KEY,
  deptname VARCHAR(20),
  loc VARCHAR(10)
);

-- 직원 테이블 생성
CREATE TABLE emp(
  ename varchar(20),
  job varchar(50),
  deptno VARCHAR(10),
  hiredate date
);

-- 키 설정
ALTER TABLE emp ADD CONSTRAINT fk_emp FOREIGN KEY(deptno) REFERENCES dept(deptno);


-- 데이터 삽입
INSERT INTO dept (deptno,deptname,loc)values(1, 'sales', 'NEWYORK');
INSERT INTO dept (deptno,deptname,loc)values(2, 'dev01', 'LA');
INSERT INTO dept (deptno,deptname,loc)values(3, 'personnel', 'NEWYORK');
INSERT INTO dept (deptno,deptname,loc)values(4, 'delevery', 'BOSTON');
SELECT * FROM dept;

INSERT INTO emp (ename,job,deptno,hiredate)values('kim', 'manager', 1, STR_TO_DATE('26/01/02','%Y/%m/%d'));
INSERT INTO emp (ename,job,deptno,hiredate)values('lee', 'staff', 1, STR_TO_DATE('25/01/02','%Y/%m/%d'));
INSERT INTO emp (ename,job,deptno,hiredate)values('han', 'staff', 1, STR_TO_DATE('26/03/02','%Y/%m/%d'));
INSERT INTO emp (ename,job,deptno,hiredate)values('kim', 'assistant', 1, STR_TO_DATE('15/09/22','%Y/%m/%d'));

INSERT INTO emp (ename,job,deptno,hiredate)values('ahn', 'staff', 2, STR_TO_DATE('25/11/02','%Y/%m/%d'));
INSERT INTO emp (ename,job,deptno,hiredate)values('hwang', 'manager', 2, STR_TO_DATE('25/08/12','%Y/%m/%d'));
INSERT INTO emp (ename,job,deptno,hiredate)values('cha', 'assistant', 2, STR_TO_DATE('22/03/02','%Y/%m/%d'));
INSERT INTO emp (ename,job,deptno,hiredate)values('hong', 'staff', 2, STR_TO_DATE('24/08/02','%Y/%m/%d'));
INSERT INTO emp (ename,job,deptno,hiredate)values('gang', 'staff', 2, STR_TO_DATE('26/01/02','%Y/%m/%d'));

INSERT INTO emp (ename,job,deptno,hiredate)values('nam', 'leader', 4, STR_TO_DATE('20/01/02','%Y/%m/%d'));
SELECT * FROM emp;

-- 문제1 : han의 근무 부서 이름
SELECT * FROM emp e WHERE e.ename = "han";
SELECT * FROM dept d WHERE d.deptno = 1;

SELECT * FROM dept d WHERE d.deptno = (SELECT deptno FROM emp e WHERE e.ename = "han");


SELECT * 
	FROM emp e LEFT JOIN dept d ON e.deptno = d.deptno 
	WHERE e.ename = "han";


-- 문제2 : 부서위치가 LA 또는 BOSTON 인 부서에 속한 사람의 이름과 직책
SELECT deptno FROM dept WHERE loc IN ("LA", "BOSTON");
SELECT ename, job FROM emp WHERE deptno IN (2, 4);
SELECT ename, job FROM emp WHERE deptno IN (SELECT deptno FROM dept WHERE loc IN ("LA", "BOSTON"));

-- 문제3 : sales 부서에 근무하는 사원의 이름, 직책, 입사일을 알아보기
SELECT deptno FROM dept WHERE deptname = "sales";
SELECT ename, job, hiredate FROM emp WHERE deptno = 1;

SELECT ename, job, hiredate FROM emp WHERE deptno IN (SELECT deptno FROM dept WHERE deptname = "sales");

-- 문제4 : 직책이 MANAGER 인 사원들 (여러명일 경우 가장 빠른사람 기준) 보다 입사일이 빠른 사람들의 이름, 직책, 입사일
SELECT * FROM emp WHERE job = "MANAGER" ORDER BY hiredate ASC LIMIT 1;
SELECT ename, job, hiredate FROM emp WHERE hiredate <= "2025-08-12";
SELECT ename, job, hiredate FROM emp WHERE hiredate <= (SELECT hiredate FROM emp WHERE job = "MANAGER" ORDER BY hiredate ASC LIMIT 1);

SELECT ename, job, hiredate FROM emp WHERE hiredate <= (SELECT MIN(hiredate) FROM emp WHERE job = "MANAGER");

SELECT ename, job, hiredate FROM emp WHERE hiredate <= ALL (SELECT hiredate FROM emp WHERE job = "MANAGER");

-- 문제5 : 부서별로 직원이 몇명인지
SELECT deptno, COUNT(*) as cnt FROM emp GROUP BY deptno;

SELECT deptname, (SELECT COUNT(*) FROM emp e WHERE e.deptno = d.deptno) AS count FROM dept d;

SELECT (SELECT deptname FROM dept d WHERE e.deptno = d.deptno) AS deptname, COUNT(deptno) AS count FROM emp e GROUP BY deptno;





