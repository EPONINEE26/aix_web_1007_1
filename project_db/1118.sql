-- sql query구문을 사용해서 데이터검색,입력,수정,삭제
-- 테이블 생성,삭제,변경

-- 주석임.
select * from member;
select * from employees;

-- 테이블의 컬럼 속성을 보여줌.
desc employees;

-- NUMBER : 숫자타입(자리수,소수점)
-- num number(4,2) -- 4:전체자리수, 2:소수점  (정수부분 2자리만 사용가능) 
create table memnum (bno number(4,2),bno2 number(3));

insert into memnum (bno,bno2) values 
(12.12,999);

-- 4.2 : 정수부분 2자리여야 함. 소수점자리가 2자리
insert into memnum (bno) values 
(12);

select * from memnum;

-- 테이블 삭제
-- drop table memnum;

desc employees;

select create_date+100 from employees;
select create_date-100 from employees;
select create_date*100 from employees;
select create_date/100 from employees;

-- select문 : 검색
-- insert문 : 입력
-- update문 : 수정
-- delete문 : 삭제

select employee_id,emp_name from employees;
-- 삭제 후에는 무조건 주석처리해야함. 그렇지 않을 경우 중요한 정보까지 삭제될 가능성이 높음
-- drop table member;

create table member(
id varchar2(20) primary key, --중복이 안됨, null입력이 안됨. 유일키
pw varchar2(100) not null,
name varchar2(50),
phone varchar2(20)
);

select * from member;

insert into member (id,pw,name,phone) values (
'aaa','1111','홍길동','010-1111-1111'
);

insert into member values (
'bbb','1111','유관순','010-2222-2222'
);
insert into member values (
'ccc','1111','이순신','010-3333-3333'
);
insert into member values (
'ddd','1111','강감찬','010-3333-3333'
);


delete from member where id='ccc';

update member set pw='0000' where id='ddd';
update member set pw='4444' where id='ddd';

select * from member;
commit;
-- commit 하기 전엔 rollback 가능. 
rollback; 

-- -------------------------
desc employees;

-- 사원번호,이름,입사일,연봉을 출력하시오.
select 
employee_id,emp_name,hire_date,salary from employees;

desc employees;
select salary+1000 from employees;
select salary-1000 from employees;
select salary*1000 from employees;
select salary/1000 from employees;

-- 사원번호,이름,월급,년봉을 출력하시오.
select employee_id,emp_name,salary,salary*12 from employees;
-- 달러인데, 원화금액 월급으로 변경하시오.
-- 사원번호, 이름, 월급, 원화월급
select employee_id, emp_name,salary, salary*1330 from employees;

-- as 이름 : 별칭
select emp_name,salary, nvl(commission_pct,0) as nvl, 
salary+(salary*nvl(commission_pct,0)) as last_salary from employees;

select * from departments;

-- null값 출력
-- 매니저가 100 사원들을 출력하시오.
-- select 컬럼 from 테이블 조건절 where
select * from departments where manager_id<=200;

select * from departments where manager_id = null; -- 출력이 안 되거나 에러가 남 
-- IS NULL 
select * from departments where manager_id is null;
select manager_id from departments;

-- 2개의 컬럼을 1개의 컬럼으로 출력하는 방법
select * from employees;
select emp_name,email from employees;
select emp_name||email as total from employees;
select concat(emp_name,email) from employees;

-- distinct : 중복제거, 정렬-asc:순차정렬,desc:역순정렬
-- count() : 개수
select count(distinct(manager_id)) from employees
order by manager_id;

-- 총개수 : 107
select count(*) from employees;

desc employees;
-- job_id를 중복제거해서 출력하시오.
-- department_id를 중복제거해서 출력하시오.
-- departments테이블에서 부서가 몇개 있는지 확인하시오.
select distinct(job_id) from employees;
select count(job_id) from employees;
select * from jobs;

select distinct(department_id) from employees order by department_id;
select count(department_id) from employees;
select department_id from departments;

select emp_name,salary from employees 
where salary>=5000 and salary<=9000;

select emp_name,salary from employees 
where salary<=5000 or salary>=9000;

