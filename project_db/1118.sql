--A, a (대소문자)가 들어가 있는 id를 출력하시오
select id from board where lower(id) like '%a%';
-- _, % 
select job_id from employees;
select job_id from employees where job_id like '%SH_%';
select job_id from employees where job_id like '%_%';
select job_id from employees where job_id like '%#_%' escape '#';
-- is null
select * from employees where manager_id is null;

-- 정렬 
-- 순차정렬 : order by asc,
-- 역순정렬 : order by desc,
-- 역순정렬은 null 값이 제일 위, 순차정렬은 null 제일 아래 위치함
select * from board order by bno desc;
select * from board order by bno asc;

select department_id, hire_date from employees;
select department_id, hire_date from employees order by department_id desc;
-- 앞 명령어인 역순정렬을 먼저 하고 난 후 뒤 같은 부서 든 이름이든 할 경우 뒤의 명령어를 실행함. 
select department_id, hire_date from employees order by department_id desc, hire_date asc;

-- 월급으로 역순정렬 출력하시오
select salary from employees order by salary desc;
-- 사원명으로 순처정렬 하시오
select emp_name from employees order by emp_name asc;
select emp_name from employees order by emp_name;

