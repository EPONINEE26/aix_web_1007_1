-- 테이블 전체 확인
select * from tab;

--select : 검색, insert : 입력, update : 수정, delete : 삭제
-- 적용하려면 commit를 무조건 해야함 (commit : 적용)
-- commit 되기 전에 rollback 하면 되돌리기 기준점이 commit 했던 때
--각 테이블에 있는 row 데이터 검색
--테이블에 있는 컬럼유형 확인
desc member;

-- number : 정수, 실수 모두 포함하여 저장 가능
-- number(4) : 4자리까지 저장 가능 number (precision, sccle) 로 지정 (number(4,2) : 4자리 소숫점 2자리까지)
-- date : 2025년 12월 4일 / 04-12-25 / 04/12/25 이렇게 입력해도 가능
-- char, varchar 지정하고 난 후 수정할 경우 null값에 대한 처리 정보 입력을 위한 질문을 많이 함. 그렇기에 null=True로 지정을 해야함
-- create date, update date 를 두 개의 컬럼 생성이 좋음 

-- select : * 전체, 부분적 컬럼을 가지고 검색 가능
select * from employees;
select * from member;
select employee_id, emp_name, department_id from employees;
desc employees;

--number,char,varchar2,date 타입
--number : 사칙연산 (+,-,*,/)가능 
--date : +, - 가능
--varchar2 : 시칙연산 불가능 
select '가'+'나' from dual; -- 불가능. 에러 남 
select '가'||'나' from dual; -- 문자열 타입 || :가나... 이런 식으로는 가능 

select emp_name, email, emp_name||email from employees;

--number타입
select emp_name,salary from employees;
select salary*10 from employees; -- 숫자에만 사칙연산 가능. 
select salary*1342 from employees; -- *1342 (당일 환율로 곱해서 원화로 변경가능)
select emp_name,salary,salary*1342 from employees; 
select emp_name,salary,salary*1342 as k_salary from employees; 
select emp_name,salary,salary*1342 + (salary*1341*0.02) from employees; 
select sysdate from member;
select sysdate,sysdate+100 from member;  -- 금일부터 100일후의 날짜 확인
select sysdate-100,sysdate,sysdate+100 from member; --금일부터 100일전,후의 날짜 확인

--연산자
--salary, 원화로 원급출력, 원화로 연봉출력
-- 소문자가 에러가 날 경우 select 부분을 대문자로 변경해서 실행하면 처리 가능
select salary, salary*1342, salary*1342*12 FROM employees;
select salary, salary*1342 as k_salary, salary*1342*12 as k_anuel_salary from employees;

--판매부서만 commission (salary+salary*commission_pct : 실제 월급 계산식)
select salary, commission_pct,salary+salary*commission_pct from employees; -- commission_pct가 없을 경우 null값으로 출력되기에 월급정산이 안 됨
-- nvl(컬럼,0) : 없을때는 0으로 변경
select salary, commission_pct,salary+salary*nvl(commission_pct,0) real_salary from employees; 
--"" 안에 특수문자(@,$,%,&), 한글 등을 사용가능
select salary, commission_pct,salary+salary*nvl(commission_pct,0) "실제월급" from employees;

--부서테이블 모든 컬럼을 출력하시오
select * from departments;
select department_id, department_name from departments;
select department_id ||' 부서는 ' ||department_name from departments;

-- distinct : 중복 제거 
select distinct(department_id) from employees; 

-- job_id 중복제거 후 출력하시오
select distinct(job_id) from employees;
select * from jobs;

select department_id department_name from departments;
select department_id, department_name from employees;

--join의 기능
SELECT employees.department_id, department_name FROM employees, departments -- where 조건문 앞에는 세메콜론 없음
WHERE employees.department_id = departments.department_id;

-- where 조건절 : 비고 <,>,<=,>=,=,다르다 : <>,!=,
-- 두개 이상일 경우 and , or 가능
select salary from employees;
select emp_name,salary from employees
where salary>5000;
select salary from employees
where salary = 6000;
select employee_id,salary from employees
where salary >= 6000 and department_id=50;

-- 급여가 4000이하, 사원번호, 사원이름, 급여를 출력하시오
select department_id,emp_name, salary from employees
where salary<=4000;

select hire_date from employees;
-- 날짜 비교
select hire_date from employees
where hire_date > '07/01/01';

select hire_date from employees
where hire_date > '2007/01/01';

select hire_date from employees
where hire_date > '2007-01-01';

--select hire_date from employees
--where hire_date > '2007년01월01일'; -- 년,월,일 입력할 경우는 불가. 에러 

select hire_date from employees
where hire_date >= '2007-01-01' and hire_date <= '07/12/31';

-- 부서번호가 50 이면서 월급 8000 이상인 사원을 출력하시오.
select * from employees
where department_id = 50 and salary >= 8000;

-- 부서번호가 10 이거나 30 이거나 100 인 사원을 출력하시오.
select * from employees
where department_id=10 or department_id = 30 or department_id = 100;