select count(*) from employees 
where salary>=5000 ;

-- 3000 2명, 아닌사원 105명
select salary from employees 
where salary!=3000;

select salary from employees 
where salary = 3000 or salary=4000 or salary=6000;

select salary from employees 
where salary in(3000,4000,6000);


-- 사원번호 150~200까지 출력하시오
-- 사원번호 130번 이하, 180번이상 출력하시오.
-- 사원번호가 110,130,140,150번 출력하시오.
select employee_id,salary from employees 
where employee_id>=150 and employee_id<=200;
select employee_id,salary from employees 
where employee_id<=130 or employee_id>=180;
select employee_id,salary from employees 
where employee_id in (110,130,140,150);


select * from employees;

select * from employees where EMAIL = 'DOCONNEL';

SELECT * FROM EMPLOYEES WHERE EMAIL = 'DOCONNEL';

-- 문자검색
select * from employees where emp_name = 'Donald OConnell';

-- 날짜 검색 <,>,=
select * from employees where hire_date <= '2005/01/01';



-- 110,130,140,150 가 아닌 사원을 출력하시오.
select employee_id from employees
where employee_id in(110,130,140,150);

-- 급여가 5000~7000 사이 또는 8000,9000 인 사원을 출력하시오.
select * from employees
where (salary>=5000 and salary<=7000) or salary in(8000,9000);

-- 직급이 man, 부서번호 50 인 사원을 출력하시오.
select employee_id,emp_name,job_id,department_id from employees;

select employee_id,emp_name,job_id,department_id from employees
where (job_id like '%MAN%') and department_id=50;

-- 100~109까지 출력하시오.
select * from employees
where employee_id>100 and employee_id<=109
order by employee_id;

-- >=, <=
select * from employees
where employee_id between 100 and 109;


-- 사원번호 130~140 / 170~180까지 출력하시오.
select * from employees
where (employee_id between 130 and 140) 
or (employee_id between 170 and 180);


select * from employees
where employee_id in (110,120,130);

-- 110,120,130 을 출력하시오.
select * from employees
where employee_id=110 or employee_id=120 or employee_id=130;


-- like
-- L% : 첫번째 글자가 L
-- _e%
select * from employees where emp_name like 'L%';

select * from employees where emp_name like '__e%';

-- H가 포함되어 있는 이름을 출력하시오.
-- 9번째 h가 들어가 있는 이름을 출력하시오.
select * from employees where emp_name like '________H%';

-- board 테이블 생성
create table board (
-- bno,id,btitle,bcontent,bgroup,bstep,bindent,bhit,bdate,bfile
    bno number(4),
    id varchar2(30),
    btitle varchar2(1000),
    bcontent varchar2(2000), --clob
    bgroup number(4),
    bstep number(4),
    bindent number(4),
    bhit number(4),
    bdate date,
    bfile varchar2(100)
);

--drop table board;
 

select * from board order by bno;

-- btitle 사진이 들어가 있는 게시글을 출력하시오.
select * from board where btitle like '%사진%';
select * from board where bcontent like '%사진%';

-- btitle,bcontent 사진이 들어가 있는 게시글을 출력하시오.
select * from board
where btitle like '%사진%' or bcontent like '%사진%';

select * from board where bno between 11 and 20; 

-- 함수
select lower(id) from board;
select bdate,substr(bdate,0,2) from board;

-- 월만 출력하시오.
select bdate,substr(bdate,4,2) from board;

-- A,a(대소문자)가 들어가 있는 id를 출력하시오.
-- _, %
select id from board where lower(id) like '%a%';

select job_id from employees; 

select job_id from employees where job_id like '%_%';

select * from employees where manager_id is null;

-- 정렬
-- 순차정렬 order by asc, 역순정렬 order by desc
-- 역순정렬 null 제일 위, 순차정렬 null 제일 아래
select * from board order by bno asc;

select department_id,hire_date from employees
order by department_id desc, hire_date asc;

-- 월급으로 역순정렬 출력하시오.
select salary from employees order by salary desc;
-- 사원명으로 순차정렬 하시오.
select emp_name from employees order by emp_name asc;
select emp_name from employees order by emp_name;




















