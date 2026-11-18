-- 컬럼 확인
desc employees;
-- 사원번호, 이름, 입사일, 연봉을 출력하시오.
select employee_id, emp_name, hire_date, salary from employees;
select 
employee_id, emp_name, hire_date, salary 
from employees;

-- date : + - 만 가능
-- varchar2, char : + 만 가능
-- number : +,-,*,/ 가능 

select salary+1000 from employees;
select salary-1000 from employees;
select salary*1000 from employees;
select salary/1000 from employees;

-- salary 월급 / 년봉을 동시에 구하시오.
select employee_id, emp_name, salary as m_salary, salary*12 as y_salary from employees;

-- 달러인데, 원화금액 월급으로 변경하시오.
select employee_id, emp_name, salary as m_salary, salary*1330 as KWON from employees;
select emp_name, salary, commission_pct,salary+(salary*commission_pct) from employees;
select emp_name, salary, nvl(commission_pct,0),salary+(salary*nvl(commission_pct,0)) from employees;

-- as 이름 : 별칭 
select emp_name, salary, nvl(commission_pct,0) as nvl,salary+(salary*nvl(commission_pct,0)) as last_salary 
from employees;

select * from departments;
-- null 값 출력
-- manager 100번인 사원들을 출력하시오 
-- select 다음에 컬럼, from 다음에 table, 조건절 where 
select * from departments where manager_id=100 ;
select * from departments where manager_id<=500 ; 
select * from departments where manager_id>=200 ;
select * from departments where manager_id == null; -- 에러나거나 출력이 안 됨
select * from departments where manager_id is null;
select manager_id from departments;

- 2개의 컬럼을 1개의 컬럼으로 출력하는 방법
select * from employees;
select emp_name, email from employees; -- 2개의 컬럼으로 출력 
select emp_name || email as total from employees; -- 1개의 컬럼으로 합쳐서 출력
select concat(emp_name,email) from employees; -- concat이라는 명령어로 합쳐서 출력

select * from employees;
select manager_id from employees;

-- 중복 제거 
-- 정렬 : asc:순차정렬, desc:역순정렬
select distinct(manager_id) from employees;
select count(distinct(manager_id)) from employees;
select count(distinct(manager_id)) from employees
order by manager_id;
--총 개수 :107 
select count(*) from employees;

-- 
desc employees;
select job_id from employees;
select distinct(job_id) from employees;
select distinct(job_id) from employees order by job_id;
select distinct(department_id) from employees;
select distinct(department_id) from employees order by department_id;
select distinct(department_id||job_id) from employees;
select count(job_id) from employees;
select count(distinct(job_id)) from employees;
-- departments 테이블에서 부서가 몇 개인지 확인하시오.
select count(department_id) from employees;
select count(distinct(department_id)) from employees;
-- departments 테이블에서 어떠한 부서가 있는지 확인하시오. 
select department_name from departments;
select * from jobs;

select emp_name, salary from employees where salary>=5000;
select count(*) from employees where salary>=5000;
select emp_name, salary from employees where salary>=5000 and salary<=9000;
select emp_name, salary from employees where salary<=5000 or salary>=9000;

-- IS NULL, LIKE, IN 
-- <>, !=, ^= 
-- 3000은 2명 아닌 사람은 105명 
select salary from employees where salary=3000; 
select salary from employees where salary!=3000;
select salary from employees where salary=3000 or salary=4000 or salary=6000;
select salary from employees where salary in(3000,4000,6000);

-- 사원번호가 150번부터 200번까지 출력하시오
-- 사원번호가 130번 이하, 180번이상 출력하시오
-- 사원번호가 100,130,140,150번 출력하시오
select emp_name, employee_id from employees where employee_id>=150 and employee_id<=200;
select employee_id from employees;
desc employees;
select emp_name, employee_id from employees where employee_id<=130 or employee_id>=180;
select emp_name, employee_id from employees where employee_id in (100,130,140,150);

select * from employees;
select * from employees where email = 'DOCONNEL'; -- 값은 대소문자를 구별하고, 나머지 명령어는 대소문자를 구별하지 않음
SELECT * FROM EMPLOYEES WHERE EMAIL = 'DOCONNEL';
-- 문자 검색 = 만 가능 
select * from employees where emp_name = 'Donald O''Connell'; 

--날짜 검색. 날짜 형태는 형태지정은 없음
select * from employees where hire_date <='2005/01/01';
select * from employees where hire_date <='05-01-01';

-- 110,130,140,150 번 사원번호가 아닌 사원을 출력하시오
select employee_id from employees where employee_id not in (110,130,140,150);

-- 급여가 5000~7000 사이 또는 8000,9000인 사원을 출력하시오.
-- 묶음으로 묶어서 실행
select * from employees where (salary<=5000 and salary>=7000) or salary in (8000,9000);
-- 직급이 manager이면서 부서번호 50번인 사원을 출력하시오
select job_id from employees;
select * from employees;

-- like : 포함된 것
select employee_id, job_id, department_id from employees;
select job_id from employees where job_id like '%MAN%' and department_id=50;
select employee_id, job_id, department_id from employees where job_id like '%MAN%' and department_id=50;

-- 100번부터 109번까지 출력하시오
select * from employees order by employee_id;
select * from employees order by employee_id;
select * from employees where employee_id>=100 and employee_id<=190 order by employee_id ;
select * from employees where employee_id between 100 and 190;

-- 사원번호 130~140번 / 170~180번까지 출력하시오
select * from employees where (employee_id>=130 and employee_id<=140) or (employee_id>=170 and employee_id<=180);
select * from employees where employee_id between 130 and 140 or employee_id between 170 and 180;




