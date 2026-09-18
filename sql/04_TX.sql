-- 트랜잭션 : 쪼갤 수 없는 논리적 업무 단위
-- 실제로는 여러 단계이지만 한 단계로 가정하는 것
-- 송금은 출금과 입금 두 단계 이지만, 둘 중 하나라도 실패하면 송금은 취소된다.
-- 이때 작업을 확정하는 것을 commit
-- 작업을 취소하는 것을 rollback
-- SQL 에서는 무조건 commit 을 해야 작업이 확정 된다.

-- 1) AUTOCOMMIT 이 설정되어 있어서 자동으로 커밋이 된다.
SELECT @@AUTOCOMMIT;

-- 2) AUTOCOMMIT 변경
SET @@AUTOCOMMIT = 0;

-- 지금까지의 상태를 저장
COMMIT;
DELETE FROM employees;

-- 이전 상태로 되돌리기
ROLLBACK;
SELECT * FROM employees;