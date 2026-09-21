-- [QUERY] [UNION | UNION ALL | INTERSECT] [QUERY]
-- 동일한 컬럼이 있어야 SET 연산이 가능하다.
SELECT deptno FROM dept UNION SELECT deptno FROm emp;
SELECT deptno FROM dept UNION ALL SELECT deptno FROm emp;
SELECT deptno FROM dept INTERSECT SELECT deptno FROm emp;

-- LEFT JOIN + RIGHT JOIN 효과를 UNOIN 으로
SELECT e.ename, deptno, d.deptname FROM emp e LEFT JOIN dept d USING (deptno)
UNION
SELECT e.ename, deptno, d.deptname FROM emp e RIGHT JOIN dept d USING (deptno);

-- 교집합(INTERSECT) : 등가조인과 같은 효과
SELECT deptno FROM dept
INTERSECT
SELECT deptno FROM emp;

-- 차집합(MINUS) NOT IN

SELECT DISTINCT deptno FROM dept;
SELECT DISTINCT deptno FROM emp;

SELECT DISTINCT deptno FROM dept WHERE deptno NOt IN (SELECT DISTINCT deptno FROM emp);
SELECT DISTINCT deptno FROM emp WHERE deptno NOt IN (SELECT DISTINCT deptno FROM dept);
